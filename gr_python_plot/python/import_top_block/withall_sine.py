#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.8.0.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import spectral_analysis

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.sensor_count = sensor_count = 2
        self.samp_rate = samp_rate = 1e6/100
        self.plot = plot = 100
        self.freq = freq = -2000
        self.fft_size = fft_size = 1024
        self.polycoeff = [[2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08],[2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08]]
        self.fshift = 24e6 * 5
        self.offset = [130.0,200.0]
        self.thres = 0.03
        self.min_dist = 1

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0_0_0 = zeromq.push_sink(gr.sizeof_gr_complex, 1, 'tcp://*:5589', 10, False, -1)
        self.zeromq_push_sink_0_0 = zeromq.push_sink(gr.sizeof_float, self.sensor_count, 'tcp://*:5588', 10, False, -1)
        self.variable_qtgui_range_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq+300, 1, 0, 0)
        self.variable_qtgui_range_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq, 1, 0, 0)
        self.spectral_analysis_temperature_calc_ff_0 = spectral_analysis.temperature_calc_ff(sensor_count, self.polycoeff, self.fshift, self.offset)
        self.spectral_analysis_periodogram_py_cc_0 = spectral_analysis.periodogram_py_cc(samp_rate, fft_size, 'boxcar')
        self.spectral_analysis_peak_finding_cf_0 = spectral_analysis.peak_finding_cf(fft_size, sensor_count, self.thres, self.min_dist)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*10,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_add_xx_0 = blocks.add_vcc(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.spectral_analysis_periodogram_py_cc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.zeromq_push_sink_0_0_0, 0))
        self.connect((self.spectral_analysis_peak_finding_cf_0, 0), (self.spectral_analysis_temperature_calc_ff_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 0), (self.spectral_analysis_peak_finding_cf_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 1), (self.spectral_analysis_peak_finding_cf_0, 1))
        self.connect((self.spectral_analysis_temperature_calc_ff_0, 0), (self.zeromq_push_sink_0_0, 0))
        self.connect((self.variable_qtgui_range_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.variable_qtgui_range_0_0, 0), (self.blocks_add_xx_0, 1))

    def get_sensor_count(self):
        #return self.sensor_count
        return self.spectral_analysis_temperature_calc_ff_0.get_sensor_count()

    def set_sensor_count(self, sensor_count):
        self.sensor_count = sensor_count
        #self.spectral_analysis_temperature_calc_ff_0.set_polycoeff(self.polycoeff)
        #self.spectral_analysis_peak_finding_cf_0.set_offset(self.offset)

    def get_polycoeff(self):
        return self.polycoeff

    def set_polycoeff(self, polycoeff):
        self.polycoeff = polycoeff
        self.spectral_analysis_temperature_calc_ff_0.set_polycoeff(self.polycoeff)

    def set_offset(self, offset):
        self.offset = offset
        self.spectral_analysis_temperature_calc_ff_0.set_offset(self.offset)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.spectral_analysis_peak_finding_cf_0.set_fft_size(self.fft_size)
        
    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*10)
        self.variable_qtgui_range_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0.set_sampling_freq(self.samp_rate)
        self.spectral_analysis_periodogram_py_cc_0.set_sample_rate(self.samp_rate)

    def get_fshift(self):
        return self.fshift

    def set_fshift(self, fshift):
        self.fshift = fshift
        self.spectral_analysis_temperature_calc_ff_0.set_fshift(self.fshift)

    def get_thres(self):
        return self.thres

    def set_thres(self, thres):
        self.thres = thres
        self.spectral_analysis_peak_finding_cf_0.set_thres(self.thres)

    def get_min_dist(self):
        return self.min_dist

    def set_min_dist(self, min_dist):
        self.min_dist = min_dist
        self.spectral_analysis_peak_finding_cf_0.set_min_dist(self.min_dist)

    def get_plot(self):
        return self.plot

    def set_plot(self, plot):
        self.plot = plot

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.variable_qtgui_range_0.set_frequency(self.freq)
        self.variable_qtgui_range_0_0.set_frequency(self.freq+300)

    def get_fshift(self):
        return self.fshift

    def set_fshift(self, fshift):
        self.fshift = fshift
        self.spectral_analysis_temperature_calc_ff_0.set_fshift(self.fshift)

   
def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
