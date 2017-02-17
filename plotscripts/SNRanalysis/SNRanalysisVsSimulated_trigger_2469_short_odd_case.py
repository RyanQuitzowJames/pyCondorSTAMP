# Written by Ryan Quitzow-James

from __future__ import division
from scanSNRlibV2 import *
import os
import pickle
from numpy import argsort, sqrt#, linspace
#from scipy.interpolate import spline
#import webpageGenerateLib as webGen
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
    snr_file = glueFileLocation(base_dir, "SNR_data/SNR_data.txt")
    directory_exists = os.path.isfile(snr_file)
    if directory_exists and not reload_data:
        print("Loading previously saved data...")
        with open(snr_file, "rb") as infile:
            run_info = pickle.load(infile)
    else:
        if not directory_exists:
            os.mkdir(glueFileLocation(base_dir, "SNR_data"))
        run_info = search_run_info_no_alphas_v2(base_dir)
        with open(snr_file, "wb") as outfile:
           pickle.dump(run_info, outfile)
    return run_info

#def interp_line(x_data, y_data, points = 100):
#    y_interp = linspace(min(y_data), max(y_data), points)
#    x_interp = spline(y_data, x_data, y_interp)
#    return x_interp, y_interp

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
    new_background_basedir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2469/stochtrack/v3_abs/stamp_analysis_anteproc-2015_10_20"

elif triggerNumber == 2471:
    basedir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/v3/stamp_analysis_anteproc-2015_9_17"
    basesimdirs = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_16_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v5,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2471/stochtrack_v4/simulated/stamp_analysis_anteproc-2015_8_17_v6"
    #if includepseudoevents:
        #pseudoeventsnrdir = #"/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/pseudo_onsource/stamp_analysis_anteproc-2015_9_11"
    #else:
    #    pseudoeventsnrdir = none
    pseudoeventsnrdir = None

    eventsnrdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/stamp_analysis_anteproc-2015_8_13_v2"

    #dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2471/stochtrack/plot"
    dir_name = "/home/quitzow/public_html/Magnetar/upper_limits/sgr_trigger_2471/plot/background"

elif triggerNumber == 2475:
    basedir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/v3/stamp_analysis_anteproc-2015_9_19"
    basesimdirs = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_27,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_28_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v2,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v3,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v4,/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/simulated/stamp_analysis_anteproc-2015_8_29_v5"
    if includepseudoevents:
        pseudoeventsnrdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/pseudo_onsource/stamp_analysis_anteproc-2015_9_11"
    else:
        pseudoeventsnrdir = None

    if comparison_plot:
        eventsnrdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/v2_abs/stamp_analysis_anteproc-2015_10_22/"
    else:
        eventsnrdir = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/stamp_analysis_anteproc-2015_9_11"

    dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2475/stochtrack/plot"
    #need directory name
    new_background_basedir = "/home/quitzow/public_html/Magnetar/closed_box/sgr_trigger_2475/stochtrack/v3_abs/stamp_analysis_anteproc-2015_10_20/"

eventsnrs = []
pseudoeventsnrs = []

print("loading data...")
#runinfo = search_run_info_no_alphas_v2(basedir)
runinfo = load_snr_object(basedir)
print("data loaded")
if comparison_plot:
    print("loading new background data...")
    #simulatedruninfo = [search_run_info_no_alphas_v2(x) for x in basesimdirs.split(',')]
    simulatedruninfo = [load_snr_object(x) for x in [new_background_basedir]]
    #simulatedruninfo = search_run_info_no_alphas(basesimdir)
    print("new background data loaded")
else:
    print("loading simulated data...")
    #simulatedruninfo = [search_run_info_no_alphas_v2(x) for x in basesimdirs.split(',')]
    simulatedruninfo = [load_snr_object(x) for x in basesimdirs.split(',')]
    #simulatedruninfo = search_run_info_no_alphas(basesimdir)
    print("simulated data loaded")
#print("loading second simulated data...")
#simulatedruninfo2 = search_run_info_no_alphas(basesimdir2)
#print("second simulated data loaded")
if eventsnrdir:
    print("loading event data...")
    eventruninfo = load_snr_object(eventsnrdir)
    print("event data loaded")
