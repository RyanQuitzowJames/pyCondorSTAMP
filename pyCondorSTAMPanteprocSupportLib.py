from __future__ import division
from pyCondorSTAMPLib import nested_dict_entry
from grandStochtrackSupportLib import load_if_number, load_number

def parse_jobs(raw_data, quit_program):
    'Helper function to parse jobs for STAMP'
    print("Fix this (grand_stochtrack selection) part to handle numbers properly! And less jumbled if possible!")
    jobs = {}
    commentsToPrintIfVerbose = []
    job_groups = []
    jobDuplicates = False
    anteproc_jobs_1 = []
    anteproc_jobs_2 = []
    seeds = []
    #waveforms = {'default':None}
    waveforms = {}
    varying_anteproc_variables = {"set": {}, "random": {}, "num_space": {}}
    # set is a given set, random is from a uniform distribution, and num_space is evenly spaced as viewed on either a linear or logarithmic axis.
    if not quit_program:
        for line in raw_data:
            temp = line[0].lower()
            if temp[0] in ["#", "%"]:
                commentsToPrintIfVerbose.append(line)
            elif len(line) == 1:
                print("Warning, line contains only 1 entry:")
                print(line)
                quit_program = True
            # user set defaults
            elif temp == 'constants': # make this 'general' instead at some point
                job_key = temp
                if job_key not in jobs:
                    jobs[job_key] = {}
                if "preprocParams" not in jobs[job_key]:
                    jobs[job_key]["preprocParams"] = {}
                if "anteprocParamsH" not in jobs[job_key]:
                    jobs[job_key]["anteprocParamsH"] = {}
                if "anteprocHjob_seeds" not in jobs[job_key]:
                    jobs[job_key]["anteprocHjob_seeds"] = {}
                if "anteprocH_parameters" not in jobs[job_key]:
                    jobs[job_key]["anteprocH_parameters"] = {}
                if "anteprocH_waveforms" not in jobs[job_key]:
                    jobs[job_key]["anteprocH_waveforms"] = {}
                if "anteprocParamsL" not in jobs[job_key]:
                    jobs[job_key]["anteprocParamsL"] = {}
                if "anteprocLjob_seeds" not in jobs[job_key]:
                    jobs[job_key]["anteprocLjob_seeds"] = {}
                if "anteprocL_parameters" not in jobs[job_key]:
                    jobs[job_key]["anteprocL_parameters"] = {}
                if "anteprocL_waveforms" not in jobs[job_key]:
                    jobs[job_key]["anteprocL_waveforms"] = {}
                if "grandStochtrackParams" not in jobs[job_key]:
                    jobs[job_key]["grandStochtrackParams"] = {}
                    jobs[job_key]["grandStochtrackParams"]["params"] = {}
            elif temp == 'waveform':
                if len(line) != 3:
                    print("Alert, the following line contains a different number of entries than 3:")
                    print(line)
                    quit_program = True
                else:
                    wave_id = line[1]
                    wave_file_path = line[2]
                    waveforms[wave_id] = wave_file_path
            # job specific settings
            elif temp == 'job':
                job_key = temp + "_" + line[1]
                temp_key = job_key
                temp_num = 1
                #print(jobs.keys())
                #print(temp_key)
                while temp_key in jobs:
                    jobDuplicates = True
                    temp_num += 1
                    temp_key = job_key + 'v' + str(temp_num)
                    print(temp_key)
                    if temp_key not in jobs:
                        print("WARNING: Duplicate of job_" + line[1] + ". Renaming " + temp_key + ".")
                job_key = temp_key
                if job_key not in jobs:
                    jobs[job_key] = {}
                jobs[job_key]["jobNum"] = line[1]
                if "preprocParams" not in jobs[job_key]:
                    jobs[job_key]["preprocParams"] = {}
                if "anteprocParamsH" not in jobs[job_key]:
                    jobs[job_key]["anteprocParamsH"] = {}
                if "anteprocParamsL" not in jobs[job_key]:
                    jobs[job_key]["anteprocParamsL"] = {}
                if "grandStochtrackParams" not in jobs[job_key]:
                    jobs[job_key]["grandStochtrackParams"] = {}
                    jobs[job_key]["grandStochtrackParams"]["params"] = {}
                if "job_group" not in jobs[job_key]:
                    jobs[job_key]["job_group"] = None
            # job_group
            elif temp == "job_group":
                jobs[job_key]["job_group"] = line[1]
                job_groups += [line[1]]
            # info for adjusted job file
            elif temp == "job_start_shift":
                jobs[job_key]["job_start_shift"] = line[1]
            elif temp == "job_duration":
                jobs[job_key]["job_duration"] = line[1]
            # preproc settings
            elif temp == "preproc":
                if line[1].lower() == "job":
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = line[2]
                        jobs[job_key]["preprocJobs"] = jobNumber
                else:
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobs[job_key]["preprocParams"][line[1]] = line[2]
            elif temp == "anteproc_h":
                if line[1].lower() == "job":
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = line[2]
                        jobs[job_key]["preprocJobs"] = jobNumber
                elif line[1] == "job_seed":
                    if len(line) != 4:
                        print("Alert, the following line contains a different number of entries than 4:")
                        print(line)
                        quit_program = True
                    elif line[2] in jobs['constants']["anteprocHjob_seeds"]:
                        print("Alert, the seed for job " + line[2] + " is already recorded. Quiting program.")
                        quit_program = True
                    elif line[3] in seeds:
                        print("Alert, the seed " + line[3] + " has already been used in another job. Quiting program.")
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        seed = int(line[3])
                        jobs['constants']["anteprocHjob_seeds"][jobNumber] = seed
                        seeds += [seed]
                elif line[1] == "anteproc_param":
                    if len(line) != 5:
                        print("Alert, the following line contains a different number of entries than 5:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        parameter = line[3]
                        value = load_if_number(line[4])
                        if jobNumber not in jobs['constants']["anteprocH_parameters"]:
                            jobs['constants']["anteprocH_parameters"][jobNumber] = {}
                        jobs['constants']["anteprocH_parameters"][jobNumber][parameter] = value
                elif line[1] == "anteproc_injection":
                    if len(line) <4:
                        print("Alert, the following line contains less than 4:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        wave_ids = [x.strip("[]") for group in line[3:] for x in group.split(',')]
                        if jobNumber not in jobs['constants']["anteprocH_waveforms"]:
                            jobs['constants']["anteprocH_waveforms"][jobNumber] = wave_ids
                        else:
                            print("Duplicate waveform assignment line:")
                            print(line)
                            quit_program = True
                else:
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobs[job_key]["anteprocParamsH"][line[1]] = line[2]
            elif temp == "anteproc_l":
                if line[1].lower() == "job":
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = line[2]
                        jobs[job_key]["preprocJobs"] = jobNumber
                elif line[1] == "job_seed":
                    if len(line) != 4:
                        print("Alert, the following line contains a different number of entries than 4:")
                        print(line)
                        quit_program = True
                    elif line[2] in jobs['constants']["anteprocLjob_seeds"]:
                        print("Alert, the seed for job " + line[2] + " is already recorded. Quiting program.")
                        quit_program = True
                    elif line[3] in seeds:
                        print("Alert, the seed " + line[3] + " has already been used in another job. Quiting program.")
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        seed = int(line[3])
                        jobs['constants']["anteprocLjob_seeds"][jobNumber] = seed
                        seeds += [seed]
                elif line[1] == "anteproc_param":
                    if len(line) != 5:
                        print("Alert, the following line contains a different number of entries than 5:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        parameter = line[3]
                        value = load_if_number(line[4])
                        if jobNumber not in jobs['constants']["anteprocL_parameters"]:
                            jobs['constants']["anteprocL_parameters"][jobNumber] = {}
                        jobs['constants']["anteprocL_parameters"][jobNumber][parameter] = value
                elif line[1] == "anteproc_injection":
                    if len(line) <4:
                        print("Alert, the following line contains less than 4:")
                        print(line)
                        quit_program = True
                    else:
                        jobNumber = int(line[2])
                        wave_ids = [x.strip("[]") for group in line[3:] for x in group.split(',')]
                        if jobNumber not in jobs['constants']["anteprocL_waveforms"]:
                            jobs['constants']["anteprocL_waveforms"][jobNumber] = wave_ids
                        else:
                            print("Duplicate waveform assignment line:")
                            print(line)
                            quit_program = True
                else:
                    if len(line) != 3:
                        print("Alert, the following line contains a different number of entries than 3:")
                        print(line)
                        quit_program = True
                    else:
                        jobs[job_key]["anteprocParamsL"][line[1]] = line[2]
            elif temp == "injection_tag":
                if len(line) != 2:
                    print("Alert, the following line contains a different number of entries than 2:")
                    print(line)
                    quit_program = True
                else:
                    #wave_ids = [x.strip("[]") for group in line[1:] for x in group.split(',')]
                    jobs[job_key]["injection_tags"] = line[1]
            elif temp == "anteproc_varying_param":
                temp_variable = line[2]
                if line[1] == "num_jobs_to_vary":
                    if int(line[2]) != float(line[2]) or int(line[2]) <= 0:
                        print("Error, please choose a positive integer value for 'num_jobs_to_vary'. Value chosen was:")
                        print(line[2])
                        quit_program = True
                    varying_anteproc_variables["num_jobs_to_vary"] = int(line[2])
                elif line[1] == "set":
                    varying_anteproc_variables["set"][temp_variable] = [x for x in line[3:]]
                elif line[1] == "random":
                    distribution_type = line[3]
                    if distribution_type != "uniform":
                        print("Alert, random varying parameters should be from uniform distribution. Other distributions not yet recognized. Unrecognized option:")
                        print(distribution_type)
                        quit_program = True
                    elif distribution_type == "uniform" and len(line) != 6:
                        print("Alert, the following line contains a different number of entries than 6:")
                        print(line)
                        quit_program = True
                    else:
                        lower_range = line[4]
                        upper_range = line[5]
                        distribution_info = [distribution_type, lower_range, upper_range]
                        varying_anteproc_variables["random"][temp_variable] = distribution_info
                elif line[1] = "num_space":
                    distribution_type = line[3]
                    if distribution_type != "linear" or distribution_type != "logarithmic":
                        print("Alert, random varying parameters should be linear or logarithmic. Other distributions not yet recognized. Unrecognized option:")
                        print(distribution_type)
                        quit_program = True
                    elif distribution_type == "linear" and len(line) != 6:
                        print("Alert, the following line contains a different number of entries than 6:")
                        print(line)
                        quit_program = True
                    elif distribution_type == "logarithmic" and (len(line) != 6 or len(line) != 7):
                        print("Alert, the following line contains a different number of entries than 6 or 7:")
                        print(line)
                        quit_program = True
                    else:
                        lower_range = line[4]
                        upper_range = line[5]
                        distribution_info = [distribution_type, lower_range, upper_range]
                        if distribution_type == "logarithmic" and if len(line) == 7:
                            base = line[6]
                            distribution_info += [base]
                        varying_anteproc_variables["num_space"][temp_variable] = distribution_info
                else:
                    print("Alert, the following line contains a non-recognized option for anteproc_varying_param:")
                    print(line)
                    quit_program = True
            elif temp == "grandstochtrack":
                #print("Fix this part to handle numbers properly! And less jumbled if possible!")
                if line[1] == "StampFreqsToRemove":
                    rawFreqs = [x.split(",") for x in line[2:]] # this part actually just strips the comma. The really frequency splitting is actually due to the list comprehension itself, or rather this part: line[2:]. Since the frequencies were already split in an earlier line.
                    # not a terrible check to have, just in case commas are used and spaces forgotten
                    rawFreqs = [item for sublist in rawFreqs for item in sublist]
                    rawFreqs = [x.replace("[", "") if "[" in x else x for x in rawFreqs]
                    rawFreqs = [x.replace("]", "") if "]" in x else x for x in rawFreqs]
                    freqList = [float(x) for x in rawFreqs if x]#[load_number(x) for x in rawFreqs if x]
                    #print("StampFreqsToRemove")
                    #print(freqList)
                    jobs[job_key]["grandStochtrackParams"]["params"][line[1]] = freqList
                elif line[1] == "doGPU" and job_key != "constants":
                    print("Current job: " + job_key)
                    quit_program = True
                    print("WARNING: non-default value for 'doGPU' detected. This functionality is not currently supported but may be supported in a future version. Quitting script. \n\nPress enter to exit.")
                    version_input("")
                elif len(line) != 3:
                    print("Alert, the following line contains a different number of entries than 3:")
                    print(line)
                    quit_program = True
                    # if statements to catch if attribute is boolean. This may need to be handled another way, but
                    # check in the created .mat file to see if this successfully sets the variables to booleans.
                elif line[2].lower() == "true":
                    jobs[job_key]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job_key]["grandStochtrackParams"]["params"], line[1], True)
                elif line[2].lower() == "false":
                    jobs[job_key]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job_key]["grandStochtrackParams"]["params"], line[1], False)
                    # maybe place here if statments to catch if the start and end times are being set, and if so
                    # inform the user that this will overwite the times from the job files and prompt user for input
                    # on whether this is okay. If not, quit program so user can fix input file.
                else:
                    if line[1] == "anteproc.jobNum1":
                        anteproc_jobs_1 += [int(line[2])]
                    if line[1] == "anteproc.jobNum2":
                        anteproc_jobs_2 += [int(line[2])]
                    jobs[job_key]["grandStochtrackParams"]["params"] = nested_dict_entry(jobs[job_key]["grandStochtrackParams"]["params"], line[1], load_if_number(line[2]))
            else:
                print("WARNING: Error in config file. Option " + temp + " not recognized. Quitting program.")
                quit_program = True
        if 'constants' not in jobs:
            jobs['constants'] = {}
            jobs['constants']["preprocParams"] = {}
            jobs['constants']["grandStochtrackParams"] = {}
            jobs['constants']["grandStochtrackParams"]["params"] = {}
    return quit_program, jobs, commentsToPrintIfVerbose, job_groups, jobDuplicates, anteproc_jobs_1, anteproc_jobs_2, waveforms, varying_anteproc_variables

