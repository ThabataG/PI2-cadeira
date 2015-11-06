from serialObject import *

pinNumber = 11
serialObjectJoystick = None
serialObjectEngine = None
messageFromJoystick = None

class Joystick(object):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinNumber,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.setupInterruption()
#        self.setupWriteSerial()

    def getMessageFromJoystick(self):
        return messageFromJoystick

    def setupInterruption(self):
        global serialObjectJoystick
        usbPort = "/dev/ttyACM0"
        serialObjectJoystick = SerialObject.initSerialObject(usbPort)
        GPIO.add_event_detect(pinNumber, GPIO.FALLING, callback=readMsg, bouncetime=300)

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
def readMsg(channel):
    global serialObjectJoystick #to set serial object
    global messageFromJoystick
    serialObjectJoystick = SerialObject.connectWithSerialPort(serialObjectJoystick)
    if serialObjectJoystick.isOpen():
        try:
            serialObjectJoystick.flushInput() # Flush input buffer, discarding all its contents
            serialObjectJoystick.flushOutput() # Flush output buffer, aborting current output and discard all that is in buffer
    		# Write data
    		#s.write("AT+CSQ")
    		#print("write data: AT+CSQ")
    		#time.sleep(0.5)  				# Give the serial port sometime to receive the data
            try:
                response = serialObjectJoystick.readline()
                response = serialObjectJoystick.readline()
#                for char in response:
#                    print(char)
#                print("Received Msg")
                messageFromJoystick = response
            except KeyboardInterrupt:
                GPIO.cleanup()

            serialObjectJoystick.close()
        except Exception as e:
            print("error communicating...: " + str(e))
    else:
    	print("cannot open serial port ")
