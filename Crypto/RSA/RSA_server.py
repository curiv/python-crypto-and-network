#!/usr/bin/env python
# PAP server
from math import gcd as bltin_gcd
import random
import Crypto.Util.number
import asyncio
import websockets

def encrypt_message(message,n,e):
    message = ord(message)
    n = int(n)
    e = int(e)

    cyphertext = pow(message,e,n)

    return cyphertext


async def serve(websocket, path):
    hello_message = "Please provide me your public key!"
    await websocket.send(hello_message)

    received_Pkey = await websocket.recv()
    print(f"received_Pkey: '{received_Pkey.decode()}'")

    n,e = received_Pkey.decode().split(',')

    print(f"Got new Pkey (n, e):'{n}, {e}'")
    
    message = 'm'

    print(f"Encrypted message '{message} ({ord(message)})' using public key '{e},{n}'")
    ctext = str(encrypt_message(message,n,e))

    print(f"Отправляем защифрованное сообщение: {ctext}")
    await websocket.send(ctext)
    

print("Server started!")
start_server = websockets.serve(serve, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
