import threading

class Motor(threading.Thread):
	# Initialize thread and Motor instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.kill_received = False

	# Start thread
	def run(self):
		while not self.kill_received:
			print("b")
