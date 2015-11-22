
# usr/bin/bash -tt
import sys,os,inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../motor")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
print (cmd_subfolder)

import unittest
from mock import patch

from Motor import *

class testMotor(unittest.TestCase):

    motor = None
    def setUp(self):
        global motor
        motor = Motor()

    def tearDown(self):
        motor = None

    def testInit(self):
        self.assertNotEqual(motor,None)

    def testSendMessageToMSPEngines(self):
        #[commandX,commandY,markerCharacter]
        x = int(200)
        y = int(201)
        isSendedWithSuccess = motor.sendMessageToMSP(x,y)

        self.assertEqual(isSendedWithSuccess,True)

if __name__ == '__main__':
	unittest.main()
