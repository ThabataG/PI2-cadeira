import sys,os,inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../joystick")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
print cmd_subfolder

import unittest
from mock import patch

#from joystick import Joystick
from Joystick import *

class testJoystick(unittest.TestCase):

	def testInit(self):
		joy = Joystick(10,11)
		self.assertNotEqual(joy,None)

unittest.main()