if pseudoeventsnrdir:
    print("loading pseudo event data...")
    pseudoeventruninfo = load_snr_object(pseudoeventsnrdir)
    print("pseudo event data loaded")

#loudestsnrs = runinfo.get_high_snrs()
print("pulling snrs...")
allsnrs = runinfo.get_snrs()
allsimulatedsnrs = [x.get_snrs() for x in simulatedruninfo]
if eventsnrdir:
    eventsnrs += eventruninfo.get_snrs()
if pseudoeventsnrdir:
    pseudoeventsnrs += pseudoeventruninfo.get_snrs()
#allsimulatedsnrs2 = simulatedruninfo2.get_snrs()
#print(allsnrs)
#temp = runinfo.get_data()
print("done")

alldata = runinfo.get_data(False)
alldatasorted = [[group[2][jobnum], group[0][jobnum], group[1][jobnum]] for group in alldata for jobnum in range(len(group[0]))]
sortedindices = argsort([x[0] for x in alldatasorted])
alldatasorted = [alldatasorted[index] for index in sortedindices]
alldatasorted = alldatasorted[::-1]

allsimulateddata = [x.get_data(False) for x in simulatedruninfo]
allsimulateddatasorted = [[[group[2][jobnum], group[0][jobnum], group[1][jobnum]] for group in x for jobnum in range(len(group[0]))] for x in allsimulateddata]
sortedsimulatedindices = [argsort([x[0] for x in y]) for y in allsimulateddatasorted]
allsimulateddatasorted = [[allsimulateddatasorted[x][index] for index in sortedsimulatedindices[x]] for x in range(len(sortedsimulatedindices))]
allsimulateddatasorted = [x[::-1] for x in allsimulateddatasorted]

#allsimulateddata2 = simulatedruninfo2.get_data(False)
#allsimulateddatasorted2 = [[group[2][jobnum], group[0][jobnum], group[1][jobnum]] for group in allsimulateddata2 for jobnum in range(len(group[0]))]
#sortedsimulatedindices2 = argsort([x[0] for x in allsimulateddatasorted2])
#allsimulateddatasorted2 = [allsimulateddatasorted2[index] for index in sortedsimulatedindices2]
#allsimulateddatasorted2 = allsimulateddatasorted2[::-1]

#print(temp[1][0])
#print(temp[1][2])

# create directory
#dir_name = glueFileLocation(options.outputdirectory, "simulated_vs_actual_snr_comparison")
#dir_name = create_dir(dir_name)
##dir_name = "/home/quitzow/public_html/Magnetar/open_box/sgr_trigger_2469/stochtrack/plot"

##filename4 = "rundataactual.txt"
#output_text3 = "\n".join("\n".join(", ".join(str(x) for x in [group[2][jobnum], group[0][jobnum], group[1][jobnum]]) for jobnum in range(len(group[0]))) for group in alldata)
output_text4 = "\n".join(", ".join(str(x) for x in line) for line in alldatasorted)#[::-1])
with open(glueFileLocation(dir_name, filename4), "w") as outfile:
    outfile.write(output_text4)

for simnum in range(len(allsimulateddatasorted)):
    if comparison_plot:
        filename5 = "rundata_new_background_" + str(simnum) + ".txt"
    else:
        filename5 = "rundatasimulated_" + str(simnum) + ".txt"
    #output_text3 = "\n".join("\n".join(", ".join(str(x) for x in [group[2][jobnum], group[0][jobnum], group[1][jobnum]]) for jobnum in range(len(group[0]))) for group in alldata)
    output_text5 = "\n".join(", ".join(str(x) for x in line) for line in allsimulateddatasorted[simnum])#[::-1])
    with open(glueFileLocation(dir_name, filename5), "w") as outfile:
        outfile.write(output_text5)

