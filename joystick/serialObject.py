import serial, time
import RPi.GPIO as GPIO

class SerialObject(object):

    @staticmethod
    def initSerialObject(usbPort):
        serialObject = serial.Serial()

        serialObject.port = usbPort
        serialObject.baudrate = 9600
        serialObject.bytesize = serial.EIGHTBITS 			# Number of bits per bytes
        serialObject.parity = serial.PARITY_NONE 			# Set parity check: no parity
        serialObject.stopbits = serial.STOPBITS_ONE 		# Number of stop bits
        serialObject.timeout = 1            				# Timeout block read
        serialObject.xonxoff = False     					# Disable software flow control
        serialObject.rtscts = False     					# Disable hardware (RTS/CTS) flow control
        serialObject.dsrdtr = False       					# Disable hardware (DSR/DTR) flow control
        serialObject.writeTimeout = 2     					# Timeout for write
        return serialObject

    @staticmethod
    def connectWithSerialPort(serialObject):
        try:
        	serialObject.open()
        except Exception as e:
        	print("error open serial port: " + str(e))
        	exit()
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
    def writeWithSerial(serialObject, command):
        try:
            serialObject.write('\n')	
            serialObject.write(chr(command[0]))
            serialObject.write(chr(command[1]))
        except Exception as e:
            print("Error write in serial port: " + str(e))
            return False
        return True
