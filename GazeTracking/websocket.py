import asyncio
import random
import websockets
from random import randrange



async def time(websocket, path):
    while True:
        moods = ['sad', 'happy', 'sleepy', 'neutral']
        mood = moods[randrange(4)]
        await websocket.send(mood)
        await asyncio.sleep(5)

async def main():
    async with websockets.serve(time, "localhost", 5678):
        await asyncio.Future()  # run forever

asyncio.run(main())