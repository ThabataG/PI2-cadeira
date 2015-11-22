import serial, time

# Initialization and open the port
# Possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call
s = serial.Serial()
s.port = "/dev/ttyACM0"
s.baudrate = 115200
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
	print "Error opening serial port: " + str(e)
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
		print("Start writing...")
		loops = 1
		try:
			while True:
				for i in range(250,255):
					for j in range(loops):
						time.sleep(0.1)
						s.write(chr(i|0))
						s.write(chr(i|1))
				for i in range(255,250,-1):
					for j in range(loops):
						time.sleep(0.1)
						s.write(chr(i|0))
						s.write(chr(i|1))
		except KeyboardInterrupt:
			s.close()
			print("\nCommunication closed.")
	except Exception, e1:
		print "Error communicating: " + str(e1)
else:
	print "Cannot open serial port."
