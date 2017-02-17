# Written by Ryan Quitzow-James

from __future__ import division
from scanSNRlibV2 import *
import os
import pickle
from numpy import argsort, sqrt#, linspace
from plotClustersLib import returnMatrixFilePath, plotClusterInfo_v2, getPixelInfo, getFrequencyInfo
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#plt.rcParams['legend.numpoints'] = 1

"""parser = OptionParser()
parser.set_defaults(verbose = False)
parser.set_defaults(pdf_latex_mode = False)
parser.set_defaults(dots = False)
parser.set_defaults(reload_data = False)
parser.add_option("-d", "--dir", dest = "targetDirectory",
                  help = "Path to directory containing completed STAMP jobs to use for analysis",
                  metavar = "DIRECTORY")
parser.add_option("-s", "--simDir", dest = "simulationDirectory",
                  help = "Path to directory containing completed simulated STAMP jobs to use for analysis",
                  metavar = "DIRECTORY")
parser.add_option("-o", "--outputDir", dest = "outputDirectory",
                  help = "Path to directory to create to contain background plots",
                  metavar = "DIRECTORY")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help = "Prints internal status messages to terminal as script runs")
parser.add_option("-e", "--eventSNR", dest="eventSNR",
                  help = "Option to set event SNRs from open box search (separate by commas if multiple)")
parser.add_option("-E", "--eventSNRdir", dest="eventSNRdir",
                  help = "Path to data with event SNRs from open box search (separate by commas if multiple)")
parser.add_option("-P", "--pseudoEventSNRdir", dest="pseudoEventSNRdir",
                  help = "Path to data with event SNRs from open box search (separate by commas if multiple)")
parser.add_option("-m", "--maxLim", dest="maxLim")
parser.add_option("-n", "--minLim", dest="minLim")
parser.add_option("-L", action="store_true", dest="pdf_latex_mode")
parser.add_option("-D", action="store_true", dest="dots")
parser.add_option("-R", action="store_true", dest="reload_data")

(options, args) = parser.parse_args()"""

pdf_latex_mode = True
verbose = True
includePseudoEvents = False
dots = False
maxLim = None
minLim = None
reload_data = False
eventSNR = False

background_only = True

triggerNumber = 2471

#libertine = True
comparison_plot = False#True

if triggerNumber == 2471:
    print("Data not rerun with abs-SNR clustering algorithm for SGR trigger 2471.")


def color_conversion(R, G, B):
    return (R/256, G/256, B/256)


# color blind 10
colours = [color_conversion(0, 107, 164),
color_conversion(255, 128, 14),
color_conversion(171, 171, 171),
color_conversion(89, 89, 89),
color_conversion(95, 158, 209),
color_conversion(200, 82, 0),
color_conversion(137, 137, 137),
color_conversion(162, 200, 236),
color_conversion(255, 188, 121),
color_conversion(207, 207, 207)]#"""


print("NOTE: script ignores all files and directories starting with '.'")

print("WARNING: Script is currently not set up to handle directories with multiple files with the name base.")

def verbosePrint(string, switch = verbose):
    if switch:
        print(string)

print("Parsing commandline arguments")

def load_snr_object(base_dir):
    snr_file = os.path.join(base_dir, "SNR_data/SNR_data.txt")
    directory_exists = os.path.isfile(snr_file)
    if directory_exists and not reload_data:
        print("Loading previously saved data...")
        with open(snr_file, "rb") as infile:
            run_info = pickle.load(infile)
    else:
        if not directory_exists:
            os.mkdir(os.path.join(base_dir, "SNR_data"))
        run_info = search_run_info_no_alphas_v2(base_dir)
        with open(snr_file, "wb") as outfile:
           pickle.dump(run_info, outfile)
    return run_info

fileName4 = "runDataActual.txt"

if triggerNumber == 2469:
    #baseDir = options.targetDirectory
    baseDir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/v3/stamp_analysis_anteproc-2015_9_17"
    #baseSimDirs = options.simulationDirectory
    baseSimDirs = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v5,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v6,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v7,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v8,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v9,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/simulated/stamp_analysis_anteproc-2015_8_31_v10"
    #baseSimDir2 = options.simulationDirectory2
    if includePseudoEvents:
        pseudoEventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2469/stochtrack/pseudo_onsource/stamp_analysis_anteproc-2015_9_11"
    else:
        pseudoEventSNRdir = None

    if comparison_plot:
        eventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2469/stochtrack/v2_abs/stamp_analysis_anteproc-2015_10_22"
    else:
        eventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2469/stochtrack/stamp_analysis_anteproc-2015_9_11"

    dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2469/stochtrack/plot"
    #need directory name
    new_background_baseDir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/v3_abs/stamp_analysis_anteproc-2015_10_20"

