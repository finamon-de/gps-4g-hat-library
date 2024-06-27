'''
  demo_echo.py - This is basic Finamon GNSS/4G Modem HAT Shield UDP echo example.
'''

import time
import os, sys
sys.path.append('./')   # Adds higher directory to python modules path.

from gps4ghat.BG77X import BG77X

module = BG77X()
module.debug_print("UDP echo demo")
time.sleep(2.)

contextID = "1"
module.getHardwareInfo()
module.getFirmwareInfo()
module.getIMEI()

if module.initNetwork(contextID): 
    module.setIPAddress(os.environ.get("ECHO_SERVER_IP"))    
    module.setPort(os.environ.get("ECHO_SERVER_PORT"))    
    module.activatePdpContext(contextID, 5)

    module.openConnection(contextID, "UDP", 5)
    module.sendUdpData("Hello " + module.board + " IMEI: " + module.IMEI)
    module.recvUdpData()

    module.closeConnection()
    module.deactivatePdpContext(contextID, 5)
    
module.close()
