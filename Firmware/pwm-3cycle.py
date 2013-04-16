import serial
from time import *
from array import array

s = serial.Serial(port="/dev/ttyUSB0", baudrate=500000, timeout=2e-1)

cmd = array('B')
cmd.append(0x00)
clrstr = cmd.tostring() * 16
s.write(clrstr)
retval = s.read(len(clrstr))
for c in retval:
    print '%.2x' % ord(c),
print ''

cmd = array('B')
cmd.append(0x03)
cmd.append(0x80)
cmd.append(0x00)
cmd.append(0x00)

while True:
    cmd[0] = 0x03 | (((cmd[0] & 0xf0) + 0x10) % 0x30)
    cmd[2] = (cmd[2] + 85) % 256
    cmd[3] = (cmd[3] + 85) % 256
    cmdstr = cmd.tostring()
    s.write(cmdstr)
    retval = s.read(len(cmdstr))
    for c in retval:
        print '%.2x' % ord(c),
    print ''
    sleep(0.01 / 3)
