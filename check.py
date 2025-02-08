#!/usr/bin/python
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mkDynamixel
import time




<<<<<<< Updated upstream
portHandler = PortHandler('/dev/ttyUSB0')
if portHandler.openPort():
    pass
else:
    print("Failed to open the port")
    quit()


=======
portHandler = PortHandler('COM12')
#portHandler = PortHandler('/dev/ttyUSB0')
>>>>>>> Stashed changes
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
    time.sleep(0.05)
    j1.set_position(700)
    time.sleep(0.25)


