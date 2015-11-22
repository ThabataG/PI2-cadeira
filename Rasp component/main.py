import sys, os, inspect
import logging
import threading

# Relative importation of pathsToImport modules
pathsToImport = ['local']
for path in pathsToImport:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],path)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

import joystickController
import motorController
import globs

if __name__ == "__main__":
	# Config log file
	logging.basicConfig(filename='main.log',level=logging.INFO)

	# Init global variables
	globs.init_globals()

	# Create new threads
	joy = joystickController.JoystickController()
	motor = motorController.MotorController()

	# Start new Threads
	joy.start()
	motor.start()

	while True:
		try:
			continue
		except KeyboardInterrupt:
			print("keyboard interruption here")
			print("Exiting Main Thread")
			exit()
	# Wait for thread to finish running
	#joy.join()
	#motor.join()
