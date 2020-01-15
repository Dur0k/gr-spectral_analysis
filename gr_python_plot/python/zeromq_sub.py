import zmq
import time
import sys
import numpy as np
import random


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://0.0.0.0:5556")
socket.setsockopt(zmq.SUBSCRIBE,b'')

a = socket.recv_pyobj()
print(a)
