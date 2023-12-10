# flip-radio
A project to convert an old Philips RS-100 clock radio into a modern smart speaker.

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
- Scrap aluminium for brackets + fasteners

## Max Power Consumption
- Raspberry Pi Zero WH (5V, 1.2A)
- 28BYJ-48 Stepper Motor (5V, 240mA)
- Adafruit MAX98357 (2.5-5V, 650mA)
- SPI OLED Display (3-5V, 55mA)
- LED (2.7V, 20mA)
- DS3231 (3.3V, < 300µA)

Napkin maths... eh? 2.5A 'ought to be enough.

## Acknowledgements
Massive shout out to @dpwe's [StepperFlipClock](https://github.com/dpwe/StepperFlipClock/tree/main) respository which provides the basis for 28BYJ-48 stepper motors to replace the failing motors in flip clocks.