#filename6 = "rundatasimulated2.txt"
#output_text3 = "\n".join("\n".join(", ".join(str(x) for x in [group[2][jobnum], group[0][jobnum], group[1][jobnum]]) for jobnum in range(len(group[0]))) for group in alldata)
#output_text6 = "\n".join(", ".join(str(x) for x in line) for line in allsimulateddatasorted2)#[::-1])
#with open(glueFileLocation(dir_name, filename6), "w") as outfile:
#    outfile.write(output_text6)

sortedallsnrs = allsnrs[:]
sortedallsnrs.sort()
#all_percentage = [100 - (x)/len(sortedallsnrs)*100 for x in range(len(sortedallsnrs))]
all_percentage = [1 - (x)/len(sortedallsnrs) for x in range(len(sortedallsnrs))]

sortedallsimulatedsnrs = [x[:] for x in allsimulatedsnrs]
for x in sortedallsimulatedsnrs:
    x.sort()
#sortedallsimulatedsnrs.sort()
#allsimulated_percentage = [100 - (x)/len(sortedallsimulatedsnrs)*100 for x in range(len(sortedallsnrs))]
allsimulated_percentage = [[1 - (x)/len(y) for x in range(len(y))] for y in sortedallsimulatedsnrs]

#sortedallsimulatedsnrs2 = allsimulatedsnrs2[:]
#sortedallsimulatedsnrs2.sort()
#allsimulated_percentage2 = [1 - (x)/len(sortedallsimulatedsnrs2) for x in range(len(sortedallsnrs))]

numsimulations = len(sortedallsimulatedsnrs)
numjobs = len(sortedallsimulatedsnrs[0])
meansimulatedsnr = [sum([sortedallsimulatedsnrs[simindex][jobindex] for simindex in range(numsimulations)])/numsimulations for jobindex in range(numjobs)]
stdevsimulatedsnr = [sqrt(sum([(sortedallsimulatedsnrs[simindex][jobindex] - meansimulatedsnr[jobindex])**2 for simindex in range(numsimulations)])/numsimulations) for jobindex in range(numjobs)]
sigmaonesimsnrlow = [meansimulatedsnr[jobindex] - stdevsimulatedsnr[jobindex] for jobindex in range(numjobs)]
sigmaonesimsnrhigh = [meansimulatedsnr[jobindex] + stdevsimulatedsnr[jobindex] for jobindex in range(numjobs)]
sigmatwosimsnrlow = [meansimulatedsnr[jobindex] - stdevsimulatedsnr[jobindex]*2 for jobindex in range(numjobs)]
sigmatwosimsnrhigh = [meansimulatedsnr[jobindex] + stdevsimulatedsnr[jobindex]*2 for jobindex in range(numjobs)]
sigmathreesimsnrlow = [meansimulatedsnr[jobindex] - stdevsimulatedsnr[jobindex]*3 for jobindex in range(numjobs)]
sigmathreesimsnrhigh = [meansimulatedsnr[jobindex] + stdevsimulatedsnr[jobindex]*3 for jobindex in range(numjobs)]

"""sigmaonesimsnrlow_interp, all_percentage_interp = interp_line(sigmaonesimsnrlow, all_percentage)
print(min(all_percentage_interp))
print(max(all_percentage_interp))
print(min(sigmaonesimsnrlow))
print(max(sigmaonesimsnrlow))
print(min(sigmaonesimsnrlow_interp))
print(max(sigmaonesimsnrlow_interp))
sigmaonesimsnrhigh_interp, all_percentage_interp = interp_line(sigmaonesimsnrhigh, all_percentage)
sigmatwosimsnrlow_interp, all_percentage_interp = interp_line(sigmatwosimsnrlow, all_percentage)
sigmatwosimsnrhigh_interp, all_percentage_interp = interp_line(sigmatwosimsnrhigh, all_percentage)
sigmathreesimsnrlow_interp, all_percentage_interp = interp_line(sigmathreesimsnrlow, all_percentage)
sigmathreesimsnrhigh_interp, all_percentage_interp = interp_line(sigmathreesimsnrhigh, all_percentage)"""

if eventsnr:
    eventsnrs += [float(x) for x in eventsnr.split(',')]
