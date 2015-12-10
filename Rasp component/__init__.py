# Import defensive programming tools
import logging
logging.basicConfig(filename="main.log", level=logging.DEBUG)

# Relative referenciation of modules
import sys, os, inspect
def referencePaths(pathsToImport):
	for path in pathsToImport:
		absolutePath = os.path.abspath(path)
		if absolutePath not in sys.path:
			sys.path.insert(0, absolutePath)

# Referencing and importing modules
pathsToImport = ["joystick", "motor", "communication"]
referencePaths(pathsToImport)

# Import modules
from Joystick import *
from Motor import *
