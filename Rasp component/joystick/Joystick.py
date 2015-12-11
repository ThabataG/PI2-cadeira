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
			#print("(" + str(Globals.coordinates['x']) + ", " + str(Globals.coordinates['y']) + ")")
			Globals.lock.notify()
			Globals.lock.release()
		return updated
