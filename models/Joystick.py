import RPi.GPIO as GPIO

class Joystick:

    def __init__(self, pin1In, pin2In):
        self.pin1In = pin1In
        self.pin2In = pin2In 
