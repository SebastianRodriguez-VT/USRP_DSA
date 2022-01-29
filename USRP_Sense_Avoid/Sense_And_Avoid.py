#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Sense_And_Avoid
# Author: Sebastian
# GNU Radio version: 3.9.0.0-git

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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from SubbandFilterBank import SubbandFilterBank  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import epy_block_0_0
import epy_block_1
import math
import time
import threading

from gnuradio import qtgui

class Sense_And_Avoid(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Sense_And_Avoid", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Sense_And_Avoid")
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

        self.settings = Qt.QSettings("GNU Radio", "Sense_And_Avoid")

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
        self.vol_lvl = vol_lvl = 0.0015
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.samp_rate = samp_rate = 4.8e6
        self.activate_txer_fhss = activate_txer_fhss = 1
        self.Freq_lvl = Freq_lvl = -639e3

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_0_0 = epy_block_0_0.blk()
        # Create the options list
        self._activate_txer_fhss_options = (1, )
        # Create the labels list
        self._activate_txer_fhss_labels = ('Activate', )
        # Create the combo box
        # Create the radio buttons
        self._activate_txer_fhss_group_box = Qt.QGroupBox('activate_txer_fhss' + ": ")
        self._activate_txer_fhss_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._activate_txer_fhss_button_group = variable_chooser_button_group()
        self._activate_txer_fhss_group_box.setLayout(self._activate_txer_fhss_box)
        for i, _label in enumerate(self._activate_txer_fhss_labels):
            radio_button = Qt.QRadioButton(_label)
            self._activate_txer_fhss_box.addWidget(radio_button)
            self._activate_txer_fhss_button_group.addButton(radio_button, i)
        self._activate_txer_fhss_callback = lambda i: Qt.QMetaObject.invokeMethod(self._activate_txer_fhss_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._activate_txer_fhss_options.index(i)))
        self._activate_txer_fhss_callback(self.activate_txer_fhss)
        self._activate_txer_fhss_button_group.buttonClicked[int].connect(
            lambda i: self.set_activate_txer_fhss(self._activate_txer_fhss_options[i]))
        self.top_grid_layout.addWidget(self._activate_txer_fhss_group_box)
        def _variable_function_probe_0_probe():
          while True:

            val = self.epy_block_0_0.change_channel(activate_txer_fhss)
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_variable_function_probe_0,val))
              except AttributeError:
                self.set_variable_function_probe_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=1,
                taps=None,
                fractional_bw=None)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            5, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(5):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.DOUBLE, '1', 'Frequency', True, True, 'freq', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, [1], 0, samp_rate)
        self.epy_block_1 = epy_block_1.blk(example_param=2)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/seb/Documents/TestingFreqHop/hairdryer.wav', True)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(vol_lvl)
        self.blocks_complex_to_float_4 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_3 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_2 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_4 = blocks.add_const_cc(1.2)
        self.blocks_add_const_vxx_3 = blocks.add_const_cc(1.6)
        self.blocks_add_const_vxx_2 = blocks.add_const_cc(2)
        self.blocks_add_const_vxx_1 = blocks.add_const_cc(0.4)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(0.8)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*math.pi*(5e3)/samp_rate)
        self.SubbandFilterBank_0 = SubbandFilterBank()
        self._Freq_lvl_range = Range(-1.0e6, -500e3, 1000, -639e3, 200)
        self._Freq_lvl_win = RangeWidget(self._Freq_lvl_range, self.set_Freq_lvl, 'Freq_lvl', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Freq_lvl_win)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'freq'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))
        self.connect((self.SubbandFilterBank_0, 1), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.SubbandFilterBank_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.SubbandFilterBank_0, 4), (self.blocks_add_const_vxx_2, 0))
        self.connect((self.SubbandFilterBank_0, 3), (self.blocks_add_const_vxx_3, 0))
        self.connect((self.SubbandFilterBank_0, 2), (self.blocks_add_const_vxx_4, 0))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_complex_to_float_2, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_add_const_vxx_2, 0), (self.blocks_complex_to_float_3, 0))
        self.connect((self.blocks_add_const_vxx_3, 0), (self.blocks_complex_to_float_1, 0))
        self.connect((self.blocks_add_const_vxx_4, 0), (self.blocks_complex_to_float_4, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.epy_block_1, 3))
        self.connect((self.blocks_complex_to_float_2, 0), (self.epy_block_1, 1))
        self.connect((self.blocks_complex_to_float_3, 0), (self.epy_block_1, 4))
        self.connect((self.blocks_complex_to_float_4, 0), (self.epy_block_1, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.SubbandFilterBank_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.epy_block_1, 1), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.epy_block_1, 4), (self.qtgui_time_sink_x_1, 4))
        self.connect((self.epy_block_1, 2), (self.qtgui_time_sink_x_1, 2))
        self.connect((self.epy_block_1, 3), (self.qtgui_time_sink_x_1, 3))
        self.connect((self.epy_block_1, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Sense_And_Avoid")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_vol_lvl(self):
        return self.vol_lvl

    def set_vol_lvl(self, vol_lvl):
        self.vol_lvl = vol_lvl
        self.blocks_multiply_const_vxx_1_0.set_k(self.vol_lvl)

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*math.pi*(5e3)/self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_activate_txer_fhss(self):
        return self.activate_txer_fhss

    def set_activate_txer_fhss(self, activate_txer_fhss):
        self.activate_txer_fhss = activate_txer_fhss
        self._activate_txer_fhss_callback(self.activate_txer_fhss)

    def get_Freq_lvl(self):
        return self.Freq_lvl

    def set_Freq_lvl(self, Freq_lvl):
        self.Freq_lvl = Freq_lvl





def main(top_block_cls=Sense_And_Avoid, options=None):

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
