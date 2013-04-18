import serial
import time
from math import *
from array import array

s = serial.Serial(port="COM3", baudrate=1000000, timeout=2e-2)
# s.open()
# for c in 'a123456':
#	s.write(c)
cmd = array('B')
cmd.append(0x40)
cmd.append(0x00)
cmd.append(0x01)
cmd.append(0x02)
cmd.append(0x03)
# cmd.append(0x00)
n_clear = 0

sin_val = 0
cos_val = 0
f = open('test_data.txt', 'w')

# for i in f:
i = 0
# while 1:
while time.clock() < 20:
#	cmd[2] = i
    cmd_string = cmd.tostring()
    s.write(cmd_string)
#	i = (i + 1)%64
    retval = s.read(len(cmd_string))

    if len(retval) < 5:
        continue
    sin_val = ord(retval[1]) * 256 + ord(retval[2]) - 1207
    cos_val = ord(retval[3]) * 256 + ord(retval[4]) - 1207

    # for c in retval:
#	for j in range(len(retval)):
#		print '%.2x'%ord(retval[j])

#        outstring = str(time.clock())
    outstring = str(time.clock()) + ',' + str(sin_val) + ',' + str(cos_val) + ',' + str(atan2(sin_val, cos_val)) + '\n'
#        print(outstring)
    f.write(outstring)
#        print sin_val, cos_val, atan2(sin_val, cos_val)
#	print ''

#	time.sleep(0.002)
f.close()
s.close()
