# Telementry ZMQ Message Forwarding
# Copyright (c) 2022 Applied Engineering
import concurrent.futures
import logging
import msgpack
import zmq
import time
import traceback
# set log level
log_level = logging.INFO

# overview:
# a suscriber is setup up to listen to messages from the raspberry-pi which is at ip address 192.168.3.1

# setup up some zeromq
ctx = zmq.Context()
sub = ctx.socket(zmq.SUB)

# setup suscriber to listen to the raspberry pi

address_rpi = "tcp://192.168.3.1:5556"

address_to_bind = "tcp://*:5556" # the pub server is connected to port 5556 
# to recieve pub data from the atomic pi, you will need to connect to 192.168.3.2 at port 5556

sub.subscribe("") #suscribe to all topics
sub.setsockopt(zmq.RCVHWM, 1)
sub.setsockopt(zmq.RCVBUF, 1*1024)
sub.setsockopt(zmq.CONFLATE, 1)
sub.connect(address_rpi)

# setup up the pub network
pub = ctx.socket(zmq.PUB)
pub.bind(address_to_bind)


def handleForwarding():
	try:
		logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
		logging.info("Listening for data from the raspberrypi which is located at %s", address_rpi)
		while True:
			try:
				data_from_rpi = sub.recv(copy=False, flags=zmq.NOBLOCK)
				print(msgpack.unpackb(data_from_rpi)) # just print out the data so we can see it

				# we now need to forward the data to people's phones
				pub.send(data_from_rpi)
				print("Forwarded incoming data through port 5556")

				logging.info("Recieved data from the raspberry pi")
			except zmq.ZMQError as e:
				if e.errno == zmq.EAGAIN:
					pass # no message is ready yet
				else:
					print("There was an error!!!")
					traceback.print_exc()
			#time.sleep(0.01)
	except KeyboardInterrupt:
		logging.info('Exiting now')
		sub.close()
		pub.close()
		context.term()
	except:
		traceback.print_exc()


# setup the timestamp forwarding

# setup a recv socket at port 5546#time_port = 5546
time_socket = ctx.socket(zmq.REP)
time_socket.bind("tcp://*:%s" % 55561)


def handleTimestamp():
	# handle the timestamp
	while True:
		# Wait for next request from client
		message = time_socket.recv()
		# Forward the message
		print("Got a message from a phone: ")
		print(msgpack.unpackb(message))


def parallel_executor():
	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = []
		futures.append(executor.submit(handleForwarding))
		futures.append(executor.submit(handleTimestamp))

# the if statement below is kind of like a main method
if __name__ == '__main__':
	parallel_executor()
#	Thread(target = handleForwarding).start()
#	Thread(target = handleTimestamp).start()
	#handleTimestamp()
