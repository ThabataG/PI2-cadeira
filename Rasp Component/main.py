# Relative referenciation of modules
def referencePaths(pathsToImport):
	import sys, os, inspect
	for path in pathsToImport:
		absolutePath = os.path.abspath(path)
		if absolutePath not in sys.path:
			print("insert with success " + absolutePath)
			sys.path.insert(0, absolutePath)

# Referencing modules to be imported
pathsToImport = ['joystick', 'motor', 'communication']
referencePaths(pathsToImport)

from Joystick import *

# Main
if __name__ == "__main__":
	joystick = Joystick()
	joystick.start()
	
	try:
		joystick.join()
	except KeyboardInterrupt:
		joystick.kill_received = True
		print("aê bixin")