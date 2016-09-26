#pyCondorSTAMPanteproc_full.py
from __future__ import division
from generateInputFileLib import *
from numpy import argsort, sqrt, arccos, pi, array, object
from pyCondorSTAMPLib import *
from pyCondorSTAMPanteprocSupportLib_v2 import *
from preprocSupportLib import *
from grandStochtrackSupportLib import *
from condorSTAMPSupportLib_v2 import *
import webpageGenerateLib as webGen
import scipy.io as sio
import random
import json
import os
from optparse import OptionParser
from load_defaults import getDefaultCommonParams
from copy import deepcopy

def main():
    parser = OptionParser()
    
    parser.add_option("-p", "--params-file", dest = "params_file",
                      help = "Path to params file")
    
    (options, args) = parser.parse_args()
    
    params_file_path = options.params_file
    
    if params_file_path[0] == ".":
        params_file_path = os.getcwd() + params_file_path[1:]
    elif params_file_path[0] == "~":
        params_file_path = os.path.expanduser('~') + params_file_path[1:]
    elif not params_file_path[0] == "/":
        params_file_path = os.getcwd() + "/" + params_file_path[0:]
        
    
    input_params = json.load(open(params_file_path))
    
    #Following lines DISABLED, dictionary now used due to increased security
    #this loads all of the input parameters into local variables.  It's kind of magic
    #for key, val in input_params.iteritems():
    #    exec(key + '=val')
        
    onsource = input_params['search_type'] == "onsource"
    pseudo_onsource = input_params['search_type'] == "pseudo_onsource"
    upper_limits = input_params['search_type'] == "upper_limits"
    offsource = input_params['search_type'] == "offsource"
    
    if input_params['injection_bool'] and not input_params['onTheFly'] and not os.isfile(injection_file):
        pyCondorSTAMPanteprocError("Injection file does not exist.  Make onTheFly true if you do not wish to specify an injection file")
        
    if input_params['long_tau']:
        wave_tau = 400
    else:
        wave_tau = 150
        
    wave_duration = wave_tau*3
    
    if input_params['polarization_smaller_response']: #this might need adjustment for particular triggers
        wave_iota = 120
        wave_psi = 45
    else:
        wave_iota = 0
        wave_psi = 0
    
    if onsource:
        input_params['injection_bool'] = False
        input_params['simulated'] = False
        input_params['relative_direction'] = False
        
    if pseudo_onsource:
        relative_directoin = False
    
    if not input_params['injection_bool']:
        input_params['onTheFly'] = False
        input_params['polarization_smaller_response'] = False
        input_params['injection_random_start_time'] = False
        input_params['include_variations'] = False
        
    if input_params['singletrack_bool']:
        input_params['single_cpu'] = True
    
    jobPath = make_file_path_absolute(input_params['jobFile'])
    configPath = glueFileLocation(input_params['outputDir'], "config_file.txt")
    outputDir = make_file_path_absolute(input_params['outputDir'])
    outputDir += "stamp_analysis_anteproc" if input_params['outputDir'][-1] == "/" else "/stamp_analysis_anteproc"
    baseDir = dated_dir(outputDir)
            # copy input parameter file and jobs file into a support directory here
        # support directory
    supportDir = create_dir(baseDir + "/input_files")
        # copy input files to this directory
    copy_input_file(configPath, supportDir)
    copy_input_file(params_file_path, supportDir)
    newJobPath = copy_input_file(jobPath, supportDir)
    
    
    commonParamsDictionary = getDefaultCommonParams()   
    #commonParamsDictionary = {'grandStochtrack': {'stochtrack': {'singletrack': {}}}, 'anteproc_h': {'stamp': {}}, 'anteproc_l': {'stamp': {}}, 'preproc': {}}
    stochtrackParamsDictionary = {}

    #load default file
    #THING TO FIX: read in the default config file into the dictionary
    inputFileData = readFile(make_file_path_absolute(input_params['default_config_file']))
    inputFileString = "\n".join(" ".join(x for x in line) for line in inputFileData)
    
    inputFileString += "\n\n" + "grandStochtrack stochtrack.T " + str(input_params['T'])
    inputFileString += "\n" + "grandStochtrack stochtrack.F " + str(input_params['F'])
    commonParamsDictionary['grandStochtrack']['stochtrack']['T'] = input_params['T']
    commonParamsDictionary['grandStochtrack']['stochtrack']['F'] = input_params['F']
    
    times = [[int(y) for y in x] for x in readFile(input_params['jobFile'])]
    
    if input_params['burstegard']:
        inputFileString += "\n\n" + "grandStochtrack doBurstegard true"
        commonParamsDictionary['grandStochtrack']['doBurstegard'] = True
    else:
        if input_params['long_pixel']:
            inputFileString += "\n\n" + "anteproc_h segmentDuration 4"
            inputFileString += "\n\n" + "anteproc_l segmentDuration 4"
            commonParamsDictionary['anteproc_h']['segmentDuration'] = 4
            commonParamsDictionary['anteproc_l']['segmentDuration'] = 4
        else:
            inputFileString += "\n\n" + "anteproc_h segmentDuration 1"
            inputFileString += "\n\n" + "anteproc_l segmentDuration 1"
            commonParamsDictionary['anteproc_h']['segmentDuration'] = 1
            commonParamsDictionary['anteproc_l']['segmentDuration'] = 1
            
        inputFileString += "\n\n" + "grandStochtrack doStochtrack true"
        commonParamsDictionary['grandStochtrack']['doStochtrack'] = True
        
        if input_params['long_pixel']:
            inputFileString += "\n\n" + "grandStochtrack stochtrack.mindur 25"
            inputFileString += "\n\n" + "preproc segmentDuration 4"
            commonParamsDictionary['grandStochtrack']['stochtrack']['mindur'] = 25
            commonParamsDictionary['preproc']['segmentDuration'] = 4

        else:
            inputFileString += "\n\n" + "grandStochtrack stochtrack.mindur 100"
            inputFileString += "\n\n" + "grandStochtrack stochtrack.F 600"
            commonParamsDictionary['grandStochtrack']['stochtrack']['mindur'] = 100
            commonParamsDictionary['grandStochtrack']['stochtrack']['F'] = 600
    
    if input_params['simulated']:
        inputFileString += "\n\n" + "anteproc_h doDetectorNoiseSim true"
        inputFileString += "\n\n" + "anteproc_l doDetectorNoiseSim true"
        inputFileString += "\n\n" + "anteproc_h DetectorNoiseFile " + input_params['LHO_Welch_PSD_file']
        inputFileString += "\n\n" + "anteproc_l DetectorNoiseFile " + input_params['LLO_Welch_PSD_file']
        commonParamsDictionary['anteproc_h']['doDetectorNoiseSim'] = True
        commonParamsDictionary['anteproc_l']['doDetectorNoiseSim'] = True
        commonParamsDictionary['anteproc_h']['DetectorNoiseFile'] = input_params['LHO_Welch_PSD_file']
        commonParamsDictionary['anteproc_l']['DetectorNoiseFile'] = input_params['LLO_Welch_PSD_file']

        if not input_params['show_plots_when_simulated']:
            inputFileString += "\n\n" + "grandStochtrack savePlots false"
            commonParamsDictionary['grandStochtrack']['savePlots'] = False
    else:
        inputFileString += "\n\n" + "anteproc_h doDetectorNoiseSim false"
        inputFileString += "\n\n" + "anteproc_l doDetectorNoiseSim false"        
        commonParamsDictionary['anteproc_h']['doDetectorNoiseSim'] = False
        commonParamsDictionary['anteproc_l']['doDetectorNoiseSim'] = False
    
    
    # Add in injections (if desired)
    if input_params['injection_bool']:
        if input_params['onTheFly']:
            # stamp_alpha was waveformPowerAmplitudeScaling here
            inputFileString += "\n\n" + """anteproc_h stampinj true
    anteproc_h stamp.alpha """ + str(input_params['stamp_alpha']) + """
    
    anteproc_h stamp.iota """ + str(wave_iota) + """
    anteproc_h stamp.psi """ + str(wave_psi) + """
    
    anteproc_l stampinj true
    anteproc_l stamp.alpha """ + str(input_params['stamp_alpha']) + """
    
    anteproc_l stamp.iota """ + str(wave_iota) + """
    anteproc_l stamp.psi """ + str(wave_psi)
            commonParamsDictionary['anteproc_h']['stampinj'] = True
            commonParamsDictionary['anteproc_h']['stamp']['alpha'] = input_params['stamp_alpha']
            commonParamsDictionary['anteproc_h']['stamp']['iota'] = wave_iota
            commonParamsDictionary['anteproc_h']['stamp']['psi'] = wave_psi         
            commonParamsDictionary['anteproc_l']['stampinj'] = True
            commonParamsDictionary['anteproc_l']['stamp']['alpha'] = input_params['stamp_alpha']
            commonParamsDictionary['anteproc_l']['stamp']['iota'] = wave_iota
            commonParamsDictionary['anteproc_l']['stamp']['psi'] = wave_psi
            
            
        else:
            inputFileString += "\n\n" + """anteproc_h stampinj true
    anteproc_h stamp.alpha """ + str(input_params['stamp_alpha']) + """
    
    anteproc_h stamp.iota 0
    anteproc_h stamp.psi 0
    
    anteproc_l stampinj true
    anteproc_l stamp.alpha """ + str(input_params['stamp_alpha']) + """
    
    anteproc_l stamp.iota 0
    anteproc_l stamp.psi 0"""
            commonParamsDictionary['anteproc_h']['stampinj'] = True
            commonParamsDictionary['anteproc_h']['stamp']['alpha'] = input_params['stamp_alpha']
            commonParamsDictionary['anteproc_h']['stamp']['iota'] = 0
            commonParamsDictionary['anteproc_h']['stamp']['psi'] = 0           
            commonParamsDictionary['anteproc_l']['stampinj'] = True
            commonParamsDictionary['anteproc_l']['stamp']['alpha'] = input_params['stamp_alpha']
            commonParamsDictionary['anteproc_l']['stamp']['iota'] = 0
            commonParamsDictionary['anteproc_l']['stamp']['psi'] = 0
    
    if input_params['singletrack_bool']:
        inputFileString += '\n\n' + "grandStochtrack stochtrack.singletrack.doSingletrack true"
        inputFileString += "\n" + "grandStochtrack stochtrack.singletrack.trackInputFiles " + ",".join(input_params['singletrack_input_files'])
        commonParamsDictionary['grandStochtrack']['stochtrack']['singletrack']['doSingletrack'] = True
        commonParamsDictionary['grandStochtrack']['stochtrack']['singletrack']['trackInputFiles'] = array(input_params['singletrack_input_files'], dtype=object)
    else:
        commonParamsDictionary['grandStochtrack']['stochtrack'].pop('singletrack')
        
    if input_params['set_stochtrack_seed']:
        inputFileString += "\n\n" + "grandStochtrack stochtrack.doSeed true"
        inputFileString += "\n\n" + "grandStochtrack stochtrack.seed 2015"
        commonParamsDictionary['grandStochtrack']['stochtrack']['doSeed'] = True
        commonParamsDictionary['grandStochtrack']['stochtrack']['seed'] = 2015
        
    if input_params['maxband']:
        if input_params['maxband_mode'] == "percent":
            inputFileString += "\n\n" + "grandStochtrack stochtrack.doMaxbandPercentage true"
            inputFileString += "\n\n" + "grandStochtrack stochtrack.maxbandPercentage " + str(input_params['maxband'])
            commonParamsDictionary['grandStochtrack']['stochtrack']['doMaxBandPercentage'] = True
            commonParamsDictionary['grandStochtrack']['stochtrack']['maxbandPercentage'] = input_params['maxband']
            print("WARNING - doMaxbandPercentage is active - this only works with STAMP revision 12522 or later")
        elif input_params['maxband_mode'] == "absolute":
            inputFileString += "\n\n" + "grandStochtrack stochtrack.doMaxbandPercentage false"
            inputFileString += "\n\n" + "grandStochtrack stochtrack.maxband " + str(input_params['maxband'])
            commonParamsDictionary['grandStochtrack']['stochtrack']['doMaxBandPercentage'] = False
            commonParamsDictionary['grandStochtrack']['stochtrack']['maxband'] = input_params['maxband']


        else:
            raise pyCondorSTAMPanteprocError("Unrecognized option for maxband_mode: " + input_params['maxband_mode'] + ".  Must be either 'percent' or 'absolute'")
    
    if not input_params['long_pixel']:
        inputFileString += "\n\n" + "job_start_shift 6"
        inputFileString += "\n\n" + "job_duration 400"
        commonParamsDictionary['job_start_shift'] = 6
        commonParamsDictionary['job_duration'] = 400
    
    if input_params['simulated'] and onsource and input_params['pre_seed']:
        inputFileString += "\n\n" + "anteproc_h job_seed 1 2694478780"
        inputFileString += "\n\n" + "anteproc_l job_seed 1 4222550304"
        commonParamsDictionary['anteproc_h']['job_seed'] = 2694478780        
        commonParamsDictionary['anteproc_h']['job_seed'] = 4222550304
        #NEED TO FIGURE OUT HOW THIS ONE WORKS

    
    job_group = 1
    
    params = {}
    
    if not input_params['relative_direction']:
        params["granchStochtrack ra"] = input_params['RA']
        params["grandStochtrack dec"] = input_params['DEC']
        commonParamsDictionary['grandStochtrack']['ra'] = input_params['RA']
        commonParamsDictionary['grandStochtrack']['dec'] = input_params['DEC']
    
    if input_params['injection_bool'] and not input_params['onTheFly']:
        params["preproc stamp.file"] = injection_file
        params["preproc stamp.alpha"] = 1e-40
        commonParamsDictionary['preproc']['stamp']['file'] = injection_file
        commonParamsDictionary['preproc']['stamp']['alpha'] = 1e-40
        
    
    
    #this ensures there's enough data to be able to estimate the background
    # 9-NumberofSegmentsPerInterval (NSPI), -1 (take out the pixel that's being analyzed), /2 to get one side of those
    # *4 (pixel duration) 2 + (buffer seconds), + 2 (window started 2 seconds before trigger time)
    if input_params['long_pixel'] or input_params['burstegard']:
        triggerJobStart = input_params['triggerTime'] - (2 + (9-1)*4/2 + 2)
    else:
        triggerJobStart = input_params['triggerTime'] - (2 + (9-1)/2 + 2)
    
    # analysis starts 2 pixels before trigger time
    trigger_hStart = input_params['triggerTime'] - 2
    
    deltaTotal = []
    jobPairs = []
    jobPairsTotal = 1000 #number of background job pairs set
    
    #Next section finds the job number PAIRS run by stochtrack, and job NUMBERS run by anteproc
    
    if upper_limits:
    
        with open(input_params['off_source_json_path'], 'r') as infile:
            temp_job_data = json.load(infile)
        sortedJobPairs = [x[1:3] for x in temp_job_data if x[1:3] != [34, 34]]
        sortedJobPairs = [[x-1 for x in y] for y in sortedJobPairs] # goes from job number to job index
        source_file_dict = {}
    
        for num in range(len(sortedJobPairs)):
    
            if sortedJobPairs[num][0] not in source_file_dict:
                source_file_dict[sortedJobPairs[num][0]] = {}
                
            if sortedJobPairs[num][1] in source_file_dict[sortedJobPairs[num][0]]:
                print("Warning, multiple copies of job pair exist.")
                print(sortedJobPairs[num])
            elif sortedJobPairs[num][0] == 33 or sortedJobPairs[num][1] == 33:
                print("Warning, on-source and off-source jobs possibly mixed.")
                print(sortedJobPairs[num])
            else:
                source_file_dict[sortedJobPairs[num][0]][sortedJobPairs[num][1]] = temp_job_data[num][-1]
            # add on-source jobs and path, it's job number 34, and index number 33
        sortedJobPairs = [[33,33]] + sortedJobPairs
        source_file_dict[33] = {}
        source_file_dict[33][33] = input_params['on_source_file_path']
        
        #cut down to max number of jobs (if needed)
        if len(sortedJobPairs) > input_params['job_subset_limit']:
            sortedJobPairs = sortedJobPairs[:input_params['job_subset_limit']]
        else:
            input_params['job_subset_limit'] = None
            
    elif onsource:
        sortedJobPairs = [[0,0]]
    
    elif pseudo_onsource:
        before_possible_job_indices = [index for index, val in enumerate(times) if triggerJobStart - val[1] >= 3600]
        after_possible_job_indices = [index for index, val in enumerate(times) if val[1] - triggerJobStart >= 3600]
        job_index_list_1 = random.sample(before_possible_job_indices, input_params['pseudo_random_jobs_per_side'])
        job_index_list_2 = random.sample(after_possible_job_indices, input_params['pseudo_random_jobs_per_side'])
        sortedJobPairs = [[x,x] for x in job_index_list_1] + [[x,x] for x in job_index_list_2]
    
    elif offsource:
        for index1, job1 in enumerate(times):
            for index2, job2 in enumerate(times):
                if index1 != index2:
                    deltaTotal += [abs(triggerJobStart - job1[1]) + abs(triggerJobStart - job2[1])]
                    jobPairs += [[index1, index2]]
        sortedIndices = argsort(deltaTotal)[:jobPairsTotal]
        sortedJobPairs = [jobPairs[x] for x in sortedIndices]
        
    else:
        print("Error: need to define search type correctly")
        raise
    #These are the job indices run by anteproc 
    tempNumbersH = list(set([x[0] for x in sortedJobPairs])) #job indices
    tempNumbersL = list(set([x[1] for x in sortedJobPairs])) #job indices
    
    
    
    #Now build the job-specific parameters for anteproc - only needed for injections
    anteprocHParamsList = [{'stamp':{}} for i in range(0, max(tempNumbersH) + 1)]
    anteprocLParamsList = [{'stamp':{}} for i in range(0, max(tempNumbersL) + 1)]
    if input_params['injection_bool']:

        for H1_job_index in tempNumbersH:
            H1_job = H1_job_index + 1
            job1StartTime = times[H1_job_index][1]
    
            if input_params['long_pixel'] or input_params['burstegard']:
                job1_hstart = job1StartTime + (9-1)*4/2+2
            else:
                job1_hstart = job1StartTime + (9-1)/2+2
            
            job1_hstop = job1_hstart + 1602 if input_params['long_pixel'] or input_params['burstegard'] else job1_hstart + 400
    
            if not input_params['relative_direction']:
                inputFileString += "\n\n" + "anteproc_h anteproc_param " + str(H1_job) + " stamp.ra " + str(input_params['RA'])
                inputFileString += "\n" + "anteproc_h anteproc_param " + str(H1_job) + " stamp.decl " + str(input_params['DEC'])
                anteprocHParamsList[H1_job_index]['stamp.ra'] = input_params['RA']
                anteprocHParamsList[H1_job_index]['stamp.decl'] = input_params['DEC']

            elif H1_job == 34:
                inputFileString += "\n\nanteproc_h anteproc_param 34 useReferenceAntennaFactors false"
                anteprocHParamsList[33]['useReferenceAntennaFactors'] = False

            else:
                inputFileString += "\n\nanteproc_h anteproc_param " + str(H1_job) + " useReferenceAntennaFactors true"
                anteprocHParamsList[H1_job_index]['useReferenceAntennaFactors'] = True

            if input_params['onTheFly']:
                inputFileString += "\n" + "anteproc_h anteproc_param " + str(H1_job) + " stamp.start " + str(job1_hstart+2)
                anteprocHParamsList[H1_job_index]['stamp.start'] = job1_hstart+2  

            else:
                inputFileString += "\n" + "anteproc_h stamp.startGPS " + str(job1_hstart+2)
                anteprocHParamsList[H1_job_index]['stamp.startGPS'] = job1_hstart+2


        for L1_job_index in tempNumbersL:
            L1_job = L1_job_index + 1
            job1StartTime = times[L1_job_index][1]
    
            if input_params['long_pixel'] or input_params['burstegard']:
                job1_hstart = job1StartTime + (9-1)*4/2+2
            else:
                job1_hstart = job1StartTime + (9-1)/2+2
            
            job1_hstop = job1_hstart + 1602 if input_params['long_pixel'] or input_params['burstegard'] else job1_hstart + 400
        
            if not input_params['relative_direction']:
                inputFileString += "\n\n" + "anteproc_l anteproc_param " + str(L1_job) + " stamp.ra " + str(input_params['RA'])
                inputFileString += "\n" + "anteproc_l anteproc_param " + str(L1_job) + " stamp.decl " + str(input_params['DEC'])
                anteprocLParamsList[L1_job_index]['stamp.ra'] = input_params['RA']
                anteprocLParamsList[L1_job_index]['stamp.decl'] = input_params['DEC']

            elif L1_job == 34:
                inputFileString += "\n\nanteproc_l anteproc_param 34 useReferenceAntennaFactors false"                
                anteprocLParamsList[33]['useReferenceAntennaFactors'] = False

            else:
                inputFileString += "\n\nanteproc_l anteproc_param " + str(L1_job) + " useReferenceAntennaFactors true"
                anteprocLParamsList[L1_job_index]['useReferenceAntennaFactors'] = True

            if input_params['onTheFly']:
                inputFileString += "\n" + "anteproc_l anteproc_param " + str(L1_job) + " stamp.start " + str(job1_hstart+2)
                anteprocLParamsList[L1_job_index]['stamp.start'] = job1_hstart+2
            else:
                inputFileString += "\n" + "anteproc_l stamp.startGPS " + str(job1_hstart+2)
                anteprocLParamsList[L1_job_index]['stamp.startGPS'] = job1_hstart+2
    

        if input_params['onTheFly']:
            #here we put in parameters for the on-the-fly injection, including waveform, frequency, amplitude (sqrt(2)/2, so that
            # they sum in quadrature to 1
            inputFileString += """
    
    anteproc_h stamp.inj_type fly
    anteproc_h stamp.fly_waveform half_sg
    anteproc_l stamp.inj_type fly
    anteproc_l stamp.fly_waveform half_sg
    
    anteproc_h stamp.h0 """ + str(sqrt(0.5)) + """
    anteproc_h stamp.f0 """ + str(input_params['wave_frequency']) + """
    anteproc_h stamp.phi0 0
    anteproc_h stamp.fdot 0
    anteproc_h stamp.duration """ + str(wave_duration) + """
    anteproc_h stamp.tau """ + str(wave_tau) + """
    
    anteproc_l stamp.h0 """ + str(sqrt(0.5)) + """
    anteproc_l stamp.f0 """ + str(input_params['wave_frequency']) + """
    anteproc_l stamp.phi0 0
    anteproc_l stamp.fdot 0
    anteproc_l stamp.duration """ + str(wave_duration) + """
    anteproc_l stamp.tau """ + str(wave_tau)
            
            commonParamsDictionary['anteproc_h']['stamp']['inj_type'] = "fly"
            commonParamsDictionary['anteproc_h']['stamp']['fly_waveform'] = "half_sg"
            commonParamsDictionary['anteproc_l']['stamp']['inj_type'] = "fly"
            commonParamsDictionary['anteproc_l']['stamp']['fly_waveform'] = "half_sg"

            commonParamsDictionary['anteproc_h']['stamp']['h0'] = sqrt(0.5)
            commonParamsDictionary['anteproc_h']['stamp']['f0'] = input_params['wave_frequency']
            commonParamsDictionary['anteproc_h']['stamp']['phi0'] = 0
            commonParamsDictionary['anteproc_h']['stamp']['fdot'] = 0
            commonParamsDictionary['anteproc_h']['stamp']['duration'] = wave_duration
            commonParamsDictionary['anteproc_h']['stamp']['tau'] = wave_tau

            commonParamsDictionary['anteproc_l']['stamp']['h0'] = sqrt(0.5)
            commonParamsDictionary['anteproc_l']['stamp']['f0'] = input_params['wave_frequency']
            commonParamsDictionary['anteproc_l']['stamp']['phi0'] = 0
            commonParamsDictionary['anteproc_l']['stamp']['fdot'] = 0
            commonParamsDictionary['anteproc_l']['stamp']['duration'] = wave_duration
            commonParamsDictionary['anteproc_l']['stamp']['tau'] = wave_tau

            
        else:
            inputFileString += "\n\n" + "\n".join(" ".join(x for x in ["waveform", temp_name, glueFileLocation(waveformDirectory, temp_name + waveformFileExtention)]) for temp_name in waveformFileNames)
            for waveform in waveformFileNames:
                commonParamsDictionary["waveform"][waveform] = glueFileLocation(waveformDirectory, temp_name + waveformFileExtention)
    
    
    if input_params['relative_direction']:
    
        refTime = input_params['triggerTime'] - 2
    
        inputFileString += "\n\ngrandStochtrack useReferenceAntennaFactors true"
        inputFileString += "\n\ngrandStochtrack referenceGPSTime " + str(refTime)
        inputFileString += "\nanteproc_h referenceGPSTime " + str(refTime)
        inputFileString += "\nanteproc_l referenceGPSTime " + str(refTime)
    
        inputFileString += "\n\ngrandStochtrack ra " + str(input_params['RA'])
        inputFileString += "\ngrandStochtrack dec " + str(input_params['DEC'])
        inputFileString += "\n\nanteproc_h stamp.ra " + str(input_params['RA'])
        inputFileString += "\nanteproc_h stamp.decl " + str(input_params['DEC'])
        inputFileString += "\n\nanteproc_l stamp.ra " + str(input_params['RA'])
        inputFileString += "\nanteproc_l stamp.decl " + str(input_params['DEC'])
        
        commonParamsDictionary['grandStochtrack']['useReferenceAntennaFactors'] = True
        commonParamsDictionary['grandStochtrack']['referenceGPSTime'] = refTime
        commonParamsDictionary['anteproc_h']['referenceGPSTime'] = refTime
        commonParamsDictionary['anteproc_l']['referenceGPSTime'] = refTime

        commonParamsDictionary['grandStochtrack']['ra'] = input_params['RA']
        commonParamsDictionary['grandStochtrack']['dec'] = input_params['DEC']
        commonParamsDictionary['anteproc_h']['stamp']['ra'] = input_params['RA']
        commonParamsDictionary['anteproc_h']['stamp']['decl'] = input_params['DEC']
        commonParamsDictionary['anteproc_l']['stamp']['ra'] = input_params['RA']
        commonParamsDictionary['anteproc_l']['stamp']['decl'] = input_params['DEC']

    
    if input_params['constant_f_window']:
        inputFileString += "\n\ngrandStochtrack fmin 40"
        inputFileString += "\ngrandStochtrack fmax 2500"
        commonParamsDictionary['grandStochtrack']['fmin'] = 40
        commonParamsDictionary['grandStochtrack']['fmax'] = 2500

    if input_params['constant_f_mask']:
        inputFileString += "\n\ngrandStochtrack StampFreqsToRemove [" + ", ".join(str(x) for x in input_params['lines_to_cut']) + "]"
        commonParamsDictionary['grandStochtrack']['StampFreqsToRemove'] = input_params['lines_to_cut']
    
    if input_params['remove_cluster']:
        inputFileString += "\n\ngrandStochtrack maskCluster true"
        commonParamsDictionary['grandStochtrack']['maskCluster'] = True
    
    if input_params['include_variations']:
        inputFileString += "\n\nanteproc_varying_param num_jobs_to_vary " + str(input_params['number_variation_jobs'])
        inputFileString += "".join("\nanteproc_varying_param " + " ".join(str(y) for y in x) for x in input_params['anteproc_varying_param'])
        commonParamsDictionary['grandStochtrack']['maskCluster'] = True
    
    if input_params['injection_random_start_time']:
        start_variation_line = "varying_injection_start -2 " + str(1604 - wave_duration - 2) #check what this does exactly

        inputFileString += "\n" + start_variation_line
        commonParamsDictionary['varying_injection_start'] = [-2, 1604 - wave_duration - 2]
    
    text_output = inputFileString
    
    
    #this for loop builds each individual job
    current_job = 0
    stochtrackParamsList = []
    H1AnteprocJobNums = set()
    L1AnteprocJobNums = set()
    for [jobIndex1, jobIndex2] in sortedJobPairs:#[jobNum1, jobNum2] in sortedJobPairs:
        jobNum1 = jobIndex1 + 1
        jobNum2 = jobIndex2 + 1
        job1StartTime = times[jobIndex1][1]
        job1EndTime = times[jobIndex1][2]
        
        #jobDictionary = {"preproc" : {}, "grandStochtrack": {"anteproc" : {}}}
        jobDictionary = {'grandStochtrackParams': {'params':deepcopy(commonParamsDictionary['grandStochtrack'])}}
        job_dir = baseDir + "/jobs/job_group_1/job_" + str(current_job + 1)
        jobDictionary["grandStochtrackParams"]["params"]["plotdir"] = job_dir + "/grandStochtrackOutput/plots/"
        jobDictionary["grandStochtrackParams"]["params"]["outputfilename"] = job_dir + "/grandStochtrackOutput/map"
        jobDictionary["grandStochtrackParams"]["params"]["ofile"] = job_dir + "/grandStochtrackOutput/bknd"
        jobDictionary["grandStochtrackParams"]["params"]["jobsFile"] = newJobPath
        
        if input_params['long_pixel'] or input_params['burstegard']:
            job1_hstart = job1StartTime + (9-1)*4/2+2
        else:
            job1_hstart = job1StartTime + (9-1)/2+2
            
        job1_hstop = job1_hstart + 1602 if input_params['long_pixel'] or input_params['burstegard'] else job_hstart + 400
    
        if input_params['injection_bool'] and not input_params['relative_direction']:
            #params["preproc stamp.startGPS"] = int(jobH1StartTime)
            params["preproc stamp.ra"] = input_params['RA']
            jobDictionary["preproc"]["stamp"]["ra"] = input_params['RA']
    
        if not input_params['relative_direction']:
            params["grandStochtrack ra"] = input_params['RA']
            jobDictionary["grandStochtrackParams"]["params"]["ra"] = input_params['RA']

        if input_params['remove_cluster']:
            params["grandStochtrack clusterFile"] = source_file_dict[jobIndex1][jobIndex2]
            jobDictionary["grandStochtrackParams"]["params"]["clusterFile"] = source_file_dict[jobIndex1][jobIndex2]
    
        params["preproc job"] = jobNum1#this needed anymore?
        jobDictionary["preprocJobs"] = jobNum1
    
        if input_params['anteproc_bool']:
            params["grandStochtrack anteproc.jobNum1"] = jobNum1
            params["grandStochtrack anteproc.jobNum2"] = jobNum2
            jobDictionary["grandStochtrackParams"]["params"]["anteproc"]["jobNum1"] = jobNum1
            jobDictionary["grandStochtrackParams"]["params"]["anteproc"]["jobNum2"] = jobNum2
    
        else:
            params["preproc doShift1"] = 0
            params["preproc ShiftTime1"] = 0
            params["preproc doShift2"] = 1
            params["preproc ShiftTime2"] = base_shift + timeShift - 1
            jobDictionary["preproc"]["doShift1"] = 0
            jobDictionary["preproc"]["ShiftTime1"] = 0
            jobDictionary["preproc"]["doShift2"] = 1
            jobDictionary["preproc"]["ShiftTime2"] = base_shift + timeShift - 1

    
        if input_params['relative_direction']:
            if jobIndex1 == 33:
                params["grandStochtrack useReferenceAntennaFactors"] = "false"
                jobDictionary["grandStochtrackParams"]["params"]["useReferenceAntennaFactors"] = False

            elif "grandStochtrack useReferenceAntennaFactors" in params:
                del params["grandStochtrack useReferenceAntennaFactors"]
                jobDictionary["grandStochtrackParams"]["params"].pop("useReferenceAntennaFactors", None)
    
        if input_params['injection_bool'] and not input_params['onTheFly']:
            for temp_waveform in waveformFileNames:
                params["injection_tag"] = temp_waveform
                jobDictionary["injection_tag"] = temp_waveform
                current_job += 1
                temp_output = ""
                temp_output += "job " + str(current_job) + "\n"
                temp_output += "job_group " + str(job_group) + "\n"
                temp_output += "\n".join([str(x) + " " + str(params[x]) for x in params])    
                text_output += "\n\n" + temp_output
                
                stochtrackParamsList.append(deepcopy(jobDictionary))
                stochtrackParamsList[current_job - 1]["grandStochtrackParams"]["params"]['job_group']=  job_group
                stochtrackParamsList[current_job - 1]["grandStochtrackParams"]["params"]['jobNumber'] = current_job
                H1AnteprocJobNums.add(jobNum1)
                L1AnteprocJobNums.add(jobNum2)
                
        else:
            current_job +=1
            temp_output = ""
            temp_output += "job " + str(current_job) + "\n"
            temp_output += "job_group " + str(job_group) + "\n"
            temp_output += "\n".join([str(x) + " " + str(params[x]) for x in params])
            text_output += "\n\n" + temp_output
            
            stochtrackParamsList.append(deepcopy(jobDictionary))
            stochtrackParamsList[current_job - 1]["grandStochtrackParams"]["params"]['job_group'] = job_group
            stochtrackParamsList[current_job - 1]["grandStochtrackParams"]["params"]['jobNumber'] = current_job
            H1AnteprocJobNums.add(jobNum1)
            L1AnteprocJobNums.add(jobNum2)


    
    saveText(glueFileLocation(input_params['outputDir'], "config_file.txt"), text_output)
    
    
    ###################################################################################
    ###################################################################################
    ###################################################################################
    #########
    ######### Now moving on to the pyCondorSTAMPanteproc_v4 - like part
    #########
    ###################################################################################
    ###################################################################################
    ###################################################################################
    
    

    
    verbose = False
    archived_frames_okay = True
    all_clusters = False
    restrict_cpus = True
    no_job_retry = False
    

    
    STAMP_setup_script = glueFileLocation(input_params['STAMP2_installation_dir'], "test/stamp_setup.sh")
    # set other defaults this way too instead of definining them inside the preprocSupportLib.py file
    
    # paths to executables
    anteprocExecutable = glueFileLocation(input_params['STAMP2_installation_dir'], "compilationScripts/anteproc")
    grandStochtrackExecutable = glueFileLocation(input_params['STAMP2_installation_dir'], "compilationScripts/grand_stochtrack")
    grandStochtrackExecutableNoPlots = glueFileLocation(input_params['STAMP2_installation_dir'], "compilationScripts/grand_stochtrack_nojvm")
    
    # load info from config file
    rawData = read_text_file(configPath, ' ')
    
    # load default dictionary if selected
    # TODO: fix this for option to exclude default dictionary if wished
    defaultDictionary = load_dict_from_json(input_params['defaultDictionaryPath'])
    
    # load data from jobFile
    with open(jobPath, "r") as infile:
        jobDataDict = dict((x.split()[0], x.split()[1:]) for x in infile)
    
    # parse jobs
    
    jobs, commentsToPrintIfVerbose, job_groups, jobDuplicates, H1_jobs, L1_jobs, waveforms, varyingAnteprocVariables = parse_jobs(rawData)


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
    
    if commentsToPrintIfVerbose and verbose:
        print(commentsToPrintIfVerbose)
    
    # TODO: Warnings and error catching involving default job number and undefined job numbers
    print("\n\nRemember: Finish this part.\n\n")
    
    if jobDuplicates:
        ans = raw_input("Duplicate jobs exist.  Continue? (y/n)")
        if not ans == 'y':
            raise pyCondorSTAMPanteprocError("Process Terminated")
    
    # update default dictionary
    defaultDictionary = load_default_dict(jobs['constants']['grandStochtrackParams']['params'] , defaultDictionary)
    

    
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
    
    if "num_jobs_to_vary" in varyingAnteprocVariables:
        multiple_job_group_version = True
    else:
        multiple_job_group_version = False
    
    cacheFilesCreated = []
    
    anteprocJobs = {}
    anteprocJobs["H1"] = {}
    anteprocJobs["L1"] = {}
    organizedSeeds = {}
    organizedSeeds["H1"] = {}
    organizedSeeds["L1"] = {}
    used_seeds = [jobs["constants"]["anteprocHjob_seeds"][x] for x in jobs["constants"]["anteprocHjob_seeds"]]
    used_seeds += [jobs["constants"]["anteprocLjob_seeds"][x] for x in jobs["constants"]["anteprocLjob_seeds"]]
        # Build base analysis directory
        # stochtrack_condor_job_group_num
    
    

    
    newAdjustedJobPath = adjust_job_file(jobPath, supportDir, jobs)
    
        # create directory to host all of the jobs. maybe drop the cachefiles in here too?
    jobsBaseDir = create_dir(baseDir + "/jobs")
    
        # create cachefile directory
    print("Creating cache directory")
    anteproc_dir = create_dir(baseDir + "/anteproc_data")
    commonParamsDictionary['anteproc_h']["outputfiledir"] = anteproc_dir + "/"
    commonParamsDictionary['anteproc_l']["outputfiledir"] = anteproc_dir + "/"  
    if jobs["constants"]["anteprocParamsH"]["doDetectorNoiseSim"] == "false":
        cacheDir = create_dir(baseDir + "/cache_files") + "/"
        fakeCacheDir = None
        commonParamsDictionary['anteproc_h']["gpsTimesPath1"] = cacheDir
        commonParamsDictionary['anteproc_h']["frameCachePath1"] = cacheDir
        commonParamsDictionary['anteproc_l']["gpsTimesPath1"] = cacheDir
        commonParamsDictionary['anteproc_l']["frameCachePath1"] = cacheDir        
    else:
        fakeCacheDir = create_dir(baseDir + "/fake_cache_files") + "/"
        cacheDir = None
        commonParamsDictionary['anteproc_h']["gpsTimesPath1"] = fakeCacheDir
        commonParamsDictionary['anteproc_h']["frameCachePath1"] = fakeCacheDir
        commonParamsDictionary['anteproc_l']["gpsTimesPath1"] = fakeCacheDir
        commonParamsDictionary['anteproc_l']["frameCachePath1"] = fakeCacheDir
    
    print("Creating anteproc directory and input files")

    
        # load default anteproc - this is already done
    with open(input_params['anteprocDefault'], 'r') as infile:
        anteprocDefaultData = [line.split() for line in infile]
    
    #this is done already above
    if cacheDir:
        anteproc_H, anteproc_L = anteproc_setup(anteproc_dir, anteprocDefaultData, jobs, cacheDir)
    else:
        anteproc_H, anteproc_L = anteproc_setup(anteproc_dir, anteprocDefaultData, jobs, fakeCacheDir)
        
    anteproc_H["ASQchannel1"] = input_params['channel']
    anteproc_H["frameType1"] = "H1_" + input_params['frame_type']
    anteproc_L["ASQchannel1"] = input_params['channel']
    anteproc_L["frameType1"] = "L1_" + input_params['frame_type']
    
    multiple_waveforms = False
    
    if "stampinj" in anteproc_H and "stampinj" in anteproc_L:
        if len(waveforms) > 0:
            multiple_waveforms = True
        if anteproc_H["stampinj"] != anteproc_L["stampinj"]:
            raise pyCondorSTAMPanteprocError("Warning, injections settings in detectors do not match, one has 'stampinj = true' and one has 'stampinj = false'. Please edit code for further capabilities of this behavior is intentional.")
    elif "stampinj" in anteproc_H or "stampinj" in anteproc_L:
        raise pyCondorSTAMPanteprocError("Warning, injections settings in detectors do not match, one has 'stampinj' and one does not. Please edit code for further capabilities of this behavior is intentional.")
    anteprocJobDictTracker = createPreprocessingJobDependentDict(jobs)
    if "varying_injection_start" in jobs["constants"]:
        frontStartTime = jobs["constants"]["varying_injection_start"][0]
        backStartTime = jobs["constants"]["varying_injection_start"][1]
        injectionStartTimes = generate_random_start_times(jobs, varyingAnteprocVariables, frontStartTime, backStartTime)
    else:
        injectionStartTimes = None
    
    anteprocJobs, used_seeds, organizedSeeds = anteproc_job_specific_setup(H1_jobs, "H1",
            anteproc_dir, jobs, anteproc_H, used_seeds, organizedSeeds, multiple_waveforms, waveforms, anteprocDefaultData,
            anteprocJobs, varyingAnteprocVariables, anteprocJobDictTracker = anteprocJobDictTracker, injectionStartTimes = injectionStartTimes)
    
    anteprocJobs, used_seeds, organizedSeeds = anteproc_job_specific_setup(L1_jobs, "L1",
            anteproc_dir, jobs, anteproc_L, used_seeds, organizedSeeds, multiple_waveforms, waveforms, anteprocDefaultData,
            anteprocJobs, varyingAnteprocVariables, anteprocJobDictTracker = anteprocJobDictTracker, injectionStartTimes = injectionStartTimes)
            
    #new loop to make anteproc files
    
    for jobNum in H1AnteprocJobNums:
        
        temp_anteproc_h_dict = deepcopy(commonParamsDictionary['anteproc_h'])
        temp_anteproc_h_dict = deepupdate(temp_anteproc_h_dict, anteprocHParamsList[jobNum - 1])
        for key, val in temp_anteproc_h_dict['stamp'].iteritems():
            temp_anteproc_h_dict['stamp.' + key] = val
        temp_anteproc_h_dict.pop('stamp')
        anteproc_dict = deepcopy(commonParamsDictionary['anteproc'])
        anteproc_dict.update(temp_anteproc_h_dict)
        anteproc_dict['ifo1'] = "H1"
        anteproc_dict['frameType1'] = "H1_" + input_params['frame_type']
        anteproc_dict['ASQchannel1'] = input_params['channel']
        
        with open(anteproc_dir + "/H1-anteproc_params_" + str(jobNum) + "new.txt", 'w') as h:
            print >> h, "\n".join([key + ' ' + str(val).lower() if not isinstance(val, basestring) else key + ' ' + val for key, val in anteproc_dict.iteritems()])
            
    for jobNum in L1AnteprocJobNums:
        
        temp_anteproc_l_dict = deepcopy(commonParamsDictionary['anteproc_l'])
        temp_anteproc_l_dict = deepupdate(temp_anteproc_l_dict, anteprocLParamsList[jobNum - 1])
        for key, val in temp_anteproc_l_dict['stamp'].iteritems():
            temp_anteproc_l_dict['stamp.' + key] = val
        temp_anteproc_l_dict.pop('stamp')
        
        anteproc_dict = deepcopy(commonParamsDictionary['anteproc'])
        anteproc_dict.update(temp_anteproc_l_dict)
        anteproc_dict['ifo1'] = "L1"
        anteproc_dict['frameType1'] = "L1_" + input_params['frame_type']
        anteproc_dict['ASQchannel1'] = input_params['channel']
        
        with open(anteproc_dir + "/L1-anteproc_params_" + str(jobNum) + "new.txt", 'w') as h:
            print >> h, "\n".join([key + ' ' + str(val).lower() if not isinstance(val, basestring) else key + ' ' + val for key, val in anteproc_dict.iteritems()])        
      
        
    if jobs["constants"]["anteprocParamsH"]["doDetectorNoiseSim"] == "true" or jobs["constants"]["anteprocParamsL"]["doDetectorNoiseSim"] == "true":
        with open(anteproc_dir + "/seeds_for_simulated_data.txt", "w") as outfile:
            json.dump(organizedSeeds, outfile, sort_keys = True, indent = 4)
    if "num_jobs_to_vary" in varyingAnteprocVariables:
        print("\nVariable parameter option active.\n")
        with open(anteproc_dir + "/varying_parameters_input_record.txt", "w") as outfile:
            json.dump(varyingAnteprocVariables, outfile, sort_keys = True, indent = 4)
    else:
        print("\nVariable parameter option not active.\nIf it's supposed to be active, add 'anteproc_varying_param num_jobs_to_vary' option to input parameter file.\n")
    
    anteproc_grand_stochtrack_values["anteproc.inmats1"] = anteproc_dir + "/H-H1_map"
    anteproc_grand_stochtrack_values["anteproc.inmats2"] = anteproc_dir + "/L-L1_map"
    anteproc_grand_stochtrack_values["anteproc.jobfile"] = newAdjustedJobPath
    
    added_anteproc_dict = {"loadFiles": True,
                            "timeShift1": 0,
                            "timeShift2": 0,
                            "jobFileTimeShift": True,
                            "bkndstudy": False,
                            "bkndstudydur": 100,
                            "jobfile": newAdjustedJobPath}
    #NEW LOOP, hopefully replaces next 2 loops
    #this can likely be moved to much earlier
    #need to add support for varying parameters
    for i in range(0, len(stochtrackParamsList)):
        stochtrackParamsList[i]['grandStochtrackParams']['params']['anteproc']['inmats1'] = anteproc_dir + "/H-H1_map"
        stochtrackParamsList[i]['grandStochtrackParams']['params']['anteproc']['inmats2'] = anteproc_dir + "/L-L1_map"
        if "injection_tags" in stochtrackParamsList[i]:
            stochtrackParamsList[i]['grandStochtrackParams']['params']['anteproc']['inmats1'] += "_" + stochtrackParamsList[i]["injection_tags"]
            stochtrackParamsList[i]['grandStochtrackParams']['params']['anteproc']['inmats2'] += "_" + stochtrackParamsList[i]["injection_tags"]
        stochtrackParamsList[i]['grandStochtrackParams']['params']['anteproc'].update(added_anteproc_dict)
        
        jobDir = create_dir(jobsBaseDir + "/" + "job_group_" + str(stochtrackParamsList[i]["grandStochtrackParams"]["params"]["job_group"]) + "/job_" + str(i + 1))
        
        stochtrackParamsList[i]["jobDir"] = jobDir
        stochtrackParamsList[i]["stochtrackInputDir"] = create_dir(jobDir + "/grandStochtrackInput")
        stochtrackParamsList[i]["grandstochtrackOutputDir"] = create_dir(jobDir + "/grandStochtrackOutput")
        stochtrackParamsList[i]["plotDir"] = create_dir(jobDir + "/grandStochtrackOutput" + "/plots")
        
    
    for job in jobs:
            #"adjust inmats entries here maybe if needed? yes."
        for anteprocParameter in anteprocOrder:
            if (anteprocParameter == "anteproc.inmats1" or anteprocParameter == "anteproc.inmats2") and "injection_tags" in jobs[job]:
                jobs[job]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job]["grandStochtrackParams"]["params"], anteprocParameter, anteproc_grand_stochtrack_values[anteprocParameter] + "_" + jobs[job]["injection_tags"])
            else:
                jobs[job]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job]["grandStochtrackParams"]["params"], anteprocParameter, anteproc_grand_stochtrack_values[anteprocParameter])
    
    '''
        # cycle through jobs
    print("Creating job directories")
    for job in jobs:
        if job != "constants":
            jobs[job]["jobDir"] = []
            jobs[job]["stochtrackInputDir"] = []
            jobs[job]["grandstochtrackOutputDir"] = []
            jobs[job]["plotDir"] = []
    
            if multiple_job_group_version:
                for index in range(varyingAnteprocVariables["num_jobs_to_vary"]):
                    temp_number = index + 1
                    temp_suffix = "_v" + str(temp_number)
                    jobs = create_job_directories(jobs, jobsBaseDir, job, temp_suffix)
            else:
                jobs = create_job_directories(jobs, jobsBaseDir, job)
                """# stochtrack_day_job_num (injection? gps time?)
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
                jobs[job]["plotDir"] = plotDir"""
    
            # NOTE: recording any directories other than the base job directory may not have any value
            # because the internal structure of each job is identical.
    '''
        # build dag directory, support directories
    dagDir = create_dir(baseDir + "/dag")
    dagLogDir = create_dir(dagDir + "/dagLogs")
    logDir = create_dir(dagLogDir + "/logs")
    
    
    # create grandstochtrack execution script
    
    print("Creating shell scripts")
    grandStochtrack_script_file = dagDir + "/grand_stochtrack.sh"
    if jobs['constants']['grandStochtrackParams']['params']['savePlots']:
        write_grandstochtrack_bash_script(grandStochtrack_script_file, grandStochtrackExecutable, STAMP_setup_script)
    else:
        write_grandstochtrack_bash_script(grandStochtrack_script_file, grandStochtrackExecutableNoPlots, STAMP_setup_script)
    os.chmod(grandStochtrack_script_file, 0o744)
    
    matlabMatrixExtractionExectuable_script_file = dagDir + "/matlab_matrix_extraction.sh"
    write_grandstochtrack_bash_script(matlabMatrixExtractionExectuable_script_file, input_params['matlabMatrixExtractionExectuable'], STAMP_setup_script)
    os.chmod(matlabMatrixExtractionExectuable_script_file, 0o744)
    
    anteprocExecutable_script_file = dagDir + "/anteproc.sh"
    write_anteproc_bash_script(anteprocExecutable_script_file, anteprocExecutable, STAMP_setup_script)
    os.chmod(anteprocExecutable_script_file, 0o744)
    
    # If relative injection value set, override any existing injection time with calculated relative injection time.
    
    # find frame files
    for tempJob in set(H1_jobs):
        print("Finding frames for job " + str(tempJob) + " for H1")
        tempJobData = jobDataDict[str(tempJob)]
        if anteproc_H["doDetectorNoiseSim"] == "false":
            temp_frames = create_frame_file_list("H1_" + input_params['frame_type'], str(times[tempJob][1] - 2), str(times[tempJob][1] + 1602), "H")
            create_cache_and_time_file(temp_frames, "H",tempJob,cacheDir, archived_frames_okay = archived_frames_okay)
        else:
            create_fake_cache_and_time_file(str(times[tempJob][1] - 2), str(times[tempJob][1] + 1602), "H", tempJob, fakeCacheDir)
    for tempJob in set(L1_jobs):
        print("Finding frames for job " + str(tempJob) + " for L1")
        tempJobData = jobDataDict[str(tempJob)]
        if anteproc_L["doDetectorNoiseSim"] == "false":
            temp_frames = create_frame_file_list("L1_" + input_params['frame_type'], str(times[tempJob][1] - 2), str(times[tempJob][1] + 1602), "L")
            create_cache_and_time_file(temp_frames, "L",tempJob,cacheDir, archived_frames_okay = archived_frames_okay)
        else:
            create_fake_cache_and_time_file(str(times[tempJob][1] - 2), str(times[tempJob][1] + 1602), "L", tempJob, fakeCacheDir)
            
    for job in stochtrackParamsList:
        job['grandStochtrackParams'] = recursive_ints_to_floats(job['grandStochtrackParams'])
        sio.savemat(job['stochtrackInputDir'] + "/params_new.mat", job['grandStochtrackParams'])
        
    # write preproc parameter files for each job
    '''
    print("Saving grand_stochtrack paramter files")
    for job in jobs:
        if job != "constants":
            jobs[job]["grandStochtrackParams"]["params"]["jobsFile"] = newJobPath
            # write stochtrack parameter files for each job
            jobs[job]['grandStochtrackParams']['params'] = load_default_dict(jobs[job]['grandStochtrackParams']['params'] , defaultDictionary)
            print("The way this following line is done needs to be reviewed.")
            jobs[job]['grandStochtrackParams'] = load_default_dict(jobs[job]['grandStochtrackParams'], jobs["constants"]['grandStochtrackParams'])
    
            # new for loop to handle possible multiple job group versions due to variable parameters
            for temp_index in range(len(jobs[job]["plotDir"])):
                temp_number = temp_index+1
                if "varying_injection_start" in jobs["constants"]:
                    temp_suffix = "_v" + str(temp_number) + "_" + job
                else:
                    temp_suffix = "_v" + str(temp_number)
    
                # put output directories in grand_stochtrack dictionary
                jobs[job]["grandStochtrackParams"]["params"]["plotdir"] = jobs[job]["plotDir"][temp_index] + "/"
                jobs[job]["grandStochtrackParams"]["params"]["outputfilename"] = jobs[job]["grandstochtrackOutputDir"][temp_index] + "/map"
                jobs[job]["grandStochtrackParams"]["params"]["ofile"] = jobs[job]["grandstochtrackOutputDir"][temp_index] + "/bknd"
                if "lonetrack" in jobs["constants"]["grandStochtrackParams"]["params"]["stochtrack"]:
                    if jobs["constants"]["grandStochtrackParams"]["params"]["stochtrack"]["lonetrack"] == 1:
                        temp_directory = create_dir(jobs[job]["grandStochtrackParams"]["params"]["plotdir"]+"tmp")
                        jobs[job]["grandStochtrackParams"]["params"]["lonetrackdir"] = temp_directory + "/"
    
                if multiple_job_group_version:
                    base_inmat1 = jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats1"]
                    base_inmat2 = jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats2"]
                    jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats1"] = base_inmat1 + temp_suffix
                    jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats2"] = base_inmat2 + temp_suffix
    
                sio.savemat(jobs[job]["stochtrackInputDir"][temp_index] + "/" + "params.mat", jobs[job]["grandStochtrackParams"])
    
                if multiple_job_group_version:
                    jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats1"] = base_inmat1
                    jobs[job]["grandStochtrackParams"]["params"]["anteproc"]["inmats2"] = base_inmat2
    '''
    # order plots by job
    
    # This line likely needs fixing if it's going to work with the variable parameters. otherwise it's fine.
    '''
    jobTempDict = dict((int(job[job.index("_")+1:]),{"job" : job, "job dir" : "job_group_" + jobs[job]["job_group"] + "/" + job}) for job in [x for x in jobs if x != "constants"])
    
    if input_params['burstegard']:
        plotTypeList = ["SNR", "Largest Cluster", "All Clusters", "sig map", "y map", "Xi snr map"]
        plotTypeDict = {"SNR" : "snr.png", "Largest Cluster" : "large_cluster.png", "All Clusters": "all_clusters.png", "sig map" : "sig_map.png", "y map" : "y_map.png", "Xi snr map" : "Xi_snr_map.png"}
    elif all_clusters:
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
    print("Creating webpage")
    webGen.make_display_page("jobs", baseDir, jobOrderWeb, "grandStochtrackOutput/plots", plotTypeList, plotTypeDict, outFile)
    '''
    # build DAGs
    # preproc DAG
    # build submission file
    doGPU = input_params["doGPU"]
    if doGPU and not input_params['burstegard']:
        extract_from_gpu = True
    else:
        extract_from_gpu = False

    print("Creating dag and sub files")
    #create_anteproc_dag_v6(jobs, grandStochtrack_script_file, matlabMatrixExtractionExectuable_script_file, anteprocExecutable_script_file, dagDir, newJobPath, H1_jobs, L1_jobs, anteprocJobs, multiple_job_group_version, job_order = jobOrder, use_gpu = doGPU, restrict_cpus = restrict_cpus, no_job_retry = no_job_retry, extract_from_gpu = extract_from_gpu, single_cpu = input_params['single_cpu'])
    
    anteprocSub = write_anteproc_sub_file(input_params['anteprocMemory'], anteprocExecutable_script_file, dagDir, input_params['accountingGroup'])
    stochtrackSub = write_stochtrack_sub_file(input_params['grandStochtrackMemory'], grandStochtrack_script_file, dagDir, input_params['accountingGroup'], input_params['doGPU'], input_params['numCPU'])
    write_dag(dagDir, anteproc_dir, newJobPath, H1AnteprocJobNums, L1AnteprocJobNums, anteprocSub, stochtrackParamsList, stochtrackSub, input_params['maxJobsAnteproc'], input_params['maxJobsGrandStochtrack'])
    
    print("NOTE: Job ordering is not currently set up to handle multiple jobs of the same number as numbered by this program.")
    
    #create summary of parameters
    generate_summary(input_params, baseDir)
    
    # create webpage
    
    # run top DAG
    import pprint
    pprint.pprint(jobs, open(glueFileLocation(input_params['outputDir'], "jobs_dict.txt"), "w"))
    pprint.pprint(commonParamsDictionary, open(glueFileLocation(input_params['outputDir'], "commonParams_dict.txt"), "w"))
    pprint.pprint(anteprocHParamsList, open(glueFileLocation(input_params['outputDir'], "anteprocHParams_list.txt"), "w"))
    pprint.pprint(anteprocLParamsList, open(glueFileLocation(input_params['outputDir'], "anteprocLParams_list.txt"), "w"))
    pprint.pprint(stochtrackParamsList, open(glueFileLocation(input_params['outputDir'], "stochtrackParams_list.txt"), "w"))

if __name__ == "__main__":
    main()
