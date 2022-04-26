import serial, time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout = 0)

targetAngle = 180

'''
Arduino Code Reference:

Retrieval
M - get current compass (server motor) angle relative to north

Commands
L - set servo motor to turn left
R - set servo motor to turn right
'''

def scriptLoop():
	while True:
		handleServoMotor()

def handleServoMotor():
		# read angle
		currentAngle = retrieveValueFromArduino('M')

		print(currentAngle)

		if(currentAngle > targetAngle):
			sendCommandToArduino('R')
		else:
			sendCommandToArduino('L')

def retrieveValueFromArduino(code, number=True):
	output = 0
	arduino.write(code.encode())
	time.sleep(0.01) # some time for measurement to be taken
	if(number):
		incomingData = str(arduino.readline().strip(), 'utf-8')
		try :
			output = float(incomingData)
		except ValueError:
			pass

	return output

def sendCommandToArduino(code):
	arduino.write(code.encode())

if __name__ == "__main__":
	scriptLoop()
