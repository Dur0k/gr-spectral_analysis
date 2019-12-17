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
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from peak_finding_cf import peak_finding_cf

class qa_peak_finding_cf (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        fft_size = 20
        sensor_count = 4
        thres = 0.0001
        min_dist = 0.5
        f_data = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
        Pxx_data = (0+0j,0+0j,0+0j,1+0j,0+0j,0+0j,0+0j,0+0j,1+0j,0+0j,0+0j,1+0j,0+0j,0+0j,0+0j,0+0j,0+0j,1+0j,0+0j,0+0j)
        expected_result = (3, 8, 11, 17)
        f_data = numpy.array(f_data)
        Pxx_data = numpy.array(Pxx_data)
        f = blocks.vector_source_f(f_data)
        Pxx = blocks.vector_source_c(Pxx_data)
        s2v0 = blocks.stream_to_vector(gr.sizeof_float, fft_size)
        s2v1 = blocks.stream_to_vector(gr.sizeof_gr_complex, fft_size)
        peaks = peak_finding_cf(fft_size, sensor_count, thres, min_dist)
        v2s = blocks.vector_to_stream(gr.sizeof_float, sensor_count)
        dst = blocks.vector_sink_f()
        self.tb.connect(f, s2v0, (peaks,0))
        self.tb.connect(Pxx, s2v1, (peaks,1))
        self.tb.connect(peaks, v2s, dst)
        self.tb.run()
        # check data
        result_data = dst.data()
        self.assertFloatTuplesAlmostEqual (expected_result, result_data, 6)


if __name__ == '__main__':
    gr_unittest.run(qa_peak_finding_cf, "qa_peak_finding_cf.xml")
