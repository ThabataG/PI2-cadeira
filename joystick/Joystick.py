import RPi.GPIO as GPIO
from serialObject import *

pinNumber = 11

class Joystick(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pinNumber,GPIO.IN)
        self.setupInterruption()

    def setupInterruption(self):
        initSerialObject()
        GPIO.add_event_detect(pinNumber, GPIO.RISING, callback=readMsg, bouncetime=300)

    def translateCommandFromMSP(self,message):
        message = message.rstrip('\n')
        command = message.split(" ",1)
        return command

    def sendMessageToMSP(self,command):
        return False
