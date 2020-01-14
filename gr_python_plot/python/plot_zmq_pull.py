import zmq
import time
import numpy
from scipy import signal as sg

from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import gridplot, column
from bokeh.colors import groups

# Input variables
port_temp = 5558
port_sig = 5559

# gr variables
fA = 1e6/100
sensor_count = 2

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
## Temperature Plot
p0 = figure(title="Temperature", y_range=(0, 40), plot_height=500, plot_width=1000, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="left")
#p0.xaxis.axis_label = 'Time'
p0.yaxis.axis_label = 'Temperature [°C]'
p0.x_range.follow = "end"
p0.x_range.follow_interval = 500
p0.x_range.range_padding = 0
data = dict(
        time=[]
    )

for i in range(0, sensor_count):
    data.update({'temp_'+str(i): []})

source = ColumnDataSource(data)

for i in range(0, sensor_count):
    p0.line(x='time', y='temp_'+str(i), source=source, line_width=2, line_color=groups.black[i+5])


## Spectrum Plot
source_fft = ColumnDataSource(dict(
    freq=[], sp=[]
))
p1 = figure(title="Spectrum", y_range=(10**-10, 1), x_range=(-2500, 2500), plot_height=500, plot_width=1000, y_axis_type='log', tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="left")
p1.xaxis.axis_label = 'Frequency [Hz]'
p1.line(x='freq', y='sp', source=source_fft, line_width=2, line_color='black')


# functions
def _update_function():
    socks_temp = dict(poller_temp.poll())
    if socks_temp.get(socket_temp) == zmq.POLLIN:
        message_temp = socket_temp.recv()
    socks_sig = dict(poller_sig.poll())
    if socks_sig.get(socket_sig) == zmq.POLLIN:
        message_sig = socket_sig.recv()
    T = numpy.frombuffer(message_temp, dtype=numpy.float32())
    T = numpy.reshape(T, (len(T)//sensor_count, sensor_count))
    signal = numpy.frombuffer(message_sig, dtype=numpy.complex64())
    return T, signal

def _calc_spectrum(x, fA):
    f, Pxx = sg.periodogram(x, fA, window=None, nfft=len(x)//2,return_onesided=False, scaling='spectrum')
    Pxx = Pxx[f.argsort()]
    f.sort()
    ptr = len(f)//2
    Pxx = numpy.append(Pxx[:ptr], Pxx[ptr+1:])
    f = numpy.append(f[:ptr], f[ptr+1:])
    return f, Pxx

def _replaceNaN(x):
    x = numpy.array(x)
    i,j = numpy.argwhere(numpy.isnan(x)).T
    x[i, j] = 0.0
    return x

@count()
def update(t):
    T, signal = _update_function()
    new_data = dict(
        time=[t]
    )
    T = _replaceNaN(T)
    for ii in range(0, sensor_count):
        new_data.update({'temp_'+str(ii): [numpy.mean(T[0, ii])]})

    f, Pxx = _calc_spectrum(signal, fA)
    new_fft_data = dict(
        freq=f,
        sp=Pxx,
    )
    source.stream(new_data, 500)
    source_fft.stream(new_fft_data, len(Pxx))



curdoc().add_root(column(p0, p1))
curdoc().add_periodic_callback(update, 20)
curdoc().title = "test plot"

