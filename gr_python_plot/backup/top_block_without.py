#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import spectral_analysis
from gnuradio import qtgui

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sensor_count = sensor_count = 2
        self.samp_rate = samp_rate = 1e6/100
        self.plot = plot = 100
        self.fft_size = fft_size = 128

        ##################################################
        # Blocks
        ##################################################
        self.variable_qtgui_range_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, -900, 1, 0, 0)
        self.variable_qtgui_range_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, -1200, 1, 0, 0)
        self.spectral_analysis_temperature_calc_ff_0 = spectral_analysis.temperature_calc_ff(2, [[2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08],[2.22769620e-02, -1.70367733e+00, -1.58914013e+01, 1.19999708e+08]], 24e6 * 5, [130.0,200.0])
        self.spectral_analysis_periodogram_py_cc_0 = spectral_analysis.periodogram_py_cc(samp_rate, fft_size, 'boxcar')
        self.spectral_analysis_peak_finding_cf_0 = spectral_analysis.peak_finding_cf(fft_size, sensor_count, 0.03, 1)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_f(sensor_count, 1024)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*10,True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_add_xx_0 = blocks.add_vcc(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.spectral_analysis_periodogram_py_cc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.spectral_analysis_peak_finding_cf_0, 0), (self.spectral_analysis_temperature_calc_ff_0, 0))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 1), (self.spectral_analysis_peak_finding_cf_0, 1))
        self.connect((self.spectral_analysis_periodogram_py_cc_0, 0), (self.spectral_analysis_peak_finding_cf_0, 0))
        self.connect((self.spectral_analysis_temperature_calc_ff_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.variable_qtgui_range_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.variable_qtgui_range_0_0, 0), (self.blocks_add_xx_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sensor_count(self):
        return self.sensor_count

    def set_sensor_count(self, sensor_count):
        self.sensor_count = sensor_count

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*10)
        self.variable_qtgui_range_0.set_sampling_freq(self.samp_rate)
        self.variable_qtgui_range_0_0.set_sampling_freq(self.samp_rate)

    def get_plot(self):
        return self.plot

    def set_plot(self, plot):
        self.plot = plot

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size



def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
