#!/usr/bin/env python
import asyncio
import websockets
import json
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mxDynamixel, mxRequest
import time


base_pitch = None
base_yaw = None
portHandler = None
packetHandler = None



# Define the WebSocket handler function
async def handle_message(websocket):
    try:
        # Keep the connection open and listen for messages
        async for message in websocket:
            request = json.loads(message)
            print(request)

            if(request["command"] == "set_position_delta"):
                set_position_delta(request)

            telemetry = json.dumps(get_telemetry())

            # send telemetry
            await websocket.send(telemetry)



    except websockets.ConnectionClosed:
        print("Client disconnected")


def get_telemetry():
    by = base_yaw.get_position()
    by = by.data

    bp = base_pitch.get_position()
    bp = bp.data


    ep = elbow_pitch.get_position()
    ep = ep.data


    wp = wrist_pitch.get_position()
    wp = wp.data

    wy = wrist_yaw.get_position()
    wy = wy.data

    wr = wrist_roll.get_position()
    wr = wr.data

    g = grip.get_position()
    g = g.data


    return {"command": "telemetry", "data": {"base_yaw": by, "base_pitch": bp, "elbow_pitch": ep, "wrist_pitch": wp, "wrist_yaw": wy, "wrist_roll" : wr, "grip": g}}



def set_position_delta(request):
    id = request["data"]["id"]
    if(id == None):
        print("Invalid id")
        return

    servo = None


    if(id == "base_yaw"):
        servo = base_yaw
    elif(id == "base_pitch"):
        servo = base_pitch
    elif(id == "elbow_pitch"):
        servo = elbow_pitch
    elif(id == "wrist_pitch"):
        servo = wrist_pitch
    elif(id == "wrist_yaw"):
        servo = wrist_yaw
    elif (id == "wrist_roll"):
        servo = wrist_roll
    elif(id == "grip"):
        servo = grip
    else:
        print("Invalid servo")
        return


    response = servo.get_position()
    if(response.ok == False):
        print("Error: Could not get position")
        return

    value = float(request["data"]["value"])
    
    delta = 0
    if(value < 0):
        delta = -100
    else:
        delta = 100

    #delta = int(50 * value)

    #newpos =  response.data + int(float(data["data"]["value"]) * 30)
    newpos = response.data + delta
    servo.set_position(newpos)







def setup_verso():
    portHandler = PortHandler('/dev/ttyUSB0')
    packetHandler = PacketHandler(1.0)
    if portHandler.setBaudRate(1000000):
        pass
    else:
        print("Failed to change the baudrate")
        quit()
        
 

    global base_yaw, base_pitch,  elbow_pitch, wrist_pitch, wrist_yaw, wrist_roll, grip
    base_yaw = mxDynamixel(3, 'AX-12A', portHandler, packetHandler)
    base_yaw.set_torque(True)
    base_yaw.set_speed(100)

    base_pitch = mxDynamixel(2, 'AX-12A', portHandler, packetHandler)
    base_pitch.set_torque(True)
    base_pitch.set_speed(100)


    elbow_pitch = mxDynamixel(4, 'AX-12A', portHandler, packetHandler)
    elbow_pitch.set_torque(True)
    elbow_pitch.set_speed(100)

    wrist_pitch = mxDynamixel(5, 'AX-12A', portHandler, packetHandler)
    wrist_pitch.set_torque(True)
    wrist_pitch.set_speed(100)


    wrist_yaw = mxDynamixel(6, 'AX-12A', portHandler, packetHandler)
    wrist_yaw.set_torque(True)
    wrist_yaw.set_speed(100)

    wrist_roll = mxDynamixel(7, 'AX-12A', portHandler, packetHandler)
    wrist_roll.set_torque(True)
    wrist_roll.set_speed(100)
    
    grip = mxDynamixel(9, 'AX-12A', portHandler, packetHandler)
    grip.set_torque(True)
    grip.set_speed(100)



# Start the WebSocket server
async def main():

    setup_verso()

    # Set host and port
    host = "0.0.0.0"
    port = 8765
    
    # Create and start the server
    server = await websockets.serve(
        handle_message,
        host,
        port
    )
    
    print(f"WebSocket server started at ws://{host}:{port}")
    
    # Keep the server running
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
