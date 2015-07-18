#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 National Instruments Corp. All rights reserved.
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

import os
import numpy
import struct
import errno
import sys
import datetime
import pmt
import time
from gnuradio import gr

ETH_HDR_LEN = 14
ETH_CKSUM_LEN = 2

class pipe_sink(gr.basic_block):
    """
    This block takes PDUs and writes them to a named pipe.
    """
    def __init__(self, fifo, enc_type=1):
        gr.basic_block.__init__(self,
            name="pipe_sink",
            in_sig=None,
            out_sig=None,
        )

        try:
            self.fifo = os.mkfifo(fifo)
        except OSError:
            self.fifo = open(fifo, 'wb')
        self.write_header()

        self.message_port_register_in(pmt.intern('burst'))
        self.set_msg_handler(pmt.intern('burst'), self.handle_msg)
    def __del__(self):
        self.fifo.close()

    def write_header(self):
        self.fifo.write(struct.pack("=IHHiIII",
            0xa1b2c3d4,   # magic number
            2,            # major version number
            4,            # minor version number
            0,            # GMT to local correction
            0,            # accuracy of timestamps
            65535,        # max length of captured packets, in octets
            1,          # data link type (DLT) - IEEE 802.15.4
        ))
        self.fifo.flush()

    def write_packet(self, data):
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple()))
        self.fifo.write(struct.pack("=IIII",
            timestamp,        # timestamp seconds
            now.microsecond,  # timestamp microseconds
            ETH_HDR_LEN + len(data) + ETH_CKSUM_LEN,        # number of octets of packet saved in file
            ETH_HDR_LEN + len(data) + ETH_CKSUM_LEN,        # actual length of packet
        ))
        self.fifo.write(
           struct.pack('=B11xH', 0, 0x2323) + data + struct.pack('=H', 0)
        )
        self.fifo.flush()

    def handle_msg(self, msg_pmt):
        meta = pmt.to_python(pmt.car(msg_pmt))
        msg = pmt.cdr(msg_pmt)
        #TODO: Fix this ... hack hack hack
        bin_str = int("".join(map(lambda x: '1' if x else '0', pmt.u8vector_elements(msg))), 2)
        data = struct.pack('xB7xBB', meta['chan'], 0xe9, 0x8a)
        data += bytearray.fromhex(hex(bin_str)[2:-1])
        self.write_packet(data)
