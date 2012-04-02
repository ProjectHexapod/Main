import serial
import time

s = serial.Serial(port="COM6", baudrate=2000000, timeout=2e-2)
#s.open()
#for c in 'a123456':
#	s.write(c)
s.write('a13579c')
print s.read(7)
print ''
s.close()