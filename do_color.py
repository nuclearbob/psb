#!/usr/bin/env python
import RPi.GPIO as GPIO
red = 33
green = 35
blue = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

red_pwm = GPIO.PWM(red, 60)
green_pwm = GPIO.PWM(green, 60)
blue_pwm = GPIO.PWM(blue, 60)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def do_colors(color):
    red, green, blue = color
    print(red)
    print(green)
    print(blue)
    red_pwm.ChangeDutyCycle(int(red))
    green_pwm.ChangeDutyCycle(int(green))
    blue_pwm.ChangeDutyCycle(int(blue))

import sys
import time

do_colors(sys.argv[1:])
#do_colors([100, 100, 100])
time.sleep(600)
