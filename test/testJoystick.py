# usr/bin/bash -tt
import sys,os,inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../joystick")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
print (cmd_subfolder)

import unittest
from mock import patch

from Joystick import *

class testJoystick(unittest.TestCase):

    joy = None
    def setUp(self):
        global joy
        joy = Joystick()
        GPIO.cleanup()

    def tearDown(self):
        joy = None

    def testInit(self):
        self.assertNotEqual(joy,None)

    @patch.object(Joystick, 'readMsg')
    def testMockReceiveMsg(self,mock_output):
        mock_output.return_value="ab\n"
        receivedMsg = joy.readMsg()
        self.assertEqual(receivedMsg,"ab\n")

#using scale to engines: 1 to 10 => Foward
#                       -10 to -1 => Backward
#                        0 => Stop
    @patch.object(Joystick, 'readMsg')
    def testTranslateMsgFromMSPToCommandXAndY(self,mock_output):
        listOfValues = [200,201,10]
        mock_output.return_value=bytes(listOfValues)
        receivedMsg = joy.readMsg()
        command = joy.translateCommandFromMSP(receivedMsg)
        commandX = 200
        commandY = 201
        self.assertEqual(command,[commandX,commandY])

    @patch.object(Joystick,'readMsg')
    def testSendMessageToMSPEngines(self,mock_output):
        #[commandX,commandY,markerCharacter]
        listOfValues = [200,201,10]
        mock_output.return_value=bytes(listOfValues)
        receivedMsg = joy.readMsg()
        command = joy.translateCommandFromMSP(receivedMsg)
        success = joy.sendMessageToEnginesMSPs(command)

        self.assertEqual(success,True)

    @patch.object(Joystick,'readMsg')
    def testTranslateMessageWithMissingValue(self,mock_output):
        #[commandX,Missing commandY,markerCharacter]
        listOfValues = [200,10]
        mock_output.return_value=bytes(listOfValues)
        receivedMsg = joy.readMsg()
        isMissingValue = joy.verifyIfMessageContainsError(receivedMsg)

        self.assertEqual(isMissingValue,True)


if __name__ == '__main__':
	unittest.main()
