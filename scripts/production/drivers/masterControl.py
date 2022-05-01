import concurrent.futures
import logging
import msgpack
import threading
import traceback
import zmq
import time

import servoCompassControlDriver
import gpsDriver
from alignmentCalc import alignmentCalc
import networkingDriver

# Set logging verbosity
# CRITICAL will not log anything
# ERROR will only log exceptions
# INFO will log more information
log_level = logging.INFO

servo = servoCompassControlDriver.ServoCompassControl(prt="/dev/ttyUSB0", baud=9600)
gps = gpsDriver.GpsDriver("/dev/serial0", 115200)
networking = networkingDriver.NetworkDriver("192.168.0.159")  # 192.168.3.1 for raspberry pi
#alignmentc = alignmentCalc.AlignmentCalc()

# direction to point the nanostation at the boat
targetHeading = 0.0


def positioningThread(exit_event):
    print("start pos thread")
    global targetHeading
    while not exit_event.is_set():
        print("pos thread iteration")
        try:
            print("get ground c")
            groundC = gps.getCoordinates()  # lat, lon
            print("groundC ", groundC)
            networking.transmitPosition(groundC[0], groundC[1])

            boatC = networking.receivePosition()  # lat, lon
            print("boatC ", boatC)

            if len(boatC) != 2:
                print(f"No boat coordinates")
                time.sleep(1)
                continue

            if len(boatC) != 2 or len(groundC) != 2:
                print(
                    f"INVALID COORDINATES IN POS THREAD - {len(groundC)} : {len(boatC)}")
                time.sleep(0.01)
                continue

            targetHeading = alignmentCalc.getAngle(
                groundC[0], groundC[1], boatC[0], boatC[1])
            print("Target heading ", str(targetHeading))
            servo.setServoAngle(targetHeading)

        except:
            traceback.print_exc()
            exit_event.set()
        time.sleep(0.01)


if __name__ == '__main__':
    try:
        logging.basicConfig(
            format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
        print("program start")
        exit_event = threading.Event()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(positioningThread, exit_event)
        print("submitted executor")
    except KeyboardInterrupt:
        logging.info('Setting exit event.')
        exit_event.set()
    except:
        traceback.print_exc()
        exit_event.set()
