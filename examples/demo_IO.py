'''
	Library for Finamon GNSS/4G Modem HAT Shield.
'''

import sys
import time
sys.path.append('./')   # Adds higher directory to python modules path.

import RPi.GPIO as GPIO

from gps4ghat.GPS_4G_HAT_HW import GPS_4G_HAT_HW


shield = GPS_4G_HAT_HW()

while True:
    if GPIO.input(shield.IN1_RI):
        time.sleep(1)
        GPIO.output(shield.OUT1_RO, 0)
        time.sleep(.5)
        GPIO.output(shield.OUT1_RO, 1)

    if GPIO.input(shield.IN2_RI):
        time.sleep(1)
        for i in range (2):
            GPIO.output(shield.OUT2_RO, 0)
            time.sleep(.5)
            GPIO.output(shield.OUT2_RO, 1)
            time.sleep(.5)
 
    if not GPIO.input(shield.IN3_RI):
        time.sleep(1)
        for i in range (3):
            GPIO.output(shield.OUT3_RO, 0)
            time.sleep(.5)
            GPIO.output(shield.OUT3_RO, 1)
            time.sleep(.5)

    if not GPIO.input(shield.IN4_RI):
        time.sleep(1)
        for i in range (4):
            GPIO.output(shield.OUT4_RO, 0)
            time.sleep(.5)
            GPIO.output(shield.OUT4_RO, 1)
            time.sleep(.5)

    if not shield.readUserButton():
        time.sleep(1)
        for i in range (5*10):
            shield.turnOnUserLED()
            time.sleep(.1)
            shield.turnOffUserLED()
            time.sleep(.1)
