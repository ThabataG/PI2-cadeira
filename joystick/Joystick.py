from serialObject import *

class Joystick(object):

    def __init__(self):
        # object attributes
        self.x = 0
        self.y = 0
        self.serialPort = None
        self.usbPort = "/dev/ttyACM0"

        # set up serial connection
        self.initSerial()
        self.startConnection()
        # TODO: try to clear buffer while buffer not flushed
        SerialObject.flushBuffer(self.serialPort)
#        self.setupWriteSerial()

    def initSerial(self):
        self.serialPort = SerialObject.initSerialObject(self.usbPort)

    def startConnection(self):
        self.serialPort = SerialObject.connectWithSerialPort(self.serialPort)

    def getMessage(self):
        try:
            # Get trash from serial
            self.serialPort.readline()
            # Guarantee of read real message
            return self.serialPort.readline()
        except KeyboardInterrupt:
            exit()

    def updateXY(self):
        message = self.getMessage()
        if message != None:
            command = self.translateCommandFromMSP(message)
            self.x = command[0]
            self.y = command[1]

    def translateCommandFromMSP(self,message):
        haveNewLine = message.find(b'\n')
        if haveNewLine != -1:
            message = message.rstrip(b'\n')
            commands = []
            for char in message:
                commands.append(char)
        #        command = message.split(" ",1)
#            print("Message translated: " + ''.join(str(e) for e in commands))
            return commands
        return ""

    def verifyIfMessageContainsError(self,receivedMsg):
        if len(receivedMsg) != 3 :
            return True
        else:
            return False

    def readMsg():
        return None
