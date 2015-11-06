import serial, time

# Initialization and open the port
# Possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
s = serial.Serial()
s.port = "/dev/ttyACM0"
s.baudrate = 9600
s.bytesize = serial.EIGHTBITS 			# Number of bits per bytes
s.parity = serial.PARITY_NONE 			# Set parity check: no parity
s.stopbits = serial.STOPBITS_ONE 		# Number of stop bits
s.timeout = 1            				# Timeout block read
s.xonxoff = False     					# Disable software flow control
s.rtscts = False     					# Disable hardware (RTS/CTS) flow control
s.dsrdtr = False       					# Disable hardware (DSR/DTR) flow control
s.writeTimeout = 2     					# Timeout for write

try:
	s.open()
except Exception, e:
	print "error open serial port: " + str(e)
	exit()

if s.isOpen():
	try:
		s.flushInput() 					# Flush input buffer, discarding all its contents
		s.flushOutput()					# Flush output buffer, aborting current output 
				       					# and discard all that is in buffer
		# Write data
		#s.write("AT+CSQ")
		#print("write data: AT+CSQ")
		#time.sleep(0.5)  				# Give the serial port sometime to receive the data
		print("start writing...")
		loops = 1
		while True:
			rcv_str = s.readline()
			rcv_str = s.readline()
			print('(' + str(ord(rcv_str[0])) + ',' + str(ord(rcv_str[1])) + ')')
		s.close()
		print("communication closed.")
	except Exception, e1:
		print "error communicating...: " + str(e1)
else:
	print "cannot open serial port "
