import asyncio
import websockets
from random import randrange

async def time(websocket, path):
    i = 0
    while True:
        if i > 3:
            i = 0
        moods = ['sleepy', 'sad', 'neutral', 'happy']
        mood = moods[i]
        i += 1
        await websocket.send(mood)
        await asyncio.sleep(8)

async def main():
    async with websockets.serve(time, "localhost", 5678):
        await asyncio.Future()  # run forever

asyncio.run(main())