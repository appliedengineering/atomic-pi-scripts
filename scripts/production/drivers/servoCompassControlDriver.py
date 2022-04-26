import time
import serial
import msgpack


class ServoCompassControl:
    def __init__(self, prt, baud=9600):  # /dev/ttyUSB0, 9600
        self.servoSerial = serial.Serial(
            port=prt,
            baudrate=baud,
        )

    def setServoAngle(self, angle):
        try:
            self.servoSerial.write((str(angle)+"\n").encode())
            print("[SevoCompass Control] Sent angle of " + str(angle))
        except Exception:
            print("[SevoCompass Control] Error sending angle to servo")
