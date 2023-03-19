#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time, struct, subprocess

port = "/dev/ttyUSB0"
baudrate = 9600

ser = Serial(port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
ser.flushInput()

HEADER_BYTE = b"\xAA"
COMMANDER_BYTE = b"\xC0"
TAIL_BYTE = b"\xAB"

byte, previousbyte = b"\x00", b"\x00"

n=0
while True:
    previousbyte = byte
    byte = ser.read(size=1)

    if previousbyte == HEADER_BYTE and byte == COMMANDER_BYTE:
        packet = ser.read(size=8) # Read 8 more bytes
        readings = struct.unpack('<HHcccc', packet)
        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0
        print("PM 2.5:", pm_25, "µg/m³ \nPM 10:", pm_10, "µg/m³\n")
        time.sleep (1)
        subprocess.run(["mosquitto_pub", "-h", "192.168.1.125", "-t", "air-quality/pm10", "-m", str(pm_10)])
        time.sleep (1)
        subprocess.run(["mosquitto_pub", "-h", "192.168.1.125", "-t", "air-quality/pm25", "-m", str(pm_25)])
#        n=n+1
        time.sleep (120)
