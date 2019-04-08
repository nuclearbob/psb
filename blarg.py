#!/usr/bin/env python

import datetime
import hashlib
import json
import os
import random
import re
import string
import time

import RPi.GPIO as GPIO
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from twitter_info import *


BLANK = [0, 0, 0]
MAGENTA = [0xf7, 0x0b, 0xef]
BLUE = [0x14, 0xcd, 0xd9]
LINK = '.-.. .. -. -.-'
IMAGE = '.. -- .- --. .'
RED_PIN = 33
GREEN_PIN = 35
BLUE_PIN = 37
PWM_FREQ = 60


def show_lights(color):
    red, green, blue = color_filter(color)
    RED_PWM.ChangeDutyCycle(red)
    GREEN_PWM.ChangeDutyCycle(green)
    BLUE_PWM.ChangeDutyCycle(blue)


def morse(morsestring, dotcolor, dashcolor):
    morselist = []
    for char in morsestring:
        if char == '.':
            morselist.append(dotcolor)
        if char == '-':
            morselist.append(dashcolor)
            morselist.append(dashcolor)
        morselist.append(BLANK)
    return morselist


def hexit(thing):
    chars = ''
    for char in thing:
        digit = (ord(char.lower()) - 87) % 16
        newchar = "%x" % digit
        chars += newchar
    return chars


def stringlights(lightstring, lang):
    lights = []
    for char in lightstring:
        if char in string.whitespace:
            # print('DEBUG: whitespace')
            lights.append(BLANK)
        else:
            digits = str(ord(char)) + hexit(lang) + '0000'
            digits = hashlib.md5(digits).hexdigest()[0:6]
            hexes = [int(digits[0:2], 16),
                     int(digits[2:4], 16),
                     int(digits[4:6], 16)]
            lights.append(hexes)
    lights.append(BLANK)
    return(lights)


def tweetlights(tweet, name='@{}'.format(username), method=show_lights):
    #print(tweet)
    if tweet['user']['screen_name'] == username:
        vampirism()
    images = []
    if 'media' in tweet['entities']:
        images = [x['url'] for x in tweet['entities']['media']]
    links = []
    if 'urls' in tweet['entities']:
        links = [x['url'] for x in tweet['entities']['urls']]
    text = tweet['text']
    text = strip_name(text, name)
    text = re.sub(' ' + '(?i)' + re.escape(name), '', text)
    text = re.sub('(?i)' + re.escape(name) + ' ', '', text)
    text = re.sub('(?i)' + re.escape(name), '', text)
    handles = ['@zedmartinez', '@nuclearbob']
    resplit = '({})'.format('|'.join(images + links + handles))
    #print(text)
    #print(resplit)
    bits = re.split(resplit, text, flags=re.IGNORECASE)
    for bit in bits:
        #print('DEBUG: bit %s' % bit)
        if bit in images:
            #print('DEBUG: image')
            lightsequence(morse(IMAGE, BLUE, MAGENTA), method)
        elif bit in links:
            #print('DEBUG: link')
            lightsequence(morse(LINK, MAGENTA, BLUE), method)
        elif bit.upper() == '@ZEDMARTINEZ':
            #print('zed')
            demigod_mode()
        elif bit.upper() == '@NUCLEARBOB':
            #print('bob')
            god_mode()
        else:
           # print('regular')
            lightsequence(stringlights(bit, tweet['lang']), method)


def god_mode():
    show_lights([0x00, 0x00, 0xff])
    time.sleep(5)


def demigod_mode():
    gradient([0xfc, 0x00, 0xff], [0xff, 0x8a, 0x00], 5, 100)

def strip_name(text, name):
    text = re.sub(' ' + '(?i)' + re.escape(name), '', text)
    text = re.sub('(?i)' + re.escape(name) + ' ', '', text)
    text = re.sub('(?i)' + re.escape(name), '', text)
    return text

def lightsequence(colors, method):
    #print('sequence')
    for color in colors:
        method(color)
        time.sleep(0.072)


def color_filter(color):
    color = [int(100.0*float(x)/256.0) for x in color]
    red, green, blue = color
    try:
        if TIMES_FILE and os.path.isfile(TIMES_FILE):
            with open(TIMES_FILE, 'r') as times_file:
                for line in times_file:
                    if '#' not in line:
                        #print(line)
                        start, stop, red_x, green_x, blue_x = line.split()
                        hour = datetime.datetime.now().hour
                        minute = datetime.datetime.now().minute
                        time = int('{}{}'.format(hour, minute))
                        #print(hour)
                        if time >= int(start) and time < int(stop):
                            #print('yeppers')
                            red = red * float(red_x)
                            green = green * float(green_x)
                            blue = blue * float(blue_x)
    except Exception:
        pass
    green = green * 0.35
    blue = blue * 0.6
    return ([red, green, blue])


def gradient(start, end, duration, steps):
    start_red = float(start[0])
    start_green = float(start[1])
    start_blue = float(start[2])
    end_red = float(end[0])
    end_green = float(end[1])
    end_blue = float(end[2])
    duration = float(duration)
    steps = int(steps)
    step_red = (end_red - start_red)/steps
    step_green = (end_green - start_green)/steps
    step_blue = (end_blue - start_blue)/steps
    red = start_red
    green = start_green
    blue = start_blue
    wait = duration/steps
    for _ in range(steps):
        #print([red, green, blue])
        show_lights([red, green, blue])
        red += step_red
        green += step_green
        blue += step_blue
        time.sleep(wait)


def a():
    gradient([0xfc, 0x05, 0xd6], [0x70, 0x00, 0x05], 0.2, 10)
    show_lights(BLANK)
    time.sleep(0.02)


def b():
    start = [0xd9, 0x02, 0x0b]
    show_lights(start)
    time.sleep(0.2)
    gradient(start, BLANK, 0.1, 10)


def c():
    gradient([0xe7, 0x3b, 0x05], [0xf0, 0x58, 0x04], 0.6, 10)
    gradient([0xf0, 0x68, 0x04], [0xff, 0xb4, 0x00], 0.25, 10)
    show_lights(BLANK)


def d():
    show_lights(BLANK)
    time.sleep(0.2)


def vampirism():
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    a()
    a()
    a()
    a()
    d()
    b()
    b()
    c()


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)


RED_PWM = GPIO.PWM(RED_PIN, PWM_FREQ)
GREEN_PWM = GPIO.PWM(GREEN_PIN, PWM_FREQ)
BLUE_PWM = GPIO.PWM(BLUE_PIN, PWM_FREQ)


RED_PWM.start(0)
GREEN_PWM.start(0)
BLUE_PWM.start(0)


class StdOutListener(StreamListener):
    def on_data(self, data):
        actual_data = json.loads(data)
        tweetlights(actual_data)
    def on_error(self, status):
        print(status)


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
#    stream.filter(follow=['@' + username])
    stream.filter(track=['@' + username])


if __name__ == '__main__':
    main()
