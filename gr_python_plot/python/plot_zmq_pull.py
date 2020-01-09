import zmq
import time
import numpy
from scipy import signal as sg

import matplotlib.pyplot as plt
from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import gridplot, column

# Input variables
port_temp = 5558
port_sig = 5559


# zmq stuff
context = zmq.Context()
socket_temp = context.socket(zmq.PULL)
socket_temp.connect("tcp://localhost:"+str(port_temp))
socket_sig = context.socket(zmq.PULL)
socket_sig.connect("tcp://localhost:"+str(port_sig))
poller_temp = zmq.Poller()
poller_sig = zmq.Poller()
poller_temp.register(socket_temp, zmq.POLLIN)
poller_sig.register(socket_sig, zmq.POLLIN)

# bokeh stuff
source = ColumnDataSource(dict(
    time=[], Temp=[]
))
source_fft = ColumnDataSource(dict(
    freq=[], sp=[]
))
p0 = figure(y_range=(0,40),plot_height=500, plot_width=1000, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="left")

p0.x_range.follow = "end"
p0.x_range.follow_interval = 500
p0.x_range.range_padding = 0
p0.line(x='time', y='Temp', source=source, line_width=2)

p1 = figure(y_range=(10**-10,1),x_range=(-1500,1500), plot_height=500, plot_width=1000, y_axis_type='log', tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="left")

p1.line(x='freq', y='sp', source=source_fft, line_width=2)


# functions
def _update_function():
    socks_temp = dict(poller_temp.poll())
    if socks_temp.get(socket_temp) == zmq.POLLIN:
        message_temp = socket_temp.recv()
    socks_sig = dict(poller_sig.poll())
    if socks_sig.get(socket_sig) == zmq.POLLIN:
        message_sig = socket_sig.recv()
    T = numpy.frombuffer(message_temp, dtype=numpy.float32())
    sig = numpy.frombuffer(message_sig, dtype=numpy.complex64())
    return T, sig

@count()
def update(t):
    T, sig = _update_function()
    f, Pxx = sg.periodogram(sig, 1e6/100, return_onesided=False, scaling='spectrum')
    new_data = dict(
        time=[t],
        Temp=[T[0]]
    )
    Pxx = Pxx[f.argsort()]
    f.sort()
    ptr = len(f)//2
    Pxx = numpy.append(Pxx[:ptr],Pxx[ptr+1:])
    f = numpy.append(f[:ptr],f[ptr+1:])
    new_fft_data = dict(
        freq=f,
        sp=Pxx,
    )
    source.stream(new_data, 500)
    source_fft.stream(new_fft_data,len(Pxx))



curdoc().add_root(column(p0,p1))
curdoc().add_periodic_callback(update, 10)
curdoc().title = "test plot"