def anteproc_setup(anteproc_directory, anteproc_default_data, job_dictionary, cache_directory):
    anteproc_H = dict((x[0], x[1]) if len(x) > 1 else (x[0], "") for x in anteproc_default_data)
    anteproc_L = dict((x[0], x[1]) if len(x) > 1 else (x[0], "") for x in anteproc_default_data)
    for temp_param in job_dictionary["constants"]["anteprocParamsH"]:
        anteproc_H[temp_param] = job_dictionary["constants"]["anteprocParamsH"][temp_param]
    for temp_param in job_dictionary["constants"]["anteprocParamsL"]:
        anteproc_L[temp_param] = job_dictionary["constants"]["anteprocParamsL"][temp_param]
    """if "doDetectorNoiseSim" in job_dictionary["constants"]["anteprocParamsH"]:
        simulated = job_dictionary["constants"]["anteprocParamsH"]["doDetectorNoiseSim"]
        anteproc_H["doDetectorNoiseSim"] = simulated
        anteproc_L["doDetectorNoiseSim"] = simulated #"""
    anteproc_H["outputfiledir"] = anteproc_directory + "/"
    anteproc_L["outputfiledir"] = anteproc_directory + "/"
    """if "DetectorNoiseFile" in job_dictionary["constants"]["anteprocParamsH"]:
        anteproc_H["DetectorNoiseFile"] = job_dictionary["constants"]["anteprocParamsH"]["DetectorNoiseFile"]
    if "DetectorNoiseFile" in job_dictionary["constants"]["anteprocParamsL"]:
        anteproc_L["DetectorNoiseFile"] = job_dictionary["constants"]["anteprocParamsL"]["DetectorNoiseFile"]

    if "segmentDuration" in job_dictionary["constants"]["anteprocParamsH"]:
        anteproc_H["segmentDuration"] = job_dictionary["constants"]["anteprocParamsH"]["segmentDuration"]
    if "segmentDuration" in job_dictionary["constants"]["anteprocParamsL"]:
        anteproc_L["segmentDuration"] = job_dictionary["constants"]["anteprocParamsL"]["segmentDuration"] #"""
    anteproc_H["gpsTimesPath1"] = cache_directory
    anteproc_H["frameCachePath1"] = cache_directory
    anteproc_L["gpsTimesPath1"] = cache_directory
    anteproc_L["frameCachePath1"] = cache_directory

    anteproc_H["ifo1"] = "H1"
    anteproc_H["ASQchannel1"] = "LDAS-STRAIN"
    anteproc_H["frameType1"] = "H1_LDAS_C02_L2"
    anteproc_L["ifo1"] = "L1"
    anteproc_L["ASQchannel1"] = "LDAS-STRAIN"
    anteproc_L["frameType1"] = "L1_LDAS_C02_L2"
    return anteproc_H, anteproc_L

