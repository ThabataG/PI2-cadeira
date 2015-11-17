import threading

def init_globals():
	# Globals
	global lock
	lock = threading.Lock()
	global coordinates
	coordinates = {'x': 0, 'y': 1}
	global wait
	wait = False
