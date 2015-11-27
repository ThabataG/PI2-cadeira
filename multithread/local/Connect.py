from serialObject import *
import globs
import logging

class Connect(object):

    @staticmethod
    def findPort(objDict):
        global serialJoystick
        while objDict["port"] < 2:
            try:
                objDict["serial"] = SerialObject.initSerialObject("/dev/ttyACM" + str(objDict["port"]), True)
                objDict["port"] += 1
                return True
            except serial.SerialException:
                print("SerialException: device " + str(objDict["port"]) + " could not be found or could not be configured.")
                objDict["port"] += 1
                continue
        return False

    @staticmethod
    def tryReceiveData(obj):
        obj.dict["serial"].flushInput()
        rcv_str = obj.dict["serial"].read(10)
        if "Joystick" in str(obj.__class__):
            if(len(rcv_str) == 10):
                isOpen = True
            else:
                logging.info("Joystick :Failed to read from serial.")
                if obj.dict["serial"].isOpen():
                    obj.dict["serial"].close()
                isOpen = False
        elif "Motor" in str(obj.__class__):
            if(len(rcv_str) == 0):
                isOpen = False
            else:
                logging.info("Motor: I don't want you, joy!")
                isOpen = True
        return isOpen
