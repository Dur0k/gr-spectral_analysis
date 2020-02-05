import zmq
import time
import numpy
from scipy import signal as sg
from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool, Slider
from bokeh.layouts import gridplot, column, row
from bokeh.colors import groups
from bokeh.models.widgets import RangeSlider, TextInput

# zmq variables
port_temp = 5588
port_sig = 5589
port_send = 5555

# gr variables
fA = 1e6/100
sensor_count = 2

# periodogram variable
per_window = "boxcar"

# bokeh variable
p_update = 20
title_font_size = "25px"
label_font_size = "20px"
legend_font_size = "15px"

## Temperature Plot
sensor_list = (5,10,14)
p0_x_range_intervall = 500
p0_x_range_padding = 0
p0_title = "Sensor Temperature"
p0_ylabel = "Temperature [°C]"
p0_xlabel = "Time"
p0_y_range = (0,40)
p0_plot_height = 800
p0_plot_width = 930
p0_tools = "xpan,box_zoom,save,reset"

## Spectrum Plot
p1_y_range = (10**-10, 1)
p1_x_range = (-2500, 2500)
p1_x_bounds = (-4000,4000)
p1_plot_height = 800
p1_plot_width = 930
p1_xlabel = "Frequency [Hz]"
p1_ylabel = "Spectrum"
p1_title = "Periodogram of baseband signal"
p1_tools = "xpan,xbox_zoom,save,reset"

# zmq stuff
context = zmq.Context()
socket_temp = context.socket(zmq.PULL)
socket_temp.connect("tcp://localhost:"+str(port_temp))
socket_sig = context.socket(zmq.PULL)
socket_sig.connect("tcp://localhost:"+str(port_sig))
socket_send = context.socket(zmq.PUSH)
socket_send.bind("tcp://*:"+str(port_send))
poller_temp = zmq.Poller()
poller_sig = zmq.Poller()
poller_temp.register(socket_temp, zmq.POLLIN)
poller_sig.register(socket_sig, zmq.POLLIN)
 

# bokeh stuff

## Input controls
#freq_slider = Slider(title="Frequency of sines", value=-3000, start=-3000, end=3000, step=100, callback_policy='mouseup')
freq_slider = TextInput(title="Frequency of sines")

## Temperature Plot# y_range=(0, 40), tools="xpan,xwheel_zoom,xbox_zoom,reset", 
p0 = figure(title=p0_title, y_range=p0_y_range, plot_height=p0_plot_height, plot_width=p0_plot_width, tools=p0_tools, y_axis_location="left")
p0.yaxis.axis_label = p0_ylabel
p0.xaxis.axis_label = p0_xlabel
p0.x_range.follow = "end"
p0.x_range.follow_interval = p0_x_range_intervall
p0.x_range.range_padding = p0_x_range_padding
p0.title.text_font_size = title_font_size
p0.xaxis.axis_label_text_font_size = label_font_size
p0.yaxis.axis_label_text_font_size = label_font_size

data = dict(
        time=[]
    )

for i in range(0, sensor_count):
    data.update({'temp_'+str(i): []})

source = ColumnDataSource(data)

for i in range(0, sensor_count):
    p0.line(x='time', y='temp_'+str(i), source=source, line_width=2, line_color=groups.black[i], legend_label="Sensor "+str(sensor_list[i]))

p0.legend.location = "bottom_left"
p0.legend.click_policy = "hide"
p0.legend.label_text_font_size = legend_font_size


## Spectrum Plot
source_fft = ColumnDataSource(dict(
    freq=[], sp=[]
))

p1 = figure(title=p1_title, y_range=p1_y_range, x_range=p1_x_range, plot_height=p1_plot_height, plot_width=p1_plot_width, y_axis_type='log', tools=p1_tools, y_axis_location="left")
p1.x_range.bounds = p1_x_bounds
p1.xaxis.axis_label = p1_xlabel
p1.yaxis.axis_label = p1_ylabel
p1.title.text_font_size = title_font_size
p1.xaxis.axis_label_text_font_size = label_font_size
p1.yaxis.axis_label_text_font_size = label_font_size

p1.line(x='freq', y='sp', source=source_fft, line_width=2, line_color='black')


# functions
def _update_data():
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
    f, Pxx = sg.periodogram(x, fA, window=per_window, nfft=len(x) ,return_onesided=False, scaling='spectrum')
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

farray = (-3000,-2000,-1000,-500,0,500,1000,2000)
ia = 0
@count()
def update(t):
    T, signal = _update_data()
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
    source_fft.data = new_fft_data
    source.stream(new_data, 500)
    #source_fft.stream(new_fft_data, len(Pxx))


#y_axis_slider = RangeSlider(start=-20, end=50, value=(0,40), step=1, callback_policy='mouseup')
#y_axis_slider.on_change('value',lambda attr, old, new: update())

def update_slider():
    ii = str(freq_slider.value).encode()
    print(ii.decode("utf-8"))
    #print(str(y_axis_slider.value))
    socket_send.send(ii)

freq_slider.on_change('value', lambda attr, old, new: update_slider())
curdoc().add_root(row(p1, p0, freq_slider))#
curdoc().add_periodic_callback(update, p_update)
curdoc().title = "test plot"

#socket_temp.close()
#socket_sig.close()