elif triggerNumber == 2471:
    baseDir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/v3/stamp_analysis_anteproc-2015_9_17"
    baseSimDirs = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v5,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v6"
    #if includePseudoEvents:
        #pseudoEventSNRdir = #"/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/pseudo_onsource/stamp_analysis_anteproc-2015_9_11"
    #else:
    #    pseudoEventSNRdir = None
    pseudoEventSNRdir = None

    eventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/stamp_analysis_anteproc-2015_8_13_v2"

    #dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/plot"
    dir_name = "/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/plot/background"

elif triggerNumber == 2475:
    baseDir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/v3/stamp_analysis_anteproc-2015_9_19"
    baseSimDirs = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_27,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v5"
    if includePseudoEvents:
        pseudoEventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/pseudo_onsource/stamp_analysis_anteproc-2015_9_11"
    else:
        pseudoEventSNRdir = None

    if comparison_plot:
        eventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/v2_abs/stamp_analysis_anteproc-2015_10_22/"
    else:
        eventSNRdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/stamp_analysis_anteproc-2015_9_11"

    dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/plot"
    #need directory name
    new_background_baseDir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/v3_abs/stamp_analysis_anteproc-2015_10_20/"

eventSNRs = []
pseudoEventSNRs = []

print("Loading data...")
runInfo = load_snr_object(baseDir)
print("Data loaded")
if comparison_plot:
    print("Loading new background data...")
    simulatedRunInfo = [load_snr_object(x) for x in [new_background_baseDir]]
    print("New background data loaded")
else:
    print("Loading simulated data...")
    simulatedRunInfo = [load_snr_object(x) for x in baseSimDirs.split(',')]
    print("Simulated data loaded")
if eventSNRdir:
    print("Loading event data...")
    eventRunInfo = load_snr_object(eventSNRdir)
    print("Event data loaded")
if pseudoEventSNRdir:
    print("Loading pseudo event data...")
    pseudoEventRunInfo = load_snr_object(pseudoEventSNRdir)
    print("Pseudo event data loaded")

print("Pulling snrs...")
allSNRs = runInfo.get_snrs()
allSimulatedSNRs = [x.get_snrs() for x in simulatedRunInfo]
if eventSNRdir:
    eventSNRs += eventRunInfo.get_snrs()
if pseudoEventSNRdir:
    pseudoEventSNRs += pseudoEventRunInfo.get_snrs()
print("Done")

allData = runInfo.get_data(False)
allDataSorted = [[group[2][jobNum], group[0][jobNum], group[1][jobNum]] for group in allData for jobNum in range(len(group[0]))]
sortedIndices = argsort([x[0] for x in allDataSorted])
allDataSorted = [allDataSorted[index] for index in sortedIndices]
allDataSorted = allDataSorted[::-1]

allSimulatedData = [x.get_data(False) for x in simulatedRunInfo]
allSimulatedDataSorted = [[[group[2][jobNum], group[0][jobNum], group[1][jobNum]] for group in x for jobNum in range(len(group[0]))] for x in allSimulatedData]
sortedSimulatedIndices = [argsort([x[0] for x in y]) for y in allSimulatedDataSorted]
allSimulatedDataSorted = [[allSimulatedDataSorted[x][index] for index in sortedSimulatedIndices[x]] for x in range(len(sortedSimulatedIndices))]
allSimulatedDataSorted = [x[::-1] for x in allSimulatedDataSorted]

output_text4 = "\n".join(", ".join(str(x) for x in line) for line in allDataSorted)#[::-1])
with open(os.path.join(dir_name, fileName4), "w") as outfile:
    outfile.write(output_text4)

for simNum in range(len(allSimulatedDataSorted)):
    if comparison_plot:
        fileName5 = "runData_new_background_" + str(simNum) + ".txt"
    else:
        fileName5 = "runDataSimulated_" + str(simNum) + ".txt"
    output_text5 = "\n".join(", ".join(str(x) for x in line) for line in allSimulatedDataSorted[simNum])#[::-1])
    with open(os.path.join(dir_name, fileName5), "w") as outfile:
        outfile.write(output_text5)

sortedAllSNRs = allSNRs[:]
sortedAllSNRs.sort()
all_percentage = [1 - (x)/len(sortedAllSNRs) for x in range(len(sortedAllSNRs))]

sortedAllSimulatedSNRs = [x[:] for x in allSimulatedSNRs]
for x in sortedAllSimulatedSNRs:
    x.sort()
allSimulated_percentage = [[1 - (x)/len(y) for x in range(len(y))] for y in sortedAllSimulatedSNRs]

