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
    print ('2 arguments required but only received %d' %
           len(sys.argv))
    print "Call with ./benRun_mdm_0d.py <MZ'> <gsb>"
    quit()

mzp = float(sys.argv[1])
gsb = float(sys.argv[2])
if (gsb > 0.):
    print ('gsb=%5.3e' % gsb + ' should be less than zero')
    quit()
    
model_dir = "Zprime_MDM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = 6500.0 # LHC Run II
# 0d scan usually requires decent precision
number_of_events = 1000    
# mod of value of Wilson coefficient cbar_LL: default
x   = 1.06

benRun.print_header(x, beam_energy, model_dir, number_of_events,
                    ' gmu       lg10(gtt)  ')

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
    gmu = -(mzp / 3.6e4)**2 * x / gsb
    gtt = -gsb * 25.0
    lg10_gtt = math.log(gtt) / math.log(10.)
    benRun.do_a_point(gmu, lg10_gtt, process, model_dir, mg5_path, number_of_events, beam_energy, mzp)


    
