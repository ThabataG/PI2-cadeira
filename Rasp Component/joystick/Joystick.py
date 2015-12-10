import threading

class Joystick(threading.Thread):
	# Initialize thread and Joystick instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.kill_received = False

	# Start thread
	def run(self):
		while not self.kill_received:
			print("a")
