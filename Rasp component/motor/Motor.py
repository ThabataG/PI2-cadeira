import threading
import Globals
from Connect import *

class Motor(threading.Thread):
	# Initialize thread and Motor instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.killReceived = False
		self.x = 0
		self.y = 1
		self.rightMotor = 0
		self.leftMotor = 1
		self.port = 0
		self.serial = None

	# Start thread
	def run(self):
		while not self.killReceived:
			while not Globals.joyConnected:
				continue
			Connect.connectMotor(self)
			while not self.killReceived:
				if not self.updatePWM():
					Connect.close(self.serial)
					logging.info("Could not write data over serial")
					break

	def updatePWM(self):
		Globals.lock.acquire()
		writeWithSuccess = True
		if self.x != Globals.coordinates['x'] or self.y != Globals.coordinates['y']:
			transformXYtoM(Globals.coordinates)
			print(str(self.leftMotor) + ',' + str(self.rightMotor))
			writeWithSuccess = Connect.write(self.serial,[self.rightMotor,self.leftMotor])
		else:
			Globals.lock.wait()
			logging.info("Coordinates' data not changed")
		Globals.lock.release()
		return writeWithSuccess

	def transformXYtoM(self, coordinates):
		rightMotor = x
		leftMotor = y
