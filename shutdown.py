import serial
import time

ser = serial.Serial()

ser.port = "/dev/serial0"
ser.baudrate = 115200
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.bytesize=serial.EIGHTBITS

ser.open()
ser.write("AT+QPOWD=1\r".encode())
time.sleep(1.)
if(ser.in_waiting):
    print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'))
else:
    print("shutdown problem detected")
ser.close()

