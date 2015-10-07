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
		joy = Joystick()
		self.assertNotEqual(joy,None)

	@patch.object(Joystick, 'receiveMsg')
	def testMockReceiveMsg(self,mock_output):
            mock_output.return_value=['00','88','ff']
            joy = Joystick()
            receivedMsg = joy.receiveMsg()
            self.assertEqual(receivedMsg,['00','88','ff'])

if __name__ == '__main__':
	unittest.main()
