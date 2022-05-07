import pynmea2
import serial
import time
import msgpack
import math

ser = serial.Serial(
     port="/dev/serial0",
     baudrate=115200,
     timeout=0
)

print("connected to: " + ser.portstr)

try:
   while True:
      raw = ser.readline()
#      if len(raw) > 0:
#          print(raw)
      if (raw.startswith(b"$GPGGA")):
         try:
             msg = pynmea2.parse(raw.decode("utf-8"))
         except:
             print("Failed to parse")

         print(msg.latitude, msg.longitude)

      time.sleep(0.01)
except KeyboardInterrupt:
   print("exit")
