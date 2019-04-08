#!/usr/bin/env python

import random
import time


def hexit(thing):
    chars = ''
    for char in thing:
        digit = (ord(char.lower()) - 87) % 16
        newchar = "%x" % digit
        chars += newchar
    return chars


def tweetlights(tweet):
    lights = []
    for char in tweet.text:
        digits = str(ord(char)) + hexit(tweet.lang) + '0000'
        digits = digits[0:6]
        shuffled = ''.join(random.sample(digits, 6))
        hexes = [int(shuffled[0:2], 16),
                 int(shuffled[2:4], 16),
                 int(shuffled[4:6], 16)]
        lights.append(hexes)
    lights.append([0, 0, 0])
    return(lights)


def lightsequence(colors, method):
    for color in colors:
        method(color)
        time.sleep(0.072)
