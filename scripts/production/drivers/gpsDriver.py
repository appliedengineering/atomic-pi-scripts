import pynmea2
import serial
import time


class GpsDriver:
    # /dev/ttyS4, 115200 *very special indeed*
    def __init__(self, prt="/dev/ttyS4", baud=115200):
        self.serialGPS = serial.Serial(
            port=prt,
            baudrate=baud,
        )

    def readCoord(self):
        return self.serialGPS.readline()

    def getCoordinates(self):  # lat, lon
        raw = self.readCoord()
        
        timeoutC = 0
        while timeoutC < 100 and not raw.startswith(b"$GPGGA"):
            raw = self.readCoord()
            timeoutC += 1
            time.sleep(0.01)
            
        
        if (raw.startswith(b"$GPGGA")):
            try:
                msg = pynmea2.parse(raw.decode("utf-8"))
                lat = msg.latitude
                lon = msg.longitude
            except:
                print("[GpsDriver] Error in gps data, sent (-1.0, -1.0)")
                return -1.0, -1.0
            return lat, lon
        return 0.0, 0.0  # no data yet
