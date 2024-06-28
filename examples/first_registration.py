'''
  first_registration.py - This is script file to configure RATs and connection technology to the 4G network
'''
import time
import os, sys
sys.path.append('./')   # Adds higher directory to python modules path.
from gps4ghat.BG77X import BG77X, RAT

# Init module
registered = False
contextID = "1"
module = BG77X()
time.sleep(2)

# Configure network, change RAT type as you need
module.debug_print("INFO: Configuring network...")
_rat = module.configNetwork(RAT.eMTC)
module.debug_print("INFO: Configured for %s" % _rat)

# Step 1: Initial step, search for networks and try automatic registration
# Step 2: Manual registration but need to set numeric_operator_code
#          It can be read from step scanned operators from step 1. log. 
#          Example ...,(1,"Telekom.de","TDG","26201",8),....
#          "26201" is numeric_operator_code. Please set proper value on variable numeric_operator_code
#          Please also check validity of CONTEXT_APN in .env file

try_step = 1
numeric_operator_code = "26201"     # Example: "26201"

if try_step == 1:
    module.debug_print("INFO: Scanning operators...")
    module.scanNetworkOperators()
    module.sendATcmd("AT+COPS=0", "OK\r\n", 10) # Set automatic mode

elif try_step == 2:
    module.debug_print("INFO: Manual register to %s..." % numeric_operator_code)
    module.sendATcmd("AT+COPS=1,2,\"%s\"" % numeric_operator_code, "OK\r\n", 10)

# Start registration
if module.initNetwork(contextID, os.environ.get("CONTEXT_APN"), 300): # 300 = 5min
    registered = True
    if try_step == 2: 
        module.sendATcmd("AT+COPS=0", "OK\r\n", 10) # Set automatic mode for next time
    module.activatePdpContext(contextID, 5)
    module.ping(contextID,"google.com")
    module.deactivatePdpContext(contextID, 5)
module.close()

if registered:
    print("\nRegistration on network done! You can test demos.\n")
else:
    print("\nAutomatic registration on network not success.")
    print("Please check CONTEXT_APN in .env file and try to manual register on network.")
    print("Check and edit this script for your case, and run again.\n")
