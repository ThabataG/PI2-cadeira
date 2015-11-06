import sys,os,inspect
# Relative importation of joystick module
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"joystick")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from Joystick import *

if __name__ == "__main__":
    joy = Joystick()
    while True:
        try:
            command = joy.getMessage()
            if command != None:
                message = joy.translateCommandFromMSP(command)
                print("Command: " + ''.join(str(e) + " " for e in message))
#                print("Command:")
#                print(command)
#                if command != "":
#                    joy.sendMessageToEnginesMSPs(command)
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt occured!\n")
            exit()
