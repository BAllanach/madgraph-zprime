#! /usr/bin/env python2
# Z' cross-section and BR calculations including off-shell effects
# by Ben Allanach
# The model file must be in the correct madgraph subdirectory models/
# This file should be in the bin/ subdirectory
# VERIFIED

import math
import sys
import benRun

# Test correct number of arguments used
if len(sys.argv) != 2 :
    print ('1 arguments required but only received %d' %
           len(sys.argv))
    print "Call with ./benRun_y3_2d.py <x>"
    quit()

model_dir = "Zprime_TFHM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = 6500.0 # LHC Run II
# 2d scan usually requires no particular accuracy
number_of_events = 1    
# mod of value of Wilson coefficient cbar_LL
x   = float(sys.argv[1])  

benRun.print_header(x, beam_energy, model_dir, number_of_events,
                    ' tsb            gzp   ')

process = 'p p > zp > mu+ mu-'
for mzp in range(200, 6100, 100):
    for tsb in benRun.my_range(0.02, 0.201, 0.02):
        gzp = mzp / 3.6e4 * math.sqrt(24.0 * x
                                      / math.sin(2.0 * tsb))
        benRun.do_a_point(tsb, gzp, process, model_dir, mg5_path,
                          number_of_events, beam_energy, mzp)


    
