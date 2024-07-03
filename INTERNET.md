# gps4ghat

### About

**INTERNET** - Get the internet access over GPS 4G HAT.

We will show you how to get the internet connection from the Raspberry Pi OS, but with low speed.
It is done over ppp connection (Point-to-Point Protocol) and limited by serial port baudrate 115200.\
Setup will be splited in two parts:
- Setup a PPP and get internet access
- Setup a Wireless Hotspot and share internet access

### Notes

- **Important** to have proper APN settings for SIM card which you using! It is located in `rnet` file.
- Assume that you already done 'Installation' and 'Getting started' from [README.md](README.md)


### Setup a PPP connection
- Install required packages\
  `sudo apt update && sudo apt install ppp`
  
- Create file and insert text below.\
  **Important:** Check the APN settings.\
  `sudo nano /etc/ppp/peers/rnet`
  ```shell
  # filename: rnet
  # file located: /etc/ppp/peers

  # your_apn_address is the APN for the connection
  # Important to have proper APN settings for SIM card which you using!
  connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T your_apn_address"

  # For Raspberry Pi3 use /dev/ttyS0 as the communication port:
  /dev/serial0

  # Baudrate
  115200

  # Assumes that your IP address is allocated dynamically by the ISP.
  noipdefault

  # Try to get the name server addresses from the ISP.
  usepeerdns

  # Use this connection as the default route to the internet.
  defaultroute

  # Makes PPPD "dial again" when the connection is lost.
  persist

  # Do not ask the remote to authenticate.
  noauth

  # No hardware flow control on the serial link with GSM Modem
  nocrtscts

  # No modem control lines with GSM Modem
  local
  ```

- Power UP the module.\
  **Important:** Be sure you have activated virtual environment!\
  `python examples/power_up.py`

- Start the PPP connection.\
  `sudo pon rnet`

- Check for the interface, ppp0 interface should exist.\
  `ifconfig`

- Test the interface with ping.\
  `ping -I ppp0 8.8.8.8`
  
- If you want to have default route over ppp0, fastest way is to disable all interfaces (disconnect WiFi and LAN cable).\
  Then first start the PPP connection.

- Stop the PPP connection.\
  `sudo poff`

- For debug, take a look on system log.\
  `journalctl -f`



### Setup a Wireless Hotspot

It is based on **Debian GNU/Linux 12 (bookworm)**, as it has already installed Hotspot support.\
(*Linux 6.6.20+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.6.20-1+rpt1 (2024-03-07)*)\
Steps will drive you on the Desktop version.

- If you settings WiFi for the first time:\
  Click on the network icon (top right), then "Click here to set Wi-Fi contry".\
  Please select country and click OK.
  
- Need to reboot to accept country settings.\
  `sudo reboot now` or with mouse.
  
- Because of reboot, need to power up module and start PPP connection.\
  `python examples/power_up.py`\
  `sudo pon rnet`

- Click on the network icon (top right), then "Advanced Options", then "Create Wireless Hotspot".\
  Please input Network name and press Create.

- Now wireless network should be visible.\
  Test the connection and enjoy! :)