import logging
import threading
import motor
import globs

from serialObject import *
import serial

serialMotor = None

class MotorController(threading.Thread):

    def __init__(self):
        # Init a new thread
        threading.Thread.__init__(self)
        # set up joystick logging file
        logging.basicConfig(filename='motor.log',level=logging.INFO)
        # object attributes
        self.x = 0
        self.y = 1

    def findPort(self,port):
        global serialMotor
        while port < 2:
            try:
                serialMotor = SerialObject.initSerialObject("/dev/ttyACM" + str(port), True)
                port += 1
                return True,port
            except serial.SerialException:
                print("SerialException: device " + str(port) + " could not be found or could not be configured.")
                port += 1
                continue
        return False,port

    def tryReceiveData(self):
        rcv_str = serialMotor.read(10)
        if(len(rcv_str) == 0):
            return False
        else:
            logging.info("Motor: I don't want you, joy!")
        return True

    def tryStablishConnection(self):
        isOpen = False
        port = 0
        while True:
            isOpen,port = self.findPort(port)
            if isOpen:
                try:
                    serialMotor.flushInput()
                    if self.tryReceiveData() == False:
                        break
                except serial.SerialException:
                    logging.info("Motor: SerialException: port closed.")
                except Exception:
                    logging.info("Motor: Flush input buffer error. (?)")
                if serialMotor.isOpen():
                    serialMotor.close()
                isOpen = False
            else:
                port = 0


    def run(self):
        global serialMotor
        while True:
            while globs.wait:
                #print("Inside while wait!")
                continue
            self.tryStablishConnection()
            if serialMotor.isOpen():
                try:
                    logging.info("Motor: start writing...")
                    while True:
                        try:
                            #write information
                            #print("Writing information")
                            globs.lock.acquire()
                            if self.x != globs.coordinates['x'] or self.y != globs.coordinates['y']:
                                print(str(globs.coordinates['x']) + ',' + str(globs.coordinates['y']))
                                self.x = globs.coordinates['x']
                                self.y = globs.coordinates['y']
                                serialMotor.flushOutput()
                                success = SerialObject.writeWithSerial(serialMotor,[self.x,self.y])
                            else:
                                #print("Else writing information")
                                globs.lock.wait()
                                logging.info("Motor: X and Y not change.")
                                #break
                            globs.lock.release()
                        except KeyboardInterrupt:
                            logging.info("Motor: Exiting via keyboard interruption...")
                            serialMotor.close()
                            logging.info("Motor: communication closed.")
                            exit()
                    serialMotor.close()
                except Exception as e:
                    logging.info("Motor: error communicating...: " + str(e))
            else:
                logging.info("Motor: cannot open serial port ")
