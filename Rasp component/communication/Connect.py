from Serial import *
import logging
logging.basicConfig(filename="", level=logging.DEBUG)

class Connect(object):
	# Search serial ports until find and make a valid joystick serial port connection
	@staticmethod
	def connectJoy(obj):
		logging.debug("Start trying to make a joystick connection")
		joyConnected = False
		obj.port = 0
		while not joyConnected:
			joyConnected = Connect.searchSerialPort(obj)
			if joyConnected:
				logging.debug("Serial port found")
				joyConnected = Connect.validJoyConnection(obj)
				if not joyConnected:
					obj.port += 1
					logging.debug("Not a valid joystick serial connection")
				else:
					logging.debug("Valid joystick serial connection")
			else:
				logging.debug("No serial ports found")
				obj.port = 0

	# Search for an openned serial port between [0,maxPortNumber] and open it
	# Return False if no ports where found and True otherwise
	@staticmethod
	def searchSerialPort(obj, maxPortNumber=1, serialPrefix="/dev/ttyACM"):
		# Reset obj.port if it is greater than maxPortNumber
		if obj.port > maxPortNumber:
			obj.port = 0
			logging.debug("Reset port counter 'obj.port'")
		# Search for an openned serial port
		couldConnect = False
		while obj.port <= maxPortNumber:
			obj.serial = Serial.init(serialPrefix + str(obj.port))
			if obj.serial == None:
				obj.port += 1
				#logging.warning("Serial connection not performed in port " + str(obj.port))
			else:
				couldConnect = True
				break
		return couldConnect

	# Tests whether a serial connection is a joystick or not
	# If the connection is openned and the system is receiving data, is assumed that it is a valid 
	# joystick connection
	@staticmethod
	def validJoyConnection(obj, numBytesToReceive=10):
		isValid = False
		try:
			receivedString = Connect.read(obj.serial, numBytesToReceive)
			logging.debug(receivedString)
			if(len(receivedString) == numBytesToReceive):
				isValid = True
			else:
				obj.serial.close()
				isValid = False
		except Serial.serial.SerialException:
			isValid = False
		return isValid

	# 
	@staticmethod
	def read(serialObject, numOfBytesToRead=2):
		receivedString = ""
		try:
			serialObject.flushInput()
			receivedString = serialObject.read(numOfBytesToRead)
		except serialObject.SerialException:
			receivedString = ""
		return receivedString
'''
	# 
	@staticmethod
	def tryReceiveData(obj):
		obj.serial.flushInput()
		rcv_str = obj.serial.read(10)
		if "Joystick" in str(obj.__class__):
			if(len(rcv_str) == 10):
				isOpen = True
			else:
				logging.info("Joystick :Failed to read from serial.")
				if obj.serial.isOpen():
					obj.serial.close()
				isOpen = False
		elif "Motor" in str(obj.__class__):
			if(len(rcv_str) == 0):
				isOpen = False
			else:
				logging.info("Motor: I don't want you, joy!")
				isOpen = True
		return isOpen
'''