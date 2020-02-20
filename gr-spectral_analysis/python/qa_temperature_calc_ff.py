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
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from temperature_calc_ff import temperature_calc_ff

class qa_temperature_calc_ff(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_001_t(self):
        # set up fg
        sensor_count = 3
        p_5=numpy.array([2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08])
        p_10=numpy.array([3.75334018e-02, -2.24642587e+00, -3.69621493e+01, 1.20001284e+08])
        p_14=numpy.array([1.41016716e-02, -1.21260981e+00, -4.59088135e+01, 1.20001834e+08])
        polycoeff=numpy.stack((p_5,p_14,p_10),axis=0)
        fshift = 24e6 * 5
        #offset = numpy.array([130.0,860.0,-300.0])
        offset = numpy.array([130,860,-300])
        #offset = numpy.array([130.0])
        src_data = (-1386.7188,-527.34375,34.179688)
        src_data = numpy.array(src_data)
        src = blocks.vector_source_f(src_data, vlen=sensor_count)
        
        temp = temperature_calc_ff(sensor_count, polycoeff, fshift, offset)
        v2s = blocks.vector_to_stream(gr.sizeof_float, sensor_count)
        dst = blocks.vector_sink_f()
        self.tb.connect(src, temp, v2s, dst)
        self.tb.run ()
        result_data = dst.data()
        print(result_data)
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_temperature_calc_ff)
