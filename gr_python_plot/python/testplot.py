import zmq
import time
import numpy
from scipy import signal as sg

from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import gridplot, column

port_temp = 5558
sensor_count = 2

context = zmq.Context()
socket_temp = context.socket(zmq.PULL)
socket_temp.connect("tcp://localhost:"+str(port_temp))
poller_temp = zmq.Poller()
poller_temp.register(socket_temp, zmq.POLLIN)


data = dict(
        time=[]
    )

p0 = figure(title="Temperature", y_range=(0, 40), plot_height=500, plot_width=1000, tools="xpan,xwheel_zoom,xbox_zoom,reset", y_axis_location="left")
#p0.xaxis.axis_label = 'Time'
p0.yaxis.axis_label = 'Temperature [°C]'
p0.x_range.follow = "end"
p0.x_range.follow_interval = 500
p0.x_range.range_padding = 0


for i in range(0, sensor_count):
    data.update({'temp_'+str(i): []})

source = ColumnDataSource(data)

for i in range(0, sensor_count):
    p0.line(x='time', y='temp_'+str(i), source=source, line_width=2)



def _update_function():
    socks_temp = dict(poller_temp.poll())
    if socks_temp.get(socket_temp) == zmq.POLLIN:
        message_temp = socket_temp.recv()
    T = numpy.frombuffer(message_temp, dtype=numpy.float32())
    T = numpy.reshape(T, (len(T)//sensor_count, sensor_count))
    return T


@count()
def update(t):
    T = _update_function()
    print(T)
    new_data = dict(
        time=[t]
    )
    #,
    #    Temp=[T[0]]
    T = numpy.array(T)
    i, j = numpy.argwhere(numpy.isnan(T)).T
    T[i, j] = 0.0
    for ii in range(0, sensor_count):
        new_data.update({'temp_'+str(ii): [numpy.mean(T[0, ii])]})
    print(new_data['time'])
    source.stream(new_data, 500)


curdoc().add_root(column(p0))
curdoc().add_periodic_callback(update, 20)
curdoc().title = "test plot"
