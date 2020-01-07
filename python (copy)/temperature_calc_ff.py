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

    def temp_calc(self, f, polycoeff, fshift, offset):
        f = numpy.array(f)
        poly = numpy.array(polycoeff)
        poly[:,3] = poly[:,3] - fshift - offset - f[0]
        # For all shifted polynomials calculate roots
        roots = numpy.empty((poly.shape[0],1))
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
        return roots
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        roots = self.temp_calc(in0, self.polycoeff, self.fshift, self.offset)
        out[:] = roots.T
        print(roots)
        return len(output_items[0])

'''
        poly = self.import_poly(self.polyfile)
    def import_poly(self, polyfile):
        with open(polyfile) as f:
            readerf = csv.reader(f)
            poly = []
            for rowf in readerf:
                poly.append(rowf)
        poly = numpy.array(poly,dtype="float")
        return poly
'''
