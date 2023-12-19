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
TUNER_CLK = 5
TUNER_DT = 9
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
vol_change = 5
volClkLast = None
tunerClkLast = None

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
                vol_counter = vol_change
            else:
                vol_counter = -vol_change
        else:
            vol_counter = 0
    
    volClkLast = volClk

    # Pass encoder value to setVolume to work out the change.
    loop.call_later(0.5, lambda: asyncio.create_task(setVolume(vol_counter)))

def tuner_encoder(channel):
    global tuner_counter, tunerClkLast

    tunerClk = GPIO.input(TUNER_CLK)
    tunerDt = GPIO.input(TUNER_DT)

    #TODO: Add rotary encoder to control... something.

def clear_display():
    device.clear()

# We call this function to update the OLED with track information.
async def nowPlaying():
    last_title = None

    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_update()

        # We'll only update when the track changes.
        if player.title != last_title:
            if player.title:
                with canvas(device) as draw:
                    draw.text((left, middle), player.title, font=font_title, anchor="ls", fill="white")
                    draw.text((left, middle + 15), player.artist, font=font_artist, anchor="ls", fill="white")
            else:
                with canvas(device) as draw:
                    draw.text((left, middle), "No track information.", anchor="ls", font=font_info, fill="white")

        # This shouldn't get called... but just in case LMS is doing something odd.
        else:
            clear_display()

        last_title = player.title

# Interactions with Logitech Media Server
async def powerDevice():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_update()

        if player.power == 1: 
            await player.async_set_power(0)
        else:
            await player.async_set_power(1)

            # This makes sure the Now Playing display reappears after a manual power off.
            loop.run_in_executor(None, lambda: asyncio.run(nowPlaying()))

async def pauseTrack():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_toggle_pause()

async def setVolume(encoder_value):
    async with aiohttp.ClientSession() as session:
        lms = Server(session, LMS_SERVER)
        player = await lms.async_get_player(name=PLAYER_NAME)
        await player.async_update()

        # Add encoder value to volume.
        new_volume = player.volume + encoder_value
        new_volume = max(0, min(new_volume, 100))

        # Send to LMS.
        await player.async_set_volume(new_volume)

        # Display on OLED.
        with canvas(device) as draw:
            draw.text((left, middle), "Volume: " + str(new_volume), anchor="ls", font=font_info, fill="white")

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
    while True:
        async with aiohttp.ClientSession() as session:
            lms = Server(session, LMS_SERVER)
            player = await lms.async_get_player(name=PLAYER_NAME)
            await player.async_update()

            if player.mode == 'play':
                GPIO.output(CLOCK_LED,GPIO.HIGH)
                loop.run_in_executor(None, lambda: asyncio.run(nowPlaying()))

            # If we've stopped playback. Put away the fancy stuff.
            if player.mode == 'stop':
                GPIO.output(CLOCK_LED,GPIO.LOW)
                clear_display()

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
        GPIO.setup(TUNER_CLK, GPIO.IN)
        GPIO.setup(TUNER_DT, GPIO.IN)

        # Rotary encoders
        volClkLast = GPIO.input(VOL_CLK)

        # Event listeners
        GPIO.add_event_detect(BUTTON_VOL, GPIO.RISING, callback=pause, bouncetime=500)
        GPIO.add_event_detect(BUTTON_TUNER, GPIO.RISING, callback=tuner, bouncetime=500)
        GPIO.add_event_detect(VOL_CLK, GPIO.BOTH, callback=volume_encoder, bouncetime=225)
        GPIO.add_event_detect(TUNER_CLK, GPIO.BOTH, callback=tuner_encoder, bouncetime=225)

        # Run the main loop
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clear_display()
        GPIO.cleanup()