def save_anteproc_paramfile(anteproc_dict, anteproc_name, anteproc_default_data):
    print("Saving anteproc parameter file...")
    default_keys = [x[0] for x in anteproc_default_data]
    output_string = "\n".join(str(key) + " " + str(anteproc_dict[key]) for key in default_keys)
    output_string += "\n" + "\n".join(str(key) + " " + str(anteproc_dict[key]) for key in anteproc_dict if key not in default_keys)
    with open(anteproc_name, "w") as outfile:
        outfile.write(output_string)

def adjusted_job_file_name(filePath, outputDirectory):
    if "/" in filePath:
        reversePath = filePath[::-1]
        reverseName = reversePath[:reversePath.index("/")]
        fileName = reverseName[::-1]
    else:
        fileName = filePath
    fileName_front = fileName[:fileName.index(".")]
    fileName_back = fileName[fileName.index("."):]
    fileName = fileName_front + "_postprocessing" + fileName_back
    if outputDirectory[-1] == "/":
        outputPath = outputDirectory + fileName
    else:
        outputPath = outputDirectory + "/" + fileName
    return outputPath

def adjust_job_file(filePath, outputDirectory, job_dictionary):
    outputPath = adjusted_job_file_name(filePath, outputDirectory)
    #NSPI = int(job_dictionary["constants"]["preprocParams"]["numSegmentsPerInterval"])
    #bufferSecs = int(job_dictionary["constants"]["preprocParams"]["bufferSecs1"])
    #numSegmentsPerInterval
    start_shift = int(job_dictionary["constants"]["job_start_shift"])
    duration = int(job_dictionary["constants"]["job_duration"])
    with open(filePath, "r") as infile:
        data = [[int(x) for x in line.split()] for line in infile]
    data2 = [[x[0], x[1] + start_shift, x[1] + start_shift + duration, duration] for x in data]
    text = "\n".join(" ".join(str(x) for x in line) for line in data2)
    with open(outputPath,"w") as outfile:
        outfile.write(text)
    return outputPath

