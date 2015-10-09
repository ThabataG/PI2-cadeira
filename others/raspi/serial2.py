import serial

# Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
s = serial.Serial('/dev/ttyACM0', 9600, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False) 
s.flushInput()
s.flushOutput()
while True:
  print s.readline()
