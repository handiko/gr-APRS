"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import os, pty
import struct

import pmt
import numpy as np
from gnuradio import gr

import packet


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """
    Converts an array of bytes into a AX25Packet object.

    Connect to the "HDLC Deframer", or a block which emits a PMT tuple of
    (None, bytearray)
    """
    def __init__(self):
        gr.sync_block.__init__(self,
                               name="HDLC to AX.25",
                               in_sig=None,
                               out_sig=None)
        self.message_port_register_in(pmt.intern('hdlc in'))
        self.message_port_register_out(pmt.intern('ax25 out'))
        self.set_msg_handler(pmt.intern('hdlc in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg_pmt = pmt.pmt_to_python.pmt_to_python(msg_pmt)

        msg = bytearray(msg_pmt[1])

        try:
            pkt = packet.from_bytes(msg)
            self.message_port_pub(pmt.intern('ax25 out'), pmt.cons(pmt.make_dict(), pmt.pmt_to_python.numpy_to_uvector(np.array([ord(c) for c in (packet.dump(pkt) + '\n')], np.uint8))))
                
        except ValueError as e:
            print e

    def stop(self):
        gr.sync_block.stop(self)
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        return len(input_items[0])
        
        
        