#def check_on_the_fly_injection(anteproc_dict, job_dictionary, quit_program, specific_job = "constants"):
def check_on_the_fly_injection(job_dictionary, quit_program, specific_job = "constants"):
    on_the_fly_bool = False # When true, this will ignore an waveforms in the waveform bank and use on the fly instead
    if ("stamp.inj_type" in job_dictionary[specific_job]["anteprocParamsH"] or "stamp.inj_type" in job_dictionary[specific_job]["anteprocParamsL"])
    and not ("stamp.inj_type" in job_dictionary[specific_job]["anteprocParamsH"] and "stamp.inj_type" in job_dictionary[specific_job]["anteprocParamsL"]):
        print("WARNING: injection type set in one but not both detectors. Quitting program.")
        quit_program = True
    elif job_dictionary[specific_job]["anteprocParamsH"]["stamp.inj_type"] != "half_sg" and job_dictionary[specific_job]["anteprocParamsL"]["stamp.inj_type"] == "half_sg":
        print("WARNING: injection type not the same in both detectors. Quitting program.")
        quit_program = True
    elif job_dictionary[specific_job]["anteprocParamsH"]["stamp.inj_type"] == "half_sg" and job_dictionary[specific_job]["anteprocParamsL"]["stamp.inj_type"] == "half_sg":
        on_the_fly_bool = True
    return on_the_fly_bool, quit_program

