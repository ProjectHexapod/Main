import serial
from time import *
from array import array

s = serial.Serial(port="/dev/ttyUSB0", baudrate=1000000, timeout=2e-2)

cmd = array('B')
cmd.append(0x00)
clrstr = cmd.tostring()*16
s.write(clrstr)
retval = s.read(len(clrstr))
for c in retval:
    print '%.2x' % ord(c),
print ''

cmd = array('B')
cmd.append(0x02)
cmd.append(0x1f)
cmd.append(0x00)

while True:
    cmd[0] = 0x02|(((cmd[0]&0xf0)+0x10)%0xf0)
    cmdstr = cmd.tostring()
    s.write(cmdstr)
    retval = s.read(len(cmdstr))
    for c in retval:
        print '%.2x' % ord(c),
    print ''
    sleep(0.01/3)
