import serial, time

class Joystick(object):

    def __init__(self):
        return None

    def initSerialObject(self):
        serialObject = serial.Serial()
        serialObject.port = "/dev/ttyACM0"
        serialObject.baudrate = 9600
        serialObject.bytesize = serial.EIGHTBITS 			# Number of bits per bytes
        serialObject.parity = serial.PARITY_NONE 			# Set parity check: no parity
        serialObject.stopbits = serial.STOPBITS_ONE 		# Number of stop bits
        serialObject.timeout = 1            				# Timeout block read
        serialObject.xonxoff = False     					# Disable software flow control
        serialObject.rtscts = False     					# Disable hardware (RTS/CTS) flow control
        serialObject.dsrdtr = False       					# Disable hardware (DSR/DTR) flow control
        serialObject.writeTimeout = 2     					# Timeout for write
        return serialObject

    def connectWithSerialPort(self,serialObject):
        try:
        	serialObject.open()
        except Exception as e:
        	print("error open serial port: " + str(e))
        	exit()

        return serialObject

    def readMsg(self,serialObject):
        if serialObject.isOpen():
            try:
                serialObject.flushInput() # Flush input buffer, discarding all its contents
                serialObject.flushOutput() # Flush output buffer, aborting current output and discard all that is in buffer
        		# Write data
        		#s.write("AT+CSQ")
        		#print("write data: AT+CSQ")
        		#time.sleep(0.5)  				# Give the serial port sometime to receive the data
                numOfLines = 0
                while True:
                    response = serialObject.readline()
                    print(response)
                    for char in response:
                        print(char)
                    numOfLines = numOfLines + 1
                    if (numOfLines >= 5):
                        break
                serialObject.close()
            except Exception as e:
                print("error communicating...: " + str(e))
        else:
        	print("cannot open serial port ")

    def receiveMsg(self):
        serialObject = self.initSerialObject()
        serialObject = self.connectWithSerialPort(serialObject)
        self.readMsg(serialObject)

        return None

    def translateCommandFromMSP(self,message):
        message = message.rstrip('\n')
        command = message.split(" ",1)
        return command

    def sendMessageToMSP(self,command):
        return False
