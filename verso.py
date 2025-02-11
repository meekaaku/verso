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
j1.set_cw_limit(200)
j1.set_ccw_limit(800)

response = j1.get_position()
pos = response.data
#request = mxRequest(0,0) 
request = mxRequest(0,0)
i = 0
print("Verso ready. Press x to quit")
while True:
    if keyboard.is_pressed('w'):
        pos = pos + 10
        request = mxRequest('set_position', pos)

    if keyboard.is_pressed('s'):
        pos = pos - 10
        request = mxRequest('set_position', pos)

    if keyboard.is_pressed('q'):
        pos = 150
        request = mxRequest('set_position', pos)

    if keyboard.is_pressed('e'):
        pos = 850
        request = mxRequest('set_position', pos)

    if keyboard.is_pressed('p'):
        print(j1.ping())

    if keyboard.is_pressed('x'):
        exit()
        


    if(request.command == 'set_position'):
        response = j1.set_position(request.data)
        response = j1.get_position()
        i = i + 1
        if(response.ok):
            print(str(i) + ") set_position: ok " + str(response.data))
        else:
            print(str(i) + ") set_position:" + response.error)
    

    request = mxRequest(0,0)
    #if(response.ok):
    #    print("Set position ", pos)
    #    readpos = j1.get_position()
    #    if(readpos.ok):
    #        print("Read position ", readpos.data)
    #    else:
    #        print("Unable to read position data")
    #else:
    #    print("Error occured", response.error)


