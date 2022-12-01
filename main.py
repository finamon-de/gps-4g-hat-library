from gps4ghat import BG77X

import os
import sys
import time


module = BG77X.BG77X()
time.sleep(2.)
contextID = "1"
module.sendATcmd("AT")
module.getHardwareInfo()
module.getFirmwareInfo()
module.getIMEI()
#module.sendATcmd("AT+COPS=?", "OK", 600)
module.acquareSettings()
if module.initNetwork(contextID, os.environ.get("CONTEXT_APN"), 600): 
    module.activatePdpContext(contextID, 5)
    module.ping(contextID,"google.com")
    module.deactivatePdpContext(contextID, 5)
module.close()
time.sleep(2.)

