/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "burst_checker_vbb_impl.h"

namespace gr {
  namespace dect {

    burst_checker_vbb::sptr
    burst_checker_vbb::make()
    {
      return gnuradio::get_initial_sptr
        (new burst_checker_vbb_impl());
    }

    /*
     * The private constructor
     */
    burst_checker_vbb_impl::burst_checker_vbb_impl()
      : gr::sync_block("burst_checker_vbb",
              gr::io_signature::make(1, 1, sizeof(char) * 8),
              gr::io_signature::make(1, 1, sizeof(char) * 8))
    {}

    /*
     * Our virtual destructor.
     */
    burst_checker_vbb_impl::~burst_checker_vbb_impl()
    {
    }

    int
    burst_checker_vbb_impl::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        unsigned char *out = (unsigned char *) output_items[0];

        memcpy(out, in, noutput_items * 8);

        for (int i = 0; i < noutput_items; i++) {
          d_crc_impl.reset();
          d_crc_impl.process_bytes(in, 6);
          unsigned int crc = d_crc_impl();
          const unsigned int in_crc = in[7] | (in[6] << 8);
          std::cout << boost::format("[%s] calc:  0x%04X  in: 0x%02X%02X 0x%04x") % (crc == in_crc ? " OK " : "FAIL") % crc % int(in[6]) % int(in[7]) % in_crc << std::endl;
          in += 8;
          out += 8;
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace dect */
} /* namespace gr */

