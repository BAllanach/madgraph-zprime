#! /usr/bin/env python2
# Z' cross-section and BR calculations including off-shell effects
# by Ben Allanach
# The model file must be in the correct madgraph directory
# VERIFIED

import subprocess
import string
import os
import math
import sys
from shutil import copyfile

# user input: change for the run
process_folder = "zp_ty3"
model_dir = "Zprime_TTFHM_UFO"
mg5_path = "/home/bca20/code/MG5_aMC_v2_6_5/bin/"

if len(sys.argv) != 3 :
    print ('2 arguments required but only received %4.3e' % len(sys.argv))
    print "Call with ./benRun_ty3_0d.py mzp g_o_m"
    quit()

# Initial parameters
mzp = float(sys.argv[1])# should be divisible by 100
g_o_m = float(sys.argv[2]) # 0.22-031 is the 2 sigma range: gauge coupling x 1 TeV / MZ': free parameter
beam_energy = 6500.0    # LHC Run II
number_of_events = 1000    # 0d scan usually requires some accuracy
y = 1.06                # mod of value of Wilson coefficient cbar_LL
gzp = g_o_m * mzp / 1000
i   = int((mzp-300)/100)

run_card_name     = process_folder + '/Cards/run_card'
run_card_defname  = run_card_name + '_default.dat'
run_card_filename = run_card_name + '.dat'
new_run_card_name = run_card_name + '_temp.dat'
par_card_name     = process_folder + '/Cards/param_card'
par_card_defname  = par_card_name + '_default.dat'
par_card_filename = par_card_name + '.dat'
new_par_card_name = par_card_name + '_temp.dat'

# Header for output
print "#Note that factors for getting each intial state from the 2 protons are taken into account"
print "#gF/MZ'        gF     MZ'/GeV   wzp/GeV   sig/fb    siglim/fb br_mumu   br_tt     br_bb    siglim0.1/fb  process"

# Allows user to stop the run: type stop into "script.stop"
def check_stop_command(arg_stopcmd="stop") :
    stop_file =open("script.stop", 'r')
    for line in stop_file :
        if str.find(line,arg_stopcmd) >= 0 :
            print "stop found in script."
            exit(1)
        print "Stop command not found. Continuing... "
        stopFile.close()
        return

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

# ATLAS 139 fb^{-1} Run II 95% CLs upper limits on sigma x BR for a narrow resonance from 200 - 6000 in 100 GeV steps in MZ'
# Narrow width limit
sig_lim=[4.93777, 4.48931, 4.015, 2.074, 1.68132, 0.581599, 0.923837, 1.01589, 0.497384, 0.513057, 0.73726, 0.694133, 0.524801, 0.37448, 0.316075, 0.304548, 0.280589, 0.2419, 0.199536, 0.165452, 0.142668, 0.124836, 0.109533, 0.0991067, 0.0898019, 0.0833756, 0.0747212, 0.0691518, 0.0645587, 0.0612499, 0.057628, 0.0556406, 0.0536172, 0.0523249, 0.0511598, 0.0502525, 0.0493212, 0.0475899, 0.0468498, 0.048083, 0.0489626, 0.0489744, 0.0489538, 0.0492549, 0.0498723, 0.0499417, 0.0501216, 0.0510171, 0.0517414, 0.0530903, 0.0489538, 0.0528718, 0.0530553, 0.0541466, 0.0542299, 0.0575195, 0.0584476, 0.0570022]
# Gamma/MZ'=0.1 limit
sig_lim_0_1=[11.7203, 7.39879, 7.73113, 3.87269, 2.1168, 0.947254, 1.39581, 1.3413, 0.821517, 0.891762, 1.07272, 0.951112, 0.71826, 0.522448, 0.462264, 0.369815, 0.318178, 0.268564, 0.225904, 0.181796, 0.151381, 0.131879, 0.116186, 0.102308, 0.0923954, 0.0842573, 0.0769023, 0.0713618, 0.0666159, 0.0629116, 0.0599163, 0.057591, 0.056193, 0.0546622, 0.0529669, 0.0504863, 0.0504513, 0.0493567, 0.0492756, 0.0495705, 0.0506855, 0.0508562, 0.0520272, 0.0531361, 0.0523275, 0.0532316, 0.0545116, 0.0536775, 0.0541818, 0.0570729, 0.0567344, 0.0583914, 0.0584915, 0.0590304, 0.06, 0.0612396, 0.0619071, 0.0634932]
        
def output_line(col1, col2):
    print ('%4.3e ' % col1 + ' %4.3e' % col2 + ' %4.3e' % mzp + ' %4.3e' % wzp + ' %4.3e' % sbr + ' %4.3e' % sig_lim[i] + ' %4.3e' % br_mumu + ' %4.3e' % br_tt + ' %4.3e' % br_bb + ' %4.3e' % sig_lim_0_1[i] + ' # ' + process)

