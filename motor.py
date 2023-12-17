#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# 28BYJ-48 Pins
IN1 = 17
IN2 = 27
IN3 = 14
IN4 = 15

# Adjust to match the Copal mechanism
STEPS_PER_MINUTE = 80

pins = [IN1, IN2, IN3, IN4]
sequence = [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.OUT)

def move_motor(steps):
    for _ in range(steps):
        for step in sequence:
            for i in range(len(pins)):
                GPIO.output(pins[i], step[i])
                time.sleep(0.001)

def clock():
    current_time = time.localtime(time.time())

    if current_time.tm_sec == 0:
        move_motor(STEPS_PER_MINUTE)
        print("Moved the clocks forward.")

if __name__ == '__main__':
    try:
        while True:
            clock()
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()
