#!/usr/bin/python3
from PIL import ImageFont
from pysqueezebox import Server
import RPi.GPIO as GPIO
import aiohttp
import asyncio
import time

# OLED display
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322

# Define input pins
BUTTON_VOL = 13
BUTTON_TUNER = 0
VOL_CLK = 6
VOL_DT = 22
CLOCK_LED = 23

# Define LMS settings
LMS_SERVER = '10.0.1.100'
PLAYER_NAME = 'Radio'

# OLED display
serial = spi(device=0, port=0)
device = ssd1322(serial)

padding = 5
top = 0 + padding
left = 0 + padding
bottom = device.size[1] - padding
right = device.size[0] - padding
middle = device.size[1] / 2

font_title = ImageFont.truetype('/home/cameron/fonts/WorkSans-SemiBold.ttf', 14)
font_artist = ImageFont.truetype('/home/cameron/fonts/WorkSans-Light.ttf', 12)
font_info = ImageFont.truetype('/home/cameron/fonts/WorkSans-Light.ttf', 12)

# Rotary encoders
vol_counter = 0
vol_change = 2
volClkLast = None

# Case I/O
def pause(channel):
    loop.run_in_executor(None, lambda: asyncio.run(pauseTrack()))

def tuner(channel):
    loop.run_in_executor(None, lambda: asyncio.run(powerDevice()))

def volume_encoder(channel):
    global vol_counter, volClkLast

    volClk = GPIO.input(VOL_CLK)
    volDt = GPIO.input(VOL_DT)

    if volClkLast is not None:
        if volClk != volClkLast:
            if volDt != volClk:
                vol_counter += vol_change
            else:
                vol_counter -= vol_change
    
    vol_counter = max(0, min(vol_counter, 100))
    volClkLast = volClk

    loop.run_in_executor(None, lambda: asyncio.run(setVolume(vol_counter)))

    # Print to terminal for debugging
    print(f"Volume changed to {vol_counter}")

def clear_display():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="black", fill="black")

# Interactions with Logitech Media Server
async def powerDevice():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_update()

        if player.power == 1: 
            await player.async_set_power(0)
            print("Goodbye.")
        else:
            await player.async_set_power(1)
            print("Hello.")

async def pauseTrack():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_toggle_pause()

async def currentVolume():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)

async def setVolume(volume):
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_set_volume(volume)

async def setup():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)

        with canvas(device) as draw:
          draw.text((left, middle), "Connection established.", font=font_info, anchor="ls", fill="white")

        # If we're not playing anything, it'll show this forever. Lame.
        time.sleep(5)
        clear_display()

async def main():
    last_title = None

    while True:
        async with aiohttp.ClientSession() as session:
            lms = Server(session, LMS_SERVER)
            player = await lms.async_get_player(name=PLAYER_NAME)
            await player.async_update()

            if player.title != last_title:
                if player.mode == 'play':
                    GPIO.output(CLOCK_LED,GPIO.HIGH)

                    if player.title:
                        with canvas(device) as draw:
                            draw.text((left, middle), player.title, font=font_title, anchor="ls", fill="white")
                            draw.text((left, middle + 15), player.artist, font=font_artist, anchor="ls", fill="white")
                    else:
                        with canvas(device) as draw:
                            draw.text((left, middle), "No track information.", anchor="ls", font=font_info, fill="white")

                elif player.mode == 'stop':
                    GPIO.output(CLOCK_LED,GPIO.LOW)
                    clear_display()

            last_title = player.title
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        # Create and run the event loop for setup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)        
        loop.run_until_complete(setup())

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CLOCK_LED, GPIO.OUT)
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

        # Run the main loop
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clear_display()
        GPIO.cleanup()
