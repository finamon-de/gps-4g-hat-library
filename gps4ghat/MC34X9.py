'''
	Library for Finamon GNSS/4G Modem HAT Shield.
'''
from enum import Enum

import smbus
import time

#----------------------------------------------------------------------------------------
# Register Adresses
#----------------------------------------------------------------------------------------

#DEV_STATUS_REG =        0x05
#INTR_CTRL_REG =         0x06
#MODE_REG =              0x07
#RATE_REG =              0x08
#MOTION_CTRL_REG =       0x09
#STATUS_REG =            0x13
#INTR_STAT_REG =         0x14

#RANGE_REG =             0x20
#COMM_CTRL_REG =         0x31
#GPIO_CTRL_REG =         0x33
#TF_THRESH_REG =         0x40
#TF_DEBOUNCE_REG =       0x42
#AM_THRESH_REG =         0x43
#AM_DB_REG =             0x45
#SHK_THRESH_REG =        0x46
#PK_P2P_DUR_THRES_REG =  0x48
#TIMER_CTRL_REG =        0x4A

#XOUT_REG =              0x0D
#YOUT_REG =              0x0F
#ZOUT_REG =              0x11

class MC34X9_REG(Enum):
    DEV_STAT        = 0x05
    INTR_CTRL       = 0x06
    MODE            = 0x07
    RATE            = 0x08
    MOTION_CTRL     = 0x09
    FIFO_STAT       = 0x0A
    FIFO_RD_P       = 0x0B
    FIFO_WR_P       = 0x0C
    XOUT_LSB        = 0x0D
    XOUT_MSB        = 0x0E
    YOUT_LSB        = 0x0F
    YOUT_MSB        = 0x10
    ZOUT_LSB        = 0x11
    ZOUT_MSB        = 0x12
    STATUS          = 0x13
    INTR_STAT       = 0x14
    REG_15          = 0x15
    PROD            = 0x18
    REG_1C          = 0x1C
    RANGE           = 0x20
    XOFFL           = 0x21
    XOFFH           = 0x22
    YOFFL           = 0x23
    YOFFH           = 0x24
    ZOFFL           = 0x25
    ZOFFH           = 0x26
    XGAIN           = 0x27
    YGAIN           = 0x28
    ZGAIN           = 0x29
    REG_2B          = 0x2B
    FIFO_CTRL       = 0x2D
    FIFO_TH         = 0x2E
    FIFO_INTR       = 0x2F
    FIFO_CTRL_SR2   = 0x30
    COMM_CTRL       = 0x31
    GPIO_CTRL       = 0x33
    TF_THRESH_LSB   = 0x40
    TF_THRESH_MSB   = 0x41
    TF_DEBOUNCE     = 0x42
    AM_THRESH_LSB   = 0x43
    AM_THRESH_MSB   = 0x44
    AM_DB           = 0x45
    SHK_THRESH_LSB  = 0x46
    SHK_THRESH_MSB  = 0x47
    SHK_DUR_LSB     = 0x48
    SHK_DUR_MSB     = 0x49
    TIMER_CTRL      = 0x4A

class MC34X9_RANGE(Enum):
    RANGE_2G  = 0  #          000: ± 2g
    RANGE_4G  = 1  #          001: ± 4g
    RANGE_8G  = 2  #          010: ± 8g
    RANGE_16G = 3  #          011: ± 16g
    RANGE_12G = 4  #          100: ± 12g
    RANGE_END = 5
    
#----------------------------------------------------------------------------------------
#     defaults
#----------------------------------------------------------------------------------------

MODE_STANDBY =  0b00
MODE_WAKE =     0b01

#----------------------------------------------------------------------------------------
#	MC3419 support Class
#----------------------------------------------------------------------------------------

