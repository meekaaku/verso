#!/usr/bin/env python

import asyncio
import websockets

# Define the WebSocket handler function
async def echo_handler(websocket):
    try:
        # Keep the connection open and listen for messages
        async for message in websocket:
            print(f"Received message: {message}")
            # Echo the message back to the client
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start the WebSocket server
async def main():
    # Set host and port
    host = "0.0.0.0"
    port = 8765
    
    # Create and start the server
    server = await websockets.serve(
        echo_handler,
        host,
        port
    )
    
    print(f"WebSocket server started at ws://{host}:{port}")
    
    # Keep the server running
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())