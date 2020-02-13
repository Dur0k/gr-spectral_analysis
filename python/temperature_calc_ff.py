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
from gnuradio import gr

class temperature_calc_ff(gr.sync_block):
    """
    Block calculates Temperatures of quarz oscillators based on their frequency and approximated  temperature characteristic. Takes a vector of frequencies as input and ouputs an equal amount of temperatures.
    Args:
    - Sensor Count: number of sensors and expected number of frequencies
    - Polynomial Coefficients: coefficients for approximated thermal behaviour of oscillator frequency, expects [Sensor Countx4] matrix
    - Frequency Shift: Frequency shift in [Hz] of original signal to baseband signal at USRP
    - Frequency Offset: Frequency offset of sensors, expects 1xSensor Count
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
        offset = numpy.asarray(offset)
        offset = offset.reshape(1,self.sensor_count)
        #print(type(poly[0]))
        poly[:,3] = poly[:,3] - fshift - offset - freq
 
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
        roots = roots.reshape(1,len(roots))
        #print(roots)
        return roots
    
    def set_sensor_count(self, sensor_count):
        self.sensor_count = sensor_count

    def get_sensor_count(self):
        return self.sensor_count

    def set_offset(self, offset):
        self.offset = offset

    def get_offset(self):
        return self.offset

    def set_fshift(self, fshift):
        self.fshift = fshift

    def get_fshift(self):
        return self.fshift

    def set_polycoeff(self, polycoeff):
        self.polycoeff = polycoeff

    def get_polycoeff(self):
        return self.polycoeff

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        roots = self.temp_calc(in0, self.polycoeff, self.fshift, self.offset)
        out[:] = roots.astype(float)
        return len(output_items[0])
