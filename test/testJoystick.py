import sys,os,inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../joystick")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
print (cmd_subfolder)

import unittest
from mock import patch

from Joystick import *

class testJoystick(unittest.TestCase):


	def testInit(self):
		joy = Joystick(10,11)
		self.assertNotEqual(joy,None)

#	@patch.object(Joystick,pinX='f',pinY='8')
	def testTurnRight(self):
		joy = Joystick(10,11)
		joy.setPinX('f')
		joy.setPinY('8')
#		mock_output.
		self.assertEqual(joy.pinX,'f')
		self.assertEqual(joy.pinY,'8')

	def testTurnLeft(self):
		joy = Joystick(10,11)
		joy.setPinX('0')
		joy.setPinY('8')
		self.assertEqual(joy.pinX,'0')
		self.assertEqual(joy.pinY,'8')


#	@patch(Joystick,pinX,pinY)
#	def testRight(self,mock):

if __name__ == '__main__':
	unittest.main()
