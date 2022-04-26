import gpio as GPIO
import time

# make sure to run
# sudo chmod -R 777 /sys/class/gpio/gpio332

# use the signal id
GPIO_1 = 332
GPIO.setup(GPIO_1, GPIO.OUT)

def runServo(timeTotal, clockwise=True):
	startTime = time.time()
	pwmInterval = .0005
	if not clockwise:
		pwmInterval = 0.0025
	timeElapsed = 0
	while(timeElapsed < timeTotal):
		GPIO.output(GPIO_1, GPIO.HIGH)
		time.sleep(pwmInterval)
		GPIO.output(GPIO_1, GPIO.LOW)
		time.sleep(pwmInterval)
		timeElapsed = time.time() - startTime


# start
while True:
	runServo(2, clockwise=False)
	time.sleep(1)
	runServo(2, clockwise=True)
