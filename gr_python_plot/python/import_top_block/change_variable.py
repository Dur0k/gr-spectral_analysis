from distutils.version import StrictVersion
from PyQt5 import Qt
import sys
import signal
from time import sleep
import numpy
from withall_sine import top_block
import zmq



def main(top_block_cls=top_block, options=None):
    # ZMQ PULL
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://localhost:5555")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    tb = top_block_cls()
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    while True:
        socks = dict(poller.poll(10))
        if socks.get(socket) == zmq.POLLIN:
            message = socket.recv()
            tb.set_freq(float(message.decode("utf-8")))

        tb.start()
        sleep(5)
        tb.stop()
        tb.wait()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    




main()
