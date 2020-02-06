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

import peakutils
import numpy
from gnuradio import gr

class peak_finding_cf(gr.sync_block):
    """
    Block to find peaks in input spectrum. Takes in float f and complex Pxx vectors and ouputs vector with peaks of length Sensor Count.
    Args:
    - FFT Size: sets input vector length
    - Threshold: normalized threshold, only peaks higher amplitude will be detected
    - Peak Distance: Minimum distance between each detected peak

    Reference:
    https://peakutils.readthedocs.io/en/latest/reference.html
    """
    def __init__(self,fft_size, sensor_count, thres, min_dist):
        self.fft_size = fft_size
        self.sensor_count = sensor_count
        self.thres = thres
        self.min_dist = min_dist
        gr.sync_block.__init__(self,
            name="peak_finding_cf",
            in_sig=[(numpy.float32,self.fft_size), (numpy.complex64,self.fft_size)],
            out_sig=[(numpy.float32,self.sensor_count)])

    def peakfinding(self, f, Pxx, thres, min_dist, sensor_count):
        f_cyc = numpy.insert(f,0,f[len(f)-1])
        Pxx_cyc = abs(numpy.insert(Pxx,0,Pxx[len(f)-1]))
        peaks = peakutils.indexes(Pxx_cyc, thres, min_dist)
        peaks_zero = []
        # Set found peaks to zero
        peaks_zero = numpy.zeros(Pxx_cyc.shape)
        peaks_zero[:] = Pxx_cyc
        peaks_zero[peaks] = 0
        # Sort the peaks by height with index
        peak_sorting = numpy.vstack((f_cyc,peaks_zero))
        #high = numpy.flip(numpy.argsort(peak_sorting[1]),axis=0)
        # Ignore the first inserted freq and shift all indices by one
        high = numpy.flip(numpy.argsort(peak_sorting[1][1:len(peak_sorting[1])]),axis=0) +1
        # Add additional peaks until sensor_count is reached
        index = 0
        failure_vec = numpy.zeros(len(peaks))
        while (len(peaks) < sensor_count):
            #peaks = numpy.append(peaks, int(peaks_zero[high[index]]))
            peaks = numpy.append(peaks, int(high[index]))
            failure_vec = numpy.append(failure_vec, 1)
            index = index + 1
        while (len(peaks) > sensor_count):
            peaks = numpy.delete(peaks,len(peaks)-1,0)
            failure_vec = numpy.delete(failure_vec, len(peaks)-1, 0)
            
        f_per = f_cyc[peaks]
        return f_per

    def set_sensor_count(self, sensor_count):
        self.sensor_count = sensor_count

    def get_sensor_count(self):
        return self.sensor_count

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_fft_size(self):
        return self.fft_size

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]
        # <+signal processing here+>
        peaks = self.peakfinding(in0, in1, self.thres, self.min_dist, self.sensor_count)
        out[:] = peaks
        return len(output_items[0])

