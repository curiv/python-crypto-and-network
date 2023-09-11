#!/usr/bin/env python
# PAP client
from math import gcd as bltin_gcd
import random
from random import randint as rand
import Crypto.Util.number
import asyncio
import websockets


def gcd(a, b):
    # Функция поиска наибольшего общего делителя
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def mod_inverse(a, m):
    # Функция реализующая модулярную инверсию
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1


def isprime(n):
    # Функция проверки числа на простоту
    if n < 2:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, int(sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
    return True

def generate_keypair():
    # Берем случайные числа p,q от 1 до 1000
    #p = rand(1000, 10000)
    #q = rand(1000, 10000)

    keysize = 10

    # Выбираем диапазон чисел для генерации
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1
    primes = [2]
    # we choose two prime numbers in range(start, stop) so that the difference of bit lengths is at most 2.
    start = 1 << (keysize // 2 - 1)
    stop = 1 << (keysize // 2 + 1)

    # Prime numbers generation
    for i in range(5, nMax, 2):
        for p in primes:
            if i % p == 0:
                break
        else:
            primes.append(i)

    #choosing p and q from the generated prime numbers.
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_values = [q for q in primes if nMin <= p * q <= nMax]
        if q_values:
            q = random.choice(q_values)
            break
    print(f"p='{p}', q='{q}'")
    n = p * q
    phi = (p - 1) * (q - 1)

    #generate public key 1<e<phi(n)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while True:
        #as long as gcd(1,phi(n)) is not 1, keep generating e
        e = random.randrange(1, phi)
        g = gcd(e, phi)
        #generate private key
        d = mod_inverse(e, phi)
        if g == 1 and e != d:
            break

    return  n,e,d

def create_signature(message, privkey):
    d, n = privkey
    signature = pow(message, d, n)

    return signature

def decrypt_message(message,n,d):
    message = int(message)
    n = int(n)
    d = int(d)

    cleartext = pow(message,d,n)

    return cleartext


async def start_RSA_exchange(uri):
    async with websockets.connect(uri) as websocket:
        welcome_message = await websocket.recv()
        print(welcome_message)

        print("Generating public/private keypair...")
        n,e,d = generate_keypair()
        print(f"Public Key: {n},{e}")
        print(f"Private Key: {n},{d}")

        send_Pkey = f"{n},{e}".encode()

        print(f"Sending our Pkey '{send_Pkey}'")
        await websocket.send(send_Pkey)

        received_ctext = await websocket.recv()
        print(f"Получили шифротекст: '{received_ctext}'")

        cleartext = decrypt_message(received_ctext, n,d)
        print(f"Получили исходное сообщение: '{cleartext}'")

        

asyncio.get_event_loop().run_until_complete(
    start_RSA_exchange('ws://localhost:1234')
)
