from __future__ import division
from plot_upper_limits_lib import *
import scipy.io as sio
import os
import json
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['legend.numpoints'] = 1

save_plots = True#True
print_limit_detail = True#False
background_version = True

trigger_number = 2475

psi_test = False#False#True#False

second_plot_version = True

background_based_upper_limits = True

show_bayesian_average = False#True

alternate_polarization = True#False#True#True#False#True # edge-on polarization version
polarized_version = False#True#False#True#False#True  # polarization variation version
polarized_separate = False#True
polarized_test = False#True

if psi_test:
    alternate_polarization = False
    polarized_version = True

plot_mode = "shaded"#"plain"#"errorbar"#"shaded"
show_legend = False# controls if legend is shown if 'plot_mode' is set to 'plain'

additional_plots = True#True#False

x_Limits = True#True#False

pretty_version = True

reloadJSONs = False#True#False

lockPlot = True#False

check_mat_files_onsource = False#False#True

abs_version = True#False#True#False

plot_interpolated_points = False#True#False

if alternate_polarization:
    x_Limits = False
    #plot_interpolated_points = True

outputPath = "/home/quitzow/public_html/Magnetar/upper_limits/"

if trigger_number == 2469:
    if not background_based_upper_limits:
        # for upper limits based on open box
        if alternate_polarization:
            thresholdSNRs = [6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253]
        else:
            thresholdSNRs = [5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466]
    else:
        # for upper limits based on background only
        if alternate_polarization:
            thresholdSNRs = [7.60930175591, 7.60930175591, 7.60930175591, 7.60930175591, 7.60930175591, 7.60930175591]
        else:
            thresholdSNRs = [7.53977755475, 7.53977755475, 7.53977755475, 7.53977755475, 7.53977755475, 7.53977755475]
    #thresholdSNRs = [5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466, 5.73448522466]
    #x_Limits = False
    if psi_test:
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_variation/stamp_analysis_anteproc-2017_1_7']]
        name_tag = "sgr_trigger_2469_variable_polarization_psi_test"
        if abs_version:
            name_tag += "_abs"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2469/plot/polarization_variation/psi_test")
        x_Limits = False
    elif polarized_version:
        if not second_plot_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/polarization_overview/stamp_analysis_anteproc-2015_12_3'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/polarization_overview/stamp_analysis_anteproc-2016_1_3']]#"""
        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/polarization_overview/stamp_analysis_anteproc-2015_12_3'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_variation_imaginary/stamp_analysis_anteproc-2017_1_3_v2']]#"""

        name_tag = "sgr_trigger_2469_variable_polarization"
        if abs_version:
            name_tag += "_abs"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2469/polarization_overview")
        #x_Limits = False
    elif alternate_polarization:
        #thresholdSNRs = [6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253, 6.06371569253]
        if second_plot_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4_v3',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_5',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_5_v2'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_4_v3',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_5',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_5_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_7']]
        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_13',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_13_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_11',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_12_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_12_v3',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_3_10/'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_13',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_13_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_12',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_12_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_12_v3',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_9_15']]

        name_tag = "sgr_trigger_2469_alternate_polarization"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2469/plot/alternate_polarization/")
        #xLimits = [7e-23, 6e-22]#[9e-23, 6e-22]#[1e-22, 3e-21]#4e-21]#[6e-23, 1e-21]
    else:
        baseDirs = [["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/background/stamp_analysis_anteproc-2016_11_29", "/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_400/background/stamp_analysis_anteproc-2016_11_29_v2"],
                ["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_450/tau_400/background/stamp_analysis_anteproc-2016_12_3"],
                ["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_400/background/stamp_analysis_anteproc-2016_12_4"],
                ["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_150/tau_150/background/stamp_analysis_anteproc-2016_12_7"],
                ["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_450/tau_150/background/stamp_analysis_anteproc-2016_12_7"],
                 ["/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2469/f0_750/tau_150/background/stamp_analysis_anteproc-2016_12_7"]]

        name_tag = "sgr_trigger_2469_testing_focus_40"
        outputPath += "sgr_trigger_2469/plot/"
        xLimits = [6e-23, 1e-21]

