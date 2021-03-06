#! /usr/bin/env python2
#Useful functions for calling madgraph a la Ben Allanach

import subprocess
import os
import math
import sys
from shutil import copyfile

# Allows user to stop the run: type stop into "script.stop"
def check_stop_command(arg_stopcmd="stop") :
    stop_file = open("script.stop", 'r')
    for line in stop_file :
        if str.find(line,arg_stopcmd) >= 0 :
            print "stop found in script."
            exit(1)
        stop_file.close()
        return

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    return

def output_line(col1, col2, mzp, wzp, sbr, br_mumu, br_tt, br_bb, br_tautau, process):
    i = int((mzp - 200) / 100)
    # ATLAS 139 fb^{-1} Run II 95% CLs upper limits on sigma x BR for a narrow resonance from 200 - 6000 in 100 GeV steps in MZ'
    # Narrow width limit
    SIG_LIM=[4.93777, 4.48931, 4.015, 2.074, 1.68132, 0.581599,
             0.923837, 1.01589, 0.497384, 0.513057, 0.73726,
             0.694133, 0.524801, 0.37448, 0.316075, 0.304548,
             0.280589, 0.2419, 0.199536, 0.165452, 0.142668,
             0.124836, 0.109533, 0.0991067, 0.0898019, 0.0833756,
             0.0747212, 0.0691518, 0.0645587, 0.0612499, 0.057628,
             0.0556406, 0.0536172, 0.0523249, 0.0511598,
             0.0502525, 0.0493212, 0.0475899, 0.0468498,
             0.048083, 0.0489626, 0.0489744, 0.0489538,
             0.0492549, 0.0498723, 0.0499417, 0.0501216,
             0.0510171, 0.0517414, 0.0530903, 0.0489538,
             0.0528718, 0.0530553, 0.0541466, 0.0542299,
             0.0575195, 0.0584476, 0.0570022]
    # Gamma/MZ'=0.1 limit
    SIG_LIM_0_1=[11.7203, 7.39879, 7.73113, 3.87269, 2.1168,
                 0.947254, 1.39581, 1.3413, 0.821517, 0.891762,
                 1.07272, 0.951112, 0.71826, 0.522448, 0.462264,
                 0.369815, 0.318178, 0.268564, 0.225904, 0.181796,
                 0.151381, 0.131879, 0.116186, 0.102308,
                 0.0923954, 0.0842573, 0.0769023, 0.0713618,
                 0.0666159, 0.0629116, 0.0599163, 0.057591,
                 0.056193, 0.0546622, 0.0529669, 0.0504863,
                 0.0504513, 0.0493567, 0.0492756, 0.0495705,
                 0.0506855, 0.0508562, 0.0520272, 0.0531361,
                 0.0523275, 0.0532316, 0.0545116, 0.0536775,
                 0.0541818, 0.0570729, 0.0567344, 0.0583914,
                 0.0584915, 0.0590304, 0.06, 0.0612396,
                 0.0619071, 0.0634932]
    print ('%4.3e ' % col1 + ' %4.3e' % col2 + ' %4.3e' % mzp + ' %4.3e' % wzp + ' %4.3e' % sbr + ' %4.3e' % SIG_LIM[i] + ' %4.3e' % br_mumu + ' %4.3e' % br_tt + ' %4.3e' % br_bb + ' %4.3e' % SIG_LIM_0_1[i] + ' %4.3e' % br_tautau + ' # ' + process)
    return
    
# Header for output    
def print_header(x, beam_energy, model_dir, number_of_events,
                 header_col12):
    print ('# x=%5.3e' % x + ' beam_energy=%5.3e' % beam_energy + ' model=' + model_dir + ' number_of_events=%d' % number_of_events)
    print ("# " + header_col12 + "MZ'/GeV   wzp/GeV   sig/fb    siglim0/fb br_mumu   br_tt     br_bb    siglim0.1/fb  br_tautau  process")
    return
    
def my_output(a_string):
    if a_string == "":
        answer = 0.
    else:
        answer = float(a_string)
    return answer;

# Change run card with the options that you want
def change_run_card(process_folder, number_of_events, beam_energy):
    run_card_name     = process_folder + '/Cards/run_card'
    run_card_defname  = run_card_name + '_default.dat'
    run_card_filename = run_card_name + '.dat'
    new_run_card_name = run_card_name + '_temp.dat'
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
        elif str.find(line, "False  = cut_decays") >= 0:
            new_run_card_file.write("    True  = cut_decays    ! Cut decay products\n")
# following tests if we are applying cuts in practice            
        elif str.find(line, " = ptl ") >=0:
            new_run_card_file.write("   30.0  = ptl       ! minimum pt for the charged leptons\n")
        else:
            new_run_card_file.write(line)
    run_card_file.close()
    new_run_card_file.close()
    os.rename(new_run_card_name, run_card_filename)
    return
    
def change_par_card(process_folder, mzp, gzp, tsb, gsb, gmu, gtt):
    par_card_name     = process_folder + '/Cards/param_card'
    par_card_defname  = par_card_name + '_default.dat'
    par_card_filename = par_card_name + '.dat'
    new_par_card_name = par_card_name + '_temp.dat'
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
        elif str.find(line, "# gbs") >= 0:
	    new_par_card_file.write("    2 " + str(gsb) + ' # gsb\n')
        elif str.find(line, "# gmu") >= 0:
	    new_par_card_file.write("    1 " + str(gmu) + ' # gmu\n')
	elif str.find(line, "# gtt") >= 0:
	    new_par_card_file.write("    2 " + str(gtt) + ' # gtt\n')
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
    return
    
