import serial
import time
from array import array

s = serial.Serial(port="COM6", baudrate=1000000, timeout=2e-2)
#s.open()
#for c in 'a123456':
#	s.write(c)
cmd = array('B')
cmd.append(0x00)
clrstr = cmd.tostring()*16
f = list(range(256))
f.extend(range(255,-1,-1))
cmd = array('B')
cmd.append(0x20)
cmd.append(0x80)
cmd.append(0x00)
n_clear = 0

#for i in f:
while 1:
	cmd[2] = 0
	cmd_string = cmd.tostring()
	s.write(cmd_string)
	#retval = s.read(len(cmd_string))
	
	#for c in retval:
	#for j in range(len(retval)):
	#	print '%.2x'%ord(retval[j])
	#print ''
	#if len(retval)==0:
	#	continue
	#if ord(retval[0]) != 0x2f:
	#	print 'Clear!'
	#	n_clear += 1
	#	s.write(clrstr)
	#	s.read(65000)
	#except:
	#	for k in range(16):
	#		s.write(clrstr)
	#	retval = s.read()
	#	print 'cleared'
	#time.sleep(2e-2)
#for c in retval:
#    print hex(ord(c))
print 'Bus error detected %d times out of %d transactions'%(n_clear,len(f))
s.close()