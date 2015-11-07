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

############### TODO NEED TO REFACTOR FROM HERE!!! TODO #########


    def openConnectionToWrite(self):
        global serialObjectEngine
        serialObjectEngine = SerialObject.connectWithSerialPort(serialObjectEngine)

    def sendMessageToEnginesMSPs(self,command):
        self.openConnectionToWrite()
        successSendMessage = False
        if self.verifyIfMessageContainsError(command) == False:
            successSendMessage = SerialObject.writeWithSerial(serialObjectEngine,command)

        serialObjectEngine.serialObject.close()

        return successSendMessage

    def verifyIfMessageContainsError(self,receivedMsg):
        if len(receivedMsg) != 3 :
            return True
        else:
            return False

    def readMsg():
        return None
# MSG esta demorando pra chegar: Ou buffer do MSP não está pronto a tempo ou falha de comunicação entre MSP e Rasp
