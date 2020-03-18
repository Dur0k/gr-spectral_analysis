import zmq
import numpy
import yaml

from scipy import signal as sg
from bokeh.driving import count
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, RangeTool, Slider, Button, Select
from bokeh.layouts import gridplot, column, row, layout
from bokeh.colors import groups
from bokeh.models.widgets import RangeSlider, TextInput
from bokeh.io import show

config = yaml.safe_load(open("config.yaml"))

# zmq stuff
context = zmq.Context()
#  --------
socket_temp = context.socket(zmq.SUB)
socket_temp.setsockopt_string(zmq.SUBSCRIBE,'')
socket_temp.set_hwm(1)
socket_temp.connect("tcp://localhost:"+str(config['zmq']['port_temp']))
#  --------
socket_sig = context.socket(zmq.SUB)
socket_sig.setsockopt_string(zmq.SUBSCRIBE,'')
socket_sig.connect("tcp://localhost:"+str(config['zmq']['port_sig']))
#  --------
socket_send = context.socket(zmq.PUSH)
socket_send.bind("tcp://*:"+str(config['zmq']['port_send']))
#  --------
poller_temp = zmq.Poller()
poller_sig = zmq.Poller()
poller_temp.register(socket_temp, zmq.POLLIN)
poller_sig.register(socket_sig, zmq.POLLIN)


# bokeh stuff
sensor_count = config['bokeh']['Input_Controls']['Value']['sensor_count_input']
# Input controls
sensor_count_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['sensor_count_input'],
    value=config['bokeh']['Input_Controls']['Value']['sensor_count_input'])
polycoeff_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['polycoeff_input'],
    value=config['bokeh']['Input_Controls']['Value']['polycoeff_input'])
offset_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['offset_input'],
    value=config['bokeh']['Input_Controls']['Value']['offset_input'])
fshift_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['fshift_input'],
    value=config['bokeh']['Input_Controls']['Value']['fshift_input'])
fft_size_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['fft_size_input'],
    value=config['bokeh']['Input_Controls']['Value']['fft_size_input'])
samp_rate_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['samp_rate_input'],
    value=config['bokeh']['Input_Controls']['Value']['samp_rate_input'])
thres_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['thres_input'],
    value=config['bokeh']['Input_Controls']['Value']['thres_input'])
min_dist_input = TextInput(
    title=config['bokeh']['Input_Controls']['Title']['min_dist_input'],
    value=config['bokeh']['Input_Controls']['Value']['min_dist_input'])
harmonic_input = Select(value=str(5),
                        title=config['bokeh']['Input_Controls']['Title']['harmonic_input'],
                        options=eval(['bokeh']['Input_Controls']['Value']['harmonic_input']))
apply_button = Button(
    label=config['bokeh']['Input_Controls']['Title']['apply_button'],
    button_type=config['bokeh']['Input_Controls']['Value']['apply_button'])

# Temperature Plot
p0 = figure(title=config['bokeh']['Temperature_Plot']['title'],
            y_range=config['bokeh']['Temperature_Plot']['y_range'],
            plot_height=['bokeh']['Temperature_Plot']['plot_height'],
            plot_width=['bokeh']['Temperature_Plot']['plot_width'],
            tools=['bokeh']['Temperature_Plot']['tools'],
            y_axis_location=['bokeh']['Temperature_Plot']['y_axis_location'])
p0.yaxis.axis_label = ['bokeh']['Temperature_Plot']['ylabel']
p0.xaxis.axis_label = ['bokeh']['Temperature_Plot']['xlabel']
p0.x_range.follow = "end"
p0.x_range.follow_interval = ['bokeh']['Temperature_Plot']['x_range_interval']
p0.x_range.range_padding = ['bokeh']['Temperature_Plot']['x_range_interval']
p0.title.text_font_size = ['bokeh']['title_font_size']
p0.xaxis.axis_label_text_font_size = ['bokeh']['label_font_size']
p0.yaxis.axis_label_text_font_size = ['bokeh']['label_font_size']

data = dict(
        time=[]
    )

for i in range(0, sensor_count):
    data.update({'temp_'+str(i): []})

source = ColumnDataSource(data)

linestyles = config['bokeh']['Lines']['styles']

for i in range(0, sensor_count):
    p0.line(x='time', y='temp_'+str(i), source=source,
            line_width=config['bokeh']['Lines']['styles'],
            line_color=config['bokeh']['Lines']['colors'],
            line_dash=linestyles[i],
            legend_label="Sensor "+config['bokeh']['Temperature_Plot']['sensor_names'][i])

