#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 gr-spectral_analysis author.
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
    Block performs spectral analysis using Periodogram with different windows. A complex vector is defined and input. The block outputs two vectors with the frequency and the complex power of the spectrum.
    Args:
        sample_rate: Incoming stream sample rate
        fft_size: Number of FFT bins and input/output vector length
        window: the window used for Periodogram
    Reference:
    https://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.signal.periodogram.html
    """
    def __init__(self, sample_rate, fft_size, window):
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.window = window
        gr.sync_block.__init__(self,
            name="periodogram_py_cc",
            in_sig=[(numpy.complex64,self.fft_size)],
            out_sig=[(numpy.float32,self.fft_size),(numpy.complex64,self.fft_size)])
        
    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_fft_size(self):
        return self.fft_size

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    def get_sample_rate(self):
        return self.sample_rate

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        # <+signal processing here+>
        f, Pxx = signal.periodogram(in0, self.sample_rate, self.window, self.fft_size,return_onesided=False)#, return_onesided=False,scaling='spectrum'
        print(f.shape)
        out0[:] = f
        out1[:] = Pxx
        return len(output_items[0])

