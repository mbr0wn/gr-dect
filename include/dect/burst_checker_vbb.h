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


#ifndef INCLUDED_DECT_BURST_CHECKER_VBB_H
#define INCLUDED_DECT_BURST_CHECKER_VBB_H

#include <dect/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace dect {

    /*!
     * \brief <+description of block+>
     * \ingroup dect
     *
     */
    class DECT_API burst_checker_vbb : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<burst_checker_vbb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of dect::burst_checker_vbb.
       *
       * To avoid accidental use of raw pointers, dect::burst_checker_vbb's
       * constructor is in a private implementation
       * class. dect::burst_checker_vbb::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace dect
} // namespace gr

#endif /* INCLUDED_DECT_BURST_CHECKER_VBB_H */

