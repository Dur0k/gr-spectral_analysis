#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: durok
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

class hier_signal_source(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(self, "Not titled yet",
        gr.io_signature(1, 1, gr.sizeof_gr_complex),
        gr.io_signature(1, 1, gr.sizeof_gr_complex)))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.sig_source_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_2 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_3 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_4 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_5 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_6 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_7 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_8 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_9 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_10 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_11 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_12 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_13 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_14 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.sig_source_15 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, , 1, 0, 0)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(1, 1024)
        self.blocks_add_xx_0 = blocks.add_vcc(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.sig_source_15, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.sig_source_14, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.sig_source_13, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.sig_source_12, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.sig_source_11, 0), (self.blocks_add_xx_0, 13))
        self.connect((self.sig_source_10, 0), (self.blocks_add_xx_0, 9))
        self.connect((self.sig_source_9, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.sig_source_8, 0), (self.blocks_add_xx_0, 15))
        self.connect((self.sig_source_7, 0), (self.blocks_add_xx_0, 11))
        self.connect((self.sig_source_6, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.sig_source_5, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.sig_source_4, 0), (self.blocks_add_xx_0, 12))
        self.connect((self.sig_source_3, 0), (self.blocks_add_xx_0, 8))
        self.connect((self.sig_source_2, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.sig_source_1, 0), (self.blocks_add_xx_0, 14))
        self.connect((self.sig_source_0, 0), (self.blocks_add_xx_0, 10))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.sig_source_15.set_sampling_freq(self.samp_rate)
        self.sig_source_14.set_sampling_freq(self.samp_rate)
        self.sig_source_13.set_sampling_freq(self.samp_rate)
        self.sig_source_12.set_sampling_freq(self.samp_rate)
        self.sig_source_11.set_sampling_freq(self.samp_rate)
        self.sig_source_10.set_sampling_freq(self.samp_rate)
        self.sig_source_9.set_sampling_freq(self.samp_rate)
        self.sig_source_8.set_sampling_freq(self.samp_rate)
        self.sig_source_7.set_sampling_freq(self.samp_rate)
        self.sig_source_6.set_sampling_freq(self.samp_rate)
        self.sig_source_5.set_sampling_freq(self.samp_rate)
        self.sig_source_4.set_sampling_freq(self.samp_rate)
        self.sig_source_3.set_sampling_freq(self.samp_rate)
        self.sig_source_2.set_sampling_freq(self.samp_rate)
        self.sig_source_1.set_sampling_freq(self.samp_rate)
        self.sig_source_0.set_sampling_freq(self.samp_rate)
