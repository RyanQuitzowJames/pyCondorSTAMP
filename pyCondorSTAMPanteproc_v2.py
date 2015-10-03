from __future__ import division
from optparse import OptionParser
from pyCondorSTAMPLib import *
from pyCondorSTAMPanteprocSupportLib import *
from preprocSupportLib import *
from grandStochtrackSupportLib import *
from condorSTAMPSupportLib import *
import webpageGenerateLib as webGen
import scipy.io as sio
import json
import random

#print("WARNING: code does not currently lock the seed record file. This can lead to a race condition if more than one process is expected to access this file. Only use this code with files that are only expected to
print("Code not currently set up to handle a mix of gpu and non-gpu jobs. A future version should be able to address this.")
print('DEPRECATED: "grandstochtrack job" option in parameter files is deprecated. Please use "preproc job" option istead or this program will fail.')
print("WARNING: if using anteproc, code currently set up to handle H1 as ifo1 and H2 as ifo2. Change in future version")

#### REMINDER: Edit the grand_stochtrack parameter reader such that "." will
# allow easy access to subdirectories in the grand_stochtrack parameter matrix

# include parameter file option eventually to move plots over to get rid of initial black band (located in grand_stochtrack param file)

# command line options
parser = OptionParser()
parser.set_defaults(verbose = False)
parser.set_defaults(restrict_cpus = False)
parser.set_defaults(groupedPreprocessing = True)
parser.set_defaults(burstegard = False)
parser.set_defaults(all_clusters = False)
parser.set_defaults(archived_frames_okay = False)
parser.set_defaults(no_job_retry = False)
parser.set_defaults(extract_from_gpu = False)
parser.set_defaults(anteproc_mode = False)
parser.add_option("-c", "--conf", dest = "configFile",
                  help = "Path to config file detailing analysis for preproc and grand_stochtrack executables (preproc job options can have multiple jobs if separated by a \",\" [may be a good idea to switch to a single directory all preproc jobs are dumped, however this would require them to share many of the same parameters, or not, just don't overlap in time at all, something to think about])",
                  metavar = "FILE")
parser.add_option("-j", "--jobFile", dest = "jobFile",
                  help = "Path to job file detailing job times and durations",
                  metavar = "FILE")
parser.add_option("-d", "--dir", dest = "outputDir",
                  help = "Path to directory to hold analysis output (a new directory \
will be created with appropriate subdirectories to hold analysis)",
                  metavar = "DIRECTORY")
parser.add_option("-p", "--preprocDir", dest = "preprocDir",
                  help = "(Optional) Path to directory holding previous analysis output that contains preproccessed data to use",
                  metavar = "DIRECTORY")
parser.add_option("-v", action="store_true", dest="verbose")
parser.add_option("-g", action="store_false", dest="groupedPreprocessing")
parser.add_option("-r", action="store_true", dest="restrict_cpus")
parser.add_option("-b", action="store_true", dest="burstegard")
parser.add_option("-a", action="store_true", dest="all_clusters")
parser.add_option("-f", action="store_true", dest="archived_frames_okay")
parser.add_option("-q", action="store_true", dest="no_job_retry")
parser.add_option("-e", action="store_true", dest="extract_from_gpu")
parser.add_option("-A", action="store_true", dest="anteproc_mode")


# MAYBE maxjobs will be useful.

parser.add_option("-m", "--maxjobs", dest = "maxjobs",
                  help = "Maximum number of jobs ever submitted at once \
through condor", metavar = "NUMBER")

# add options to load defaults for preproc and grand_stochtrack

(options, args) = parser.parse_args()

if options.groupedPreprocessing:
    print("WARNING: consolidated preproc job option selected.")

if options.outputDir[0:2] == "./":
    options.outputDir = os.getcwd() + options.outputDir[1:]
elif options.outputDir == ".":
    options.outputDir = os.getcwd() + "/"
elif not options.outputDir:
    print("Please specifiy output directory.")
elif options.outputDir[0] != "/":
    options.outputDir = os.getcwd() + "/" + options.outputDir[1:]

if options.jobFile[0:2] == "./":
    options.jobFile = os.getcwd() + options.jobFile[1:]
elif options.jobFile[0] != "/":
    options.jobFile = os.getcwd() + "/" + options.jobFile[1:]

if options.configFile[0:2] == "./":
    options.configFile = os.getcwd() + options.configFile[1:]