elif trigger_number == 2471:
    if not background_based_upper_limits:
        # for upper limits based on open box
        thresholdSNRs = [5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767]
    else:
        # for upper limits based on background only
        thresholdSNRs = [7.21733013944, 7.21733013944, 7.21733013944, 7.21733013944, 7.21733013944, 7.21733013944]
    if psi_test:
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_variation/stamp_analysis_anteproc-2017_1_7']]
        name_tag = "sgr_trigger_2471_variable_polarization_psi_test"
        if abs_version:
            name_tag += "_abs"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2471/plot/polarization_variation/psi_test")
        x_Limits = False
    elif polarized_version:
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/stamp_analysis_anteproc-2015_10_19'],
                    ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/stamp_analysis_anteproc-2015_10_19_v2']]#"""
        name_tag = "sgr_trigger_2471_variable_polarization_plus"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2471/plot/polarization_variation")
        x_Limits = False
    elif alternate_polarization:
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2015_12_1',
                     '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_31',
                     '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_1',
                     '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_1_v2',
                     '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_5_27'],
                    ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_1',
                     '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_2_11']]

        name_tag = "sgr_trigger_2471_alternate_polarization"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2471/plot/alternate_polarization/")#"""
    else:
        if not background_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_6', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_6_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_6_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_6_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_8', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_8_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/stamp_analysis_anteproc-2015_11_8_v3'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_11_8', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_11_8_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_11_8_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2015_11_8_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/stamp_analysis_anteproc-2016_5_12'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/stamp_analysis_anteproc-2015_11_8_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/stamp_analysis_anteproc-2015_11_9', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/stamp_analysis_anteproc-2015_11_9_v2'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/stamp_analysis_anteproc-2015_10_18_v5', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_150/stamp_analysis_anteproc-2015_11_6', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_150/stamp_analysis_anteproc-2015_11_6_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_150/stamp_analysis_anteproc-2015_11_6_v3','/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_150/stamp_analysis_anteproc-2016_5_27'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/stamp_analysis_anteproc-2015_11_8', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/stamp_analysis_anteproc-2015_11_8_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/stamp_analysis_anteproc-2015_11_8_v3'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_11_9', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_11_9_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_11_9_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_11_9_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/stamp_analysis_anteproc-2015_11_9_v5']]#"""

        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_400/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_400/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/background/stamp_analysis_anteproc-2016_12_15', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_400/background/stamp_analysis_anteproc-2016_12_15_v2'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_150/tau_150/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_450/tau_150/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/f0_750/tau_150/background/stamp_analysis_anteproc-2016_12_15']]#"""

        #thresholdSNRs = [5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767, 5.78991295767]
        name_tag = "sgr_trigger_2471_testing_focus_40"
        outputPath += "sgr_trigger_2471/plot/"
        xLimits = [1e-22, 4e-21]

