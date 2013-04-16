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
cmd.append(0x45)
cmd.append(0x00)
cmd.append(0x00)
cmd.append(0x00)
cmd.append(0x00)
cmd.append(0x00)

while True:
    cmd[0] = 0x05 | (((cmd[0] & 0xf0) - 0x40 + 0x10) % 0x40 + 0x40)
    cmdstr = cmd.tostring()
    s.write(cmdstr)
    retval = s.read(len(cmdstr))
    for c in retval:
        print '%.2x' % ord(c),
    print ord(retval[2]) * 256 + ord(retval[3]), ord(retval[4]) * 256 + ord(retval[5]),
    print ''
    sleep(0.01 / 3)
