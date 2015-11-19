import logging
import threading
import joystick
import globs

from serialObject import *
import serial

class JoystickController(threading.Thread):

    def __init__(self):
        # Init a new thread
        threading.Thread.__init__(self)
        # set up joystick logging file
        logging.basicConfig(filename='joy.log',level=logging.INFO)

    def run(self):
        while True:
            globs.lock.acquire()
            globs.wait = True
            globs.lock.release()
            isOpen = False
            port = 0
            while True:
                while port < 2:
                    try:
                        s = SerialObject.initSerialObject("/dev/ttyACM" + str(port), False)
                        isOpen = True
                        port += 1
                        break
                    except serial.SerialException:
                        print("SerialException: device " + str(port) + " could not be found or could not be configured.")
                        port += 1
                        continue
                if isOpen:
                    try:
                        s.flushInput()
                        rcv_str = s.read(10)
                        if(len(rcv_str) == 10):
                            break
                        else:
                            logging.info("Joystick :Failed to read from serial.")
                            if s.isOpen():
                                s.close()
                            isOpen = False
                    except serial.SerialException:
                        logging.info("Joystick :SerialException: port closed.")
                        isOpen = False
                    except Exception:
                        logging.info("Joystick :Flush input buffer error. (?)")
                        if s.isOpen():
                            s.close()
                        isOpen = False
                else:
                    port = 0
            if s.isOpen():
                #logging.warning("WAARNING: HERE")
                globs.lock.acquire()
                globs.wait = False
                globs.lock.release()
                try:
                    logging.info("start reading...")
                    while True:
                        try:
                            s.flushInput()
                            c = s.read(2)
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
                                #print(c)
                            else:
                                logging.info("JOY: failed to read from serial.")
                                break
                        except KeyboardInterrupt:
                            logging.info("Exiting via keyboard interruption...")
                            s.close()
                            logging.info("Joystick :communication closed.")
                            exit()
                    s.close()
                    logging.info("Joystick :communication closed.")
                except Exception as e:
                    logging.info("Joystick : error communicating...: " + str(e))
            else:
                logging.info("Joystick: cannot open serial port ")
