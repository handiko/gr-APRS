#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: APRS - With RTL-SDR dongle
# Author: Handiko
# Description: www.github.com/handiko/gr-APRS
# Generated: Sat Jan  5 12:17:36 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from APRS_Rx import APRS_Rx  # grc-generated hier_block
from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import epy_block_0
import math
import osmosdr
import sip
import time


class APRS_RX_RTL(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "APRS - With RTL-SDR dongle")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("APRS - With RTL-SDR dongle")
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

        self.settings = Qt.QSettings("GNU Radio", "APRS_RX_RTL")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.space = space = 2400
        self.samp_rate = samp_rate = 2.88e6
        self.rfgain = rfgain = 10
        self.mu = mu = 0.5
        self.mark = mark = 1200
        self.gmu = gmu = 0.175
        self.freq = freq = 144.39e6
        self.dev_ppm = dev_ppm = 52
        self.ch_rate = ch_rate = 48e3
        self.bb_rate = bb_rate = 192e3
        self.baud = baud = 1200
        self.afgain = afgain = -7

        ##################################################
        # Blocks
        ##################################################
        self._rfgain_range = Range(0, 49, 1, 10, 100)
        self._rfgain_win = RangeWidget(self._rfgain_range, self.set_rfgain, 'RF Gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rfgain_win, 2,0,1,1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=8000,
                decimation=int(ch_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	4096/2, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	192e3, #bw
        	'RF Spectrum', #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [6, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-105, -20)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 0,2,1,1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	256, #size
        	1200, #samp_rate
        	'Clock Recovery', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2.1, 2.1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1,0,1,2)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	8e3, #bw
        	'AF Spectrum', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-80, 20)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not False)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [0.8, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 1,2,2,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	2048, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	144.39e6, #fc
        	192e3, #bw
        	'RF Spectrum', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-120, -10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [0.8, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,1,2)
        self.pfb_decimator_ccf_0_0 = pfb.decimator_ccf(
        	  int(samp_rate / ch_rate),
        	  (),
        	  0,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0_0.declare_sample_delay(0)
        	
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
        	  int(samp_rate / bb_rate),
        	  (),
        	  0,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)
        	
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(dev_ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rfgain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.fft_filter_xxx_1 = filter.fft_filter_fff(1, (firdes.band_pass(1,ch_rate,400,5e3,400,firdes.WIN_BLACKMAN)), 1)
        self.fft_filter_xxx_1.declare_sample_delay(0)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", '', '52001', 10000, False)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(ch_rate/(2*math.pi*12e3/8.0))
        self._afgain_range = Range(-20, -1, 0.1, -7, 100)
        self._afgain_win = RangeWidget(self._afgain_range, self.set_afgain, 'AF Gain (dB)', "counter_slider", float)
        self.top_grid_layout.addWidget(self._afgain_win, 2,1,1,1)
        self.APRS_Rx_0 = APRS_Rx(
            samp_rate=ch_rate,
            baud=baud,
            mark=mark,
            space=space,
            mu=mu,
            gmu=gmu,
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.APRS_Rx_0, 'HDLC'), (self.epy_block_0, 'hdlc in'))    
        self.msg_connect((self.epy_block_0, 'ax25 out'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.connect((self.APRS_Rx_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fft_filter_xxx_1, 0))    
        self.connect((self.fft_filter_xxx_1, 0), (self.APRS_Rx_0, 0))    
        self.connect((self.fft_filter_xxx_1, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.pfb_decimator_ccf_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.pfb_decimator_ccf_0_0, 0))    
        self.connect((self.pfb_decimator_ccf_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.pfb_decimator_ccf_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    
        self.connect((self.pfb_decimator_ccf_0_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "APRS_RX_RTL")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_space(self):
        return self.space

    def set_space(self, space):
        self.space = space
        self.APRS_Rx_0.set_space(self.space)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.osmosdr_source_0.set_gain(self.rfgain, 0)

    def get_mu(self):
        return self.mu

    def set_mu(self, mu):
        self.mu = mu
        self.APRS_Rx_0.set_mu(self.mu)

    def get_mark(self):
        return self.mark

    def set_mark(self, mark):
        self.mark = mark
        self.APRS_Rx_0.set_mark(self.mark)

    def get_gmu(self):
        return self.gmu

    def set_gmu(self, gmu):
        self.gmu = gmu
        self.APRS_Rx_0.set_gmu(self.gmu)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_dev_ppm(self):
        return self.dev_ppm

    def set_dev_ppm(self, dev_ppm):
        self.dev_ppm = dev_ppm
        self.osmosdr_source_0.set_freq_corr(self.dev_ppm, 0)

    def get_ch_rate(self):
        return self.ch_rate

    def set_ch_rate(self, ch_rate):
        self.ch_rate = ch_rate
        self.fft_filter_xxx_1.set_taps((firdes.band_pass(1,self.ch_rate,400,5e3,400,firdes.WIN_BLACKMAN)))
        self.analog_quadrature_demod_cf_0.set_gain(self.ch_rate/(2*math.pi*12e3/8.0))
        self.APRS_Rx_0.set_samp_rate(self.ch_rate)

    def get_bb_rate(self):
        return self.bb_rate

    def set_bb_rate(self, bb_rate):
        self.bb_rate = bb_rate

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.APRS_Rx_0.set_baud(self.baud)

    def get_afgain(self):
        return self.afgain

    def set_afgain(self, afgain):
        self.afgain = afgain


def main(top_block_cls=APRS_RX_RTL, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
