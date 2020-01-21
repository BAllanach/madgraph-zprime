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
    print "Call with ./benRun_mdm_2d.py <x>"
    quit()

model_dir = "Zprime_MDM_UFO"
mg5_path = "../"

# Initial parameters
beam_energy = 6500.0 # LHC Run II
# 2d scan usually requires no particular accuracy
number_of_events = 1    
# mod of value of Wilson coefficient cbar_LL
x   = float(sys.argv[1])  

# Header for output
print ('# x=%5.3e' % x + ' beam_energy=%5.3e' % beam_energy + ' model=' + model_dir + ' number_of_events=%d' % number_of_events)
print "# gmu       lg10(gtt)  MZ'/GeV   wzp/GeV   sig/fb    siglim0/fb br_mumu   br_tt     br_bb    siglim0.1/fb  process"

process = 'p p > zp > mu+ mu-'
for mzp in range(200, 6100, 100):
    for lg10_gtt in benRun.my_range(-3, 0, 0.2):
        gtt = math.exp(math.log(10) * lg10_gtt)
        gmu = x * 25 / gtt * (mzp / 3.60000e+04)**2
        benRun.do_a_point(gmu, lg10_gtt, process, model_dir, mg5_path, number_of_events, beam_energy, mzp)


    