numSimulations = len(sortedAllSimulatedSNRs)
numJobs = len(sortedAllSimulatedSNRs[0])
meanSimulatedSNR = [sum([sortedAllSimulatedSNRs[simIndex][jobIndex] for simIndex in range(numSimulations)])/numSimulations for jobIndex in range(numJobs)]
stDevSimulatedSNR = [sqrt(sum([(sortedAllSimulatedSNRs[simIndex][jobIndex] - meanSimulatedSNR[jobIndex])**2 for simIndex in range(numSimulations)])/numSimulations) for jobIndex in range(numJobs)]
sigmaOneSimSNRLow = [meanSimulatedSNR[jobIndex] - stDevSimulatedSNR[jobIndex] for jobIndex in range(numJobs)]
sigmaOneSimSNRHigh = [meanSimulatedSNR[jobIndex] + stDevSimulatedSNR[jobIndex] for jobIndex in range(numJobs)]
sigmaTwoSimSNRLow = [meanSimulatedSNR[jobIndex] - stDevSimulatedSNR[jobIndex]*2 for jobIndex in range(numJobs)]
sigmaTwoSimSNRHigh = [meanSimulatedSNR[jobIndex] + stDevSimulatedSNR[jobIndex]*2 for jobIndex in range(numJobs)]
sigmaThreeSimSNRLow = [meanSimulatedSNR[jobIndex] - stDevSimulatedSNR[jobIndex]*3 for jobIndex in range(numJobs)]
sigmaThreeSimSNRHigh = [meanSimulatedSNR[jobIndex] + stDevSimulatedSNR[jobIndex]*3 for jobIndex in range(numJobs)]

if eventSNR:
    eventSNRs += [float(x) for x in eventSNR.split(',')]
if comparison_plot:
    #print(len(all_percentage))
    #print(sortedAllSimulatedSNRs)
    eventPercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedAllSimulatedSNRs[0][x] <= y]) for y in eventSNRs]
    pseudoEventPercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedAllSimulatedSNRs[0][x] <= y]) for y in pseudoEventSNRs]
else:
    eventPercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedAllSNRs[x] <= y]) for y in eventSNRs]
    pseudoEventPercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedAllSNRs[x] <= y]) for y in pseudoEventSNRs]

verbosePrint("Lowest SNR of time-shifted data: " + str(min(sortedAllSNRs)))
minimumSimSNRS = [min(x) for x in sortedAllSimulatedSNRs]
minimumSimSNRS.sort()
verbosePrint("Average lowest SNR of simulations: " + str(sum(minimumSimSNRS)/len(minimumSimSNRS)))
verbosePrint("Lowest low SNR of simulations: " + str(min(minimumSimSNRS)))
verbosePrint("Highest low SNR of simulations: " + str(max(minimumSimSNRS)))
verbosePrint("All lowest SNRs of simulations: " + str(minimumSimSNRS))

required_margins = 1.25
page_width = 8.5
page_width = 6
plot_width = page_width - 2*required_margins

