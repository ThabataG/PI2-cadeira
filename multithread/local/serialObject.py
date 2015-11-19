import serial
#import RPi.GPIO as GPIO

class SerialObject(object):

    @staticmethod
    def initSerialObject(portName, allowWriting):
        serialObject = serial.Serial(
        	port = portName,
        	baudrate = 115200,
        	bytesize = serial.EIGHTBITS,			# Number of bits per bytes
        	parity = serial.PARITY_NONE,			# Set parity check: no parity
        	stopbits = serial.STOPBITS_ONE,			# Number of stop bits
        	timeout = 1,            				# Timeout block read
        	xonxoff = False,     					# Disable software flow control
        	rtscts = False,     					# Disable hardware (RTS/CTS) flow control
        	dsrdtr = False)       					# Disable hardware (DSR/DTR) flow control

        if allowWriting:
        	serialObject.writeTimeout = 2     		# Timeout for write

        return serialObject

    @staticmethod
    def connectWithSerialPort(serialObject):
       	serialObject.open()
        return serialObject

    @staticmethod
    def flushBuffer(serialObject):
        if serialObject.isOpen():
            try:
                serialObject.flushInput()
                serialObject.flushOutput()
            except Exception as exception:
                print("error communicating...: " + str(exception))
        else:
        	print("cannot open serial port ")

    @staticmethod
    def writeWithSerial(serialObject, cmd):
        try:
            serialObject.write(bytearray(cmd))
        except Exception as exception:
            print("Error writing the serial port: " + str(exception))
            return False
        return True