elif trigger_number == 2475:
    if not background_based_upper_limits:
        # for upper limits based on open box
        thresholdSNRs = [6.2449653625, 6.2449653625, 6.2449653625, 6.2449653625, 6.2449653625, 6.2449653625]
    else:
        # for upper limits based on background only
        thresholdSNRs = [7.67671444966, 7.67671444966, 7.67671444966, 7.67671444966, 7.67671444966, 7.67671444966]
    if psi_test:
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_variation/stamp_analysis_anteproc-2017_1_6']]
        baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_variation/stamp_analysis_anteproc-2017_1_7']]
        name_tag = "sgr_trigger_2475_variable_polarization_psi_test"
        if abs_version:
            name_tag += "_abs"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2475/plot/polarization_variation/psi_test")
        x_Limits = False
    elif polarized_version:
        if not second_plot_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/stamp_analysis_anteproc-2015_10_18_v9', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/stamp_analysis_anteproc-2015_10_19'],
                    ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/stamp_analysis_anteproc-2015_10_19_v3']]#"""
        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_cancel_test/stamp_analysis_anteproc-2016_12_18'],
                    ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_cancel_test/stamp_analysis_anteproc-2016_12_18_v2']]#"""
        name_tag = "sgr_trigger_2475_variable_polarization"
        if abs_version:
            name_tag += "_abs"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2475/plot/polarization_variation")
        x_Limits = False
    elif alternate_polarization:
        if not background_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_27',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_27_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_28'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_24_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_27',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_27_v2',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_1_28',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/stamp_analysis_anteproc-2016_9_16']]#,
        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_7',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_8'],
                        ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_7',
                        '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/polarization_version/background/stamp_analysis_anteproc-2017_1_8']]

        name_tag = "sgr_trigger_2475_alternate_polarization"
        outputPath = glueFileLocation(outputPath, "sgr_trigger_2475/plot/alternate_polarization/")
    else:
        if not background_version:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/stamp_analysis_anteproc-2015_11_9', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/stamp_analysis_anteproc-2015_11_11_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/stamp_analysis_anteproc-2015_11_11_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/stamp_analysis_anteproc-2015_11_11_v4'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_11_11', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_11_11_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_11_11_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_11_11_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/stamp_analysis_anteproc-2015_11_11_v5'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_11', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_11_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_12', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_12_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_12_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_12_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/stamp_analysis_anteproc-2015_11_12_v5'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/stamp_analysis_anteproc-2015_11_10', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/stamp_analysis_anteproc-2015_11_10_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/stamp_analysis_anteproc-2015_11_11', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/stamp_analysis_anteproc-2016_9_15', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/stamp_analysis_anteproc-2016_9_15_v2'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_150/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_150/stamp_analysis_anteproc-2015_10_22_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_150/stamp_analysis_anteproc-2015_11_11'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_10_22', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_11', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_11_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_12', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_12_v2', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_12_v3', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2015_11_12_v4', '/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/stamp_analysis_anteproc-2016_9_15']]#"""
        else:
            baseDirs = [['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_400/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_400/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_400/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_150/tau_150/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_450/tau_150/background/stamp_analysis_anteproc-2016_12_15'],
                ['/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2475/f0_750/tau_150/background/stamp_analysis_anteproc-2016_12_15']]#"""

        name_tag = "sgr_trigger_2475_testing_focus_40"
        outputPath += "sgr_trigger_2475/plot/"
        xLimits = [6e-23, 1e-21]

if second_plot_version:
    outputPath = glueFileLocation(outputPath, "plot_2nd/")

if plot_mode == "shaded":
    name_tag += "_shaded"
else:
    name_tag += "_thresholds"
# final save modifier
if trigger_number == 2469:
    if not background_based_upper_limits:
        name_tag += "_20"
    else:
        name_tag += "_26_background"
elif trigger_number == 2471:
    if not background_based_upper_limits:
        # open box
        name_tag += "_20"
    else:
        # background only
        name_tag += "_25_background"
elif trigger_number == 2475:
    if not background_based_upper_limits:
        name_tag += "_20"
    else:
        name_tag += "_25_background"
else:
    name_tag += "_4"
if psi_test:
    name_tag += "_psi_test"

threshold_percentages = [0.5, 0.9]

if polarized_version:
    if psi_test:
        labels = ['psi test']
    else:
        labels = ['plus', 'cross']
elif alternate_polarization:
    labels = [r'$f_0 = 150 \, \mathrm{Hz}, \tau = 400 \, \mathrm{s}$',
          r'$f_0 = 750 \, \mathrm{Hz}, \tau = 400 \, \mathrm{s}$']
else:
    labels = [r'$f_0 = 150 \, \mathrm{Hz}, \tau = 400 \, \mathrm{s}$',
          r'$f_0 = 450 \, \mathrm{Hz}, \tau = 400 \, \mathrm{s}$',
          r'$f_0 = 750 \, \mathrm{Hz}, \tau = 400 \, \mathrm{s}$',
          r'$f_0 = 150 \, \mathrm{Hz}, \tau = 150 \, \mathrm{s}$',
          r'$f_0 = 450 \, \mathrm{Hz}, \tau = 150 \, \mathrm{s}$',
          r'$f_0 = 750 \, \mathrm{Hz}, \tau = 150 \, \mathrm{s}$']

