import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5552")
farray = (-3000,-2000,-1000,-500,0,500,1000,2000, [0,0,10,1])
i=0
while True:
    i = i + 1
    # Wait for next request from client
    # Do some 'work'
    time.sleep(5)
    
    ii = str(farray[i]).encode()
    print(ii.decode("utf-8"))
    # Send reply back to client
    socket.send_pyobj(farray)

