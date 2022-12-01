'''
	Library for Finamon GNSS/4G Modem HAT Shield.
'''

import sys
import time

bRPi = False
if "win" not in sys.platform: 
    import smbus
    import RPi.GPIO as GPIO
    bRPi = True


class GPS_4G_HAT_HW:
    # Peripheral Pin Definations Finamon
    USER_BUTTON = 27  
    USER_LED = 22

    #inputs
    IN1_RI = 5
    IN2_RI = 6
    IN3_RI = 24
    IN4_RI = 25

    #outputs
    OUT1_RO = 12
    OUT2_RO = 16
    OUT3_RO = 20
    OUT4_RO = 21

    def __init__(self):
        if not bRPi:
            return
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        time.sleep(0.5)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.IN1_RI, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.IN2_RI, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.IN3_RI, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.IN4_RI, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        GPIO.setup(self.OUT1_RO, GPIO.OUT)
        GPIO.setup(self.OUT2_RO, GPIO.OUT)
        GPIO.setup(self.OUT3_RO, GPIO.OUT)
        GPIO.setup(self.OUT4_RO, GPIO.OUT)
        
        GPIO.setup(self.USER_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.USER_LED, GPIO.OUT)
        
    def getStatus(self):
        gpio_list = [
            GPIO.input(self.IN1_RI),
            GPIO.input(self.IN2_RI),
            GPIO.input(self.IN3_RI),
            GPIO.input(self.IN4_RI),
            GPIO.input(self.OUT1_RO),
            GPIO.input(self.OUT2_RO),
            GPIO.input(self.OUT3_RO),
            GPIO.input(self.OUT4_RO),
            GPIO.input(self.USER_BUTTON),
            GPIO.input(self.USER_LED)            
            ]
        status = 0
        for nr, gpio in reversed(list(enumerate(gpio_list))):
            status = (status << 1) | gpio
        return status
        
    def showIOs(self):
        print("inputs:  IN1_RI  %s  IN2_RI  %s  IN3_RI  %s  IN4_RI  %s" % 
            (GPIO.input(self.IN1_RI), GPIO.input(self.IN2_RI), GPIO.input(self.IN3_RI), GPIO.input(self.IN4_RI)))
        print("outputs: OUT1_RO %s  OUT2_RO %s  OUT3_RO %s  OUT4_RO %s" % 
            (GPIO.input(self.OUT1_RO), GPIO.input(self.OUT2_RO), GPIO.input(self.OUT3_RO), GPIO.input(self.OUT4_RO)))
        return

    # Function for reading user button
    def readUserButton(self):
        return GPIO.input(self.USER_BUTTON)

    # Function for turning on user LED
    def turnOnUserLED(self):
        if not bRPi:
            return
        GPIO.output(self.USER_LED, 1)

    # Function for turning off user LED
    def turnOffUserLED(self):
        if not bRPi:
            return
        GPIO.output(self.USER_LED, 0)

    


if __name__=='__main__':

    shield = GPS_4G_HAT_HW()
    for i in range (10):
        GPIO.output(shield.OUT1_RO, 0)
        GPIO.output(shield.OUT2_RO, 0)
        GPIO.output(shield.OUT3_RO, 0)
        GPIO.output(shield.OUT4_RO, 0)
        shield.showIOs()
        time.sleep(1)
        GPIO.output(shield.OUT1_RO, 1)
        GPIO.output(shield.OUT2_RO, 1)
        GPIO.output(shield.OUT3_RO, 1)
        GPIO.output(shield.OUT4_RO, 1)
        shield.showIOs()
        print("status: 0x%04X" % shield.getStatus())
        time.sleep(1)

    for i in range (5):
        print("\nuser LED ON") 
        shield.turnOnUserLED()
        time.sleep(1)

        print("user LED OFF") 
        shield.turnOffUserLED()
        time.sleep(1)

    print("\npress/release button\n") 
    while(True):
        if shield.readUserButton():
            shield.turnOffUserLED()
        else:
            shield.turnOnUserLED()
