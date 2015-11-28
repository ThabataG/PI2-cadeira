from serialObject import *
import globs
import logging

class Connect(object):

    @staticmethod
    def findPort(obj):
        while obj.port < 2:
            try:
                obj.serial = SerialObject.initSerialObject("/dev/ttyACM" + str(obj.port), True)
                obj.port += 1
                return True
            except serial.SerialException:
                print("SerialException: device " + str(obj.port) + " could not be found or could not be configured.")
                obj.port += 1
                continue
        return False

    @staticmethod
    def tryReceiveData(obj):
        obj.serial.flushInput()
        rcv_str = obj.serial.read(10)
        if "Joystick" in str(obj.__class__):
            if(len(rcv_str) == 10):
                isOpen = True
            else:
                logging.info("Joystick :Failed to read from serial.")
                if obj.serial.isOpen():
                    obj.serial.close()
                isOpen = False
        elif "Motor" in str(obj.__class__):
            if(len(rcv_str) == 0):
                isOpen = False
            else:
                logging.info("Motor: I don't want you, joy!")
                isOpen = True
        return isOpen
