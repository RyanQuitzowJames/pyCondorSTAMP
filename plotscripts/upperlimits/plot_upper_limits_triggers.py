from __future__ import division
from plot_upper_limits_lib import *
import scipy.io as sio

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

temp_data_sets = load_data(jsonPaths, name_tag, reloadJSONs)
orderedData = order_data(temp_data_sets, labels)

print("labels")
print(labels)
data_info = [get_info(orderedData[labels[num]], thresholdSNRs[num], temp_data_sets[num], labels[num], threshold_percentages, print_limit_detail, onsourceJob, check_mat_files_onsource) for num in range(len(labels))]

outputPath = "/home/quitzow/public_html/Magnetar/upper_limits/script_plot_test/"
if not polarized_version:
    #upper_limit_plot()
    upper_limit_plot(orderedData, threshold_percentages, labels, thresholdSNRs, data_info, outputPath, colours, name_tag, error_confidence_level, additional_plots, onsourceJob, pretty_version, save_plots, plot_mode, show_bayesian_average, plot_interpolated_points, xLimits, lockPlot)

elif polarized_version:
    polarization_variation_plot()
