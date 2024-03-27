'''
	Library for Finamon GNSS/4G Modem HAT Shield.
'''
import os
import sys
import time

bRPi = False
if "win" not in sys.platform: 
    import smbus
    import gpiod
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
        
        if os.path.exists("/dev/gpiochip4"):
            chip = gpiod.Chip("/dev/gpiochip4")
            print("found /dev/gpiochip4 - RPi type is 5\n")
        elif os.path.exists("/dev/gpiochip0"):
            chip = gpiod.Chip("/dev/gpiochip0")
            print("found /dev/gpiochip0 - RPi type is 3 or 4\n")
        else:
            print("can't find dev/gpiodchipX\n")

        self.IN1_RI_LINE = chip.get_line(self.IN1_RI)
        self.IN1_RI_LINE.request(consumer="IN1_RI", type=gpiod.LINE_REQ_DIR_IN) #pull up
        self.IN2_RI_LINE = chip.get_line(self.IN2_RI)
        self.IN2_RI_LINE.request(consumer="IN1_RO", type=gpiod.LINE_REQ_DIR_IN) #pull up
        self.IN3_RI_LINE = chip.get_line(self.IN3_RI)
        self.IN3_RI_LINE.request(consumer="IN1_RO", type=gpiod.LINE_REQ_DIR_IN) #pull up
        self.IN4_RI_LINE = chip.get_line(self.IN4_RI)
        self.IN4_RI_LINE.request(consumer="IN4_RI", type=gpiod.LINE_REQ_DIR_IN) #pull up

        self.OUT1_RO_LINE = chip.get_line(self.OUT1_RO)
        self.OUT1_RO_LINE.request(consumer="OUT1_R0", type=gpiod.LINE_REQ_DIR_OUT)
        self.OUT2_RO_LINE = chip.get_line(self.OUT2_RO)
        self.OUT2_RO_LINE.request(consumer="OUT2_RO", type=gpiod.LINE_REQ_DIR_OUT)
        self.OUT3_RO_LINE = chip.get_line(self.OUT3_RO)
        self.OUT3_RO_LINE.request(consumer="OUT3_RO", type=gpiod.LINE_REQ_DIR_OUT)
        self.OUT4_RO_LINE = chip.get_line(self.OUT4_RO)
        self.OUT4_RO_LINE.request(consumer="OUT4_RO", type=gpiod.LINE_REQ_DIR_OUT)

        self.USER_BUTTON_LINE = chip.get_line(self.USER_BUTTON)
        self.USER_BUTTON_LINE.request(consumer="USER_BUTTON", type=gpiod.LINE_REQ_DIR_IN) #pull up
      
        self.USER_LED_LINE = chip.get_line(self.USER_LED)
        self.USER_LED_LINE.request(consumer="USER_LED", type=gpiod.LINE_REQ_DIR_OUT)
        
    def getStatus(self):
        gpio_list = [
            self.IN1_RI_LINE.get_value(),
            self.IN2_RI_LINE.get_value(),
            self.IN3_RI_LINE.get_value(),
            self.IN4_RI_LINE.get_value(),
            self.OUT1_RO_LINE.get_value(),
            self.OUT2_RO_LINE.get_value(),
            self.OUT3_RO_LINE.get_value(),
            self.OUT4_RO_LINE.get_value(),
            self.USER_BUTTON_LINE.get_value(),
            self.USER_LED_LINE.get_value()            
            ]
        status = 0
        for nr, gpio in reversed(list(enumerate(gpio_list))):
            status = (status << 1) | gpio
        return status
        
    def showIOs(self):
        print("inputs:  IN1_RI  %s  IN2_RI  %s  IN3_RI  %s  IN4_RI  %s" %
           (self.IN1_RI_LINE.get_value(),
            self.IN2_RI_LINE.get_value(),
            self.IN3_RI_LINE.get_value(),
            self.IN4_RI_LINE.get_value()))
        print("outputs: OUT1_RO %s  OUT2_RO %s  OUT3_RO %s  OUT4_RO %s" %
            (self.OUT1_RO_LINE.get_value(),
            self.OUT2_RO_LINE.get_value(),
            self.OUT3_RO_LINE.get_value(),
            self.OUT4_RO_LINE.get_value()))
        return

    # Function for reading user button
    def readUserButton(self):
        return self.USER_BUTTON_LINE.get_value()

    # Function for turning on user LED
    def turnOnUserLED(self):
        if not bRPi:
            return
        self.USER_LED_LINE.set_value(1) 

    # Function for turning off user LED
    def turnOffUserLED(self):
        if not bRPi:
            return
        self.USER_LED_LINE.set_value(0)

    


if __name__=='__main__':

    shield = GPS_4G_HAT_HW()
    for i in range (10):
        shield.OUT1_RO_LINE.set_value(0)
        shield.OUT2_RO_LINE.set_value(0)
        shield.OUT3_RO_LINE.set_value(0)
        shield.OUT4_RO_LINE.set_value(0)
        shield.showIOs()
        time.sleep(1)
        shield.OUT1_RO_LINE.set_value(1)
        shield.OUT2_RO_LINE.set_value(1)
        shield.OUT3_RO_LINE.set_value(1)
        shield.OUT4_RO_LINE.set_value(1)
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

    print("\npress/release buttons\n") 
    while(True):
        if shield.readUserButton():
            shield.turnOffUserLED()
        else:
            shield.turnOnUserLED()
            
        shield.OUT1_RO_LINE.set_value(shield.IN1_RI_LINE.get_value())
        shield.OUT2_RO_LINE.set_value(shield.IN2_RI_LINE.get_value())
        shield.OUT3_RO_LINE.set_value(not shield.IN3_RI_LINE.get_value())
        shield.OUT4_RO_LINE.set_value(not shield.IN4_RI_LINE.get_value())
        
