#!/usr/bin/python3
from pysqueezebox import Server
import aiohttp
import asyncio
import RPi.GPIO as GPIO
from time import sleep

# Define input pins
BUTTON_VOL = 13
BUTTON_TUNER = 0
VOL_CLK = 6
VOL_DT = 22

# Define LMS settings
LMS_SERVER = '10.0.1.100'
PLAYER_NAME = 'Radio'

# Global variables for rotary encoder
vol_counter = 0
volClkLast = None

# Case I/O
def pause(channel):
    loop.run_in_executor(None, lambda: asyncio.run(pauseTrack()))
    
    # Print to terminal for debugging
    print("Transport command sent.")

def tuner(channel):
    loop.run_in_executor(None, lambda: asyncio.run(pauseTrack()))

def volume_encoder(channel):
    global vol_counter, volClkLast

    volClk = GPIO.input(VOL_CLK)
    volDt = GPIO.input(VOL_DT)
    
    if volClkLast is not None:
        if volClk != volClkLast:
            if volDt != volClk:
                vol_counter += 2
            else:
                vol_counter -= 2
    
    vol_counter = max(0, min(vol_counter, 100))
    volClkLast = volClk

    loop.run_in_executor(None, lambda: asyncio.run(setVolume(vol_counter)))

    # Print to terminal for debugging
    print(f"Volume changed to {vol_counter}")

async def pauseTrack():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_toggle_pause()

async def setVolume(volume):
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_set_volume(volume)

async def setup():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)

        # Print to terminal for debugging
        print("LMS connection established.")

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
        GPIO.setup(VOL_CLK, GPIO.IN)
        GPIO.setup(VOL_DT, GPIO.IN)

        # Rotary encoders
        volClkLast = GPIO.input(VOL_CLK)

        # Event listeners
        GPIO.add_event_detect(BUTTON_VOL, GPIO.RISING, callback=pause, bouncetime=500)
        GPIO.add_event_detect(BUTTON_TUNER, GPIO.RISING, callback=tuner, bouncetime=500)
        GPIO.add_event_detect(VOL_CLK, GPIO.BOTH, callback=volume_encoder, bouncetime=10)

        main_loop = asyncio.get_event_loop()
        main_loop.run_forever()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()
