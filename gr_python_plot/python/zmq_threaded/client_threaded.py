import time
import zmq
import threading

class Change_Variables:
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
        while True:#not self.stop:
            socks = dict(poller.poll(10))
            if socks.get(socket) == zmq.POLLIN:
                self.message = socket.recv_pyobj()
                self.tb.stop()
                self.tb.wait()
                self.tb.set_freq(float(message[0]))
                
            
def main():
    pull_p = Change_Variables(5555)
    message = pull_p.PullTask()
    pull_thread = threading.Thread(target=pull_p.PullTask)
    pull_thread.start()
    
    
main()
