import zmq
import time
import numpy


from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import gridplot, column

# Input variables
port = 5558



# zmq stuff
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://localhost:"+str(port))
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# bokeh stuff
source = ColumnDataSource(dict(
    time=[], data=[]
))
p = figure(y_range=(0,40),plot_height=500, plot_width=1000, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")

p.x_range.follow = "end"
p.x_range.follow_interval = 500
p.x_range.range_padding = 0
p.line(x='time', y='data', source=source, line_width=2)

p2 = figure(plot_height=250, x_range=p.x_range, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="right")

# functions
def _update_function():
    socks = dict(poller.poll())
    if socks.get(socket) == zmq.POLLIN:
        message = socket.recv()

    k = numpy.frombuffer(message, dtype=numpy.float32())
    return k

@count()
def update(t):
    y = _update_function()
    ym = numpy.mean(y[::2])
    #ym = numpy.mean(y)
    new_data = dict(
        time=[t],
        data=[y[0]]
    )
    print(len(y))
    source.stream(new_data, 500)


curdoc().add_root(column(p))
curdoc().add_periodic_callback(update, 10)
curdoc().title = "test plot"

