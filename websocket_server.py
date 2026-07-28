#!/usr/bin/env python3
import asyncio
import websockets
import json
from dynamixel_sdk import PortHandler, PacketHandler
from lib import mxDynamixel, mxRequest
from serial.tools import list_ports
import time


portHandler = None
packetHandler = None

# dictionary of servos
verso = {}  


def find_ft232h_port():
    for port in list_ports.comports():
        identity = " ".join(
            filter(None, [port.description, port.manufacturer, port.product, port.hwid])
        )
        if "Serial Converter" in identity:
            return port.device
    return None


# Define the WebSocket handler function
async def handle_message(websocket):
    try:
        # Keep the connection open and listen for messages
        async for message in websocket:
            request = json.loads(message)
            print(request)

            if(request["command"] == "change_position"):
                change_position(request)

            telemetry = json.dumps(get_telemetry())

            # send telemetry
            await websocket.send(telemetry)



    except websockets.ConnectionClosed:
        print("Client disconnected")


def get_telemetry():
    data = {}
    for id in verso['ids']:
        data[id] = verso[id].get_position().data
    return {"command": "telemetry", "data": data}



def change_position(request):
    id = request["data"]["id"]
    if id not in verso['ids']:
        print("Invalid id")
        return


    response = verso[id].get_position()
    if(response.ok == False):
        print("Error: Could not get position")
        return


    # the value will be from -1 to +1
    value = float(request["data"]["value"])

    delta = 0
    speed = 0
    if(abs(value) < 0.5):
        delta = 20
        speed = 20
    else:
        delta = 100
        speed = 100

    if(value < 0):
        delta = -delta

    newpos = response.data + delta
    verso[id].set_speed(speed)
    time.sleep(50/1000) # 50ms
    verso[id].set_position(newpos)







def setup_verso():
    device = find_ft232h_port()
    if device is None:
        print("Dynamixel USB Serial Converter not found")
        quit()

    print(f"Using Dynamixel adapter on {device}")

    portHandler = PortHandler(device)
    packetHandler = PacketHandler(1.0)
    if portHandler.setBaudRate(1000000):
        pass
    else:
        print("Failed to change the baudrate")
        quit()
        
 

    verso['ids'] = ['base_pitch', 'base_yaw', 'elbow_pitch', 'wrist_pitch', 'wrist_yaw', 'wrist_roll', 'grip']
    verso['base_pitch'] = mxDynamixel(2, 'AX-12A', portHandler, packetHandler)
    verso['base_yaw'] = mxDynamixel(3, 'AX-12A', portHandler, packetHandler)
    verso['elbow_pitch'] = mxDynamixel(4, 'AX-12A', portHandler, packetHandler)
    verso['wrist_pitch'] = mxDynamixel(5, 'AX-12A', portHandler, packetHandler)
    verso['wrist_yaw'] = mxDynamixel(6, 'AX-12A', portHandler, packetHandler)
    verso['wrist_roll'] = mxDynamixel(7, 'AX-12A', portHandler, packetHandler)
    verso['grip'] = mxDynamixel(9, 'AX-12A', portHandler, packetHandler)

    for s in verso['ids']:
        verso[s].set_torque(True)
        verso[s].set_speed(100)


        

    """"
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
    """



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
