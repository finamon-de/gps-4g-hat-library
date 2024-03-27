# gps4ghat
**GPS_4G_HAT_BG77X** 

**Library**

Python drivers for Finamon GPS 4G shield onboard devices and peripheral interfaces
- Quectel BG77/BG770 4G Modem
- Accelerometer MC3419/MC3479
- Other shield HW parts: inputs/outputs, button, LED
  
**Examples**

Basic examples showing how to work with Finamon GPS 4G shield onboard devices using Python.
- demo_echo.py
- demo_geofences.py
- demo_GPS_4G_HAT.py
- demo_mqtt.py 

![CON_DATA_jpg](./res/GPS_4G_HAT_CON_DATA.jpg)

![CON_IN_jpg](./res/GPS_4G_HAT_CON_IN.jpg)

![CON_OUT_jpg](./res/GPS_4G_HAT_CON_OUT.jpg)

![CON_ANT_jpg](./res/GPS_4G_HAT_ANT_INTERN.jpg)

![CON_ANT_jpg](./res/GPS_4G_HAT_ANT_EXTERN.jpg)

**Prerequisites**
- for NMEA message parsing install package pynmea2:\
  `pip install pynmea2`

  if you get "error: externally-managed-environment" then<br/>
  try to use pip's argument `--break-system-packages`<br/>    		
  or add following lines to ~/.config/pip/pip.conf:<br/>
  `[global]`<br/>
  `break-system-packages = true`

  
- for acces to SIM card account information install python-dotenv:\
  `pip install python-dotenv`

**Installation**  
- clone git repository https://github.com/finamon-de/gps-4g-hat-library

- change directory\
  `cd gps-4g-hat-library/gps4ghat/dist/`

- install `gps4ghat` python package\
  `pip install gps4ghat-0.1.0-py3-none-any.whl`

**Starting**  
- change directory to `gps-4g-hat-library` 

- copy example.env file to .env file and edit SIM account data:\
  `CONTEXT_APN`\
  `CONTEXT_USERNAME`\
  `CONTEXT_PASSWORD`\
  
- start examples\
  `python examples/demo_xxxx.py`


  
