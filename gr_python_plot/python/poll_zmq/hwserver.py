import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5555")

i=1
while True:
    i = i + 1
    # Wait for next request from client
    # Do some 'work'
    time.sleep(i)
    print(i)
    ii = str(i).encode()
    # Send reply back to client
    socket.send(ii)