varying_anteproc_variables

def convert_cosiota_to_iota(temp_param, temp_val):
    if temp_param == "stamp.iota":
        print("\nWARNING: Parameter " + temp_param + " found. Special case to vary in cos(iota) instead of iota. Edit code to change this option.")
        temp_val = np.arccos(temp_val)
    return temp_val

def handle_varying_variables_and_save_anteproc_paramfile(varying_anteproc_variables, anteproc_dict, anteproc_file_name, anteproc_default_data, quit_program):
    "This one applies varying variables if needed"
    if "num_jobs_to_vary" in varying_anteproc_variables:
        base_output_file_name = anteproc_dict["outputfilename"]
        num_variations = varying_anteproc_variables["num_jobs_to_vary"]
        for temp_param in varying_anteproc_variables["set"]:
            if len(varying_anteproc_variables["set"][temp_param]) != num_variations:
                print("ERROR: Number of entries in set for parameter " + temp_param + " is not equal to chosen number of variation (" + str(num_variations) + "). Quitting program.")
                quit_program = True

        spaces = {}
        for temp_param in varying_anteproc_variables["num_space"]:
            temp_range = [load_number_pi(x) for x in varying_anteproc_variables["num_space"][temp_param][1:]]
            distribution_type = varying_anteproc_variables["num_space"][temp_param][0]

            if distribution_type == "linear":
                spaces[temp_param] = np.linspace(temp_range[0], temp_range[1], num_variations)
            elif distribution_type == "logarithmic":
                if len(temp_range) == 3:
                    temp_base = temp_range[2]
                else:
                    temp_base = np.e
                spaces[temp_param] = np.logspace(temp_range[0], temp_range[1], num_variations, base = temp_base)

        for variation_index in range(0, num_variations):
            temp_number = variation_index + 1

            for temp_param in varying_anteproc_variables["set"]:
                temp_val = load_number_pi(varying_anteproc_variables["set"][variation_index])
                temp_val = convert_cosiota_to_iota(temp_param, temp_val)
                anteproc_dict[temp_param] = temp_val

            for temp_param in varying_anteproc_variables["random"]:
                temp_range = [load_number_pi(x) for x in varying_anteproc_variables["random"][temp_param][1:]]
                if varying_anteproc_variables["random"][temp_param][0] == "uniform":
                    temp_val = np.random.uniform(temp_range[0], temp_range[1])
                temp_val = convert_cosiota_to_iota(temp_param, temp_val)
                anteproc_dict[temp_param] = temp_val

            for temp_param in varying_anteproc_variables["num_space"]:
                temp_val = spaces[temp_param][variation_index]
                temp_val = convert_cosiota_to_iota(temp_param, temp_val)
                anteproc_dict[temp_param] = temp_val



            if waveform_bank[waveform_key]:
                temp_anteproc_name = anteproc_file_name[:anteproc_file_name.rindex(".")] + "_" + waveform_key + ".txt"
                anteproc_dict["stamp.file"] = waveform_bank[waveform_key]
                anteproc_dict["outputfilename"] = base_output_file_name + "_" + waveform_key
                #save_anteproc_paramfile(anteproc_dict, temp_anteproc_name, anteproc_default_data)
                #anteproc_file_names += [temp_anteproc_name]
                anteproc_file_names, quit_program = handle_varying_variables_and_save_anteproc_paramfile(varying_anteproc_variables, anteproc_dict, anteproc_file_name, anteproc_default_data)
            else:
                print("Warning! No waveform in selected waveform key!")
                quit_program = True"""
                ldkfjasdkl;fjadkls;fjadkls;"""

        anteproc_dict["outputfilename"] = base_output_file_name
    else:

        save_anteproc_paramfile(anteproc_dict, anteproc_file_name, anteproc_default_data)
        anteproc_file_names += [anteproc_file_name]

    return anteproc_file_names, quit_program