p0.legend.location = config['bokeh']['Legend_Temp']['location']
p0.legend.click_policy = config['bokeh']['Legend_Temp']['click_policy']
p0.legend.label_text_font_size = config['bokeh']['legend_font_size']


# Spectrum Plot
source_fft = ColumnDataSource(dict(
    freq=[], sp=[]
))

p1 = figure(title=config['bokeh']['Spectrum_Plot']['title'],
            y_range=config['bokeh']['Spectrum_Plot']['y_range'],
            x_range=config['bokeh']['Spectrum_Plot']['x_range'],
            plot_height=config['bokeh']['Spectrum_Plot']['plot_height'],
            plot_width=config['bokeh']['Spectrum_Plot']['plot_width'],
            y_axis_type='log',
            tools=config['bokeh']['Spectrum_Plot']['tools'],
            y_axis_location=config['bokeh']['Spectrum_Plot']['y_axis_location'])
p1.xaxis.axis_label = config['bokeh']['Spectrum_Plot']['xlabel']
p1.yaxis.axis_label = config['bokeh']['Spectrum_Plot']['ylabel']
p1.title.text_font_size = config['bokeh']['title_font_size']
p1.xaxis.axis_label_text_font_size = config['bokeh']['label_font_size']
p1.yaxis.axis_label_text_font_size = config['bokeh']['label_font_size']

p1.line(x='freq', y='sp', source=source_fft, line_width=2, line_color='black')


# functions
def _update_temp():
    socks_temp = dict(poller_temp.poll(0))
    if socks_temp.get(socket_temp) == zmq.POLLIN:
        message_temp = socket_temp.recv()
        T = numpy.frombuffer(message_temp, dtype=numpy.float32())
        T = numpy.reshape(T, (len(T)//16, 16))
        return T
    else:
        return -1


def _update_signal():
    socks_sig = dict(poller_sig.poll(0))
    if socks_sig.get(socket_sig) == zmq.POLLIN:
        message_sig = socket_sig.recv()
        signal = numpy.frombuffer(message_sig, dtype=numpy.complex64())
        return signal
    else:
        return -1


def _calc_spectrum(x, fA):
    f, Pxx = sg.periodogram(x, fA,
                            window=config['bokeh']['Periodogram']['per_window'],
                            nfft=len(x), return_onesided=False,
                            scaling='spectrum')
    Pxx = Pxx[f.argsort()]
    f.sort()
    ptr = len(f)//2
    Pxx = numpy.append(Pxx[:ptr], Pxx[ptr+1:])
    f = numpy.append(f[:ptr], f[ptr+1:])
    return f, Pxx


def _replaceNaN(x):
    x = numpy.array(x)
    i, j = numpy.argwhere(numpy.isnan(x)).T
    x[i, j] = 0.0
    return x


@count()
def update(t):
    T = _update_temp()
    signal = _update_signal()
    if not isinstance(T, int):
        new_data = dict(time=[t])
        T = _replaceNaN(T)
        for ii in range(0, sensor_count):
            if T[:, ii].any() != 0:
                new_data.update({'temp_'+str(ii): [T[:, ii]]})
            else:
                new_data.update({'temp_'+str(ii): [numpy.mean(T[:, ii])]})
        source.stream(new_data, 800)
    if not isinstance(signal, int):
        if len(signal) < 512:
            source_fft.data = source_fft.data
        else:
            f, Pxx = _calc_spectrum(signal[0:2048], samp_rate_input.value)
            f = f - numpy.asarray(float(eval(fshift_input.value))) + 24e6*5
            new_fft_data = dict(
                freq=f,
                sp=Pxx,
            )
            source_fft.data = new_fft_data


def update_variables():
    print("sending")
    ii = [harmonic_input.value, polycoeff_input.value, offset_input.value,
          fshift_input.value, fft_size_input.value, samp_rate_input.value,
          thres_input.value, min_dist_input.value]
    socket_send.send_pyobj(ii)
    print("sent")


apply_button.on_click(update_variables)
input_1 = column(harmonic_input, sensor_count_input, fft_size_input)#
input_2 = column(polycoeff_input, offset_input)
input_3 = column(samp_rate_input, thres_input, min_dist_input)
input_4 = column(fshift_input, apply_button)
input_g = layout([[p0, p1]], sizing_mode='stretch_width')
input_c = gridplot([[p0, p1], [row(input_1, input_2, input_3, input_4), None]])
#curdoc().add_periodic_callback(update, p_update)
#curdoc().add_root(input_c)#
#curdoc().title = "test plot"
show(input_c)
