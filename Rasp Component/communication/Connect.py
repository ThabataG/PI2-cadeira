import Serial

class Connect(object):
	# Search for an openned serial port between [0,maxPortNumber] and open it
	# Return False if no ports where found and True otherwise
	@staticmethod
	def searchSerialPort(obj, maxPortNumber=1, serialPrefix="/dev/ttyACM"):
		# Reset obj.port if it is greater than maxPortNumber
		if obj.port > maxPortNumber:
			obj.port = 0
			logging
		# Search for an openned serial port
		couldConnect = False
		while obj.port <= maxPortNumber:
			obj.serial = Serial.init(serialPrefix + str(obj.port))
			if obj.serial == None:
				#logging.warning("Serial connection not performed in port " + str(obj.port))
				obj.port += 1
			else:
				couldConnect = True
				break
		return couldConnect

'''
	# 
	@staticmethod
	def tryReceiveData(obj):
		obj.serial.flushInput()
		rcv_str = obj.serial.read(10)
		if "Joystick" in str(obj.__class__):
			if(len(rcv_str) == 10):
				isOpen = True
			else:
				logging.info("Joystick :Failed to read from serial.")
				if obj.serial.isOpen():
					obj.serial.close()
				isOpen = False
		elif "Motor" in str(obj.__class__):
			if(len(rcv_str) == 0):
				isOpen = False
			else:
				logging.info("Motor: I don't want you, joy!")
				isOpen = True
		return isOpen
'''