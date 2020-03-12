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
from gnuradio import uhd
from gnuradio import filter
from gnuradio.filter import firdes
import spectral_analysis

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.sensor_count = sensor_count = 16
        self.samp_rate = samp_rate = 1e6
        self.plot = plot = 100
        self.freq = freq = -2000
        self.fft_size = fft_size = 1024*1
        self.polycoeff = polycoeff = [[2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08],[3.75334018e-02, -2.24642587, -3.69621493e+01, 1.20001284e+08], [3.75334018e-02, -2.24642587, -3.69621493e+01, 1.20001284e+08], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        self.fshift = fshift = 24e6 * 5
        self.offset = offset = [235.0, -300, 326.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.thres = thres = 0.03
        self.min_dist = min_dist = 1
        ## NEW
        self.harmonic = harmonic = 5
        self.decimation = decimation = 500//harmonic
        self.lo_freq = lo_freq = harmonic*24000000-250000
        self.bpfc = bpfc = firdes.low_pass(1,samp_rate,2*samp_rate/decimation/10,500)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("addr=134.102.176.209", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_clock_source('internal', 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.lo_freq, 0)
        self.uhd_usrp_source_0_0.set_gain(30, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0_0.set_bandwidth(1000000, 0)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        # No synchronization enforced.
        self.zeromq_pub_sink_signal = zeromq.pub_sink(gr.sizeof_gr_complex, self.fft_size, 'tcp://*:5589', 10, False, -1)
        self.zeromq_pub_sink_temp = zeromq.pub_sink(gr.sizeof_float, self.sensor_count, 'tcp://*:5588', 10, False, -1)

        self.spectral_analysis_temperature_calc_ff_0 = spectral_analysis.temperature_calc_ff(self.sensor_count, self.polycoeff, self.fshift, self.offset)
        self.spectral_analysis_periodogram_py_cc_0 = spectral_analysis.periodogram_py_cc(self.samp_rate/100, self.fft_size, 'boxcar')
        self.spectral_analysis_peak_finding_cf_0 = spectral_analysis.peak_finding_cf(self.fft_size, self.sensor_count, self.thres, self.min_dist)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, self.fft_size)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(self.decimation, self.bpfc, 250000, self.samp_rate)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.zeromq_pub_sink_signal, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.spectral_analysis_periodogram_py_cc_0, 0))
        self.connect((self.spectral_analysis_peak_finding_cf_0, 0), (self.spectral_analysis_temperature_calc_ff_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 0), (self.spectral_analysis_peak_finding_cf_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 1), (self.spectral_analysis_peak_finding_cf_0, 1))
        self.connect((self.spectral_analysis_temperature_calc_ff_0, 0), (self.zeromq_pub_sink_temp, 0))


    def get_sensor_count(self):
        #return self.sensor_count
        return self.spectral_analysis_temperature_calc_ff_0.get_sensor_count()

    # not working
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
        self.disconnect(self.blocks_stream_to_vector_0)
        self.disconnect(self.spectral_analysis_periodogram_py_cc_0)
        self.disconnect(self.spectral_analysis_peak_finding_cf_0)
        del self.blocks_stream_to_vector_0
        del self.spectral_analysis_periodogram_py_cc_0
        del self.spectral_analysis_peak_finding_cf_0
        #print(type(self.fft_size))
        self.spectral_analysis_periodogram_py_cc_0 = spectral_analysis.periodogram_py_cc(self.samp_rate, self.fft_size, 'boxcar')#self.fft_size
        self.spectral_analysis_peak_finding_cf_0 = spectral_analysis.peak_finding_cf(self.fft_size, self.sensor_count, self.thres, self.min_dist)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, self.fft_size)
        self.connect((self.blocks_stream_to_vector_0, 0), (self.spectral_analysis_periodogram_py_cc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.spectral_analysis_peak_finding_cf_0, 0), (self.spectral_analysis_temperature_calc_ff_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 0), (self.spectral_analysis_peak_finding_cf_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 1), (self.spectral_analysis_peak_finding_cf_0, 1))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bpfc(firdes.low_pass(1,self.samp_rate,2*self.samp_rate/self.decimation/10,500))
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

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

    def get_fshift(self):
        return self.fshift

    def set_fshift(self, fshift):
        self.fshift = fshift
        self.spectral_analysis_temperature_calc_ff_0.set_fshift(self.fshift)

    def get_harmonic(self):
        return self.harmonic

    def set_harmonic(self, harmonic):
        self.harmonic = harmonic
        self.set_decimation(500//self.harmonic)
        self.set_lo_freq(self.harmonic*24000000-250000)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_bpfc(firdes.low_pass(1,self.samp_rate,2*self.samp_rate/self.decimation/10,500))

    def get_lo_freq(self):
        return self.lo_freq

    def set_lo_freq(self, lo_freq):
        self.lo_freq = lo_freq
        self.uhd_usrp_source_0_0.set_center_freq(self.lo_freq, 0)

    def get_bpfc(self):
        return self.bpfc

    def set_bpfc(self, bpfc):
        self.bpfc = bpfc
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(self.bpfc)

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
