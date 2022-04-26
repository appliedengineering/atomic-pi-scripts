from xml.etree.ElementTree import TreeBuilder
import servoCompassControlDriver

# other imports
import time

servoControl = servoCompassControlDriver.ServoCompassControl("COM4", 9600)

while True:
    servoControl.setServoAngle(100)
    time.sleep(2)
    servoControl.setServoAngle(260)
    time.sleep(2)