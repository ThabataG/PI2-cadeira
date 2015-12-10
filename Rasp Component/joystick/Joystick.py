import threading

class Joystick(threading.Thread):
	def __init__(self):
		# Init a new thread
		threading.Thread.__init__(self)
		self.kill_received = False
		

	def run(self):
		while not self.kill_received:
			print("a")
