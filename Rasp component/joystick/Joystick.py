import threading
import Globals
from Connect import *

class Joystick(threading.Thread):
	# Initialize thread and Joystick instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.kill_received = False
		# className = str.split(str(self.__class__),"'")[1]
		# self.logger = Logger(className)
		self.port = 0
		self.serial = None

	# Start thread
	def run(self):
		while not self.kill_received:
			Globals.lock.acquire()
			print(Globals.x)
			Globals.x += 1
			Globals.lock.release()

'''
	def run(self):
		while True:
			self.stablishConnection()
			if self.serial.isOpen():
				#logging.warning("WAARNING: HERE")
				globs.lock.acquire()
				globs.wait = False
				globs.lock.release()
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
		globs.lock.acquire()
		globs.wait = True
		globs.lock.release()
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
			globs.lock.acquire()
			if c[0] & 1:
				globs.coordinates['x'] = c[1] & 0xFE
				globs.coordinates['y'] = c[0] | 0x01

			else:
				globs.coordinates['x'] = c[0] & 0xFE
				globs.coordinates['y'] = c[1] | 0x01

			#print("(" + str(globs.coordinates['x']) + ", "+str(globs.coordinates['y']) + ")")
			globs.lock.notify()
			globs.lock.release()
			return True
		else:
			logging.info("JOY: failed to read from serial.")
			return False
'''