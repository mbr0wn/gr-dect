/* -*- c++ -*- */

#define DECT_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "dect_swig_doc.i"

%{
#include "dect/burst_checker_vbb.h"
%}


%include "dect/burst_checker_vbb.h"
GR_SWIG_BLOCK_MAGIC2(dect, burst_checker_vbb);
