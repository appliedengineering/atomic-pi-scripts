import gpio as GPIO
import time

# make sure to run
# sudo chmod -R 777 /sys/class/gpio/gpio332

# use the signal id
GPIO_1 = 332
GPIO.setup(GPIO_1, GPIO.OUT)

while True:
	GPIO.output(GPIO_1, GPIO.HIGH)
	time.sleep(10/1000)
	GPIO.output(GPIO_1, GPIO.LOW)
	time.sleep(10/1000)