markers = ['bx', 'b^', 'bo', 'gx', 'g^', 'go']
colours = ['b', 'g', 'r', 'c', 'm', 'y']

colours = [color_conversion(0, 107, 164),
color_conversion(255, 128, 14),
color_conversion(171, 171, 171),
color_conversion(89, 89, 89),
color_conversion(95, 158, 209),
color_conversion(200, 82, 0),
color_conversion(137, 137, 137),
color_conversion(162, 200, 236),
color_conversion(255, 188, 121),
color_conversion(207, 207, 207)]

# arrange colors
colours = [colours[0], colours[5], colours[3], colours[4], colours[1], colours[2]]

baseJobDirs = [[glueFileLocation(x, "jobs") for x in temp_dir] for temp_dir in baseDirs]

if not x_Limits:
    xLimits = None

onsourceJob = True
if onsourceJob:
    onsourceJob = "1"
else:
    onsourceJob = None

error_confidence_level = 0.95

jsonPaths = [[temp_dir for temp_dir in tempBaseDirs] for tempBaseDirs in baseDirs]
print("Information saved in " + str(jsonPaths))
print("Plots saved in " + outputPath)

temp_data_sets = []
for tempJsonPaths in jsonPaths:
    temp_data = []
    for temp_directory in tempJsonPaths:
        temp_files = find_path(temp_directory, name_tag)
        for temp_path in temp_files:
            if os.path.isfile(temp_path) and not reloadJSONs:
                if "tau_400" in temp_path and "f0_150" in temp_path and "sgr_trigger_2469" in temp_path:
                    with open(temp_path, 'r') as infile:
                        data_to_check = json.load(infile)
                    if not alternate_polarization:
                        data_to_check = dict((key, data_to_check[key]) for key in data_to_check if data_to_check[key][1] < 3e-44)
                    temp_data += [data_to_check]
                else:
                    with open(temp_path, 'r') as infile:
                        temp_data += [json.load(infile)]
            else:
                target_dir = glueFileLocation(temp_directory, "jobs")
                jobGroupDirs = [glueFileLocation(target_dir, x) for x in os.listdir(target_dir) if "job_group" in x]
                jobDirs = [glueFileLocation(temp_dir, x) for temp_dir in jobGroupDirs for x in os.listdir(temp_dir) if "job" in x]
                gsOutputDirs = [glueFileLocation(temp_dir, "grandstochtrackOutput") for temp_dir in jobDirs]
                bknd_files = [glueFileLocation(temp_dir, x) for temp_dir in gsOutputDirs for x in os.listdir(temp_dir) if "bknd" in x]

                single_temp_data = dict((x, getSNRandAlpha(x)) for x in bknd_files)
                temp_data += [single_temp_data]
                with open(temp_path, 'w') as outfile:
                    json.dump(single_temp_data, outfile, sort_keys = True, indent = 4)
    temp_data_sets += [temp_data]
orderedData = {}
for set_num in range(len(temp_data_sets)):
    temp_orderedData = {}
    for sub_set in temp_data_sets[set_num]:
        temp_alpha_dictionary = {}
        for x in sub_set:
            temp_SNR = sub_set[x][0]
            temp_alpha = sub_set[x][1]
            if temp_alpha not in temp_alpha_dictionary:
                temp_alpha_dictionary[temp_alpha] = []
            if temp_SNR not in temp_alpha_dictionary[temp_alpha]:
                temp_alpha_dictionary[temp_alpha] += [temp_SNR]
        for temp_temp_alpha in temp_alpha_dictionary:
            temp_orderedData[temp_temp_alpha] = temp_alpha_dictionary[temp_temp_alpha]
    orderedData[labels[set_num]] = temp_orderedData

