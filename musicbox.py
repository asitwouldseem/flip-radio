#!/usr/bin/python3
from pysqueezebox import Server, Player
import RPi.GPIO as GPIO
import aiohttp
import asyncio

SERVER = '10.0.1.100'
VOL_A = 5
VOL_B = 22
VOL_BUTTON = 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(VOL_A, GPIO.IN)
GPIO.setup(VOL_B, GPIO.IN)
GPIO.setup(VOL_BUTTON, GPIO.IN)

async def main():
  async with aiohttp.ClientSession() as session:
    lms = Server(session, SERVER)
    player = await lms.async_get_player(name="Radio")

    await player.async_update()
    print(player.album)
    await player.async_play()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
