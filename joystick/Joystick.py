from serialObject import *

pinNumber = 11
serialObjectJoystick = None
serialObjectEngine = None

class Joystick(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinNumber,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.setupInterruption()

    def setupInterruption(self):
        global serialObjectJoystick
        usbPort = "/dev/ttyACM0"
        serialObjectJoystick = SerialObject.initSerialObject(usbPort)
        GPIO.add_event_detect(pinNumber, GPIO.FALLING, callback=readMsg, bouncetime=300)

    def translateCommandFromMSP(self,message):
        message = message.rstrip('\n')
        commands = []
        for char in message:
            print(char)
            commands.append(ord(char))
#        command = message.split(" ",1)
        return commands

    def setupWriteSerial(self):
        global serialObjectEngine
        usbPort = "/dev/ttyACM1"
        serialObjectEngine = SerialObject.initSerialObject(usbPort)
        serialObjectEngine = SerialObject.connectWithSerialPort(serialObjectEngine)

    def sendMessageToMSP(self,command):
        self.setupWriteSerial()
        SerialObject.writeWithSerial(serialObjectEngine,command)

    def readMsg():
        return None

def readMsg(channel):
    global serialObjectJoystick #to set serial object
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
#                for char in response:
#                    print(char)
                print("Received Msg")
                print(response)
            except KeyboardInterrupt:
                GPIO.cleanup()

            serialObjectJoystick.close()
        except Exception as e:
            print("error communicating...: " + str(e))
    else:
    	print("cannot open serial port ")
