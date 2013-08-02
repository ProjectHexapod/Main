

from mtlib.mtdevice import MTDevice

# Set up MTx and put it in measurement mode
def get_imu_reader(port='/dev/ttyUSB1'):
    mt = MTDevice(port)
    mt.GoToConfig()
    mt.SetOutputSettings(1<<3) #matrix format orient
    mt.SetOutputMode(7) #temp, acc, rate of turn, mag, orient
    mt.GoToMeasurement()
    return mt
