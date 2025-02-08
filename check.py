#!/usr/bin/python
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mkDynamixel
import time




portHandler = PortHandler('COM12')
#portHandler = PortHandler('/dev/ttyUSB0')
packetHandler = PacketHandler(1.0)
if portHandler.setBaudRate(1000000):
    pass
else:
    print("Failed to change the baudrate")
    quit()



j1 = mkDynamixel(2, 'AX-12A', portHandler, packetHandler)
j1.set_torque(True)

while True:
    j1.set_position(500)
    time.sleep(1)
    j1.set_position(700)
    time.sleep(1)