class MC34X9:

    _motionCtrlReg = 0              # Motion control register
    _shakeDuration = 0              # Share duration
    _shakePeakToPeakDuration = 0    # Peak to peak setting for shake functionality
    _i2cAddr = 0x4C                 # Address of MC3419 device 0x4C/0x6C

    acc = {'X': 0, 'Y': 0,'Z': 0, 'Xg': .0, 'Yg': .0,'Zg': .0}
    cfgRange = MC34X9_RANGE.RANGE_2G
    
    def  __init__(self):
 
        self.i2cBus = smbus.SMBus(1)     # Get I2C bus
        pass

    # Set the mode register.
    # All bits beyond bit 1 are not used in SPI mode
    # 
    #  mode: Mode to set device to
    #      Bits 0-1: Operational state
    #          00: Standby
    #          01: Wake
    #          10: Reserved
    #          11: Reserved
    def setDeviceMode(self, mode):
        self.writeRegister(MC34X9_REG.MODE, mode)
        
    def setStandbyMode(self):
        self.writeRegister(MC34X9_REG.MODE, MODE_STANDBY)
        
    def setWakeMode(self):
        self.writeRegister(MC34X9_REG.MODE, MODE_WAKE)
        
    # Set the sample rate.
    # This is only valid for SPI speeds < 4MHz
    # 
    #  samplerate: Sample rate to set
    #      0x10: 25 Hz
    #      0x11: 50 Hz
    #      0x12: 62.5 Hz
    #      0x13: 100 Hz
    #      0x14: 125 Hz
    #      0x15: 250 Hz
    #      0x16: 500 Hz
    #      0x17: 1000 Hz
    def setSampleRate(self, sampleRate):
        self.writeRegister(MC34X9_REG.RATE, sampleRate)

    # Set range and scale of accelerometer
    # 
    #  data: data to set
    #    Bits 0-2: Low pass filter configuration
    #          000: Reserved
    #          001: Bandwidth setting 1, Fc = IDR/4.255
    #          010: Bandwidth setting 2, Fc = IDR/6
    #          011: Bandwidth setting 3, Fc = IDR/12
    #          100: Reserved
    #          101: Bandwidth setting 5, Fc = IDR/16
    #          110: Reserved
    #          111: Reserved
    #    Bit 3:    Low pass filter enabled (1):or disabled (0)
    #    Bits 4-6: Resolution range
    #          000: ± 2g
    #          001: ± 4g
    #          010: ± 6g
    #          011: ± 16g
    #          100: ± 12g
    #          101: Reserved
    #          110: Reserved
    #          111: Reserved
    #    Bit 7:    Reserved
    def  setRange(self, res_range = MC34X9_RANGE.RANGE_2G):
        self.cfgRange = res_range
        val = self.readRegister(MC34X9_REG.RANGE)
        val &= 0x07
        val |= (res_range << 4) & 0x70
        self.writeRegister(MC34X9_REG.RANGE, val)

    # Set the communication control register.
    # Bits 0-3 and 7 are reserved
    # 
    #  data: Com control
    #      Bit 4: Swap interrupt pin functionality (no swap: 0, swap: 1)
    #      Bit 5: Enable (1):or disable (0):SPI 3-wire mode. Not supported in this library
    #      Bit 6: Enable (1):or disable (1):clearing of individual interrupt flags. Not supported in this library
    def  setComControl(self, data):
        self.writeRegister(MC34X9_REG.COMM_CTRL, data)

    # Set GPIO control register
    # Bits 0, 1, 4 and 5 are reserved
    # 
    #  data: GPIO control
    #      Bit 2: Set polarity of INT1 output. Active low (0):or active high (1)
    #      Bit 3: Select between open dran (0):or push/pull (1):mode of INT1 output
    #      Bit 6: Set polarity of INT2 output. Active low (0):or active high (1)
    #      Bit 7: Select between open dran (0):or push/pull (1):mode of INT2 output
    def  setGPIOControl(self, data):
        self.writeRegister(MC34X9_REG.GPIO_CTRL, data)

    # Set motion control register. Enables flags and interrupts for motion detection features
    # 
    #  data: features to enable
    #      bit 0: Tilt & flip enable
    #      bit 1: Latch outputs (disabled: 0, enabled: 1)
    #      bit 2: Anymotion enable
    #      bit 3: Shake enable
    #      bit 4: Tilt35 enable
    #      bit 5: Z axis orientation. Positive through top (0):or bottom (1):of package
    #      bit 6: Enable (0):or disable (1):filtering of motion data
    #      bit 7: Set (1):or clear (0):motion block reset
    def  setMotionControl(self, data):
        self._motionCtrlReg = data
        self.writeRegister(MC34X9_REG.MOTION_CTRL, data)

     # Reset the motion block.
     # Sets and then clears bit 7 of the motion control register
    def  resetMotionControl(self):
        self.setDeviceMode(MODE_STANDBY)
        self.writeRegister(MC34X9_REG.MOTION_CTRL, self._motionCtrlReg | 1<<7)
        self.writeRegister(MC34X9_REG.MOTION_CTRL, self._motionCtrlReg)
        self.setDeviceMode(MODE_WAKE)

    # Get motion status data
    # Motion detection must be enabled using setMotionControl():for these flags to be active
    # 
    # @returns status: data in status register
    #      bit 0: Tilt flag
    #      bit 1: Flip flag
    #      bit 2: Anymotion flag
    #      bit 3: Shake flag
    #      bit 4: Tilt35 flag
    #      bit 5: FIFO flag
    #      bit 6: Reserved
    #      bit 7: New data flag
    def getStatus(self):
        return self.readRegister(MC34X9_REG.STATUS)

    # Configure what interrupts to enable
    # Motion detection must be enabled using setMotionControl()
    # 
    #  data:     interrupts to enable
    #      bit 0: Tilt interrupt
    #      bit 1: Flip interrupt
    #      bit 2: Anymotion interrupt
    #      bit 3: Shake interrupt
    #      bit 4: Tilt35 interrupt
    #      bit 5: Reserved
    #      bit 6: Auto clear
    #      bit 7: Acquisition interrupt
    def  setInterrupt(self, data):
        self.writeRegister(MC34X9_REG.INTR_CTRL, data)

    # Get the interrupt status. 
    # For interrupts to trigger, motion detection must be enabled using setMotionControl():and interrupts must be enabled using setInterrupt().
    # 
    # @returns interruptStatus:  data in the interrupt status register
    #      bit 0: Tilt interrupt
    #      bit 1: Flip interrupt
    #      bit 2: Anymotion interrupt
    #      bit 3: Shake interrupt
    #      bit 4: Tilt35 interrupt
    #      bit 5: FIFO interrupt
    #      bit 6: Auto clear
    #      bit 7: Acquisition interrupt
    def getInterruptStatus(self):
        return self.readRegister(MC34X9_REG.INTR_STAT)

    # Clears all interrupts in the interrupt status register
    def  clearInterrupts(self):
        self.writeRegister(MC34X9_REG.INTR_STAT, 0)

    # Gets the acceleration in x-direction
    # @returns acceleration: acceleration in x direction
    def getX(self):
        return self.readRegister(MC34X9_REG.XOUT_LSB, 2)

    # Gets the acceleration in y-direction
    # @returns acceleration: acceleration in y direction
    def getY(self):
        return self.readRegister(MC34X9_REG.YOUT_LSB, 2)

    # Gets the acceleration in x-direction
    # @returns acceleration: acceleration in x direction
    def getZ(self):
        return self.readRegister(MC34X9_REG.ZOUT_LSB, 2)

    # Sets the threshold value for the tilt/flip/tilt-35 functionality.
    # Tilt and/or flip must be enabled in the motion control register using setMotionControl().
    # 
    # Threshold value is 15 bit.
    # Acceleration values greater than the threshold value will result in a tilt condition.
    # Acceleration values smaller than the treshold value will result in a flat/flip condition, depending on the value of the z-axis
    # 
    #  threshold:  Threshold value
    def  setTiltThreshold(self, threshold):
        self.writeRegister(MC34X9_REG.TF_THRESH_LSB, threshold, 2)

    # Sets the tilt/flip debounce duration.
    # Each consecutive time a tilt/flip condition is detected, a counter is incremented. If this counter exceeds the duration value, the tilt/flip interrupt is set.
    # 
    #  duration: Duration
    def  setTiltDebounce(self, debounce):
        self.writeRegister(MC34X9_REG.TF_DEBOUNCE, debounce)

    def  setAnymotionThreshold(self, threshold):
        self.writeRegister(MC34X9_REG.AM_THRESH_LSB, threshold, 2)

    def  setAnymotionDebounce(self, debounce):
        self.writeRegister(MC34X9_REG.AM_DB, debounce)

    def  setShakeThreshold(self, data):
        self.writeRegister(MC34X9_REG.SHK_THRESH_LSB, data, 2)

    def  setShakePeakToPeakDuration(self, data):
        if (data > 4095):
            return
        _shakePeakToPeakDuration = data
        d = _shakePeakToPeakDuration | self._shakeDuration<<12
        self.writeRegister(MC34X9_REG.SHK_DUR_LSB, d, 2)

    def  setShakeDuration(self, data):
        if (data > 7):
            return
        _shakeDuration = data
        self.setShakePeakToPeakDuration(self._shakePeakToPeakDuration)

    def readAccel(self):
        faRange = [19.614, 39.228, 78.456, 156.912, 117.684] #{2g, 4g, 8g, 16g, 12g}        
        faResolution = 32768.0 #16bit

        self.acc['X'] = self.readRegister(MC34X9_REG.XOUT_LSB, 2)
        if self.acc['X'] > 0x7FFF:
            self.acc['X'] -= 0xFFFF
            
        self.acc['Y'] = self.readRegister(MC34X9_REG.YOUT_LSB, 2)
        if self.acc['Y'] > 0x7FFF:
            self.acc['Y'] -= 0xFFFF
            
        self.acc['Z'] = self.readRegister(MC34X9_REG.ZOUT_LSB, 2)
        if self.acc['Z'] > 0x7FFF:
            self.acc['Z'] -= 0xFFFF

        k = faRange[self.cfgRange]/faResolution
        self.acc['Xg'] = round((float)(self.acc['X']) * k, 3)
        self.acc['Yg'] = round((float)(self.acc['Y']) * k, 3)
        self.acc['Zg'] = round((float)(self.acc['Z']) * k, 3)

    def printAccel(self):
       print("m/s^2(counts) X %5.3f(%6d) \tY %5.3f(%6d)  \tZ %5.3f(%6d)" %
          (self.acc['Xg'], self.acc['X'], self.acc['Yg'], self.acc['Y'], self.acc['Zg'], self.acc['Z']))

    # Read data from one or more registers
    #  address:         register address to read from
    #  bytesToRead:     number of bytes to read (1 or 2)
    # @returns data:    data that has been read
    def readRegister(self, address, bytesToRead = 1):
        data = -1
        if bytesToRead == 1:
           data = self.i2cBus.read_byte_data(self._i2cAddr, address.value)
        elif bytesToRead == 2:
            data = self.i2cBus.read_word_data(self._i2cAddr, address.value)
        else:
            print("TODO: implement multibyte read")
        #print("read " + str(bytesToRead) + " bytes from registers "+ str(address))
        return data

    # Writes data to one or more registers
    #  address:     register address to write to
    #  data:        data to write
    #  bytesToSend: number of bytes to send (1 or 2)
    def  writeRegister(self, address, data, bytesToSend = 1):
        if bytesToSend == 1:
            self.i2cBus.write_byte_data(self._i2cAddr, address.value, data)
            #print("write byte \t" + hex(data) + " \tto register " + address.name)
        elif bytesToSend == 2:
            self.i2cBus.write_word_data(self._i2cAddr, address.value, data)
            #print("write word \t" + hex(data) + " \tto register " + address.name)
        else:
            print("TODO: implement multibyte write")
            print("write " + str(bytesToSend) + " bytes \tto register "+ address.name)

    # Writes data to set of registers
    def runScenario(self, list_scen):
        for setting in  list_scen:
            self.writeRegister(setting[0], setting[1])


