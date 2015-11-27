import logging
import threading
import motor
import globs

from serialObject import *
import serial

from Connect import *

class MotorController(threading.Thread):

    def __init__(self):
        # Init a new thread
        threading.Thread.__init__(self)
        # set up joystick logging file
        logging.basicConfig(filename='motor.log',level=logging.INFO)
        # object attributes
        #FIXME set this dictionary for all
        self.dict = {"port":0,
                        "serial":None}
        self.x = 0
        self.y = 1

    def run(self):
        while True:
            while globs.wait:
                #print("Inside while wait!")
                continue
            self.tryStablishConnection()
            if self.dict["serial"].isOpen():
                try:
                    logging.info("Motor: start writing...")
                    self.update()
                    self.dict["serial"].close()
                except Exception as e:
                    logging.info("Motor: error communicating...: " + str(e))
            else:
                logging.info("Motor: cannot open serial port ")

    def tryStablishConnection(self):
        isOpen = False
        self.dict["port"] = 0
        while True:
            isOpen = Connect.findPort(self.dict)
            if isOpen:
                try:
                    self.dict["serial"].flushInput()
                    if not Connect.tryReceiveData(self):
                        break
                except serial.SerialException:
                    logging.info("Motor: SerialException: port closed.")
                except Exception:
                    logging.info("Motor: Flush input buffer error. (?)")
                if self.dict["serial"].isOpen():
                    self.dict["serial"].close()
                isOpen = False
            else:
                self.dict["port"] = 0

    def update(self):
        while True:
            try:
                globs.lock.acquire()
                if self.x != globs.coordinates['x'] or self.y != globs.coordinates['y']:
                    print(str(globs.coordinates['x']) + ',' + str(globs.coordinates['y']))
                    self.x = globs.coordinates['x']
                    self.y = globs.coordinates['y']
                    self.dict["serial"].flushOutput()
                    success = SerialObject.writeWithSerial(self.dict["serial"],[self.x,self.y])
                else:
                    #print("Else writing information")
                    globs.lock.wait()
                    logging.info("Motor: X and Y not change.")
                    #break
                globs.lock.release()
            except KeyboardInterrupt:
                logging.info("Motor: Exiting via keyboard interruption...")
                self.dict["serial"].close()
                logging.info("Motor: communication closed.")
                exit()
