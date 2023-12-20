# flip-radio
A project to convert an old Philips RS-100 clock radio into a modern smart speaker.

Ahhh yes... this project. I'll admit I originally didn't set out to convert a 1970's vintage clock radio into a streaming speaker... but one late night browse on everyone's favourite online marketplace opened the rabbithole I was about to fall down for the next few months. 

I was planning to use the [Squeezelite-ESP32](https://github.com/sle118/squeezelite-esp32) firmware as the core of my tinkering, but soon realised that I needed something a little more friendlier to bodging. I had a Pi Zero W hooked up to my home network running as a DVB server which struggled keeping up with some of the HD stations. I eventually decided to rotate through my stock of single-board computers and put it to use here. Be prepared. This is my first time programming in Python, let alone asynchronous Python. Be warned. She be very rough.

This project makes use of the [PySqueezebox](https://github.com/rajlaud/pysqueezebox) library to communicate with LMS. If you are adapting my work (which you're free to do), I highly recommend using LMS for multi-room audio. I'm yet to find something to replace it (yes, even Roon). It's very 2000s out of the box, but I'm constantly surprised by what I've been able to throw it. DSD256 files? Yep. DVB radio? Yep. Streaming analogue sources to other devices? YES!

## Build
Oooh boy. This clock was filthy... Before I did anything else, I pulled it apart[^1] and left the cream-coloured plastic out to retrobright in Brisbane's unescapable sunshine. Fellow makers - a warning that Orange Power is great for cleaning muck. But it will also  melt lettering off a large grocery chain's plastic bags with ease. Sigh! Talk about making it harder for myself.

![Dirty flip clock sitting atop red car](/docs/img/original-clock.jpg "Picking up the clock" | width=200)

At this point in the process, I knew the clock didn't flip - but not why it was stubborn to flip. A deep dive into the forums revealed that it's often the AC motors which fail which was certainly the case with this particular clock. Great. Where am I meant to find a replacement motor in 2023?!

I have to make a massive shout out to @dpwe's [StepperFlipClock](https://github.com/dpwe/StepperFlipClock) repository which helped in replacing the failed Copal motor with a 28BYJ-48 stepper motor. I found myself deep in horopalettology forums and found a very active community of hobbyists keeping these old clocks going. A quick trip to my local Jaycar and I had both a stepper motor and real-time clock to hand. Huzzah!

![Split flap mechanism in clock body](/docs/img/initial-fit.jpg "Initial clock mechanism fit" | width=200)

A quick test fit discovered another common problem with these mechanisms - the hour split-flap was just a little optimistic at the top of the hour. This is by far the most fiddly work I've done to date so I didn't think to photograph it. There are plenty of great [YouTube tutorials](https://www.youtube.com/watch?v=wzLPRFDi2xg) on how to fix this particular issue.



More to follow soon.
...
...


[^1]: I am comfortable working on low voltages but not high voltages. This project is low voltage by design. Opening old electronics comes with some risk and care required to discharge things appropriately. Don't be stupid. If you're working on high voltages, please. Call an electrician.

## Bill of Materials
- 1x Philips RS-100 Clock Radio
- 1x Raspberry Pi Zero WH (A$25)
- 1x DS3231 Real Time Clock Module (A$20)
- 1x 28BYJ-48 Stepper Motor + ULN2003 Driver (A$10)
- 1x Adafruit MAX98357 I<sup>2</sup>S Amplifier (A$10)
- 1x ER-OLEDM028-1W SPI OLED Display (US$30)
- 1x 'warm white' LED (A$0.07)
- 1x 330ohm resistor (A$0.10)
- 9x 1k resistor (A$2.70)
- 9x 10k resistor (A$2.70)
- 3x 2 wire screw terminal (A$3.90)
- 1x 3 wire screw terminal (A$2.50)
- 2x 1/4 size soldered breadboard (A$5)
- 2x EC11 rotary encoder (A$4.25)
- 1x 75mm 8ohm speaker (A$7.50)
- 1x barrel jack panel mount (A$6.75)

## Max Power Consumption
- Raspberry Pi Zero WH (5V, 1.2A)
- 28BYJ-48 Stepper Motor (5V, 240mA)
- Adafruit MAX98357 (2.5-5V, 650mA)
- SPI OLED Display (3-5V, 55mA)
- LED (2.7V, 20mA)
- DS3231 (3.3V, < 300µA)

Napkin maths... eh? 2.5A 'ought to be enough.

### Generative AI
Because I was building this at the same time as a [silly gift](https://github.com/asitwouldseem/groundhog-day/) some of the stepper motor code was partly produced by Generative AI. I had to adapt it for the Pi rather than Pico, but full disclosure nonetheless.