def handle_injections_and_save_anteproc_paramfile(multiple_waveforms, waveform_bank, varying_anteproc_variables, anteproc_dict, anteproc_file_name, anteproc_default_data, quit_program):

    anteproc_file_names = []

    if multiple_waveforms and not on_the_fly_bool:
        print("Handling multiple waveform injection preprocessing...")
        base_output_file_name = anteproc_dict["outputfilename"]

        for waveform_key in waveform_bank:

            if waveform_bank[waveform_key]:
                temp_anteproc_name = anteproc_file_name[:anteproc_file_name.rindex(".")] + "_" + waveform_key + ".txt"
                anteproc_dict["stamp.file"] = waveform_bank[waveform_key]
                anteproc_dict["outputfilename"] = base_output_file_name + "_" + waveform_key
                #save_anteproc_paramfile(anteproc_dict, temp_anteproc_name, anteproc_default_data)
                #anteproc_file_names += [temp_anteproc_name]
                anteproc_file_names, quit_program = handle_varying_variables_and_save_anteproc_paramfile(varying_anteproc_variables, anteproc_dict, anteproc_file_name, anteproc_default_data)
            else:
                print("Warning! No waveform in selected waveform key!")
                quit_program = True

        anteproc_dict["outputfilename"] = base_output_file_name

    else:
        if on_the_fly_bool:
            print("\nSet for on the fly injections.\n\nNOTE: This code is currently not set up to properly handle multiple on the fly injections while varying other parameters unless every injected waveform is expected to be unique.\n")
        #save_anteproc_paramfile(anteproc_dict, anteproc_file_name, anteproc_default_data)
        #anteproc_file_names += [anteproc_file_name]
        anteproc_file_names, quit_program = handle_varying_variables_and_save_anteproc_paramfile(varying_anteproc_variables, anteproc_dict, anteproc_file_name, anteproc_default_data)

    return anteproc_file_names, quit_program

