import zmq

context = zmq.Context()

# Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:5552")
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)
message = []
# DO 10 requests, waiting each time for a response
for request in range(10):
    socks = dict(poller.poll(1000))
    if socks.get(socket) == zmq.POLLIN:
        message = socket.recv_pyobj()
        #print("Received reply %s"%  (message.decode("utf-8") ))
        print(message)
    #while socket.poll(1000) == zmq.POLLIN:
    #    message.append(socket.recv())
      
    
