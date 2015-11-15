import logging
import threading
import motor
import globs

from serialObject import *
import serial

class MotorController(threading.Thread):
	
	def __init__(self):
		# Init a new thread
		threading.Thread.__init__(self)
		# set up joystick logging file
		logging.basicConfig(filename='motor.log',level=logging.INFO)

	def run(self):
		x = 0
		y = 1
		while True:
			if x != globs.coordinates['x'] or y != globs.coordinates['y']:
				print(str(globs.coordinates['x']) + ',' + str(globs.coordinates['y']))
				x = globs.coordinates['x']
				y = globs.coordinates['y']
