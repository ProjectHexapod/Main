import serial
import time
from array import array

s = serial.Serial(port="COM6", baudrate=1000000, timeout=2e-2)
#s.open()
#for c in 'a123456':
#	s.write(c)
cmd = array('B')
cmd.append(0x00)
clrstr = cmd.tostring()
f = list(range(256))
f.extend(range(255,-1,-1))
cmd = array('B')
cmd.append(0x20)
cmd.append(0x80)
cmd.append(0x00)
for i in f:
	cmd[2] = i
	cmd_string = cmd.tostring()
	s.write(cmd_string)
	retval = s.read(len(cmd_string))
	#for c in retval:
	try:
		print '%.2x'%ord(retval[1])
	except:
		for k in range(16):
			s.write(clrstr)
		retval = s.read()
		print 'cleared'
	time.sleep(2e-2)
#for c in retval:
#    print hex(ord(c))
print ''
s.close()