if not comparison_plot:
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax1 = fig.add_subplot(111)
    ax1.grid(b=True, which='minor',linestyle=':', alpha = 1-0.85)
    ax1.grid(b=True, which='major',linestyle='-', alpha = 1-0.75)
    if dots:
        ax1.plot(sortedAllSNRs, all_percentage,'b.-', label = "Background SNR Distribution", linewidth = 2)
        ax1.plot(meanSimulatedSNR, all_percentage,'k.--', label = "Mean of Simulations")
        ax1.plot(sortedAllSimulatedSNRs[0], allSimulated_percentage[0],'g.-', label = "Monte Carlo Simulations", alpha = 0.3)
        if len(sortedAllSimulatedSNRs) > 1:
            for num in range(1,len(sortedAllSimulatedSNRs)):
                ax1.plot(sortedAllSimulatedSNRs[num], allSimulated_percentage[num],'g.-', alpha = 0.3)
        ax1.plot(sortedAllSimulatedSNRs, allSimulated_percentage,'g.--', label = "Monte Carlo Simulations")
        ax1.plot(sortedAllSimulatedSNRs2, allSimulated_percentage2,'g.--')
    else:
        plt.fill_betweenx(all_percentage, sigmaOneSimSNRLow, sigmaOneSimSNRHigh, color=str(1 - 0.5*0.7), linewidth = 0.0)#'grey', alpha='0.7', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmaTwoSimSNRLow, sigmaOneSimSNRLow, color=str(1 - 0.5*0.5), linewidth = 0.0)#'grey', alpha='0.3')#'0.5', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmaTwoSimSNRHigh, sigmaOneSimSNRHigh, color=str(1 - 0.5*0.5), linewidth = 0.0)#color='grey')#, alpha='0.5', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmaTwoSimSNRLow, sigmaThreeSimSNRLow, color=str(1 - 0.5*0.3), linewidth = 0.0)#'grey', alpha='0.3', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmaTwoSimSNRHigh, sigmaThreeSimSNRHigh, color=str(1 - 0.5*0.3), linewidth = 0.0)#, alpha='0.3')#, linewidth = None)#0.0)#, zorder = 3)
        simulationLine, = ax1.plot(sortedAllSimulatedSNRs[0], allSimulated_percentage[0],'-', label = "Gaussian Simulations", color = colours[4])#, alpha = 0.5)#, zorder = 4)
        if len(sortedAllSimulatedSNRs) > 1:
            for num in range(1,len(sortedAllSimulatedSNRs)):
                ax1.plot(sortedAllSimulatedSNRs[num], allSimulated_percentage[num],'-', color = colours[4])#, alpha = 0.5)#, zorder = 4)
        meanLine, = ax1.plot(meanSimulatedSNR, all_percentage,'--', label = "Simulation Mean", color = 'blue')#)#, zorder = 6)
        backgroundLine, = ax1.plot(sortedAllSNRs, all_percentage,'-k', label = "Background", linewidth = 1)#, color = colours[1])#, zorder = 5)
    if pseudoEventSNRs and not background_only:
        ax1.plot(pseudoEventSNRs, pseudoEventPercentages,'b^', label = "Dummy On-Source")
    if eventSNRs and not background_only:
        eventLine, = ax1.plot(eventSNRs, eventPercentages,'o', label = "On-Source Event", markeredgecolor = None, markersize = 5, color = colours[1])#, color = colours[5])
    ax1.set_xlabel("SNR")
    ymin = min(all_percentage)
    ax1.set_ylim([ymin,1])
    ax1.set_yscale('log')
    if background_only:
        legend = ax1.legend([backgroundLine, simulationLine, meanLine], ["Background", "Gaussian Simulations", "Simulation Mean"], prop={'size':7})
    else:
        legend = ax1.legend([backgroundLine, simulationLine, meanLine, eventLine], ["Background", "Gaussian Simulations", "Simulation Mean", "On-Source Event"], prop={'size':10})
    plot_save_name = "/SNRvsFAP_all_clusters_semilogy_average_2"
    if background_only:
        plot_save_name += "_background"
    if pdf_latex_mode:
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'sarif')
        plt.rc('font', serif = 'Computer Modern')
        plt.rc('font', weight = 'Normal')
        plt.rc('font', size = 9)#default 12
        ax1.set_ylabel("False Alarm Probability")
        fig.savefig(dir_name + plot_save_name + ".pdf", bbox_inches = 'tight', format='pdf')
    else:
        ax1.set_ylabel("False Alarm Probability")
        fig.savefig(dir_name + plot_save_name, bbox_inches = 'tight')
    fig.clf()
else:
    print("I'm using a quick and dirty get around to make the axes tick numbers be the right size. This also means the labels are also the same style. This may or may not be a good thing. People may prefer bolded axes labels.")
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax1 = fig.add_subplot(111)
    ax1.grid(b=True, which='minor',linestyle=':', alpha = 1-0.85)
    ax1.grid(b=True, which='major',linestyle='-', alpha = 1-0.75)
    backgroundLine, = ax1.plot(sortedAllSimulatedSNRs[0], allSimulated_percentage[0],'-', label = "Background", color = colours[0])#, zorder = 5)
    oldBackgroundLine, = ax1.plot(sortedAllSNRs, all_percentage,'-', label = "Background", color = colours[2])#, zorder = 5)
    if eventSNRs:
        eventLine, = ax1.plot(eventSNRs, eventPercentages,'o', label = "On-Source Event", markeredgecolor = None, markersize = 5, color = colours[1])#, color = colours[5])
    ax1.set_xlabel("SNR")
    ymin = min(all_percentage)
    ax1.set_ylim([ymin,1])
    ax1.set_yscale('log')
    legend = ax1.legend([backgroundLine, oldBackgroundLine, eventLine], ["Rerun Background", "Background", "On-Source Event"], prop={'size':10})
    if pdf_latex_mode:
        plt.rc('text', usetex = True)
        plt.rc('font', family = 'sarif')
        plt.rc('font', serif = 'Computer Modern')
        plt.rc('font', weight = 'Normal')
        ax1.set_ylabel("False Alarm Probability")
        fig.savefig(dir_name + "/background_vs_abs_background.pdf", bbox_inches = 'tight', format='pdf')
    else:
        ax1.set_ylabel("False Alarm Probability")
        fig.savefig(dir_name + "/background_vs_abs_background", bbox_inches = 'tight')
    fig.clf()
    #"""
print("SNRs of on-source:")
print(eventSNRs)
print("FAPs of on-source:")
print(eventPercentages)
print(eventPercentages[0])
