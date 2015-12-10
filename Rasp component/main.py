"""
  Universidade de Brasília - Campus Gama
  Disciplina: Projeto Integrador II
"""
from __init__ import *

# Main
if __name__ == "__main__":
	try:
		# Initialize and run components
		joystick = Joystick()
		motor = Motor()
		joystick.start()
		motor.start()
		# Wait for components to stop their routines
		joystick.join()
		motor.join()

	# When ^C is pressed, the kill_received flag is setted
	except KeyboardInterrupt:
		joystick.killReceived = True
		motor.killReceived = True
		logging.info("Exiting program")
		exit()

	# When a threading exception is raised
	except Exception:
		joystick.kill_received = True
		motor.kill_received = True
		logging.critical("Threading exception raised, closing the program")
		exit()
