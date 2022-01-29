"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_out(pmt.intern("freq"))
        self.centerFreq = 0.0
        self.channel = 0

    def work(self, activate_txer_fhss):
        self.channel = (self.channel + 3)%8
        if not activate_txer_fhss:
            P_freq_cmd = pmt.cons(pmt.string_to_symbol("freq"), pmt.from_double(0))
            self.message_port_pub(pmt.intern("freq"), output_items)
            return
        freq = self.channel * -200e3
        output_items = pmt.cons(pmt.string_to_symbol("freq"), pmt.from_double(freq))
        self.message_port_pub(pmt.intern("freq"), output_items)
        return output_items

    def change_channel(self, activate_txer_fhss):
        self.channel = (self.channel + 1)%5
        if not activate_txer_fhss:
            P_freq_cmd = pmt.cons(pmt.string_to_symbol("freq"), pmt.from_double(0))
            self.message_port_pub(pmt.intern("freq"), P_freq_cmd)
            print("hello")
            print(activate_txer_fhss)
            return
        else:
            print("changing to subband " + str(self.channel))
            freq = (self.channel * -200e3) + self.centerFreq
            P_freq_cmd = pmt.cons(pmt.string_to_symbol("freq"), pmt.from_double(freq))
            self.message_port_pub(pmt.intern("freq"), P_freq_cmd)
            return 1


