#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
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
import pmt
from gnuradio import gr

class burst_slicor_bb(gr.sync_block):
    """
    foooooooooooo
    """
    def __init__(self, tag_name="sauerkraut", chan_idx=None, burst_length_bits=480):
        gr.sync_block.__init__(self,
            name="burst_slicor_bb",
            in_sig=[numpy.uint8,],
            out_sig=None,
        )
        self.tag = pmt.to_pmt(tag_name)
        self.set_tag_propagation_policy(gr.TPP_DONT)
        self.last_burst = 0
        self.chan_idx = chan_idx
        self.burst_length_bits = burst_length_bits
        self.message_port_register_out(pmt.intern('burst'))

    def work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]), self.tag)
        tags = sorted(tags, reverse=True)
        for tag in tags:
            rel_offset = tag.offset - self.nitems_read(0)
            if rel_offset + self.burst_length_bits > len(input_items[0]):
                return rel_offset
            else:
                pdu = pmt.cons(
                        pmt.to_pmt({'chan': self.chan_idx}),
                        pmt.to_pmt(input_items[0][rel_offset:rel_offset+self.burst_length_bits])
                )
                self.message_port_pub(
                        pmt.intern('burst'),
                        pdu
                )
        return len(input_items[0])

