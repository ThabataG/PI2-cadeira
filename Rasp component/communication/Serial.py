import serial

class Serial(object):
	# Declare SerialException as a Serial 
	SerialException = serial.SerialException

	# Initialize connection with a serial port using UART protocol
	@staticmethod
	def init(portName, canWrite=True):
		try:
			serialObject = serial.Serial(
				port = portName,                  # Set and open serial port
				baudrate = 115200,
				bytesize = serial.EIGHTBITS,      # Number of bits per byte
				parity = serial.PARITY_NONE,      # Set parity check: no parity
				stopbits = serial.STOPBITS_ONE,   # Number of stop bits
				timeout = 0.01,                   # Timeout block read (seconds)
				xonxoff = False,                  # Disable software flow control
				rtscts = False,                   # Disable hardware (RTS/CTS) flow control
				dsrdtr = False)                   # Disable hardware (DSR/DTR) flow control
			if canWrite:
				serialObject.writeTimeout = 2     # Timeout for write (seconds)
		# If the connection could not be stablished, just return None
		except serial.SerialException:
			#logging.warning("Serial port is busy or could not be found")
			serialObject = None
		# Return the serial object created
		return serialObject

	# Write the string data to the port
	@staticmethod
	def write(serialObject, data):
		try:
			numBytesWritten = serialObject.write(bytearray(data))
		except serial.SerialException:
			#logging.error("Serial port closed")
			numBytesWritten = 0
		# Return the number of bytes written via serial
		return numBytesWritten
