#!/usr/bin/env python
# PAP server
from math import gcd as bltin_gcd
import random
import Crypto.Util.number
import asyncio
import websockets


def GenDHParams(p,g):
	bits = 8
	Privkey = random.randint(1,2**bits)
	Pkey = (g ** Privkey) % p
	return Pkey,Privkey


async def serve(websocket, path):
    hello_message = "Please provide me your public key!"
    await websocket.send(hello_message)

    received_Pkey = await websocket.recv()
    Pkey, p, g = received_Pkey.decode().split(",")
    Pkey = int(Pkey)
    p = int(p)
    g = int(g)

    print(f"Got new Pkey:'{Pkey}', Prime Number:'{p}', Primal Root:'{g}'")

    Send_Pkey, Privkey = GenDHParams(p, g)

    print(f"Sending our Pkey '{Send_Pkey}'")
    await websocket.send(str(Send_Pkey).encode())
    
    shared_secret = Pkey ** Privkey % p
    print(f"Calculated shared secret '{shared_secret}'")


print("Server started!")
start_server = websockets.serve(serve, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
