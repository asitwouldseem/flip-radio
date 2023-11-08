#!/usr/bin/python3
from pysqueezebox import Server, Player
import RPi.GPIO as GPIO
import time
import aiohttp
import asyncio

# Radio Features
SERVER = '10.0.1.100'
CLOCK_LED = 12

# Clock Features
IN1 = 24
IN2 = 23
IN3 = 17
IN4 = 27
CYCLE_STEPS = 1280

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLOCK_LED,GPIO.OUT)

# Setup Stepper Motor


# Handle LMS player interactions
async def main():
    async with aiohttp.ClientSession() as session:
      lms = Server(session, SERVER)
      player = await lms.async_get_player(name="Radio")
      await player.async_update()

      if (player.power):
        GPIO.output(CLOCK_LED,GPIO.HIGH)
        print("LED on")
      else:
        GPIO.output(CLOCK_LED,GPIO.LOW)
        print("LED off")

      await player.async_play()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
