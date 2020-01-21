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
import csv
from gnuradio import gr

class temperature_calc_ff(gr.sync_block):
    """
    docstring for block temperature_calc_ff
    """
    def __init__(self, sensor_count, polycoeff, fshift, offset):
        self.sensor_count = sensor_count
        self.polycoeff = polycoeff
        self.fshift = fshift
        self.offset = offset
        gr.sync_block.__init__(self,
            name="temperature_calc_ff",
            in_sig=[(numpy.float32,self.sensor_count)],
            out_sig=[(numpy.float32,self.sensor_count)])

    def temp_calc(self, freq, polycoeff, fshift, offset):
        freq = numpy.array(freq)
        freq = numpy.mean(freq,axis=0)
        freq = numpy.sort(freq)
        freq = freq.reshape(1,self.sensor_count)
        poly = numpy.array(polycoeff)
        offset = numpy.array(offset).reshape(1,self.sensor_count)
        poly[:,3] = poly[:,3] - fshift - offset[:] - freq
        # For all shifted polynomials calculate roots
        roots = numpy.empty((poly.shape[0]))
        roots[:] = numpy.nan
        for i in range(0,poly.shape[0]):
            tmp = numpy.roots(poly[i])
            tmp = numpy.where(numpy.iscomplex(tmp),numpy.nan,tmp)
            tmp = numpy.where(tmp>40,numpy.nan,tmp)
            tmp = numpy.where(tmp<0,numpy.nan,tmp)
            # If all entries in tmp are nan then save a nan to roots
            if (numpy.isnan(tmp).all() == True):
                roots[i] = numpy.nan
            # Otherwise if a Number exists save it to roots
            elif ((~numpy.isnan(tmp)).any() == True):
                roots[i] = tmp[numpy.where(~numpy.isnan(tmp))]
        roots = roots.reshape(1,3)
        print(roots)
        return roots

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        roots = self.temp_calc(in0, self.polycoeff, self.fshift, self.offset)
        out[:] = roots.astype(float)
        return len(output_items[0])
