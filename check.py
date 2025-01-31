#!/usr/bin/python
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mkDynamixel




portHandler = PortHandler('/dev/ttyUSB0')
packetHandler = PacketHandler(1.0)

j1 = mkDynamixel(1, 'AX-12A', portHandler, packetHandler)

j1.connect()