process_list = ['p p > zp > mu+ mu-', 'u u~ > zp > mu+ mu-', 'u c~ > zp > mu+ mu-', 'u~ c > zp > mu+ mu-','c c~ > zp > mu+ mu-', 'd d~ > zp > mu+ mu-', 'd s~ > zp > mu+ mu-', 'd~ s > zp > mu+ mu-', 'd b~ > zp > mu+ mu-', 'd~ b > zp > mu+ mu-', 's s~ > zp > mu+ mu-', 's b~ > zp > mu+ mu-', 's~ b > zp > mu+ mu-', 'b b~ > zp > mu+ mu-']
process_list=['p p > zp > mu+ mu-']
# number the cross-section should be multiplied by to get the p p initial state
# combinatorics right: each quark can come from either proton but (eg)
# s dbar is different from sbar d, since the d is valent and dbar is not
num_list = [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
count=0

for process in process_list:
    check_stop_command()
    # This sets up the process in the directory 
    cmds_y3="echo 'import model " + model_dir + "\ndefine p = u c d s b u~ c~ d~ s~ b~\ndefine maxjetflavor=5\ndefine aswgtflavor=5\ngenerate " + process + "\noutput " + process_folder + "\ny\nquit()' | " + mg5_path + "/mg5_aMC"
    output = subprocess.check_output(cmds_y3, shell=True)
    # Modify run card first
    copyfile(run_card_defname, run_card_filename)
    run_card_file = open(run_card_filename,'r')
    new_run_card_file = file(new_run_card_name,'w')
    # Modify the run card to generate number_of_events events
    for line in run_card_file.readlines():
        if str.find(line, "= nevents ! Number of unweighted events requested") >= 0:
	    new_run_card_file.write("  " + str(number_of_events) + ' = nevents ! Number of unweighted events requested\n')
        elif str.find(line, "= ebeam1  ! beam 1 total energy in GeV") >= 0:
	    new_run_card_file.write("  " + str(beam_energy) + '= ebeam1  ! beam 1 total energy in GeV\n')
        elif str.find(line, "= ebeam2  ! beam 2 total energy in GeV") >= 0:
	    new_run_card_file.write("  " + str(beam_energy) + '= ebeam2  ! beam 2 total energy in GeV\n')
        else:
            new_run_card_file.write(line)
    run_card_file.close()
    new_run_card_file.close()
    os.rename(new_run_card_name, run_card_filename)
    # Modify par_card
    copyfile(par_card_defname, par_card_filename)        
    par_card_file = open(par_card_filename,'r')
    new_par_card_file = file(new_par_card_name,'w')
    for line in par_card_file.readlines():
        if str.find(line, "# MZp") >= 0:
	    new_par_card_file.write("   32 " + str(mzp) + ' # MZp\n')
        elif str.find(line, "# mzp") >= 0:
	    new_par_card_file.write("   32 " + str(mzp) + ' # MZp\n')
        elif str.find(line, "# gzp") >= 0:
	    new_par_card_file.write("    1 " + str(gzp) + ' # gzp\n')
        elif str.find(line, "# tsb") >= 0:
	    new_par_card_file.write("    1 " + str(tsb) + ' # tsb\n')
            # Necessary to get madgraph to calculate the width:
        elif str.find(line, "DECAY  32 ") >= 0:
	    new_par_card_file.write("DECAY  32 Auto # WZp: calculate automatically\n")
            # Necessary for 5 flavour PDF scheme:
        elif str.find(line, "# ymb") >= 0:
	    new_par_card_file.write("      5 0.000000e+00 # ymb\n")
        elif str.find(line, "# MB") >= 0:
	    new_par_card_file.write("      5 0.000000e+00 # mb\n")
        else:
	    new_par_card_file.write(line)
    par_card_file.close()
    new_par_card_file.close()
    os.rename(new_par_card_name, par_card_filename)
    # Run madgraph
    s_cmd = "echo 'launch '" + process_folder + "'\n\n\nquit()' | " + mg5_path + "/mg5_aMC | grep 'Cross-section' | gawk ' { print $3 }'"
    crossSec = subprocess.check_output(s_cmd, shell=True).rstrip()
    if crossSec == "":
        crossSec = 0.
    sbr = float(crossSec) * 1000 * num_list[count]
    # Extract additional data from parameter cards etc
    wzp_cmd = "cat " + str(par_card_filename) + " | grep 'DECAY  32' | gawk ' { print $3 } '"
    wzp = subprocess.check_output(wzp_cmd, shell=True).rstrip()
    if wzp == "":
        wzp = 0.
    wzp = float(wzp)
    br_mumu_cmd = "cat " + str(par_card_filename) + " | grep '   2    13  -13' | gawk ' { print $1 } '"
    br_mumu = subprocess.check_output(br_mumu_cmd, shell=True).rstrip()
    if br_mumu == "":
        br_mumu=0.
    br_mumu = float(br_mumu)
    br_tt_cmd = "cat " + str(par_card_filename) + " | grep '   2    6  -6 #' | gawk ' { print $1 } '"
    br_tt = subprocess.check_output(br_tt_cmd, shell=True).rstrip()
    if br_tt == "":
        br_tt=0.
    br_tt = float(br_tt)
    br_bb_cmd = "cat " + str(par_card_filename) + " | grep '   2    5  -5 #' | gawk ' { print $1 } '"
    br_bb = subprocess.check_output(br_bb_cmd, shell=True).rstrip()
    if br_bb == "":
        br_bb=0.
    br_bb = float(br_bb)
    output_line(g_o_m, gzp)
    count = count + 1



