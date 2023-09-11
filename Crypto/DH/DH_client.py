#!/usr/bin/env python
# PAP client
from math import gcd as bltin_gcd
import random
import Crypto.Util.number
import asyncio
import websockets


def primRoots(modulo):
    # Функция подсчета первообразного корня по модулю. Можно найти пример реализации в интернете
    required_set = {num for num in range(1, modulo) if bltin_gcd(num, modulo) }
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]


def GenDHParams():
	bits = 8
	Privkey = random.randint(1,2**bits)
    # p - случайное простое число в диапазоне 2^8
	p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
    # g - первообразный корень по модулю p
	g = primRoots(p)[-1]
	Pkey = (g ** Privkey) % p
	return Pkey, Privkey, p, g

async def start_DH_exchange(uri):
    async with websockets.connect(uri) as websocket:
        welcome_message = await websocket.recv()
        print(welcome_message)

        send_Pkey, Privkey, p, g = GenDHParams()

        send_Pkey = f"{send_Pkey},{p},{g}".encode()

        print(f"Sending our Pkey '{send_Pkey}'")
        await websocket.send(send_Pkey)

        received_Pkey = await websocket.recv()
        print(f"Got new Pkey '{received_Pkey}'")

        shared_secret = int(received_Pkey.decode()) ** Privkey % p
        print(f"Calculated shared secret '{shared_secret}'")



asyncio.get_event_loop().run_until_complete(
    start_DH_exchange('ws://localhost:1234')
)