if __name__=='__main__':

    accel = MC34X9()
    #print("who am I: " + hex(accel.i2cBus.read_byte_data(accel._i2cAddr, 0x0D)))
    
    SAMPLE_RATE = 0x10
    TILT_DEBOUNCE = 5
    TILT_ANGLE = 10
    TILT_THRESHOLD = 15*TILT_ANGLE
    
    AM_DEBOUNCE = 5
    AM_THRESHOLD = 15*TILT_ANGLE

    accel.setStandbyMode()                      #Put accelerometer in standby mode
    accel.setGPIOControl(0b00001100)            #Set GPIO control. Set bit 2 to 1 for INT active high, set bit 3 to 1 for INT push-pull
    accel.setSampleRate(SAMPLE_RATE)            #Set the sample rate

#    accel.setInterrupt(0b00000001)              #Set the interrupt enable register, bit 0 enables tilt, bit 1 enables flip, bit 3 enables shake. Set bit 6 to 1 for autoclear
#    accel.setTiltThreshold(TILT_THRESHOLD)      #Set tilt threshold
#    accel.setTiltDebounce(TILT_DEBOUNCE)        #Set tilt debounce
#    accel.setMotionControl(0b00000001)          #Enable motion control features. Bit 0 enables tilt/flip, bit 2 enables anymotion (req for shake), bit 3 enables shake, bit 5 inverts z-axis

    accel.setInterrupt(0b00000100)              #Set the interrupt enable register, bit 0 enables tilt, bit 1 enables flip, bit 3 enables shake. Set bit 6 to 1 for autoclear
    accel.setAnymotionThreshold(AM_THRESHOLD)   #Set tilt threshold
    accel.setAnymotionDebounce(AM_DEBOUNCE)     #Set tilt debounce
    accel.setMotionControl(0b00000100)          #Enable motion control features. Bit 0 enables tilt/flip, bit 2 enables anymotion (req for shake), bit 3 enables shake, bit 5 inverts z-axis

    accel.setRange(MC34X9_RANGE.RANGE_2G.value) #Set accelerometer range
    accel.clearInterrupts()                     #Clear the interrupt register
    accel.resetMotionControl()                  #Reset the motion control
    accel.setWakeMode()                         #Wake up accelerometer

    accel.readAccel()
    accel.printAccel()

    #for reg in MC34X9_REG:       
    #    print("%02X: %02X %s" % (reg.value, accel.readRegister(reg), reg.name))
    
    print("\nmove board for any motion detection\n")
    while True:
        if accel.getStatus() != 0xA0:
            accel.readAccel()
            accel.printAccel()
        time.sleep(.5)
  


