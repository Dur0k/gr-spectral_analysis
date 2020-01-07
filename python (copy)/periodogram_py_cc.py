#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 gr-spectral_analysis author.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from scipy import signal
from gnuradio import gr

class periodogram_py_cc(gr.sync_block):
    """
    docstring for block periodogram_py_cc
    Args:
        sample_rate: Incoming stream sample rate
        fft_size: Number of FFT bins
        window: the window taps generation function
    """
    def __init__(self, sample_rate, fft_size, window):
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.window = window
        gr.sync_block.__init__(self,
            name="periodogram_py_cc",
            in_sig=[(numpy.complex64,self.fft_size)],
            out_sig=[(numpy.float32,self.fft_size),(numpy.complex64,self.fft_size)])
        


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        # <+signal processing here+>
        f, Pxx = signal.periodogram(in0, self.sample_rate, self.window, self.fft_size,return_onesided=False)#, return_onesided=False,scaling='spectrum'
        
        out0[:] = f
        out1[:] = Pxx
        return len(output_items[0])
