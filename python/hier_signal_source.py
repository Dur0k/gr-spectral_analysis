# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: hier_signal_source
# Author: durok
# GNU Radio version: 3.8.0.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal




class hier_signal_source(gr.hier_block2):
    def __init__(self, amp_0=0, amp_1=0, amp_10=0, amp_11=0, amp_12=0, amp_13=0, amp_14=0, amp_15=0, amp_2=0, amp_3=0, amp_4=0, amp_5=0, amp_6=0, amp_7=0, amp_8=0, amp_9=0, freq_0=0, freq_1=0, freq_10=0, freq_11=0, freq_12=0, freq_13=0, freq_14=0, freq_15=0, freq_2=0, freq_3=0, freq_4=0, freq_5=0, freq_6=0, freq_7=0, freq_8=0, freq_9=0):
        gr.hier_block2.__init__(
            self, "hier_signal_source",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.amp_0 = amp_0
        self.amp_1 = amp_1
        self.amp_10 = amp_10
        self.amp_11 = amp_11
        self.amp_12 = amp_12
        self.amp_13 = amp_13
        self.amp_14 = amp_14
        self.amp_15 = amp_15
        self.amp_2 = amp_2
        self.amp_3 = amp_3
        self.amp_4 = amp_4
        self.amp_5 = amp_5
        self.amp_6 = amp_6
        self.amp_7 = amp_7
        self.amp_8 = amp_8
        self.amp_9 = amp_9
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self.freq_10 = freq_10
        self.freq_11 = freq_11
        self.freq_12 = freq_12
        self.freq_13 = freq_13
        self.freq_14 = freq_14
        self.freq_15 = freq_15
        self.freq_2 = freq_2
        self.freq_3 = freq_3
        self.freq_4 = freq_4
        self.freq_5 = freq_5
        self.freq_6 = freq_6
        self.freq_7 = freq_7
        self.freq_8 = freq_8
        self.freq_9 = freq_9

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.variable_qtgui_range_0_2_1_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_10, amp_10, 0, 0)
        self.variable_qtgui_range_0_2_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_14, amp_14, 0, 0)
        self.variable_qtgui_range_0_2 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_6, amp_6, 0, 0)
        self.variable_qtgui_range_0_1_0_1_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_8, amp_8, 0, 0)
        self.variable_qtgui_range_0_1_0_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_12, amp_12, 0, 0)
        self.variable_qtgui_range_0_1_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_4, amp_4, 0, 0)
        self.variable_qtgui_range_0_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_0, amp_0, 0, 0)
        self.variable_qtgui_range_0_0_1_1_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_11, amp_11, 0, 0)
        self.variable_qtgui_range_0_0_1_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_15, amp_15, 0, 0)
        self.variable_qtgui_range_0_0_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_7, amp_7, 0, 0)
        self.variable_qtgui_range_0_0_0_0_1_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_9, amp_9, 0, 0)
        self.variable_qtgui_range_0_0_0_0_1 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_13, amp_13, 0, 0)
        self.variable_qtgui_range_0_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_5, amp_5, 0, 0)
        self.variable_qtgui_range_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_1, amp_1, 0, 0)
        self.variable_qtgui_range_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_3, amp_3, 0, 0)
        self.variable_qtgui_range_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, freq_2, amp_2, 0, 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self, 0))
        self.connect((self.variable_qtgui_range_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.variable_qtgui_range_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.variable_qtgui_range_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.variable_qtgui_range_0_0_0_0, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.variable_qtgui_range_0_0_0_0_1, 0), (self.blocks_add_xx_0, 13))
        self.connect((self.variable_qtgui_range_0_0_0_0_1_0, 0), (self.blocks_add_xx_0, 9))
        self.connect((self.variable_qtgui_range_0_0_1, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.variable_qtgui_range_0_0_1_1, 0), (self.blocks_add_xx_0, 15))
        self.connect((self.variable_qtgui_range_0_0_1_1_0, 0), (self.blocks_add_xx_0, 11))
        self.connect((self.variable_qtgui_range_0_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.variable_qtgui_range_0_1_0, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.variable_qtgui_range_0_1_0_1, 0), (self.blocks_add_xx_0, 12))
        self.connect((self.variable_qtgui_range_0_1_0_1_0, 0), (self.blocks_add_xx_0, 8))
        self.connect((self.variable_qtgui_range_0_2, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.variable_qtgui_range_0_2_1, 0), (self.blocks_add_xx_0, 14))
        self.connect((self.variable_qtgui_range_0_2_1_0, 0), (self.blocks_add_xx_0, 10))

    def get_amp_0(self):
        return self.amp_0

    def set_amp_0(self, amp_0):
        self.amp_0 = amp_0
        self.variable_qtgui_range_0_1.set_amplitude(self.amp_0)

    def get_amp_1(self):
        return self.amp_1

    def set_amp_1(self, amp_1):
        self.amp_1 = amp_1
        self.variable_qtgui_range_0_0_0.set_amplitude(self.amp_1)

    def get_amp_10(self):
        return self.amp_10

    def set_amp_10(self, amp_10):
        self.amp_10 = amp_10
        self.variable_qtgui_range_0_2_1_0.set_amplitude(self.amp_10)

    def get_amp_11(self):
        return self.amp_11

    def set_amp_11(self, amp_11):
        self.amp_11 = amp_11
        self.variable_qtgui_range_0_0_1_1_0.set_amplitude(self.amp_11)

    def get_amp_12(self):
        return self.amp_12

    def set_amp_12(self, amp_12):
        self.amp_12 = amp_12
        self.variable_qtgui_range_0_1_0_1.set_amplitude(self.amp_12)

    def get_amp_13(self):
        return self.amp_13

    def set_amp_13(self, amp_13):
        self.amp_13 = amp_13
        self.variable_qtgui_range_0_0_0_0_1.set_amplitude(self.amp_13)

    def get_amp_14(self):
        return self.amp_14

    def set_amp_14(self, amp_14):
        self.amp_14 = amp_14
        self.variable_qtgui_range_0_2_1.set_amplitude(self.amp_14)

    def get_amp_15(self):
        return self.amp_15

    def set_amp_15(self, amp_15):
        self.amp_15 = amp_15
        self.variable_qtgui_range_0_0_1_1.set_amplitude(self.amp_15)

    def get_amp_2(self):
        return self.amp_2

    def set_amp_2(self, amp_2):
        self.amp_2 = amp_2
        self.variable_qtgui_range_0.set_amplitude(self.amp_2)

    def get_amp_3(self):
        return self.amp_3

    def set_amp_3(self, amp_3):
        self.amp_3 = amp_3
        self.variable_qtgui_range_0_0.set_amplitude(self.amp_3)

    def get_amp_4(self):
        return self.amp_4

    def set_amp_4(self, amp_4):
        self.amp_4 = amp_4
        self.variable_qtgui_range_0_1_0.set_amplitude(self.amp_4)

    def get_amp_5(self):
        return self.amp_5

    def set_amp_5(self, amp_5):
        self.amp_5 = amp_5
        self.variable_qtgui_range_0_0_0_0.set_amplitude(self.amp_5)

    def get_amp_6(self):
        return self.amp_6

    def set_amp_6(self, amp_6):
        self.amp_6 = amp_6
        self.variable_qtgui_range_0_2.set_amplitude(self.amp_6)

    def get_amp_7(self):
        return self.amp_7

    def set_amp_7(self, amp_7):
        self.amp_7 = amp_7
        self.variable_qtgui_range_0_0_1.set_amplitude(self.amp_7)

    def get_amp_8(self):
        return self.amp_8

    def set_amp_8(self, amp_8):
        self.amp_8 = amp_8
        self.variable_qtgui_range_0_1_0_1_0.set_amplitude(self.amp_8)

    def get_amp_9(self):
        return self.amp_9

    def set_amp_9(self, amp_9):
        self.amp_9 = amp_9
        self.variable_qtgui_range_0_0_0_0_1_0.set_amplitude(self.amp_9)

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0
        self.variable_qtgui_range_0_1.set_frequency(self.freq_0)

    def get_freq_1(self):
        return self.freq_1

    def set_freq_1(self, freq_1):
        self.freq_1 = freq_1
        self.variable_qtgui_range_0_0_0.set_frequency(self.freq_1)

    def get_freq_10(self):
        return self.freq_10

    def set_freq_10(self, freq_10):
        self.freq_10 = freq_10
        self.variable_qtgui_range_0_2_1_0.set_frequency(self.freq_10)

    def get_freq_11(self):
        return self.freq_11

    def set_freq_11(self, freq_11):
        self.freq_11 = freq_11
        self.variable_qtgui_range_0_0_1_1_0.set_frequency(self.freq_11)

    def get_freq_12(self):
        return self.freq_12

    def set_freq_12(self, freq_12):
        self.freq_12 = freq_12
        self.variable_qtgui_range_0_1_0_1.set_frequency(self.freq_12)

    def get_freq_13(self):
        return self.freq_13

    def set_freq_13(self, freq_13):
        self.freq_13 = freq_13
        self.variable_qtgui_range_0_0_0_0_1.set_frequency(self.freq_13)

    def get_freq_14(self):
        return self.freq_14

    def set_freq_14(self, freq_14):
        self.freq_14 = freq_14
        self.variable_qtgui_range_0_2_1.set_frequency(self.freq_14)

    def get_freq_15(self):
        return self.freq_15

    def set_freq_15(self, freq_15):
        self.freq_15 = freq_15
        self.variable_qtgui_range_0_0_1_1.set_frequency(self.freq_15)

    def get_freq_2(self):
        return self.freq_2

    def set_freq_2(self, freq_2):
        self.freq_2 = freq_2
        self.variable_qtgui_range_0.set_frequency(self.freq_2)

    def get_freq_3(self):
        return self.freq_3

    def set_freq_3(self, freq_3):
        self.freq_3 = freq_3
        self.variable_qtgui_range_0_0.set_frequency(self.freq_3)

    def get_freq_4(self):
        return self.freq_4

    def set_freq_4(self, freq_4):
        self.freq_4 = freq_4
        self.variable_qtgui_range_0_1_0.set_frequency(self.freq_4)

    def get_freq_5(self):
        return self.freq_5

    def set_freq_5(self, freq_5):
        self.freq_5 = freq_5
        self.variable_qtgui_range_0_0_0_0.set_frequency(self.freq_5)

    def get_freq_6(self):
        return self.freq_6

    def set_freq_6(self, freq_6):
        self.freq_6 = freq_6
        self.variable_qtgui_range_0_2.set_frequency(self.freq_6)

    def get_freq_7(self):
        return self.freq_7

    def set_freq_7(self, freq_7):
        self.freq_7 = freq_7
        self.variable_qtgui_range_0_0_1.set_frequency(self.freq_7)

    def get_freq_8(self):
        return self.freq_8

    def set_freq_8(self, freq_8):
        self.freq_8 = freq_8
        self.variable_qtgui_range_0_1_0_1_0.set_frequency(self.freq_8)

    def get_freq_9(self):
        return self.freq_9

    def set_freq_9(self, freq_9):
        self.freq_9 = freq_9
        self.variable_qtgui_range_0_0_0_0_1_0.set_frequency(self.freq_9)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.variable_qtgui_range_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_0_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_0_0_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_0_0_1_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_1_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0_1_1_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_1_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_1_0_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_1_0_1_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_2.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_2_1.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_2_1_0.set_sampling_freq(self.samp_rate)

