from distutils.version import StrictVersion
from PyQt5 import Qt
import sys
import signal
from time import sleep
import numpy
from withall_sine import top_block #aufbau
import zmq
import threading

class Change_Variables:
    #https://www.pythonforthelab.com/blog/using-pyzmq-for-inter-process-communication-part-2/
    def __init__(self, port, top_block):
        self.tb = top_block
        self.port = port

    def PullTask(self):
        self.message = []
        self.stop = False
        context = zmq.Context()
        socket = context.socket(zmq.PULL)
        socket.connect("tcp://localhost:5555")
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        while not self.stop:
            socks = dict(poller.poll(-1))
            if socks.get(socket) == zmq.POLLIN:
                self.message = socket.recv_pyobj()
                self.tb.stop()
                self.tb.wait()
                #self.tb.lock()
                self.SetVariables(self.tb,self.message)
                #self.tb.unlock()
                self.tb.start()

    def SetVariables(self, tb, message):
        self.tb = tb
        self.message = message
        print(self.message[0])
        self.tb.set_freq(float(self.message[0]))
        self.tb.set_fshift(numpy.asarray(float(eval(self.message[4]))))
        self.tb.set_samp_rate(float(self.message[6]))
        self.tb.set_thres(float(self.message[7]))
        self.tb.set_min_dist(float(self.message[8]))
        self.tb.set_polycoeff(numpy.asarray(eval(self.message[2])))
        self.tb.set_offset(numpy.asarray(eval(self.message[3])))
        self.tb.set_sensor_count(int(self.message[1]))
        self.tb.set_fft_size(int(self.message[5]))

def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()
    change_top = Change_Variables(5555, tb)
    pull_thread = threading.Thread(target=change_top.PullTask)
    pull_thread.start()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        pull_thread.stop = True
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    tb.run()

    #try:
    #    input('Press Enter to quit: ')
    #except EOFError:
    #    pass



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
