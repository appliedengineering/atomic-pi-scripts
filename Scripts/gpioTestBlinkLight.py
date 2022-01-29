import gpio as GPIO
import time

# use the signal id
GPIO_1 = 332
GPIO.setup(GPIO_1, GPIO.OUT)

while True:
	GPIO.output(GPIO_1, True)
	time.sleep(1)
	GPIO.output(GPIO_1, False)
	time.sleep(2)
