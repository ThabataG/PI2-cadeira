from serialObject import *

serialObjectEngine = None
messageFromJoystick = None

class Joystick(object):
    __serialPort = None

    def __init__(self):
        self.initSerial()
        self.startConnection()
        # TODO: try to clear buffer while buffer not flushed
        self.flushBuffer()
#        self.setupWriteSerial()

    def initSerial(self):
        usbPort = "/dev/ttyACM0"
        self.serialPort = SerialObject.initSerialObject(usbPort)

    def startConnection(self):
        self.serialPort = SerialObject.connectWithSerialPort(self.serialPort)

    def flushBuffer(self):
        if self.serialPort.isOpen():
            try:
                self.serialPort.flushInput()
                self.serialPort.flushOutput()
            except Exception as exception:
                print("error communicating...: " + str(exception))
        else:
        	print("cannot open serial port ")

    def getMessage(self):
        try:
            self.serialPort.readline()
            return self.serialPort.readline()
        except KeyboardInterrupt:
            exit()

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


    def setupWriteSerial(self):
        global serialObjectEngine
        usbPort = "/dev/ttyACM1"
        serialObjectEngine = SerialObject.initSerialObject(usbPort)

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
