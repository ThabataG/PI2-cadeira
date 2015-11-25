import logging
import threading
import joystick
import globs

from serialObject import *
import serial

serialJoystick = None

class JoystickController(threading.Thread):

    def __init__(self):
        # Init a new thread
        threading.Thread.__init__(self)
        # set up joystick logging file
        logging.basicConfig(filename='joy.log',level=logging.INFO)

    def findPort(self,port):
        global serialJoystick
        while port < 2:
            try:
                serialJoystick = SerialObject.initSerialObject("/dev/ttyACM" + str(port), True)
                port += 1
                return True,port
            except serial.SerialException:
                print("SerialException: device " + str(port) + " could not be found or could not be configured.")
                port += 1
                continue
        return False,port

    def run(self):
        global serialJoystick
        while True:
            self.tryStablishConnection()
            if serialJoystick.isOpen():
                #logging.warning("WAARNING: HERE")
                globs.lock.acquire()
                globs.wait = False
                globs.lock.release()
                try:
                    logging.info("start reading...")
                    while True:
                        try:
                            if self.updateGlobs() == True:
                                break
                        except KeyboardInterrupt:
                            logging.info("Exiting via keyboard interruption...")
                            serialJoystick.close()
                            logging.info("Joystick :communication closed.")
                            exit()
                    serialJoystick.close()
                    logging.info("Joystick :communication closed.")
                except Exception as e:
                    logging.info("Joystick : error communicating...: " + str(e))
            else:
                logging.info("Joystick: cannot open serial port ")

    def tryReceiveData(self):
        serialJoystick.flushInput()
        rcv_str = serialJoystick.read(10)
        if(len(rcv_str) == 10):
            isOpen = True
        else:
            logging.info("Joystick :Failed to read from serial.")
            if serialJoystick.isOpen():
                serialJoystick.close()
            isOpen = False

        return isOpen


    def tryStablishConnection(self):
        globs.lock.acquire()
        globs.wait = True
        globs.lock.release()
        isOpen = False
        port = 0
        while True:
            isOpen,port = self.findPort(port)
            if isOpen:
                try:
                    isOpen = self.tryReceiveData()
                    if isOpen == True:
                        break
                except serial.SerialException:
                    logging.info("Joystick :SerialException: port closed.")
                    isOpen = False
                except Exception:
                    logging.info("Joystick :Flush input buffer error. (?)")
                    if serialJoystick.isOpen():
                        serialJoystick.close()
                    isOpen = False
            else:
                port = 0

    def updateGlobs(self):
        serialJoystick.flushInput()
        c = serialJoystick.read(2)
        if(len(c) == 2):
            globs.lock.acquire()
            if c[0] & 1:
                globs.coordinates['x'] = c[1] & 0xFE
                globs.coordinates['y'] = c[0] | 0x01

            else:
                globs.coordinates['x'] = c[0] & 0xFE
                globs.coordinates['y'] = c[1] | 0x01

            #print("(" + str(globs.coordinates['x']) + ", "+str(globs.coordinates['y']) + ")")
            globs.lock.notify()
            globs.lock.release()
            return True
        else:
            logging.info("JOY: failed to read from serial.")
            return False
