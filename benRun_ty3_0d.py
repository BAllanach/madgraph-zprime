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
if len(sys.argv) != 3 :
    print ('2 arguments needed but only received ' + str(len(sys.argv)-1))
    print "Call with ./benRun_ty3_0d.py <mzp> <g_o_m>"
    quit()

mzp = float(sys.argv[1]) # should be divisible by 100
g_o_m = float(sys.argv[2]) # 0.22-031 is the 2 sigma range: gauge coupling x 1 TeV / MZ': free parameter
gzp = g_o_m * mzp / 1000.

model_dir = "Zprime_TTFHM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = 6500.0 # LHC Run II
# 0d scan usually requires decent precision
number_of_events = 1000    
# mod of value of Wilson coefficient cbar_LL: default
x   = 1.06

benRun.print_header(x, beam_energy, model_dir, number_of_events,
                    ' g/M            gzp   ')

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
for process in process_list:
    benRun.do_a_point(g_o_m, gzp, process, model_dir, mg5_path, number_of_events, beam_energy, mzp)


    
