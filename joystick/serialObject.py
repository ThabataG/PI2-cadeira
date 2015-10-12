import serial, time

serialObject = serial.Serial()

def initSerialObject():
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

def connectWithSerialPort():
    try:
    	serialObject.open()
    except Exception as e:
    	print("error open serial port: " + str(e))
    	exit()

def readMsg(channel):
    connectWithSerialPort()
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