def anteproc_job_specific_setup(job_list, ifo, anteproc_directory, job_dictionary, anteproc_dict, used_seed_tracker, organized_seeds, multiple_waveforms, waveform_bank, anteproc_default_data, anteproc_jobs, quit_program):

    on_the_fly_bool, quit_program = check_on_the_fly_injection(job_dictionary, quit_program)
    need to have the code switch to on the fly production instead of the waveform stuff. in this case, can set anteproc stamp.file parameter to FAKE_WAVEFORM_FILE or something.

    for temp_job in job_list:
            anteproc_H_name_temp = anteproc_directory + "/" + ifo + "-anteproc_params_" + str(temp_job) + ".txt"

            if job_dictionary["constants"]["anteprocParamsH"]["doDetectorNoiseSim"] == "true":

                if temp_job in job_dictionary["constants"]["anteprocHjob_seeds"]:
                    temp_seed = job_dictionary["constants"]["anteprocHjob_seeds"][temp_job]
                    anteproc_dict["pp_seed"] = temp_seed
                else:
                    temp_seed = random.randint(0,2**32-1)
                    while temp_seed in used_seed_tracker:
                        temp_seed = random.randint(0,2**32-1)
                    used_seed_tracker += [temp_seed]
                    anteproc_dict["pp_seed"] = temp_seed
                organized_seeds[ifo][temp_job] = temp_seed

            if temp_job in job_dictionary['constants']["anteprocH_parameters"]:
                for temp_param in job_dictionary['constants']["anteprocH_parameters"][temp_job]:
                    anteproc_dict[temp_param] = job_dictionary['constants']["anteprocH_parameters"][temp_job][temp_param]

            anteproc_jobs[ifo][temp_job], quit_program = handle_injections_and_save_anteproc_paramfile(multiple_waveforms, waveform_bank, anteproc_dict,
                                                anteproc_H_name_temp, anteproc_default_data, quit_program)
    return anteproc_jobs, used_seed_tracker, organized_seeds, quit_program

load_number_pi(number):
    if "pi" in number:
        multiply = 1
        divide = 1
        if "*" in number:
            multiply = load_number(number[:number.index["*"]])
        if "/" in number:
            divide = load_number(number[number.index["/"]+1:])
        return multiply*np.pi/divide
    else:
        return load_number(number)
