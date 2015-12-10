import threading

class Motor(threading.Thread):
	# Initialize thread and Motor instance attributes
	def __init__(self):
		threading.Thread.__init__(self)
		self.killReceived = False

	# Start thread
	def run(self):
		while not self.killReceived:
			continue #print("b")
