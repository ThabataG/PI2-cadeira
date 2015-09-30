import unittest
import models.Joystick
#from unittest.mock import patch, call

#@patch("RPi.GPIO.output",autospec=True)
class TestJoystick(unittest.TestCase):
#    in1Pin = 11
#    in2Pin = 13

#    GPIO.setmode(GPIO.BOARD)
#    GPIO.setup(in1Pin,GPIO.IN)
#    GPIO.setup(in2Pin,GPIO.IN)

    def testInit(self):
        joy = Joystick(in1Pin,in2Pin)
        self.assertNotEqual(joy,nil)
#        mock_output.assert_has_calls([call(self.in1Pin, False),call(self.in2Pin, False)],any_order=True)

#if __name__ == '__main__':

unittest.main()
