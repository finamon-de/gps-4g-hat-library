'''
  power_down.py - This is script file to power down the module.
'''


import serial
import time, sys
sys.path.append('./')               # Adds higher directory to python modules path.
from gps4ghat.BG77X import BG77X

try:
    module = BG77X()
    time.sleep(2)

    module.getHardwareInfo()
    module.getFirmwareInfo()
    module.getIMEI()
    module.close()

    print("\nModule powered down with success!\n")

except Exception as e:
    # print(str(e))
    print("\nModule not powered down, an error occurred!\n")





# Manual routine
# ser = serial.Serial()

# ser.port = "/dev/serial0"
# ser.baudrate = 115200
# ser.parity=serial.PARITY_NONE
# ser.stopbits=serial.STOPBITS_ONE
# ser.bytesize=serial.EIGHTBITS

# ser.open()
# ser.write("AT+QPOWD=1\r".encode())
# time.sleep(1.)
# if(ser.in_waiting):
#     print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
# else:
#     print("shutdown problem detected")
# ser.close()