print("labels")
print(labels)
data_info = [get_info(orderedData[labels[num]], thresholdSNRs[num], temp_data_sets[num], labels[num]) for num in range(len(labels))]

if not polarized_version:
    if additional_plots:
        for num in range(len(labels)):
            required_margins = 1.25
            page_width = 8.5
            plot_width = page_width - 2*required_margins
            fig = plt.figure(figsize=(plot_width, plot_width*3/4))
            ax = fig.add_subplot(111)
            ax.grid(b=True, which='minor',linestyle=':', alpha = 1-0.85)
            ax.grid(b=True, which='major',linestyle='-', alpha = 1-0.75)

            highSNRs = data_info[num][1][0]
            highAlphas = data_info[num][1][1]
            lowSNRs = data_info[num][1][2]
            lowAlphas = data_info[num][1][3]
            highSNRsOnsource = data_info[num][2][0]
            highAlphasOnsource = data_info[num][2][1]
            lowSNRsOnsource = data_info[num][2][2]
            lowAlphasOnsource = data_info[num][2][3]
            threshold_alphas = data_info[num][0][2]
            plt.grid(b=True, which='minor',color='0.85',linestyle='--')
            plt.grid(b=True, which='major',color='0.75',linestyle='-')
            plt.plot([np.sqrt(x) for x in highAlphas], highSNRs,'rx')#, label = "SNR distribution")
            plt.plot([np.sqrt(x) for x in lowAlphas], lowSNRs,'bx', alpha = 0.5)#, label = "SNR distribution")
            if onsourceJob:
                plt.plot([np.sqrt(x) for x in highAlphasOnsource], highSNRsOnsource,'mo')#, label = "SNR distribution")
                plt.plot([np.sqrt(x) for x in lowAlphasOnsource], lowSNRsOnsource,'go', alpha = 0.5)#, label = "SNR distribution")
            plt.axhline(y=thresholdSNRs[num], xmin=0, xmax=1, hold=None, linestyle='--', color='g')
            plt.xscale('log')
            plt.xlabel(r"Injected Strain ($h_0$)")
            plt.ylabel("SNR")
            if pretty_version:
                plt.rc('text', usetex = True)
                plt.rc('font', family = 'sarif')
                plt.rc('font', serif = 'Computer Modern')
            if save_plots:
                plt.savefig(glueFileLocation(outputPath, "upper_limit_estimate_" + name_tag + "_" + labels[num]), bbox_inches = 'tight')
                plt.savefig(glueFileLocation(outputPath, "upper_limit_estimate_" + name_tag + "_" + labels[num])+ '.pdf', bbox_inches = 'tight', format='pdf')
            plt.clf()

    required_margins = 1.25
    page_width = 8.5
    plot_width = page_width - 2*required_margins
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax = fig.add_subplot(111)
    ax.grid(b=True, which='minor',linestyle=':', alpha = 1-0.85)
    ax.grid(b=True, which='major',linestyle='-', alpha = 1-0.75)
    threshold_list = []
    for num in range(len(labels)):
        sorted_percentiles = data_info[num][0][0]
        sorted_alphas_p = data_info[num][0][1]
        num_data = data_info[num][0][3]

        if 0 in sorted_percentiles:
            sorted_percentiles_min_index = [index for index, val in enumerate(sorted_percentiles) if val == 0][-1]
        else:
            sorted_percentiles_min_index = 0
        if 1 in sorted_percentiles:
            sorted_percentiles_max_index = [index for index, val in enumerate(sorted_percentiles) if val == 1][0]
        else:
            sorted_percentiles_max_index = len(sorted_percentiles) - 1
        sorted_percentiles = sorted_percentiles[sorted_percentiles_min_index:sorted_percentiles_max_index + 1]
        sorted_alphas_p = sorted_alphas_p[sorted_percentiles_min_index:sorted_percentiles_max_index + 1]
        num_data = num_data[sorted_percentiles_min_index:sorted_percentiles_max_index + 1]

        deltas = [normal_binomial_approximation_interval(x, error_confidence_level, num_data[index]) for index, x in enumerate(sorted_percentiles)]
        bayesion_intervals = [bayesian_error_bars(x, num_data[index]) for index, x in enumerate(sorted_percentiles)]
        print(bayesion_intervals)#print(wilson_intervals)
        upper_limits = [sorted_percentiles[x]+deltas[x] for x in range(len(sorted_percentiles))]
        lower_limits = [sorted_percentiles[x]-deltas[x] for x in range(len(sorted_percentiles))]
        upper_limits_2 = [x[2] for x in bayesion_intervals]#[x[2] for x in wilson_intervals]
        lower_limits_2 = [x[1] for x in bayesion_intervals]#[x[1] for x in wilson_intervals]
        bayesian_averages = [x[3] for x in bayesion_intervals]
        upper_deltas = [upper_limits_2[x] - sorted_percentiles[x] for x in range(len(sorted_percentiles))]
        lower_deltas = [sorted_percentiles[x] - lower_limits_2[x] for x in range(len(sorted_percentiles))]
        threshold_alphas = data_info[num][0][2]
        print(labels[num])
        print(threshold_alphas)
        threshold_pairs = []
        print("test interpolating")
        interp_thresholds = (interpolate_threshold(sorted_percentiles, sorted_alphas_p, 0.5), interpolate_threshold(sorted_percentiles, sorted_alphas_p, 0.9))
        threshold_list += [[labels[num], interp_thresholds]]
        print(interp_thresholds[0])
        print(interp_thresholds[1])
        print("tested interpolating")
        for index, val in enumerate(sorted_alphas_p):
            if val in threshold_alphas:
                print(val)
                print(sorted_percentiles[index])
                threshold_pairs += [[val, sorted_percentiles[index]]]
        if pretty_version:
            if plot_mode == "plain":
                plt.plot([np.sqrt(x) for x in sorted_alphas_p], sorted_percentiles, 'x-', label = "Threshold alpha = " + ", ".join(str(temp_threshold[0]) + " (" + str(temp_threshold[1]) + ")" for temp_threshold in threshold_pairs) + " " + labels[num].replace("_"," "))# + " " + labels[num])
            elif plot_mode == "errorbar":
                plt.errorbar([np.sqrt(x) for x in sorted_alphas_p], sorted_percentiles, fmt = 'x-', yerr = [lower_deltas, upper_deltas], label = "Threshold alpha = " + ", ".join(str(temp_threshold[0]) + " (" + str(temp_threshold[1]) + ")" for temp_threshold in threshold_pairs) + " " + labels[num].replace("_"," "))# + " " + labels[num])
            elif plot_mode == "shaded":
                plt.plot([np.sqrt(x) for x in sorted_alphas_p], sorted_percentiles, color = colours[num], label = labels[num])# + " " + labels[num])
                if show_bayesian_average:
                    plt.plot([np.sqrt(x) for x in sorted_alphas_p], bayesian_averages, '--', color = colours[num])#, label = labels[num])
                plt.fill_between([np.sqrt(x) for x in sorted_alphas_p], lower_limits_2, upper_limits_2, alpha = 0.5, color = colours[num], linewidth = 0.0)# Make this a custom function with the proper edge made with an actual plot line instead of the fill_between edge in ordre to get the proper alpha. #, edgecolor = (0,0,0,0))
            else:
                print("Warning: plot type uncertain")
            if plot_interpolated_points:
                for x in interp_thresholds:
                    print(x[1])
                    plt.plot(np.sqrt(x[1]), x[0], "xk")
        else:
            plt.errorbar([np.sqrt(x) for x in sorted_alphas_p], sorted_percentiles, fmt = 'x-', ecolor = (0,1,0,0.5), yerr = [lower_deltas, upper_deltas], label = "Threshold alpha = " + ", ".join(str(temp_threshold)for temp_threshold in threshold_alphas))# + " " + labels[num])
        if threshold_alphas and not pretty_version:
            for temp_threshold in threshold_alphas:
                if temp_threshold:
                    plt.axvline(x=np.sqrt(temp_threshold), ymin=0, ymax=1, hold=None, linestyle='--', color='k', alpha = 0.7, zorder = 9)
    for temp_percentage in threshold_percentages:
        plt.axhline(y=temp_percentage, xmin=0, xmax=1, hold=None, linestyle='--', color='k', zorder = 10)#, alpha = 0.5)
    if pretty_version:
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'sarif')
        plt.rc('font', serif = 'Computer Modern')
    ax.set_xscale('log')
    ax.set_xlabel(r"Injected Strain ($h_0$)")#"Square root of scale factor alpha")
    if xLimits:
        ax.set_xlim(xLimits)
    plt.ylabel("Efficiency")
    if not plot_mode == "plain" or show_legend:
        legend = plt.legend(prop={'size':8}, loc='best')#, framealpha=0.5)
    if plot_mode == "plain" and show_legend:
        legend.get_frame().set_alpha(0.5)
    if lockPlot:
        plt.ylim([0,1])
    print(glueFileLocation(outputPath, "detection_efficiency_estimate_" + name_tag))

    if save_plots:
        plt.savefig(glueFileLocation(outputPath, "detection_efficiency_estimate_" + name_tag), bbox_inches = 'tight')
        plt.savefig(glueFileLocation(outputPath, "detection_efficiency_estimate_" + name_tag) + '.pdf', bbox_inches = 'tight', format='pdf')
    plt.clf()
    if save_plots:
        with open(glueFileLocation(outputPath, "threshold_values.txt"), "w") as outfile:
            output_string = "\n".join("\n".join([parse_waveform_params(x[0]), "\n".join(" ".join(str(z) for z in y) for y in x[1])]) for x in threshold_list)
            outfile.write(output_string)

