import servoCompassControlDriver

# other imports
import time

servoControl = servoCompassControlDriver.ServoCompassControl("/dev/ttyUSB0", 9600)

while True:
    servoControl.setServoAngle(100)
    time.sleep(2)
    servoControl.setServoAngle(260)
    time.sleep(2)