elif options.configFile[0] != "/":
    options.configFile = os.getcwd() + "/" + options.configFile[1:]

# constants
quit_program = False
# can adjust path from relative to absolute here (done above?)
configPath = options.configFile
jobPath = options.jobFile
#preprocJobPath = options.preprocJobFile
# default dictionary json path
defaultDictionaryPath = "/home/quitzow/GIT/Development_Branches/pyCondorSTAMP/defaultStochtrack.json"
anteprocDefault = "/home/quitzow/GIT/Development_Branches/pyCondorSTAMP/anteproc_defaults.txt"
#STAMP_setup_script = "/home/quitzow/STAMP/STAMP_6_21_2015/stamp2/test/stamp_setup.sh"
#STAMP_setup_script = "/home/quitzow/STAMP/STAMP_8_11_2015/stamp2/test/stamp_setup.sh"
#STAMP_setup_script = "/home/quitzow/STAMP/STAMP_9_14_2015/stamp2/test/stamp_setup.sh"
STAMP_setup_script = "/home/quitzow/STAMP/STAMP_9_27_2015/stamp2/test/stamp_setup.sh"
# set other defaults this way too instead of definining them inside the preprocSupportLib.py file

#defaultDictionaryPath = "/Users/Quitzow/Desktop/Magnetar Research/STAMP Condor Related/PythonWrapper/defaultBase3.txt"
shellPath = "#!/bin/bash"

# paths to executables
#preprocExecutable = "/home/quitzow/STAMP/STAMP_4_2_2015/stamp2/compiledScripts/preproc/preproc"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_4_2_2015/stamp2/compiledScripts/grand_stochtrack/grand_stochtrack"
#preprocExecutable = "/home/quitzow/STAMP/STAMP_5_20_2015/stamp2/compiledScripts/preproc/preproc"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_5_20_2015/stamp2/compiledScripts/grand_stochtrack/grand_stochtrack"
#anteprocExecutable = "/home/quitzow/STAMP/STAMP_6_21_2015/stamp2/compiledScripts/anteproc/anteproc"
#anteprocExecutable = "/home/quitzow/STAMP/STAMP_8_11_2015/stamp2/compiledScripts/anteproc/anteproc"
#anteprocExecutable = "/home/quitzow/STAMP/STAMP_9_14_2015/stamp2/compiledScripts/anteproc/anteproc"
anteprocExecutable = "/home/quitzow/STAMP/STAMP_9_27_2015/stamp2/compiledScripts/anteproc/anteproc"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_6_21_2015/stamp2/compiledScripts/grand_stochtrack/grand_stochtrack"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_6_21_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack"
#grandStochtrackExecutableNoPlots = "/home/quitzow/STAMP/STAMP_6_21_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack_nojvm"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_8_11_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack"
#grandStochtrackExecutableNoPlots = "/home/quitzow/STAMP/STAMP_8_11_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack_nojvm"
#grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_9_14_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack"
#grandStochtrackExecutableNoPlots = "/home/quitzow/STAMP/STAMP_9_14_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack_nojvm"
grandStochtrackExecutable = "/home/quitzow/STAMP/STAMP_9_27_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack"
grandStochtrackExecutableNoPlots = "/home/quitzow/STAMP/STAMP_9_27_2015/stamp2/compiledScripts/grand_stochtrack_fast/grand_stochtrack_nojvm"

matlabMatrixExtractionExectuable = "/home/quitzow/GIT/Development_Branches/MatlabExecutableDuctTape/getSNRandCluster"

# check for minimum commands line arguments to function
if not options.configFile or not options.outputDir or not options.jobFile:
    print("\nMissing arguments: please specify at least a configuration file, a \
job file and \nan output plot directory to run this program.\n\n")
    quit_program = True
else:
    quit_program = False

# load info from config file
if not quit_program:
    rawData = read_text_file(configPath, ' ')
else:
    rawData = []

# load info from job file
if not quit_program:
    jobData = read_text_file(jobPath, ' ')
    jobNumbers = [line[0] for line in jobData]
    jobData = [[load_if_number(item) for item in line] for line in jobData]
else:
    jobData = []

print("Note: change code to use 'jobDataDict' instead of 'jobData' in the future.")

# load default dictionary if selected
# TODO: fix this for option to exclude default dictionary if wished
if not quit_program:
    defaultDictionary = load_dict_from_json(defaultDictionaryPath)
else:
    defaultDictionary = {}

