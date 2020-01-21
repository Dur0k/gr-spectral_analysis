import zmq
import time
import sys
import numpy as np
import random
import itertools


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://0.0.0.0:5556")

while True:
    A = np.random.rand(1)
    # can also send arrays
    socket.send_pyobj(A)
    print(A)
    time.sleep(2)
