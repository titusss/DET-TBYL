import asyncio
import random
import websockets
from random import randrange
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

async def time(websocket, path):
    while True:
        moods = ['sad', 'happy', 'sleepy', 'neutral']
        mood = moods[randrange(4)]
        data, addr = sock.recvfrom(1024)
        data = data.decode("utf-8")
        await websocket.send(data)
        await asyncio.sleep(0.1)

async def main():
    async with websockets.serve(time, "localhost", 5678):
        await asyncio.Future()  # run forever

asyncio.run(main())