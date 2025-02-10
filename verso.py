#!/usr/bin/python
import keyboard
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mxDynamixel, mxRequest
import time



portHandler = PortHandler('COM12')
#portHandler = PortHandler('/dev/ttyUSB0')
packetHandler = PacketHandler(1.0)
if portHandler.setBaudRate(1000000):
    pass
else:
    print("Failed to change the baudrate")
    quit()



j1 = mxDynamixel(2, 'AX-12A', portHandler, packetHandler)
j1.set_torque(True)
j1.set_speed(300)

pos = 500
request = None 
while True:
    if keyboard.is_pressed('w'):
        pos = pos + 50
        request = mxRequest('set_position', pos)
        print(j1.set_position(pos))

    if keyboard.is_pressed('s'):
        pos = pos - 50
        print(j1.set_position(pos))

    if keyboard.is_pressed('q'):
        pos = 150
        print(j1.set_position(pos))

    if keyboard.is_pressed('e'):
        pos = 850
        print(j1.set_position(pos))

    if keyboard.is_pressed('p'):
        print(j1.ping())
        


    if(request.command == 'set_position'):
        response = j1.set_position(request.data)
        if(response.ok):
            print("set_position: ok")
        else:
            print("set_position:" + response.error)
    
    #if(response.ok):
    #    print("Set position ", pos)
    #    readpos = j1.get_position()
    #    if(readpos.ok):
    #        print("Read position ", readpos.data)
    #    else:
    #        print("Unable to read position data")
    #else:
    #    print("Error occured", response.error)


