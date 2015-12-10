import sys, os, inspect

# Import defensive programming tools
import logging
logging.basicConfig(filename="main.log", level=logging.DEBUG)

# Relative referenciation of modules
def referencePaths(pathsToImport):
	for path in pathsToImport:
		absolutePath = os.path.abspath(path)
		if absolutePath not in sys.path:
			sys.path.insert(0, absolutePath)

# Referencing and importing modules
# import sys, os, inspect
pathsToImport = ["joystick", "motor", "communication"]
referencePaths(pathsToImport)

from Joystick import *
from Motor import *
