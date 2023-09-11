#!/usr/bin/env python
# PAP server
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


async def serve(websocket, path):
    shared_key = "supersecret"
    access_granted_message = "Access granted!"
    access_denied_message = "Access denied!"
    hello_message = "Please provide me a comma-separated message,hmac"
    await websocket.send(hello_message)

    client_data = await websocket.recv()
    client_message,client_hmac = client_data.split(",")
    print(f"Got new message '{client_message}' with HMAC '{client_hmac}'")

    server_side_hmac = gen_sha1_hmac(client_message,shared_key)
    print(f"Will compare client_HMAC '{client_hmac}' and server_side_HMAC '{server_side_hmac}' with shared_key '{shared_key}'")
    if client_hmac == server_side_hmac:
        print(access_granted_message)
        await websocket.send(access_granted_message)
    else:
        print(access_denied_message)
        await websocket.send(access_denied_message)


print("Server started!")
start_server = websockets.serve(serve, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
