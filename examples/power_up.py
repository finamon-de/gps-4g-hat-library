'''
  power_up.py - This is script file to power up module and let it powered on.
'''
import time, sys
sys.path.append('./')   # Adds higher directory to python modules path.
from gps4ghat.BG77X import BG77X

try:
    module = BG77X()
    time.sleep(2)

    module.getHardwareInfo()
    module.getFirmwareInfo()
    module.getIMEI()

    print("\nModule powered up with success!\n")

except Exception as e:
    # print(str(e))
    print("\nModule not powered up, an error occurred!\n")



