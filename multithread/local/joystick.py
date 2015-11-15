import serial
import serialObject

class Joystick(object):

	def __init__(self):
		# object attributes
		self.coordinates = {'x': 0, 'y': 1}
		self.serialPort = None
		self.MAX_PORT_NUMBER = 10

	def connect(self):
		couldOpenSerial = False
		portNumber = 0
		while True:
			while portNumber < self.MAX_PORT_NUMBER:
				try:
					self.serialPort = serialObject.SerialObject.initSerialObject("/dev/ttyACM" + str(portNumber), False)
					couldOpenSerial = True
					portNumber += 1
					break
				except serial.SerialException:
					print("SerialException: device " + str(portNumber) + " could not be found or could not be configured.")
					portNumber += 1
					continue
			if couldOpenSerial:
				try:
					self.serialPort.flushInput()
					test_read = self.serialPort.read(100)
					if(len(test_read) == 100):
						break
					else:
						print("Failed to read from serial.")
						if self.serialPort.isOpen():
							self.serialPort.close()
						couldOpenSerial = False
				except serial.SerialException:
					print("SerialException: port closed.")
					couldOpenSerial = False
				except Exception:
					print("Flush input buffer error. (?)")
					if self.serialPort.isOpen():
						self.serialPort.close()
					couldOpenSerial = False
			else:
				portNumber = 0

	# Only update pair (x,y) if it's valid
	def update_performed(self):
		if self.serialPort.isOpen():
			coordinates = self.readCoordinates()
			if self.areValidCoordinates(coordinates):
				if coordinates[0] & 1:
					self.coordinates['x'] = coordinates[1] & 0xFE
					self.coordinates['y'] = coordinates[0] | 0x01
				else: 
					self.coordinates['x'] = coordinates[0] & 0xFE
					self.coordinates['y'] = coordinates[1] | 0x01
				return True
			else:
				print("JOY: failed to read from serial.")
				return False
		else:
			#logging.info("Could not open serial port.")
			print("JOY: serial connection is closed.")
			return False

	# (x,y) were received correctly?
	# As (x,y) are identified by their LSB, a simple way to verify both were received correctly is to XOR them and check if its resulting LSB is equal to 1, in other words, if (x,y) LSBs were different, representing both x and y.
	def areValidCoordinates(self, coordinates):
		areValid = False
		if len(coordinates) == 2:
			if (coordinates[0]^coordinates[1]) & 0x01:
				areValid = True
		return areValid
	
	def readCoordinates(self):
		return self.serialPort.read(2)

	def close_connection(self):
		self.serialPort.close()

"""
#####################################################################
		# set up serial connection
		while True:
			while not self.initSerial():
				continue
			if not self.updateCoordinates():

	def run(self):
		while self.serialPort.isOpen():
			self.updateXY()
			print("(" + str(self.x) + "," + str(self.y) + ")")
		print("Exiting joy thread...")
	
	# Search in any /dev/ttyACM* port until find and open a connection along with a serial device
	def initSerial(self):
		for portNumber in range(3):
			try:
				self.configSerial(portNumber)
				self.startConnection()
				SerialObject.flushBuffer(self.serialPort)
				return True
			except Exception as exception:
				print("error opening serial: " + str(exception))
		return False

	def configSerial(self, port):
		self.serialPort = SerialObject.initSerialObject("/dev/ttyACM" + str(port), False)

	def startConnection(self):
		self.serialPort = SerialObject.connectWithSerialPort(self.serialPort)

"""
