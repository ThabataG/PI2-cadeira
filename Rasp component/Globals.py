import threading

# Initialize global variables
def init_globals():
	global lock
	lock = threading.Condition()
	global coordinates
	coordinates = {'x': 0, 'y': 1}
	global x
	x = 0