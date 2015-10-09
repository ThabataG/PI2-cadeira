class Joystick(object):
    def __init__(self):
        return None

    def receiveMsg(self):
        return None

    def translateCommandFromMSP(self,message):
        message = message.rstrip('\n')
        command = message.split(" ",1)
        return command

    def sendMessageToMSP(self,command):
        return False
