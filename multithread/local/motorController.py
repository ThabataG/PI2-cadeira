import logging
import threading
import motor
import globs

from serialObject import *
import serial

class MotorController(threading.Thread):

    def __init__(self):
        # Init a new thread
        threading.Thread.__init__(self)
        # set up joystick logging file
        logging.basicConfig(filename='motor.log',level=logging.INFO)
        # object attributes
        self.x = 0
        self.y = 1

    def run(self):
        while True:
            while globs.wait:
                #print("Inside while wait!")
                continue
            isOpen = False
            port = 0
            while True:
                while port < 2:
                    try:
                        s = SerialObject.initSerialObject("/dev/ttyACM" + str(port), True)
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
                        if(len(rcv_str) == 0):
                            break
                        else:
                            logging.info("Motor: I don't want you, joy!")
                    except serial.SerialException:
                        logging.info("Motor: SerialException: port closed.")
                    except Exception:
                        logging.info("Motor: Flush input buffer error. (?)")
                    if s.isOpen():
                        s.close()
                    isOpen = False
                else:
                    port = 0
            if s.isOpen():
                try:
					#reset_input_buffer()				# Flush input buffer, discarding all its contents
					# reset_output_buffer()				# Flush output buffer, aborting current output
									   					# and discard all that is in buffer
					# Write data
					#s.write("AT+CSQ")
					#print("write data: AT+CSQ")
					#time.sleep(0.5)  				# Give the serial port sometime to receive the data
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
                                s.flushOutput()
                                success = SerialObject.writeWithSerial(s,[self.x,self.y])
                            else:
                                #print("Else writing information")
                                globs.lock.wait()
                                logging.info("Motor: X and Y not change.")
                                #break
                            globs.lock.release()
                        except KeyboardInterrupt:
                            logging.info("Motor: Exiting via keyboard interruption...")
                            s.close()
                            logging.info("Motor: communication closed.")
                            exit()
                    s.close()
                except Exception as e:
                    logging.info("Motor: error communicating...: " + str(e))
            else:
                logging.info("Motor: cannot open serial port ")
