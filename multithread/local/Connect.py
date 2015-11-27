from serialObject import *
import globs

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
