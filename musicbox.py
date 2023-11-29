#!/usr/bin/python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
import RPi.GPIO as GPIO

# OLED Display
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322

# Define input pins
BUTTON_VOL = 13
BUTTON_TUNER = 0
VOL_A = 6
VOL_B = 22
TUNER_A = 5
TUNER_B = 9

# Define LMS settings
LMS_SERVER = '10.0.1.100'
PLAYER_NAME = 'Radio'

# Setup OLED
serial = spi(device=0, port=0)
device = ssd1322(serial)

# Case I/O
def pause(channel):
    print("Pausing stream.")

def tuner(channel):
    print("Tuner pressed.")

def volume_encoder(channel):
    print("Encoder engaged.")

def tuner_encoder(channel):
    print("Encoder engaged.")

async def setup():
    async with aiohttp.ClientSession() as session:
      lms = Server(session, LMS_SERVER)
      player = await lms.async_get_player(name=PLAYER_NAME)
      await player.async_update()

if __name__ == '__main__':
  try:
    # Create and run the event loop for setup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(setup())

    # Now set up GPIO and the main event loop
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_VOL, GPIO.IN)
    GPIO.setup(BUTTON_TUNER, GPIO.IN)
    GPIO.setup(VOL_A, GPIO.IN)
    GPIO.setup(VOL_B, GPIO.IN)
    GPIO.setup(TUNER_A, GPIO.IN)
    GPIO.setup(TUNER_B, GPIO.IN)

    # Event listeners
    GPIO.add_event_detect(BUTTON_VOL, GPIO.RISING, callback=pause, bouncetime=500)
    GPIO.add_event_detect(BUTTON_TUNER, GPIO.RISING, callback=tuner, bouncetime=500)
    GPIO.add_event_detect(VOL_A, GPIO.RISING, callback=volume_encoder, bouncetime=10)
    GPIO.add_event_detect(TUNER_A, GPIO.RISING, callback=tuner_encoder, bouncetime=10)

    main_loop = asyncio.get_event_loop()
    main_loop.run_forever()

  except KeyboardInterrupt:
    pass
  except Exception as e:
    print(f"Error: {e}")
  finally:
    GPIO.cleanup()
