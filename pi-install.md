Audio: [Adafruit MAX98357 I2S](https://www.adafruit.com/product/3006)
RTC: [DS3231 Real Time Clock](https://www.jaycar.com.au/rtc-clock-module-for-raspberry-pi/p/XC9044)

# Installation
## I2S DAC/Amp
Follow the Adafruit instructions for now. I'll update later :) 

## Real Time Clock
I use a Jaycar-special DS3231 RTC module. There wasn't much documentation out there, but it connects to pins 1,3,5,7 and 9. A real-time clock is possibly overkill given internet-connected and a flip clock. But let's do it anyway.

Install our dependencies:
```
sudo apt-get update
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```

We should have enabled I2C kernel support previously, but just in case. Go into raspi-config is enable it.

We'll now edit the modules file to add support for the RTC.
```
sudo nano /etc/modules

i2c-bcm2708
i2c-dev
rtc-ds1307
```

Check whether the DS3231 is detected. You should get a 'UU' in row 60, column 8.
```sudo i2cdetect -y 1```

Load the clock at boot. 
```
sudo nano /etc/rc.local
```

Add the following lines before exit 0
```
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
hwclock -s
```
