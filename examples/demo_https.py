'''
  demo_echo.py - This is basic Finamon GNSS/4G Modem HAT Shield HTTP(S) example.
'''

import time
import os, sys
sys.path.append('./')   # Adds higher directory to python modules path.

from gps4ghat.BG77X import BG77X

module = BG77X()
module.debug_print("HTTP(S) demo")
time.sleep(2.)

contextID = "1"
# module.getHardwareInfo()
# module.getFirmwareInfo()
# module.getIMEI()

URL_ADDRESS_GET = "https://httpbin.org/get?argument=number_one&more=yes_please"
URL_ADDRESS_POST = "https://httpbin.org/post?name=you_are_smart"
DATA = "Message=be_focused&Points=2222&Multiply=3333&Result=7405926_or_not?"

if module.initNetwork(contextID):  
    module.activatePdpContext(contextID, 5)
    
    # Send a GET request
    # response = module.sendHttpGetRequest(URL_ADDRESS_GET)

    # Send a POST request
    response = module.sendHttpPostRequest(DATA, URL_ADDRESS_POST)

    print("Response:")
    print(response)

    module.deactivatePdpContext(contextID, 5)
    
module.close()