# load data from jobFile
if not quit_program:
    with open(jobPath, "r") as infile:
        jobDataDict = dict((x.split()[0], x.split()[1:]) for x in infile)
else:
    jobDataDict = {}

# parse jobs

quit_program, jobs, commentsToPrintIfVerbose, job_groups, jobDuplicates, H1_jobs, L1_jobs, waveforms = parse_jobs(rawData, quit_program)
H1_jobs = set(H1_jobs)
L1_jobs = set(L1_jobs)

job_group_iterator = 1
for job in jobs:
    if job != "constants":
        if not jobs[job]["job_group"]:
            while str(job_group_iterator) in job_groups:
                job_group_iterator += 1
            jobs[job]["job_group"] = str(job_group_iterator)
            job_groups += [str(job_group_iterator)]

anteproc_grand_stochtrack_values = {"anteproc.loadFiles": True,
                                    "anteproc.timeShift1": 0,
                                    "anteproc.timeShift2": 0,
                                    "anteproc.jobFileTimeShift": True,
                                    "anteproc.bkndstudy": False,
                                    "anteproc.bkndstudydur": 100}
anteprocOrder = ["anteproc.loadFiles",
                 "anteproc.timeShift1",
                 "anteproc.timeShift2",
                 "anteproc.jobFileTimeShift",
                 "anteproc.bkndstudy",
                 "anteproc.bkndstudydur",
                 "anteproc.inmats1",
                 "anteproc.inmats2",
                 "anteproc.jobfile"]

# set job durations
print("Code currently not set up to handle 'hstart' or 'hstop' individually without the other in specific jobs or 'constants'.")
if not (options.anteproc_mode or anteproc_grand_stochtrack_values["anteproc.jobFileTimeShift"]):
    for job in jobs:
        if (not bool(checkEssentialParameter(jobs[job]["grandStochtrackParams"]["params"], "jobdur"))) and bool(checkEssentialParameter(jobs[job]["grandStochtrackParams"]["params"], "hstart")) and bool(checkEssentialParameter(jobs[job]["grandStochtrackParams"]["params"], "hstop")):
            startTime = float(jobs[job]["grandStochtrackParams"]["params"]["hstart"])
            jobs[job]["grandStochtrackParams"]["params"]["hstart"] = startTime
            endTime = float(jobs[job]["grandStochtrackParams"]["params"]["hstop"])
            jobs[job]["grandStochtrackParams"]["params"]["hstop"] = endTime

            jobs[job]["grandStochtrackParams"]["jobdur"] = endTime - startTime
        if bool(checkEssentialParameter(jobs[job]["grandStochtrackParams"]["params"], "jobdur")):
            jobs[job]["grandStochtrackParams"]["jobdur"] = float(jobs[job]["grandStochtrackParams"]["jobdur"])
    print("Got a lot of float checks here. May want to either have all the float checks occur here, or maybe make them as the data is loaded.")

if commentsToPrintIfVerbose and options.verbose:
    print(commentsToPrintIfVerbose)

# TODO: Warnings and error catching involving default job number and undefined job numbers
print("\n\nRemember: Finish this part.\n\n")

if jobDuplicates and not quit_program:
    quit_program = not ask_yes_no_bool("Duplicate jobs exist. Continue? (y/n)\n")

# update default dictionary
defaultDictionary = load_default_dict(jobs['constants']['grandStochtrackParams']['params'] , defaultDictionary)

# load default anteproc
with open(anteprocDefault, 'r') as infile:
    anteprocDefaultData = [line.split() for line in infile]

# create directory structure
# Build file system

#create directory structure for jobs:
#	stochtrack_condor_job_group_num
#		README.txt with SNR and other information on all jobs? GPS times as well? Whether there is an injection or not?
#		stochtrack_day_job_num (injection? gps time?)
#			README.txt with job information? json maybe? job type
#			preproc inputs
#			inputs for stochtrack clustermap
#			grand_stochtrack inputs
#			results
#				overview mat
#				some other thing?
#				plotDir

cacheFilesCreated = []

