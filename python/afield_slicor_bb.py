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

AFIELD_LENGTH = 64

class afield_slicor_bb(gr.basic_block):
    """
    docstring for block afield_slicor_bb
    """
    def __init__(self, tag_name="sauerkraut", chan_idx=None):
        gr.basic_block.__init__(self,
            name="afield_slicor_bb",
            in_sig=[numpy.uint8,],
            out_sig=[(numpy.uint8, AFIELD_LENGTH)]
        )
        self.tag = pmt.to_pmt(tag_name)
        self.set_tag_propagation_policy(gr.TPP_DONT)
        self.last_burst = 0
        self.chan_idx = chan_idx

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        tags = self.get_tags_in_window(0, 0, len(input_items[0]), self.tag)
        tags = sorted(tags, reverse=True)
        n_bursts_written = 0
        n_consumed = 0
        for tag in tags:
            rel_offset = tag.offset - self.nitems_read(0)
            if rel_offset + AFIELD_LENGTH > len(input_items[0]):
                self.consume_each(rel_offset)
                return n_bursts_written
            else:
                output_items[0][n_bursts_written][:] = input_items[0][rel_offset:rel_offset+AFIELD_LENGTH]
                print "Chan %d" % self.chan_idx,
                print "%010d %05d " % (tag.offset, tag.offset - self.last_burst),
                self.last_burst = tag.offset
                print "".join(map(str, output_items[0][n_bursts_written]))
                n_bursts_written += 1
        self.consume_each(len(input_items[0]))
        return n_bursts_written

