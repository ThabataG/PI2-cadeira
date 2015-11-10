import sys,os,inspect

# Relative importation of pathsToImport modules
pathsToImport = ['joystick', 'motor']
for path in pathsToImport:
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],path)))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)

from Joystick import *
from Motor import *

if __name__ == "__main__":
    joy = Joystick()
    motor = Motor()
    while True:
        try:
            joy.updateXY()
            print("Command: " + str(joy.x) + " " + str(joy.y))
            # motor.sendMessageToMSP(joy.x, joy.y)
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt occured!\n")
            exit()