# INPUTS: process_folder
# OUTPUT: wzp - width of Z'
#     br_mumu - BR(Z' -> mu+ mu-)
#     br_tt   - BR(Z' -> t tbar )
#     br_bb   - BR(Z' -> b bbar )
def get_decays(process_folder):
    par_card_filename = process_folder + "/Cards/param_card.dat"
    wzp_cmd = "cat " + str(par_card_filename)
    wzp_cmd += " | grep 'DECAY  32' | gawk ' { print $3 } '"
    wzp = my_output(subprocess.check_output
                    (wzp_cmd, shell=True).rstrip())
    br_mumu_cmd = "cat " + str(par_card_filename) + " | grep "
    br_mumu_cmd += "'   2    13  -13' | gawk ' { print $1 } '"
    br_mumu = my_output(subprocess.check_output
                        (br_mumu_cmd, shell=True).rstrip())
    br_tt_cmd = "cat " + str(par_card_filename) + " | grep "
    br_tt_cmd += "'   2    6  -6 #' | gawk ' { print $1 } '"
    br_tt = my_output(subprocess.check_output
                      (br_tt_cmd, shell=True).rstrip())
    br_bb_cmd = "cat " + str(par_card_filename) + " | grep "
    br_bb_cmd += "'   2    5  -5 #' | gawk ' { print $1 } '"
    br_bb = my_output(subprocess.check_output
                      (br_bb_cmd, shell=True).rstrip())
    br_tautau_cmd = "cat " + str(par_card_filename) + " | grep "
    br_tautau_cmd += "'   2    15  -15' | gawk ' { print $1 } '"
    br_tautau = my_output(subprocess.check_output
                        (br_tautau_cmd, shell=True).rstrip())
    return (wzp, br_mumu, br_tt, br_bb, br_tautau)
    
# col1 and col2 are the independent arguments for the scan
# process is the madgraph process cross-section
# model_dir is the UFO model directory name
# mg5_path is the directory path to the executable from this dir
# number_of_events is the number to simulate
def do_a_point(col1, col2, process, model_dir, mg5_path,
               number_of_events, beam_energy, mzp):
    if (int(mzp) % 100 != 0 or mzp < 200 or mzp > 6000):
        print (mzp + ' not appropriate for benRun.do_a_point:')
        print ('must be divisible by 100 and 200-6000 for ATLAS')
        quit()
    factor = 1
    # For non-identical final states, we multiply by 2 to taken into
    # account the fact that the anti-quark could come from either proton
    if (process == "p p > zp > mu+ mu-" or
        process == "p p > zp, zp > mu+ mu-" or
        process == "p p > zp > t t~" or
        process == "p p > zp > tau+ tau-" or
        process == "p p > zp > b b~"):
        factor = 1
    elif (process == 'u u~ > zp > mu+ mu-'
          or process == 'u c~ > zp > mu+ mu-'
          or process == 'u~ c > zp > mu+ mu-'
          or process == 'c c~ > zp > mu+ mu-'
          or process == 'd d~ > zp > mu+ mu-'
          or process == 'd s~ > zp > mu+ mu-'
          or process == 'd~ s > zp > mu+ mu-'
          or process == 'd b~ > zp > mu+ mu-'
          or process == 'd~ b > zp > mu+ mu-'
          or process == 's s~ > zp > mu+ mu-'
          or process == 's b~ > zp > mu+ mu-'
          or process == 's~ b > zp > mu+ mu-'
          or process == 'b b~ > zp > mu+ mu-'):
        factor = 2
    else:
        print "In benRun.py: process=" + process + " is not in list"
        quit()
    # set initial variables to zero
    gzp = 0; tsb = 0; gsb = 0; gmu = 0; gtt = 0
    # need to set couplings depending on model_dir
    if model_dir == "Zprime_MDM_UFO":
        gmu = col1
        lg10_gtt = col2
        gtt = math.exp(math.log(10) * lg10_gtt)
    elif model_dir == "Zprime_MUM_UFO":
        gmu = col1
        lg10_gsb = col2
        gsb = math.exp(math.log(10) * lg10_gsb)
    elif model_dir == "Zprime_TFHM_UFO":
        tsb = col1
        gzp = col2
    elif model_dir == "Zprime_TTFHM_UFO":
        g_o_m = col1
        gzp   = col2
    else:
        print ('model_dir=' + model_dir +
               ' not one of options in benRun.py')
        quit()
    process_folder = "zp_out"
    check_stop_command()
    # This sets up the process in the directory 
    cmds_y3 = "echo 'import model " + model_dir + "\n" + "define p = u c d s b u~ c~ d~ s~ b~\n" + "define maxjetflavor=5\n" + "define aswgtflavor=5\ngenerate " + process + "\n" + "output " + process_folder + "\n" + "y\n" + "quit()' | " + mg5_path + "/mg5_aMC"
    output = subprocess.check_output(cmds_y3, shell=True)
    change_run_card(process_folder, number_of_events, beam_energy)
    change_par_card(process_folder, mzp, gzp, tsb, gsb, gmu, gtt);
    # Run madgraph
    s_cmd = "echo 'launch " + process_folder + "\n\n\n" + "quit()' | " + mg5_path + "/mg5_aMC" + " | gawk '/Cross-section/{ print $3 }'"
    crossSec = my_output(subprocess.check_output
                         (s_cmd, shell=True).rstrip())
    sbr = crossSec * 1000. # default is in pb but we want fb
    sbr *= factor
    (wzp, br_mumu, br_tt, br_bb, br_tautau) = get_decays(process_folder)
    output_line(col1, col2, mzp, wzp, sbr, br_mumu, br_tt,
                br_bb, br_tautau, process)
    return