anteprocJobs = {}
anteprocJobs["H1"] = {}
anteprocJobs["L1"] = {}
organizedSeeds = {}
organizedSeeds["H1"] = {}
organizedSeeds["L1"] = {}
used_seeds = [jobs["constants"]["anteprocHjob_seeds"][x] for x in jobs["constants"]["anteprocHjob_seeds"]]
used_seeds += [jobs["constants"]["anteprocLjob_seeds"][x] for x in jobs["constants"]["anteprocLjob_seeds"]]
if not quit_program:
    # Build base analysis directory
    # stochtrack_condor_job_group_num
    if options.outputDir[-1] == "/":
        baseDir = dated_dir(options.outputDir + "stamp_analysis_anteproc")
    else:
        baseDir = dated_dir(options.outputDir + "/stamp_analysis_anteproc")
    print("Files to run analysis will be saved in:")
    print(baseDir)#debug

    # copy input parameter file and jobs file into a support directory here
    # support directory
    supportDir = create_dir(baseDir + "/input_files")
    # copy input files to this directory
    copy_input_file(options.configFile, supportDir)#, options.configFile)
    newJobPath = copy_input_file(options.jobFile, supportDir)#, options.jobFile)
    if options.anteproc_mode:
        newAdjustedJobPath = adjust_job_file(options.jobFile, supportDir, jobs)

    # create directory to host all of the jobs. maybe drop the cachefiles in here too?
    jobsBaseDir = create_dir(baseDir + "/jobs")

    # create cachefile directory
    print("Creating cache directory")

    if jobs["constants"]["anteprocParamsH"]["doDetectorNoiseSim"] == "false":
        cacheDir = create_dir(baseDir + "/cache_files") + "/"
        fakeCacheDir = None
    else:
        fakeCacheDir = create_dir(baseDir + "/fake_cache_files") + "/"
        cacheDir = None

    if options.anteproc_mode:
        print("Creating anteproc directory and input files")
        anteproc_dir = create_dir(baseDir + "/anteproc_data")

        if cacheDir:
            anteproc_H, anteproc_L = anteproc_setup(anteproc_dir, anteprocDefaultData, jobs, cacheDir)
        else:
            anteproc_H, anteproc_L = anteproc_setup(anteproc_dir, anteprocDefaultData, jobs, fakeCacheDir)
        multiple_waveforms = False

        if "stampinj" in anteproc_H and "stampinj" in anteproc_L:
            if len(waveforms) > 0:
                multiple_waveforms = True
            if anteproc_H["stampinj"] != anteproc_L["stampinj"]:
                print("Warning, injections settings in detectors do not match, one has 'stampinj = true' and one has 'stampinj = false'. Please edit code for further capabilities of this behavior is intentional.")
                quit_program = True
        elif "stampinj" in anteproc_H or "stampinj" in anteproc_L:
            print("Warning, injections settings in detectors do not match, one has 'stampinj' and one does not. Please edit code for further capabilities of this behavior is intentional.")
            quit_program = True

        anteprocJobs, used_seeds, organizedSeeds, quit_program = anteproc_job_specific_setup(H1_jobs, "H1",
            anteproc_dir, jobs, anteproc_H, used_seeds, organizedSeeds, multiple_waveforms, waveforms, anteprocDefaultData,
            anteprocJobs, quit_program)

        anteprocJobs, used_seeds, organizedSeeds, quit_program = anteproc_job_specific_setup(L1_jobs, "L1",
            anteproc_dir, jobs, anteproc_L, used_seeds, organizedSeeds, multiple_waveforms, waveforms, anteprocDefaultData,
            anteprocJobs, quit_program)

        if jobs["constants"]["anteprocParamsH"]["doDetectorNoiseSim"] == "true" or jobs["constants"]["anteprocParamsL"]["doDetectorNoiseSim"] == "true":
            with open(anteproc_dir + "/seeds_for_simulated_data.txt", "w") as outfile:
                json.dump(organizedSeeds, outfile, sort_keys = True, indent = 4)

        anteproc_grand_stochtrack_values["anteproc.inmats1"] = anteproc_dir + "/H-H1_map"
        anteproc_grand_stochtrack_values["anteproc.inmats2"] = anteproc_dir + "/L-L1_map"
        anteproc_grand_stochtrack_values["anteproc.jobfile"] = newAdjustedJobPath

        for job in jobs:
            #"adjust inmats entries here maybe if needed? yes."
            for anteprocParameter in anteprocOrder:
                if (anteprocParameter == "anteproc.inmats1" or anteprocParameter == "anteproc.inmats2") and "injection_tags" in jobs[job]:
                    jobs[job]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job]["grandStochtrackParams"]["params"], anteprocParameter, anteproc_grand_stochtrack_values[anteprocParameter] + "_" + jobs[job]["injection_tags"])
                else:
                    jobs[job]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job]["grandStochtrackParams"]["params"], anteprocParameter, anteproc_grand_stochtrack_values[anteprocParameter])
    else:
        anteproc_dir = None

    # cycle through jobs
    print("Creating job directories")
    for job in jobs:
        if job != "constants":
            # stochtrack_day_job_num (injection? gps time?)
            jobDir = create_dir(jobsBaseDir + "/" + "job_group_" + jobs[job]["job_group"] + "/" + job)
            jobs[job]["jobDir"] = jobDir

