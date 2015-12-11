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
			print(str(Globals.coordinates['x']) + ',' + str(Globals.coordinates['y']))
			self.x = Globals.coordinates['x']
			self.y = Globals.coordinates['y']
			writeWithSuccess = Connect.write(self.serial,[self.x,self.y])
		else:
			Globals.lock.wait()
			logging.info("Coordinates' data not changed")
		Globals.lock.release()
		return writeWithSuccess