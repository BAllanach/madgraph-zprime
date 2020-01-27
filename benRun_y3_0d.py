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
if len(sys.argv) != 6 :
    print ('5 arguments required but received %d' %
           len(sys.argv)-1)
    print "Call with ./benRun_y3_0d.py <MZ'> <tsb> <beam_energy> <x> '<process>/default'"
    quit()

mzp = float(sys.argv[1]) # should be divisible by 100
tsb = float(sys.argv[2]) # theta_sb: 0-0.2 is a range that fits

model_dir = "Zprime_TFHM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = float(sys.argv[3]) # LHC Run II
# 0d scan usually requires decent precision
number_of_events = 1000    
# mod of value of Wilson coefficient cbar_LL: default
x   = float(sys.argv[4])
process = sys.argv[5]
if process == "default":
    process_list = ['p p > zp > mu+ mu-',
                'u u~ > zp > mu+ mu-',
                'u c~ > zp > mu+ mu-',
                'u~ c > zp > mu+ mu-',
                'c c~ > zp > mu+ mu-',
                'd d~ > zp > mu+ mu-',
                'd s~ > zp > mu+ mu-',
                'd~ s > zp > mu+ mu-',
                'd b~ > zp > mu+ mu-',
                'd~ b > zp > mu+ mu-',
                's s~ > zp > mu+ mu-',
                's b~ > zp > mu+ mu-',
                's~ b > zp > mu+ mu-',
                'b b~ > zp > mu+ mu-']
else:
    process_list = [ process ]

benRun.print_header(x, beam_energy, model_dir, number_of_events,
                    ' tsb            gzp   ')

for process in process_list:
    gzp = mzp / 3.6e4 * math.sqrt(24.0 * x / math.sin(2.0 * tsb))    
    benRun.do_a_point(tsb, gzp, process, model_dir, mg5_path, number_of_events, beam_energy, mzp)


    