#			inputs for stochtrack clustermap in text file (put this here or in the "/params" directory)
#			grand_stochtrack inputs
            stochtrackInputDir = create_dir(jobDir + "/grandstochtrackInput")
            jobs[job]["stochtrackInputDir"] = stochtrackInputDir
#			results
            grandstochtrackOutputDir = create_dir(jobDir + "/grandstochtrackOutput")
            jobs[job]["grandstochtrackOutputDir"] = grandstochtrackOutputDir
#				overview mat
#				some other thing?
#				plotDir
            plotDir = create_dir(grandstochtrackOutputDir + "/plots")
            jobs[job]["plotDir"] = plotDir

        # NOTE: recording any directories other than the base job directory may not have any value
        # because the internal structure of each job is identical.

    # build dag directory
    dagDir = create_dir(baseDir + "/dag")

    # Build support file sub directory for dag logs
    dagLogDir = create_dir(dagDir + "/dagLogs")

    # Build support file sub directory for job logs
    logDir = create_dir(dagLogDir + "/logs")
else:
    baseDir = None

# create grandstochtrack execution script

print("Creating shell scripts")
grandStochtrack_script_file = dagDir + "/grand_stochtrack.sh"
if jobs['constants']['grandStochtrackParams']['params']['savePlots']:
    write_grandstochtrack_bash_script(grandStochtrack_script_file, grandStochtrackExecutable, STAMP_setup_script)
else:
    write_grandstochtrack_bash_script(grandStochtrack_script_file, grandStochtrackExecutableNoPlots, STAMP_setup_script)
os.chmod(grandStochtrack_script_file, 0744)

matlabMatrixExtractionExectuable_script_file = dagDir + "/matlab_matrix_extraction.sh"
write_grandstochtrack_bash_script(matlabMatrixExtractionExectuable_script_file, matlabMatrixExtractionExectuable, STAMP_setup_script)
os.chmod(matlabMatrixExtractionExectuable_script_file, 0744)

anteprocExecutable_script_file = dagDir + "/anteproc.sh"
write_anteproc_bash_script(anteprocExecutable_script_file, anteprocExecutable, STAMP_setup_script)
os.chmod(anteprocExecutable_script_file, 0744)

# If relative injection value set, override any existing injection time with calculated relative injection time.

# find frame files
for tempJob in set(H1_jobs):
    print("Finding frames for job " + str(tempJob) + " for H1")
    tempJobData = jobDataDict[str(tempJob)]
    if anteproc_H["doDetectorNoiseSim"] == "false":
        temp_frames, quit_program = create_frame_file_list("H1_LDAS_C02_L2", tempJobData[0], tempJobData[1], "H", quit_program)
        quit_program = create_cache_and_time_file(temp_frames, "H",tempJob,cacheDir,quit_program, archived_frames_okay = options.archived_frames_okay)
    else:
        quit_program = create_fake_cache_and_time_file(tempJobData[0], tempJobData[1], "H", tempJob, fakeCacheDir, quit_program)
for tempJob in set(L1_jobs):
    print("Finding frames for job " + str(tempJob) + " for L1")
    tempJobData = jobDataDict[str(tempJob)]
    if anteproc_L["doDetectorNoiseSim"] == "false":
        temp_frames, quit_program = create_frame_file_list("L1_LDAS_C02_L2", tempJobData[0], tempJobData[1], "L", quit_program)
        quit_program = create_cache_and_time_file(temp_frames, "L",tempJob,cacheDir,quit_program, archived_frames_okay = options.archived_frames_okay)
    else:
        quit_program = create_fake_cache_and_time_file(tempJobData[0], tempJobData[1], "L", tempJob, fakeCacheDir, quit_program)
