import threading
import Globals
from Connect import *
from Logger import *

class Joystick(threading.Thread):
	# Initialize thread and Joystick instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.killReceived = False
		self.port = 0
		self.serial = None

		className = str.split(str(self.__class__),"'")[1]
		self.logger = Logger(className)


	# Start thread
	def run(self):
		while not self.killReceived:
			Connect.connectJoy(self)
			self.setJoyConnectedFlag()
			while not self.killReceived:
				coordinates = Connect.read(self.serial,2)
				#print(coordinates)
				if not self.updateGlobals(coordinates):
					Connect.close(self.serial)
					break

	# 
	def setJoyConnectedFlag(self):
		Globals.lock.acquire()
		Globals.joyConnected = True
		Globals.lock.release()

	# Update global variable 'coordinates'
	def updateGlobals(self, coordinates):
		updated = False
		if len(coordinates) < 2:
			self.logger.logger.warn("Any problem happened, trying to connect again.")
			updated = False
		else:
			updated = True
			Globals.lock.acquire()
			if coordinates[0] & 1:
				Globals.coordinates['x'] = coordinates[1] & 0xFE
				Globals.coordinates['y'] = coordinates[0] | 0x01
			else:
				Globals.coordinates['x'] = coordinates[0] & 0xFE
				Globals.coordinates['y'] = coordinates[1] | 0x01
			print("(" + str(Globals.coordinates['x']) + ", " + str(Globals.coordinates['y']) + ")")
			Globals.lock.notify()
			Globals.lock.release()
		return updated

'''
	def run(self):
		while True:
			self.stablishConnection()
			if self.serial.isOpen():
				#logging.warning("WAARNING: HERE")
				Globals.lock.acquire()
				Globals.wait = False
				Globals.lock.release()
				try:
					logging.info("start reading...")
					while True:
						try:
							if self.updateGlobs() == True:
								break
						except KeyboardInterrupt:
							logging.info("Exiting via keyboard interruption...")
							self.serial.close()
							logging.info("Joystick :communication closed.")
							exit()
					self.serial.close()
					logging.info("Joystick :communication closed.")
				except Exception as e:
					logging.info("Joystick : error communicating...: " + str(e))
			else:
				logging.info("Joystick: cannot open serial port ")

	def tryStablishConnection(self):
		Globals.lock.acquire()
		Globals.wait = True
		Globals.lock.release()
		isOpen = False
		self.port = 0
		while True:
			isOpen = Connect.findPort(self)
			if isOpen:
				try:
					isOpen = Connect.tryReceiveData(self)
					if isOpen == True:
						break
				except self.serial.SerialException:
					logging.info("Joystick :SerialException: port closed.")
					isOpen = False
				except Exception:
					logging.info("Joystick :Flush input buffer error. (?)")
					if self.serial.isOpen():
						self.serial.close()
					isOpen = False
			else:
				port = 0

	def updateGlobs(self):
		self.serial.flushInput()
		c = self.serial.read(2)
		if(len(c) == 2):
			Globals.lock.acquire()
			if c[0] & 1:
				Globals.coordinates['x'] = c[1] & 0xFE
				Globals.coordinates['y'] = c[0] | 0x01

			else:
				Globals.coordinates['x'] = c[0] & 0xFE
				Globals.coordinates['y'] = c[1] | 0x01

			#print("(" + str(Globals.coordinates['x']) + ", "+str(Globals.coordinates['y']) + ")")
			Globals.lock.notify()
			Globals.lock.release()
			return True
		else:
			logging.info("JOY: failed to read from serial.")
			return False
'''
