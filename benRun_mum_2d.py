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
    print "Call with ./benRun_mum_2d.py <x>"
    quit()

model_dir = "Zprime_MUM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = 6500.0 # LHC Run II
# 2d scan usually requires no particular accuracy
number_of_events = 1    
# mod of value of Wilson coefficient cbar_LL
x   = float(sys.argv[1])  

benRun.print_header(x, beam_energy, model_dir, number_of_events,
                    ' gmu       lg10(gsb)  ')

process = 'p p > zp > mu+ mu-'
for mzp in range(200, 6100, 100):
    for lg10_gsb in benRun.my_range(-3., -1., 0.2):
        gsb = math.exp(math.log(10) * lg10_gsb)
        gmu = -x / gsb * (mzp / 3.60000e+04)**2
        benRun.do_a_point(gmu, lg10_gsb, process, model_dir, mg5_path, number_of_events, beam_energy, mzp)


    
