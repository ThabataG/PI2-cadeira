import logging
import threading
import joystick
import globs

from serialObject import *
import serial

class JoystickController(threading.Thread):

	def __init__(self):
		# Init a new thread
		threading.Thread.__init__(self)
		# set up joystick logging file
		logging.basicConfig(filename='joy.log',level=logging.INFO)

	def run(self):
		while True:
			isOpen = False
			port = 0
			while True:
				while port < 10:
					try:
						s = SerialObject.initSerialObject("/dev/ttyACM" + str(port), False)
						isOpen = True
						port += 1
						break
					except serial.SerialException:
						print("SerialException: device " + str(port) + " could not be found or could not be configured.")
						port += 1
						continue
				if isOpen:
					try:
						s.flushInput()
						rcv_str = s.read(100)
						if(len(rcv_str) == 100):
							break
						else:
							logging.info("Failed to read from serial.")
							if s.isOpen():
								s.close()
							isOpen = False
					except serial.SerialException:
						logging.info("SerialException: port closed.")
						isOpen = False
					except Exception:
						logging.info("Flush input buffer error. (?)")
						if s.isOpen():
							s.close()
						isOpen = False
				else:
					port = 0
			if s.isOpen():
				try:
					#reset_input_buffer()				# Flush input buffer, discarding all its contents
					# reset_output_buffer()				# Flush output buffer, aborting current output
									   					# and discard all that is in buffer
					# Write data
					#s.write("AT+CSQ")
					#print("write data: AT+CSQ")
					#time.sleep(0.5)  				# Give the serial port sometime to receive the data
					logging.info("start writing...")
					while True:
						try:
							c = s.read(30)
							if(len(c) == 30):
								globs.lock.acquire()
								if c[0] & 1:
									globs.coordinates['x'] = c[1] & 0xFE
									globs.coordinates['y'] = c[0] | 0x01
								else:
									globs.coordinates['x'] = c[0] & 0xFE
									globs.coordinates['y'] = c[1] | 0x01
								globs.lock.release()
								#print(c)
							else:
								logging.info("JOY: failed to read from serial.")
								break
						except KeyboardInterrupt:
							logging.info("Exiting via keyboard interruption...")
							s.close()
							logging.info("communication closed.")
							exit()
					s.close()
					logging.info("communication closed.")
				except Exception as e:
					logging.info("error communicating...: " + str(e))
			else:
				logging.info("cannot open serial port ")

"""""""""""""""""""""""""""""""""
	def connect(self):
		isOpen = False
		port = 0
		while True:
			while port < 10:
				try:
					s = SerialObject.initSerialObject("/dev/ttyACM" + str(port), False)
					isOpen = True
					port += 1
					break
				except serial.SerialException:
					print("SerialException: device " + str(port) + " could not be found or could not be configured.")
					port += 1
					continue
			if isOpen:
				try:
					s.flushInput()
					rcv_str = s.read(100)
					if(len(rcv_str) == 100):
						return s
					else:
						logging.info("Failed to read from serial.")
						if s.isOpen():
							s.close()
						isOpen = False
				except serial.SerialException:
					logging.info("SerialException: port closed.")
					isOpen = False
				except Exception:
					logging.info("Flush input buffer error. (?)")
					if s.isOpen():
						s.close()
					isOpen = False
			else:
				port = 0

	def update(self, s):
		if s.isOpen():
			try:
				logging.info("start writing...")
				while True:
					try:
						c = s.read(2)
						if(len(c) == 2):
							globs.lock.acquire()
							if c[0] & 1:
								globs.coordinates['x'] = c[1] & 0xFE
								globs.coordinates['y'] = c[0] | 0x01
							else:
								globs.coordinates['x'] = c[0] & 0xFE
								globs.coordinates['y'] = c[1] | 0x01
							globs.lock.release()
							#print(c)
						else:
							logging.info("JOY: failed to read from serial.")
							break
					except KeyboardInterrupt:
						logging.info("Exiting via keyboard interruption...")
						s.close()
						logging.info("communication closed.")
						exit()
				s.close()
				logging.info("communication closed.")
			except Exception as e:
				logging.info("error communicating...: " + str(e))
		else:
			logging.info("cannot open serial port ")
"""""""""""""""""""""""""""""""""

'''''''''''''''''''''''''''''''''
	def run(self):
		joy = joystick.Joystick()
		try:
			while True:
				joy.connect()
				while True:
					if joy.update_performed():
						globs.lock.acquire()
						globs.coordinates = joy.coordinates
						print(str(globs.coordinates['x']) + ',' + str(globs.coordinates['y']) + ' ')
						globs.lock.release()
					else:
						joy.close_connection()
						break
		except KeyboardInterrupt:
			print("\nExiting via keyboard interruption...")
			joy.close_connection()
			exit()
'''''''''''''''''''''''''''''''''
