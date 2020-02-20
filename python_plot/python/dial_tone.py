#!/usr/bin/env python3
# https://wiki.gnuradio.org/index.php/TutorialsWritePythonApplications
from gnuradio import gr
from gnuradio import audio, analog
from time import sleep

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        sample_rate = 32000
        ampl = 0.1

        self.src0 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 350, ampl)
        self.src1 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 440, ampl)
        self.dst = audio.sink(sample_rate, "")
        self.connect(self.src0, (self.dst, 0))
        self.connect(self.src1, (self.dst, 1))
        
    def set_freq(self, freq):
        self.freq = freq
        self.src0.set_frequency(self.freq)

if __name__ == '__main__':
    while True:
        tb = my_top_block()
        tb.start()
        sleep(1)
        tb.stop()
        tb.wait()
        tb.set_freq(1000)
        tb.start()
        sleep(2)
        #tb.stop()
