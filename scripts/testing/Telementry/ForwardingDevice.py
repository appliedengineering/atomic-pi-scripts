import zmq
import concurrent.futures

def pub_sub_forwarding_device():
    print("starting zmq pub sub forwarding device")
    try:
        context = zmq.Context(1)

        # Socket facing raspi
        clientEnd = context.socket(zmq.SUB)
        clientEnd.bind("tcp://*:5556")
        
        clientEnd.setsockopt(zmq.SUBSCRIBE, b"") # b is needed
        
        # Socket facing clients
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:55563")

        # raspi PUB -> this device SUB -> this device PUB -> client SUB
        zmq.device(zmq.FORWARDER, clientEnd, backend) # this is a blocking statment
    except Exception as e:
        print("ERROR - the pub sub device will exit")
        print(e)
    finally:
        pass
        clientEnd.close()
        backend.close()
        context.term()

def timestamp_forwarding_device():
    print("starting zmq timestamp forwarding device")
    try:
        context = zmq.Context(1)
        # Socket facing clients
        deviceend = context.socket(zmq.XREP)
        deviceend.bind("tcp://*:31415")

        # Socket facing raspi (the "server")
        serverend = context.socket(zmq.XREQ)
        serverend.bind("tcp://*:55561")

        zmq.device(zmq.QUEUE, deviceend, serverend)
    except Exception as e:
        print("ERROR - the timestamp device will exit")
        print(e)
    finally:
        pass
        deviceend.close()
        serverend.close()
        context.term()

    
def parallel_executor():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [] # maybe use the result later
        futures.append(executor.submit(pub_sub_forwarding_device))
        futures.append(executor.submit(timestamp_forwarding_device))



if __name__ == "__main__":
    parallel_executor()