# write preproc parameter files for each job
if not quit_program:
    print("Saving grand_stochtrack paramter files")
    for job in jobs:
        if job != "constants":
            # put output directories in grand_stochtrack dictionary
            jobs[job]["grandStochtrackParams"]["params"]["plotdir"] = jobs[job]["plotDir"] + "/"
            jobs[job]["grandStochtrackParams"]["params"]["outputfilename"] = jobs[job]["grandstochtrackOutputDir"] + "/map"
            jobs[job]["grandStochtrackParams"]["params"]["jobsFile"] = newJobPath
            jobs[job]["grandStochtrackParams"]["params"]["ofile"] = jobs[job]["grandstochtrackOutputDir"] + "/bknd"

            # write stochtrack parameter files for each job
            jobs[job]['grandStochtrackParams']['params'] = load_default_dict(jobs[job]['grandStochtrackParams']['params'] , defaultDictionary)
            # the way this following line is done needs to be reviewed.
            jobs[job]['grandStochtrackParams'] = load_default_dict(jobs[job]['grandStochtrackParams'], jobs["constants"]['grandStochtrackParams'])
            sio.savemat(jobs[job]["stochtrackInputDir"] + "/" + "params.mat", jobs[job]["grandStochtrackParams"])

# order plots by job

jobTempDict = dict((int(job[job.index("_")+1:]),{"job" : job, "job dir" : "job_group_" + jobs[job]["job_group"] + "/" + job}) for job in [x for x in jobs if x != "constants"])

if options.burstegard:
    plotTypeList = ["SNR", "Largest Cluster", "All Clusters", "sig map", "y map", "Xi snr map"]
    plotTypeDict = {"SNR" : "snr.png", "Largest Cluster" : "large_cluster.png", "All Clusters": "all_clusters.png", "sig map" : "sig_map.png", "y map" : "y_map.png", "Xi snr map" : "Xi_snr_map.png"}
elif options.all_clusters:
    plotTypeList = ["SNR", "Loudest Cluster (stochtrack)", "Largest Cluster (burstegard)", "All Clusters (burstegard)", "sig map", "y map", "Xi snr map"]
    plotTypeDict = {"SNR" : "snr.png", "Loudest Cluster (stochtrack)" : "rmap.png", "Largest Cluster (burstegard)" : "large_cluster.png", "All Clusters (burstegard)": "all_clusters.png", "sig map" : "sig_map.png", "y map" : "y_map.png", "Xi snr map" : "Xi_snr_map.png"}
else:
    plotTypeList = ["SNR", "Loudest Cluster", "sig map", "y map", "Xi snr map"]
    plotTypeDict = {"SNR" : "snr.png", "Loudest Cluster" : "rmap.png", "sig map" : "sig_map.png", "y map" : "y_map.png", "Xi snr map" : "Xi_snr_map.png"}

outFile = "pageDisplayTest.html"

jobNumOrder = [jobNum for jobNum in jobTempDict]
jobNumOrder.sort()
jobOrder = [jobTempDict[jobNum]["job"] for jobNum in jobNumOrder]
jobOrderWeb = [jobTempDict[jobNum]["job dir"] for jobNum in jobNumOrder]

#webGen.make_display_page(directory, saveDir, subDirList, subSubDir, plotTypeList, plotTypeDict, outputFileName)
print('DEBUG NOTE: Maybe figure out how to variablize "grandstochtrackOutput/plots" in next line?')
if not quit_program:
    print("Creating webpage")
    webGen.make_display_page("jobs", baseDir, jobOrderWeb, "grandstochtrackOutput/plots", plotTypeList, plotTypeDict, outFile)

# build DAGs
# preproc DAG
if not quit_program:
    # build submission file
    doGPU = jobs["constants"]["grandStochtrackParams"]["params"]["doGPU"]
    if doGPU and not options.burstegard:
        extract_from_gpu = True
    else:
        extract_from_gpu = False
    extract_from_gpu = options.extract_from_gpu
    print("Creating dag and sub files")
    create_anteproc_dag_v5(jobs, grandStochtrack_script_file, matlabMatrixExtractionExectuable_script_file, anteprocExecutable_script_file, dagDir, shellPath, newJobPath, H1_jobs, L1_jobs, anteprocJobs, quit_program, job_order = jobOrder, use_gpu = doGPU, restrict_cpus = options.restrict_cpus, no_job_retry = options.no_job_retry, extract_from_gpu = extract_from_gpu, alternate_preproc_dir = options.preprocDir)

print("NOTE: Job ordering is not currently set up to handle multiple jobs of the same number as numbered by this program.")

# create webpage

# run top DAG
