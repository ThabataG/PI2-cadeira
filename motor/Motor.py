import sys,os,inspect

# Relative importation of pathsToImport modules
pathsToImport = ['serialObject']
for path in pathsToImport:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../"+path)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)


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
        return SerialObject.writeWithSerial(self.serialPort, [x|1, y|1])