if comparison_plot:
    #print(len(all_percentage))
    #print(sortedallsimulatedsnrs)
    eventpercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedallsimulatedsnrs[0][x] <= y]) for y in eventsnrs]
    pseudoeventpercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedallsimulatedsnrs[0][x] <= y]) for y in pseudoeventsnrs]
else:
    eventpercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedallsnrs[x] <= y]) for y in eventsnrs]
    pseudoeventpercentages = [min([all_percentage[x] for x in range(len(all_percentage)) if sortedallsnrs[x] <= y]) for y in pseudoeventsnrs]
#else:
#    eventsnrs = []
#    eventpercentages = []

"""print([[all_percentage[x] for x in range(len(all_percentage)) if sortedallsnrs[x] <= y] for y in eventsnrs])
print(len(all_percentage))
print(all_percentage[0])
print(all_percentage[10])
print([[all_percentage[x] for x in range(len(all_percentage)) if all_percentage[x] > 0.99] for y in eventsnrs])
print([all_percentage[x] for x in range(len(all_percentage)) if all_percentage[x] > 0.99])
print(all_percentage[:10])
print(all_percentage[10])
print([all_percentage[-1]])
print([all_percentage[0]])
print([all_percentage[1]])"""

verboseprint("lowest snr of time-shifted data: " + str(min(sortedallsnrs)))
minimumsimsnrs = [min(x) for x in sortedallsimulatedsnrs]
minimumsimsnrs.sort()
verboseprint("average lowest snr of simulations: " + str(sum(minimumsimsnrs)/len(minimumsimsnrs)))
verboseprint("lowest low snr of simulations: " + str(min(minimumsimsnrs)))
verboseprint("highest low snr of simulations: " + str(max(minimumsimsnrs)))
verboseprint("all lowest snrs of simulations: " + str(minimumsimsnrs))

#required_margins = 1.25
#page_width = 8.5
page_width = 4
plot_width = page_width - 2*required_margins

