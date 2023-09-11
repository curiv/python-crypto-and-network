#!/usr/bin/env python
# PAP client
import asyncio
import websockets


async def check_answer(received_answer):
    access_granted_message = "Access granted!"
    access_denied_message = "Access denied!"

    if received_answer == access_granted_message:
        return True
    elif received_answer == access_denied_message:
        return False
    else:
        raise "Wrong Answer!"

async def try_auth(uri):
    async with websockets.connect(uri) as websocket:
        password = "letmein"
        await websocket.send(password)
        welcome_message = await websocket.recv()
        print(welcome_message)

        answer = await websocket.recv()

        if await check_answer(answer):
            print("Continue")
        else:
            print("Try again")


asyncio.get_event_loop().run_until_complete(
    try_auth('ws://localhost:1234')
)
