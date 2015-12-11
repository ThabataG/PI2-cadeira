from Serial import *
import logging
from Logger import *

logger = Logger("Connect")

class Connect(object):
	# Search serial ports until find and make a valid joystick serial port connection
	@staticmethod
	def connectJoy(obj):
		logger.logger.debug("Start trying to make a joystick connection")
		joyConnected = False
		obj.port = 0
		while not joyConnected:
			usbConnected = Connect.searchSerialPort(obj)
			if usbConnected:
				logger.logger.debug("Serial port opened")
				joyConnected = Connect.validJoyConnection(obj)
				if not joyConnected:
					obj.port += 1
					Connect.close(obj.serial)
					logger.logger.debug("Not a valid joystick serial connection")
				else:
					logger.logger.debug("Valid joystick serial connection")
			else:
				joyConnected = False
				logger.logger.warn("No serial ports found")
				obj.port = 0

	# Search for an opened serial port between [0,maxPortNumber] and open it
	# Return False if no ports where found and True otherwise
	@staticmethod
	def searchSerialPort(obj, maxPortNumber=1, serialPrefix="/dev/ttyACM"):
		# Reset obj.port if it is greater than maxPortNumber
		if obj.port > maxPortNumber:
			obj.port = 0
			logger.logger.warn("Reset port counter 'obj.port'")
		# Search for an opened serial port
		couldConnect = False
		while obj.port <= maxPortNumber:
			obj.serial = Serial.init(serialPrefix + str(obj.port))
			print(str(obj.serial.__class__))
			logger.logger.info("Make a new serial object at port " + str(obj.port))
			if obj.serial == None:
				logger.logger.warn("Serial connection not performed in port " + str(obj.port))
				obj.port += 1
			else:
				couldConnect = True
				logger.logger.info("Connection stablished")
				break
		return couldConnect

	# Tests whether a serial connection is a joystick or not
	# If the connection is opened and the system is receiving data, is assumed that it is a valid
	# joystick connection
	@staticmethod
	def validJoyConnection(obj, numBytesToReceive=10):
		isValid = False
		receivedString = Connect.read(obj.serial, numBytesToReceive)
		print(receivedString)
		if(len(receivedString) == numBytesToReceive):
			isValid = True
		else:
			isValid = False
		return isValid

	#
	@staticmethod
	def read(serialObject, numOfBytesToRead=2):
		receivedString = ""
		try:
			serialObject.flushInput()
			receivedString = serialObject.read(numOfBytesToRead)
		except Serial.SerialException:
			receivedString = ""
			serialObject.close()
		except Exception:
			logger.logger.error("Flush input error: probably the usb was disconnected")
			receivedString = ""
			serialObject.close()
		return receivedString

	#
	@staticmethod
	def close(serialObject):
		if(serialObject.isOpen()):
			logger.logger.debug("Serial port closed")
			serialObject.close()

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