if not comparison_plot:
    print("i'm using a quick and dirty get around to make the axes tick numbers be the right size. this also means the labels are also the same style. this may or may not be a good thing. people may prefer bolded axes labels.")
    #plt.grid(b=true, which='minor',color='0.85',linestyle='--')
    #plt.grid(b=true, which='major',color='0.75',linestyle='-')
    ##plot_size = 5
    #fig = plt.figure(figsize=(8,6))
    #fig = plt.figure(figsize=(plot_size*1.61803398875,plot_size))
    #fig = plt.figure(figsize=(plot_width, plot_width/1.61803398875))
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax1 = fig.add_subplot(111)
    #ax1.grid(b=true, which='minor',linestyle='--', alpha = 1-0.85)
    ax1.grid(b=true, which='minor',linestyle=':', alpha = 1-0.85)
    ax1.grid(b=true, which='major',linestyle='-', alpha = 1-0.75)
    if dots:
        ax1.plot(sortedallsnrs, all_percentage,'b.-', label = "background snr distribution", linewidth = 2)
        ax1.plot(meansimulatedsnr, all_percentage,'k.--', label = "mean of simulations")
        ax1.plot(sortedallsimulatedsnrs[0], allsimulated_percentage[0],'g.-', label = "monte carlo simulations", alpha = 0.3)
        if len(sortedallsimulatedsnrs) > 1:
            for num in range(1,len(sortedallsimulatedsnrs)):
                ax1.plot(sortedallsimulatedsnrs[num], allsimulated_percentage[num],'g.-', alpha = 0.3)
        ax1.plot(sortedallsimulatedsnrs, allsimulated_percentage,'g.--', label = "monte carlo simulations")
        ax1.plot(sortedallsimulatedsnrs2, allsimulated_percentage2,'g.--')
    else:
        ##ax1.fill_betweenx(all_percentage, sigmaonesimsnrlow, sigmaonesimsnrhigh, color='grey', alpha='0.7', linewidth = 0.0)#, zorder = 3)
        ##ax1.fill_betweenx(all_percentage, sigmatwosimsnrlow, sigmaonesimsnrlow, color='grey', alpha='0.5', linewidth = 0.0)#, zorder = 3)
        ##ax1.fill_betweenx(all_percentage, sigmatwosimsnrhigh, sigmaonesimsnrhigh, color='grey', alpha='0.5', linewidth = 0.0)#, zorder = 3)
        ##ax1.fill_betweenx(all_percentage, sigmatwosimsnrlow, sigmathreesimsnrlow, color='grey', alpha='0.3', linewidth = 0.0)#, zorder = 3)
        ##ax1.fill_betweenx(all_percentage, sigmatwosimsnrhigh, sigmathreesimsnrhigh, color='grey', alpha='0.3', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmaonesimsnrlow, sigmaonesimsnrhigh, color=str(1 - 0.5*0.7), linewidth = 0.0)#'grey', alpha='0.7', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmatwosimsnrlow, sigmaonesimsnrlow, color=str(1 - 0.5*0.5), linewidth = 0.0)#'grey', alpha='0.3')#'0.5', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmatwosimsnrhigh, sigmaonesimsnrhigh, color=str(1 - 0.5*0.5), linewidth = 0.0)#color='grey')#, alpha='0.5', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmatwosimsnrlow, sigmathreesimsnrlow, color=str(1 - 0.5*0.3), linewidth = 0.0)#'grey', alpha='0.3', linewidth = 0.0)#, zorder = 3)
        plt.fill_betweenx(all_percentage, sigmatwosimsnrhigh, sigmathreesimsnrhigh, color=str(1 - 0.5*0.3), linewidth = 0.0)#, alpha='0.3')#, linewidth = none)#0.0)#, zorder = 3)
        ##simulationline, = ax1.plot(sortedallsimulatedsnrs[0], allsimulated_percentage[0],'-', label = "gaussian simulations", color = colours[1])#, alpha = 0.5)#, zorder = 4)
        ##simulationline, = ax1.plot(sortedallsimulatedsnrs[0], allsimulated_percentage[0],'-', label = "gaussian simulations", color = colours[4])#, alpha = 0.5)#, zorder = 4)
        simulationline, = ax1.plot(sortedallsimulatedsnrs[0], allsimulated_percentage[0],'-', label = "gaussian simulations", color = colours[4])#, alpha = 0.5)#, zorder = 4)
        if len(sortedallsimulatedsnrs) > 1:
            for num in range(1,len(sortedallsimulatedsnrs)):
                ##ax1.plot(sortedallsimulatedsnrs[num], allsimulated_percentage[num],'-', color = colours[1])#, alpha = 0.5)#, zorder = 4)
                ##ax1.plot(sortedallsimulatedsnrs[num], allsimulated_percentage[num],'-', color = colours[4])#, alpha = 0.5)#, zorder = 4)
                ax1.plot(sortedallsimulatedsnrs[num], allsimulated_percentage[num],'-', color = colours[4])#, alpha = 0.5)#, zorder = 4)
        meanline, = ax1.plot(meansimulatedsnr, all_percentage,'--', label = "simulation mean", color = 'blue')#)#, zorder = 6)
        #backgroundline, = ax1.plot(sortedallsnrs, all_percentage,'-', label = "background", linewidth = 1.5, color = colours[0])#, zorder = 5)
        backgroundline, = ax1.plot(sortedallsnrs, all_percentage,'-k', label = "background", linewidth = 1)#, color = colours[1])#, zorder = 5)
    if pseudoeventsnrs and not background_only:
        ax1.plot(pseudoeventsnrs, pseudoeventpercentages,'b^', label = "dummy on-source")
    if eventsnrs and not background_only:
        ##eventline, = ax1.plot(eventsnrs, eventpercentages,'o', zorder = 6, label = "on-source event", markeredgecolor = none, markersize = 5, color = colours[1])#, color = colours[5])
        eventline, = ax1.plot(eventsnrs, eventpercentages,'o', label = "on-source event", markeredgecolor = none, markersize = 5, color = colours[1])#, color = colours[5])
        ##eventline, = ax1.plot(eventsnrs, eventpercentages,'co', zorder = 6, label = "on-source event", markeredgecolor = "c")#, color = colours[5])
    #plt.xlabel("snr")
    ax1.set_xlabel("snr")
    ymin = min(all_percentage)
    #plt.ylim([ymin,1])
    ax1.set_ylim([ymin,1])
    #plt.yscale('log')
    ax1.set_yscale('log')
    #legend = ax1.legend(prop={'size':12})
    if background_only:
        legend = ax1.legend([backgroundline, simulationline, meanline], ["background", "gaussian simulations", "simulation mean"], prop={'size':10})
    else:
        legend = ax1.legend([backgroundline, simulationline, meanline, eventline], ["background", "gaussian simulations", "simulation mean", "on-source event"], prop={'size':10})
    #legend.get_frame().set_alpha(0.5)
    plot_save_name = "/snrvsfap_all_clusters_semilogy_average_2"
    if background_only:
        plot_save_name += "_background"
    if pdf_latex_mode:
        plt.rc('text', usetex = true)
        #plt.rc('text.latex', preamble = '\usepackage[t1]{fontenc}')
        #if libertine:
        #    plt.rc('text.latex', preamble = '\usepackage[t1]{fontenc}, \usepackage{fbb}, \usepackage[libertine]{newtxmath}, \usepackage[italic]{mathastext}, \mtsetmathskips{f}{5mu}{1mu}')
        #else:
        #    plt.rc('text.latex', preamble = '\usepackage[t1]{fontenc}, \usepackage[notextcomp]{kpfonts}')
        plt.rc('font', family = 'sarif')
        #if libertine:
        #    plt.rc('font', serif = 'libertine')
        #else:
        #    plt.rc('font', serif = 'palatino')
        #plt.rc('font', serif = 'palatino')
        #plt.rc('font', serif = 'libertine')
        plt.rc('font', serif = 'computer modern')
        #plt.rc('font', size = 11)#default 12
        #plt.ylabel("false alarm probability")
        ax1.set_ylabel("false alarm probability")
        fig.savefig(dir_name + plot_save_name + ".pdf", bbox_inches = 'tight', format='pdf')
    else:
        #plt.ylabel("false alarm probability")
        ax1.set_ylabel("false alarm probability")
        fig.savefig(dir_name + plot_save_name, bbox_inches = 'tight')
    fig.clf()
    #"""
