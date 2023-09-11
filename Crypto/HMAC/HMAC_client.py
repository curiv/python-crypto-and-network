#!/usr/bin/env python
# PAP client
import asyncio
import websockets
import hashlib


def gen_sha1_hmac(message,key):
    '''
    Source: https://ru.wikipedia.org/wiki/HMAC
    '''

    blocksize=64

    # aka ipad
    trans_5C = bytes((x ^ 0x5C) for x in range(256))

    # aka opad
    trans_36 = bytes((x ^ 0x36) for x in range(256))

    key_hex = key.encode().hex()[2:]

    # Convert hex key to bytes object
    key_bytes = bytes.fromhex(key_hex)

    # Add a zero-bytes padding to apply to blocksize
    key_bytes = key_bytes.ljust(blocksize, b'\0')

    # Xor each byte with 0x36 constant
    # K0 ⊕ ipad :
    xored_key_bytes_ipad = key_bytes.translate(trans_36)

    # Concatinate last value with hex-encoded message and do SHA1 on it
    # H( ( K ⊕  ipad ) || text )
    h1 = hashlib.sha1(xored_key_bytes_ipad + message.encode())

    # Xor each byte with 0x36 constant
    xored_key_bytes_opad = key_bytes.translate(trans_5C)

    # Now concat last value and previous hash-obj and do SHA1 on it
    return hashlib.sha1(xored_key_bytes_opad + h1.digest()).hexdigest()


async def try_auth(uri):
    async with websockets.connect(uri) as websocket:
        shared_key = "supersecret"
        message = "Hello from Kirill"

        welcome_message = await websocket.recv()
        print(f"Server answered: {welcome_message}")

        message_HMAC = gen_sha1_hmac(message, shared_key)

        print(f"I send message '{message}' with HMAC '{message_HMAC}' based on password '{shared_key}'")
        client_data = f"{message},{message_HMAC}"
        await websocket.send(client_data)

        answer = await websocket.recv()

        print(answer)

asyncio.get_event_loop().run_until_complete(
    try_auth('ws://localhost:1234')
)
