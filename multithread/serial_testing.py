import serial
import logging

# Initialization and open the port
# Possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
def initSerialObject(portName, allowWriting):
    serialObject = serial.Serial(
    	port = portName,
    	baudrate = 115200,
    	bytesize = serial.EIGHTBITS,			# Number of bits per bytes
    	parity = serial.PARITY_NONE,			# Set parity check: no parity
    	stopbits = serial.STOPBITS_ONE,			# Number of stop bits
    	timeout = 1,            				# Timeout block read
    	xonxoff = False,     					# Disable software flow control
    	rtscts = False,     					# Disable hardware (RTS/CTS) flow control
    	dsrdtr = False)       					# Disable hardware (DSR/DTR) flow control
    if allowWriting:
    	serialObject.writeTimeout = 2     		# Timeout for write
    return serialObject

logging.basicConfig(filename='info.log',level=logging.INFO)
while True:
	isOpen = False
	port = 0
	while True:
		while port < 10:
			try:
				s = initSerialObject("/dev/ttyACM" + str(port), False)
				isOpen = True
				port += 1
				break
			except serial.SerialException:
				print("SerialException: device " + str(port) + " could not be found or could not be configured.")
				port += 1
				continue
		if isOpen:
			try:
				s.flushInput()
				rcv_str = s.read(100)
				if(len(rcv_str) == 100):
					break
				else:
					print("Failed to read from serial.")
					if s.isOpen():
						s.close()
					isOpen = False
			except serial.SerialException:
				print("SerialException: port closed.")
				isOpen = False
			except Exception:
				print("Flush input buffer error. (?)")
				if s.isOpen():
					s.close()
				isOpen = False
		else:
			port = 0
	if s.isOpen():
		try:
			#reset_input_buffer()				# Flush input buffer, discarding all its contents
			# reset_output_buffer()				# Flush output buffer, aborting current output
							   					# and discard all that is in buffer
			# Write data
			#s.write("AT+CSQ")
			#print("write data: AT+CSQ")
			#time.sleep(0.5)  				# Give the serial port sometime to receive the data
			logging.info("start writing...")
			while True:
				try:
					c = s.read(100)
					if(len(c) == 100):
						print(c)
					else:
						print("Failed to read from serial.")
						break
				except KeyboardInterrupt:
					logging.info("\nExiting via keyboard interruption...")
					s.close()
					logging.info("communication closed.")
					exit()
			s.close()
			logging.info("communication closed.")
		except Exception as e:
			logging.info("error communicating...: " + str(e))
	else:
		logging.info("cannot open serial port ")
