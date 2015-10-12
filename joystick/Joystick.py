from serialObject import *

pinNumber = 11
serialObject = None

class Joystick(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinNumber,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        self.setupInterruption()

    def setupInterruption(self):
        global serialObject
        serialObject = SerialObject.initSerialObject()
        GPIO.add_event_detect(pinNumber, GPIO.FALLING, callback=readMsg, bouncetime=300)
        print("Setup interruption")

    def translateCommandFromMSP(self,message):
        message = message.rstrip('\n')
        command = message.split(" ",1)
        return command

    def sendMessageToMSP(self,command):
        return False

def readMsg(channel):
    print(channel)
    global serialObject #to set serial object
    serialObject = SerialObject.connectWithSerialPort(serialObject)
    if serialObject.isOpen():
        try:
            serialObject.flushInput() # Flush input buffer, discarding all its contents
            serialObject.flushOutput() # Flush output buffer, aborting current output and discard all that is in buffer
    		# Write data
    		#s.write("AT+CSQ")
    		#print("write data: AT+CSQ")
    		#time.sleep(0.5)  				# Give the serial port sometime to receive the data
            try:
                response = serialObject.readline()
#                for char in response:
#                    print(char)
                print("Received Msg")
                print(response)
            except KeyboardInterrupt:
                GPIO.cleanup()

            serialObject.close()
        except Exception as e:
            print("error communicating...: " + str(e))
    else:
    	print("cannot open serial port ")
