#!/usr/bin/env python
# PAP server
import asyncio
import websockets

async def check_pass(received_password):
    stored_password = "letmein"
    if received_password == stored_password:
        return True
    else:
        return False


async def serve(websocket, path):
    access_granted_message = "Access granted!"
    access_denied_message = "Access denied!"
    hello_message = "Please provide me a password!"
    await websocket.send(hello_message)

    received_password = await websocket.recv()
    print(f"Got new auth attempt '{received_password}'")

    if await check_pass(received_password):
        await websocket.send(access_granted_message)
        print(access_granted_message)
    else:
        await websocket.send(access_denied_message)
        print(access_denied_message)


print("Server started!")
start_server = websockets.serve(serve, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
