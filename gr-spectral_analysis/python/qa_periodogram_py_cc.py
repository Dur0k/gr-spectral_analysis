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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from periodogram_py_cc import periodogram_py_cc
import numpy

class qa_periodogram_py_cc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        sample_rate = 2000
        fft_size = 20
        window = 'boxcar'
        src_data = (-0.88384927-4.67771805e-01j, -0.27915375-9.60246418e-01j,
        0.49531971-8.68710758e-01j,  0.96854571-2.48835708e-01j,
        0.8527139 +5.22378215e-01j,  0.2182718 +9.75888017e-01j,
       -0.54892057+8.35874514e-01j, -0.98226609+1.87492228e-01j,
       -0.81820923-5.74920566e-01j, -0.1565274 -9.87673616e-01j,
        0.6003525 -7.99735503e-01j,  0.99210526-1.25407916e-01j,
        0.78047159+6.25191250e-01j,  0.09416452+9.95556650e-01j,
       -0.64941227+7.60436520e-01j, -0.99802436+6.28280835e-02j,
       -0.73965009-6.72991634e-01j, -0.03142957-9.99505969e-01j,
        0.69590604-7.18132846e-01j,  1.        -3.21416646e-13j)
        src_data = numpy.array(src_data)
        src = blocks.vector_source_c(src_data)
        s2v = blocks.stream_to_vector(gr.sizeof_gr_complex, fft_size)
        per = periodogram_py_cc(sample_rate,fft_size,window)
        v2s0 = blocks.vector_to_stream(gr.sizeof_float, fft_size)
        dst0 = blocks.vector_sink_f()
        v2s1 = blocks.vector_to_stream(gr.sizeof_gr_complex, fft_size)
        dst1 = blocks.vector_sink_c()
        self.tb.connect(src, s2v, (per,0), v2s0, dst0)
        self.tb.connect((per,1), v2s1, dst1)
        self.tb.run ()
        result_data0 = dst0.data()
        result_data1 = dst1.data()
        print(len(result_data0))
        print(len(result_data1))


if __name__ == '__main__':
    gr_unittest.run(qa_periodogram_py_cc)
