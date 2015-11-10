from serialObject import *

class Motor(object):

    def __init__(self):
        # Object variables
        self.serialPort = None
        self.usbPort = "/dev/ttyACM1"

        # set up serial connection
        self.initSerial()
        self.startConnection()
        SerialObject.flushBuffer(self.serialPort)

    def initSerial(self):
        self.serialPort = SerialObject.initSerialObject(self.usbPort)

    def startConnection(self):
        self.serialPort = SerialObject.connectWithSerialPort(self.serialPort)

    def sendMessageToMSP(self,x,y):
        return SerialObject.writeWithSerial(self.serialPort, [x, y])
