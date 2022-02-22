import serial, time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 0)

targetAngle = 180

while True:
	try :
		# read angle
		arduino.write('M'.encode())
		time.sleep(0.01) # some time for measurement to be taken
		incomingData = str(arduino.readline().strip(), 'utf-8')
		# print(incomingData)
		print(float(incomingData))

		currentAngle = float(incomingData)

		if(currentAngle > targetAngle):
			arduino.write('R'.encode())
		else:
			arduino.write('L'.encode())
	except ValueError as e:
		pass
		# invalid data
		# print( e)