else:
    print("i'm using a quick and dirty get around to make the axes tick numbers be the right size. this also means the labels are also the same style. this may or may not be a good thing. people may prefer bolded axes labels.")
    fig = plt.figure(figsize=(plot_width, plot_width*3/4))
    ax1 = fig.add_subplot(111)
    ax1.grid(b=true, which='minor',linestyle=':', alpha = 1-0.85)
    ax1.grid(b=true, which='major',linestyle='-', alpha = 1-0.75)
    backgroundline, = ax1.plot(sortedallsimulatedsnrs[0], allsimulated_percentage[0],'-', label = "background", color = colours[0])#, zorder = 5)
    oldbackgroundline, = ax1.plot(sortedallsnrs, all_percentage,'-', label = "background", color = colours[2])#, zorder = 5)
    if eventsnrs:
        eventline, = ax1.plot(eventsnrs, eventpercentages,'o', label = "on-source event", markeredgecolor = None, markersize = 5, color = colours[1])#, color = colours[5])
    ax1.set_xlabel("snr")
    ymin = min(all_percentage)
    ax1.set_ylim([ymin,1])
    ax1.set_yscale('log')
    legend = ax1.legend([backgroundline, oldbackgroundline, eventline], ["rerun background", "background", "on-source event"], prop={'size':10})
    if pdf_latex_mode:
        plt.rc('text', usetex = true)
        plt.rc('font', family = 'sarif')
        plt.rc('font', serif = 'computer modern')
        ax1.set_ylabel("false alarm probability")
        fig.savefig(dir_name + "/background_vs_abs_background.pdf", bbox_inches = 'tight', format='pdf')
    else:
        ax1.set_ylabel("false alarm probability")
        fig.savefig(dir_name + "/background_vs_abs_background", bbox_inches = 'tight')
    fig.clf()
    #"""
print("SNRs of on-source:")
print(eventSNRs)
print("FAPs of on-source:")
print(eventPercentages)
print(eventPercentages[0])
