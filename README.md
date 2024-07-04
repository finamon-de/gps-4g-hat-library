# gps4ghat
**GPS_4G_HAT_BG77X** 

### Library

Python drivers for Finamon GPS 4G shield onboard devices and peripheral interfaces
- Quectel BG77/BG770 4G Modem
- Accelerometer MC3419/MC3479
- Other shield HW parts: inputs/outputs, button, LED

  
### Examples

Basic examples showing how to work with Finamon GPS 4G shield onboard devices using Python.
- demo_echo.py
- demo_geofences.py
- demo_GPS_4G_HAT.py
- demo_IO.py
- demo_mqtt.py
- demo_mqtt_sensors.py


### Prerequisites

__Raspberry Pi Config__

In your Raspberry Pi configuration within the _Interfaces_ section, please make sure that

1. I2C is **enabled**
2. Serial Port is **enabled**
3. Serial Console is **disabled**


### Installation
- Clone git repository\
  `git clone https://github.com/finamon-de/gps-4g-hat-library`

- Install required packages\
  `sudo apt update && sudo apt install python3-libgpiod screen`
  
- Change directory\
  `cd gps-4g-hat-library`

<!-- - Change directory\
  `cd gps-4g-hat-library/gps4ghat/dist/`

- Install `gps4ghat` python package\
  `pip install gps4ghat-0.1.0-py3-none-any.whl` -->

__Global setup__

If you prefer to setup your projects using global package installations, please take a look at the prerequisites below.

> With newer versions of Python you might experience the message *error: externally-managed-environment*<br/>
  In this case try using pip's argument `--break-system-packages`<br/>    		
  or add the following lines to ~/.config/pip/pip.conf:<br/>
  `[global]`<br/>
  `break-system-packages = true`

- To be able to parse NMEA messages install package `pynmea2`:\
  `pip install pynmea2`
  
- For access to SIM card account information install `python-dotenv`:\
  `pip install python-dotenv`


__Virtual Enivironment__

If you prefer to setup your projects using virtual environments, the necessary steps to be able to run the examples are:

1. Even using the virtual environment the project needs access to a global package to work with GPIOs.\
`python3-libgpiod` should already be installed in Installation step.
2. Now you can create the virtual environment 
    - Run `python3 -m venv .venv --system-site-packages`
    - The parameter `--system-site-packages` allows to access packages from outside of the virtual environment
3. Activate the environment 
    - Run `source .venv/bin/activate`
    - (use the command `deactivate` to leave the virtual environment)
4. Install the dependencies to run the demo scripts 
    - Run `python3 -m pip install pynmea2 python-dotenv pyserial smbus`


### Getting started
- Make sure you are in the root project directory\
  `cd gps-4g-hat-library` 

- Copy .env.example file to .env file\
  `cp .env.example .env`

- Edit .env file for APN settings\
  `nano .env`
  
- Start examples\
  `python examples/demo_xxxx.py`


### Notes

- **Important**: Please make sure you have the proper APN settings for your SIM card at hand!
- By default the GPS 4G HAT is configured to use the **internal/onboard** GSM antenna and the **external** GNSS RF antenna (that is part of the deliverables). You can ensure this configuration by having a look at the resistors close to antenna connectors.
- When you use your SIM card for the first time or after a long period, you may experience that the examples return a message containing `+CEREG: 0,2`. This message indicates that it not registered on network _but_ it is searching for new operator to register to - that's what the **2** indicates. When registered on network the message will be `+CEREG: 0,5`, the **5** indicating that the registered (roaming) on network. While testing different SIM cards, we expirienced (very) long timespans until **the first** registration to the network is possible - After the first successful registration, next registrations are not an issue because SIM card storing information about network.
If you experience similar issue, please follow "First registration on network" procedure.


### First registration on the network
The first registration on the network is related to the SIM card. That is because the network information is stored on the SIM card. When it is brand new, there is no information about network stored on it.\
Using its default settings the BG77 module will do a very wide scanning for networks, and it will take very long time until the registration on the network is successful.\
After the first registration on the network and a graceful power down of the BG77 module, all network information will be stored on the SIM card. This means that any next registration should be fast.
Speeding up the process of the network search can be achieved by disabling NB-IoT and enabling only the required RAT(s), or when NB-IoT is necessary, it is recommended to enable only the bands supported by the current service
operator.\
By default, in script `examples/first_registration.py`, configured RAT is CAT-M1 (eMTC). Feel free to change RAT as your needs.\
In thhis script you can find an explanation for step 1 and 2. Step 1 will try automatic registration. If it fails you can try step 2 for manual registration for configured network operator. Please also check CONTEXT_APN settings in .env file.
- Script run:\
    `python examples/first_registration.py`


### UART console for AT commands
If you want direct access to the UART (serial port), you can get it with `screen /dev/serial0 115200`.
- Run this command only for first time, to set permissions on file `console.sh`\
    `sudo chmod +x console.sh`

- Use this command to open UART console to the module\
    `./console.sh`


### Module power UP & DOWN
If you want only to power up or power down the module and let in that state.
- Command for power up\
    `python examples/power_up.py`

- Command for power down\
    `python examples/power_down.py`


### INTERNET Access
This HAT can provide you with internet access from the host operating system.
Please check the [INTERNET.md](INTERNET.md)



### Images

#### Data pins
![CON_DATA_jpg](./res/GPS_4G_HAT_CON_DATA.jpg)

#### Input pins
![CON_IN_jpg](./res/GPS_4G_HAT_CON_IN.jpg)

#### Output pins
![CON_OUT_jpg](./res/GPS_4G_HAT_CON_OUT.jpg)

#### Configuration to use the internal/onboard antennas
![CON_ANT_jpg](./res/GPS_4G_HAT_ANT_INTERN.jpg)

#### Configuration to use the external antenna connectors
![CON_ANT_jpg](./res/GPS_4G_HAT_ANT_EXTERN.jpg)
