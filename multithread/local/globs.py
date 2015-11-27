import threading

def init_globals():
	# Globals
    global lock
    lock = threading.Condition()
    global coordinates
    coordinates = {'x': 0, 'y': 1}
    global wait
    wait = True
#    global serialJoystick
#    serialJoystick = None
