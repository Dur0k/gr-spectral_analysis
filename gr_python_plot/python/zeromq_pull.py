import zmq
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

context = zmq.Context()

socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5558")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
i=0
while True:
    i = i + 1
    socks = dict(poller.poll())
    if socks.get(socket) == zmq.POLLIN:
        message = socket.recv()

    k = np.frombuffer(message, dtype=np.float32())
    print("------------------------- NEW POLL ------------------------------")
    print(len(k))
    print(k)
    #plt.plot(k)
    #plt.show()

socket.close()