elif polarized_version:
    iotas = []
    iotas_1 = []
    iotas_2 = []
    psis = []
    SNRs = []
    SNRs_1 = []
    SNRs_2 = []
    min_iotas = []
    min_SNRs = []
    cos_iotas = []
    cos_iotas_1 = []
    cos_iotas_2 = []
    for set_num in range(len(temp_data_sets)):
        temp_orderedData = {}
        temp_SNRs = []
        temp_SNRs_1 = []
        temp_SNRs_2 = []
        temp_iotas = []
        temp_iotas_1 = []
        temp_iotas_2 = []
        temp_psis = []
        temp_min_SNRs = []
        temp_min_iotas = []
        for x in temp_data_sets[set_num]:
            temp_temp_SNRs = [x[y][0] for y in x]
            temp_temp_iotas = [x[y][2] for y in x]
            if psi_test:
                temp_temp_psis = [x[y][3] for y in x]
            temp_SNRs += temp_temp_SNRs
            temp_iotas += temp_temp_iotas
            if psi_test:
                temp_psis += temp_temp_psis

            temp_temp_SNRs_1 = [x[y][0] for y in x if 'job_1' in y]
            temp_temp_iotas_1 = [x[y][2] for y in x if 'job_1' in y]
            temp_temp_SNRs_2 = [x[y][0] for y in x if 'job_2' in y]
            temp_temp_iotas_2 = [x[y][2] for y in x if 'job_2' in y]

            temp_SNRs_1 += temp_temp_SNRs_1
            temp_iotas_1 += temp_temp_iotas_1
            temp_SNRs_2 += temp_temp_SNRs_2
            temp_iotas_2 += temp_temp_iotas_2

            print("Minimum finding option currently only works for 2 individual job-pairs currently.")
            temp_min_SNR_1 = min(temp_temp_SNRs_1)
            temp_min_SNR_2 = min(temp_temp_SNRs_2)
            print("Maximum finding option currently only works for 2 individual job-pairs currently.")
            print(max(temp_temp_SNRs_1))
            print(max(temp_temp_SNRs_2))
            if trigger_number == 2475:
                target_SNR_value = 27.910364328766665
                find_surrounding_values(target_SNR_value, temp_temp_iotas_1, temp_temp_SNRs_1)
                find_surrounding_values(target_SNR_value, temp_temp_iotas_2, temp_temp_SNRs_2)
            for temp_num in range(len(temp_temp_iotas_1)):
                if temp_temp_SNRs_1[temp_num] == temp_min_SNR_1:
                    temp_min_iotas += [temp_temp_iotas_1[temp_num]]
                    temp_min_SNRs += [temp_temp_SNRs_1[temp_num]]
            for temp_num in range(len(temp_temp_iotas_2)):
                if temp_temp_SNRs_2[temp_num] == temp_min_SNR_2:
                    temp_min_iotas += [temp_temp_iotas_2[temp_num]]
                    temp_min_SNRs += [temp_temp_SNRs_2[temp_num]]
        temp_cos_iotas = [np.cos(np.deg2rad(x)) for x in temp_iotas]
        temp_cos_iotas_1 = [np.cos(np.deg2rad(x)) for x in temp_iotas_1]
        temp_cos_iotas_2 = [np.cos(np.deg2rad(x)) for x in temp_iotas_2]
        iotas+= [temp_iotas]
        psis += [temp_psis]
        SNRs+= [temp_SNRs]
        SNRs_1+= [temp_SNRs_1]
        SNRs_2+= [temp_SNRs_2]
        iotas_1 += [temp_iotas_1]
        iotas_2 += [temp_iotas_2]
        cos_iotas += [temp_cos_iotas]
        cos_iotas_1 += [temp_cos_iotas_1]
        cos_iotas_2 += [temp_cos_iotas_2]

        min_iotas+= [temp_min_iotas]
        min_SNRs+= [temp_min_SNRs]

    print(min_iotas)
    print(min_SNRs)
    required_margins = 1.25
    page_width = 8.5
    plot_width = page_width - 2*required_margins
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax = fig.add_subplot(111)
    ax.grid(b=True, which='minor',linestyle=':', alpha = 1-0.85)
    ax.grid(b=True, which='major',linestyle='-', alpha = 1-0.75)
    for x in range(len(SNRs)):
        if polarized_separate:
            plt.plot(cos_iotas_1[x], SNRs_1[x], 'x', label = labels[x])
            plt.plot(cos_iotas_2[x], SNRs_2[x], 'x', label = labels[x])
        elif abs_version:
            if psi_test:
                plt.plot(psis[x], [abs(y) for y in SNRs[x]], 'x', label = labels[x], markersize=4)#, color = colours[x])
            else:
                plt.plot(cos_iotas[x], [abs(y) for y in SNRs[x]], 'x', label = labels[x], markersize=4)#, color = colours[x])
        else:
            plt.plot(cos_iotas[x], SNRs[x], 'x', label = labels[x], markersize=4)#, color = colours[x])
    if polarized_test:
        plt.plot([np.cos(np.radians(69.049882206987093)), np.cos(np.radians(69.852525329854856))], [27.910364328766665, 27.910364328766665], 'x')
        plt.plot([np.cos(np.radians(68.556710444058893)), np.cos(np.radians(69.690743750961829))], [27.910364328766665, 27.910364328766665], 'x')
    if psi_test:
        plt.xlabel(r"$\psi$")
    else:
        plt.xlabel(r"$\cos{\iota}$")
    plt.ylabel("SNR")

    if pretty_version:
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'sarif')
        plt.rc('font', serif = 'Computer Modern')
    if save_plots:
        if psi_test:
            plt.savefig(glueFileLocation(outputPath, "SNR_vs_psi_" + name_tag), bbox_inches = 'tight')
            plt.savefig(glueFileLocation(outputPath, "SNR_vs_psi_" + name_tag + '.pdf'), bbox_inches = 'tight', format='pdf')
        else:
            plt.savefig(glueFileLocation(outputPath, "SNR_vs_cos_iota_" + name_tag), bbox_inches = 'tight')
            plt.savefig(glueFileLocation(outputPath, "SNR_vs_cos_iota_" + name_tag + '.pdf'), bbox_inches = 'tight', format='pdf')
    plt.clf()
