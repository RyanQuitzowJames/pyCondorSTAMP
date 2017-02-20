from __future__ import division
import os
import json
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['legend.numpoints'] = 1

def glueFileLocation(directory, filename):
    output = None
    if directory[-1] == "/":
        if filename[0] == "/":
            output = directory + filename[1:]
        else:
            output = directory + filename
    else:
        if filename[0] == "/":
            output = directory + filename
        else:
            output = directory + "/" + filename
    return output

def getSNRandAlpha(file_path):
    temp_mat = sio.loadmat(file_path)
    temp_snr = temp_mat['stoch_out']['max_SNR'][0,0][0,0]
    temp_alpha = temp_mat['stoch_out']['params'][0,0][0,0]['stamp']['alpha'][0,0][0,0]
    temp_iota = float(temp_mat['stoch_out']['params'][0,0][0,0]['stamp']['iota'][0,0][0,0])
    temp_psi = float(temp_mat['stoch_out']['params'][0,0][0,0]['stamp']['psi'][0,0][0,0])
    return [temp_snr, temp_alpha, temp_iota, temp_psi]

def find_path(directory, temp_tag):
    temp_files = [glueFileLocation(directory, x) for x in os.listdir(directory) if "job_pairs_with_low_SNR_" in x]
    if temp_files:
        return temp_files
    else:
        temp_path = glueFileLocation(directory, "job_pairs_with_low_SNR_" + temp_tag + ".txt")
        return [temp_path]

def str_truncate(number, decimal_values = 2):
    power_ten = np.floor(np.log10(number))
    truncated_number = str(int(np.round(number/np.power(10,power_ten)*np.power(10,decimal_values))))
    truncated_number = truncated_number[0] + "." + truncated_number[1:] + "e" + str(int(power_ten))
    return truncated_number

def color_conversion(R, G, B):
    return (R/256, G/256, B/256)

def find_surrounding_values(target_value, iota_values, SNR_values):
    max_SNR_value = max(SNR_values)
    min_SNR_value = min(SNR_values)
    if not (max_SNR_value >= target_value) or not (min_SNR_value <= target_value) or min(iota_values) > 0:
        print("No values")
    else:
        SNR_lower_split = [SNR_values[x] for x in range(len(SNR_values)) if SNR_values[x] < target_value and iota_values[x] < 90]
        SNR_upper_split = [SNR_values[x] for x in range(len(SNR_values)) if SNR_values[x] >= target_value and iota_values[x] < 90]
        iota_lower_split = [iota_values[x] for x in range(len(SNR_values)) if SNR_values[x] < target_value and iota_values[x] < 90]
        iota_upper_split = [iota_values[x] for x in range(len(SNR_values)) if SNR_values[x] >= target_value and iota_values[x] < 90]
        lower_values = [[SNR_lower_split[ind], iota_lower_split[ind]] for ind, value in enumerate(SNR_lower_split) if value == max(SNR_lower_split)]
        upper_values = [[SNR_upper_split[ind], iota_upper_split[ind]] for ind, value in enumerate(SNR_upper_split) if value == min(SNR_upper_split)]
        print("lower values")
        print(lower_values)
        print("upper values")
        print(upper_values)

        transformed_lower = [lower_values[0][0], np.cos(np.radians(lower_values[0][1]))]
        transformed_upper = [upper_values[0][0], np.cos(np.radians(upper_values[0][1]))]
        cos_iota_slope = (transformed_upper[1] - transformed_lower[1])/(transformed_upper[0] - transformed_lower[0])
        shift_ammount = (target_SNR_value - transformed_lower[0])*cos_iota_slope
        cos_iota_target = transformed_lower[1]+shift_ammount
        iota_target = np.degrees(np.arccos(cos_iota_target))
        print("target values")
        print([target_value, iota_target])

def parse_waveform_params(input_string):
    temp_list = input_string.split(",")
    f_0_val = temp_list[0][1:-1].strip()
    f_0_unit = "Hz"
    tau_val = temp_list[2][2:-1].strip()
    tau_unit = "s"
    return " ".join([f_0_val, f_0_unit, tau_val, tau_unit])

#better to start making this structure everytime and saving it instead of the list.
def get_info(ordered_data, threshold_SNR, temp_temp_data, waveform_label, threshold_percentages, print_limit_detail, onsourceJob, check_mat_files_onsource):
    test_lengths = [len(ordered_data[x]) for x in ordered_data]
    num_above_threshold = [[len([y for y in ordered_data[x] if y > threshold_SNR]), x] for x in ordered_data]
    passed_alphas = [[x[1] for ind, x in enumerate(num_above_threshold) if x[0]/test_lengths[ind] >= temp_percent] for temp_percent in threshold_percentages]
    if isinstance(passed_alphas, list) and len(passed_alphas) > 0:
        threshold_alphas = [min(x) if len(x) > 0 else None for x in passed_alphas]
    else:
        threshold_alphas = None
    print(waveform_label)
    print(test_lengths)
    if print_limit_detail:
        print([x[0] for x in num_above_threshold])
        print([x for x in ordered_data])
    percentiles = [num_above_threshold[x][0]/test_lengths[x] for x in range(len(test_lengths))]
    alphas_p = [x[1] for x in num_above_threshold]
    temp_indices = np.argsort(alphas_p)
    sorted_percentiles = [percentiles[x] for x in temp_indices]
    sorted_alphas_p = [alphas_p[x] for x in temp_indices]
    sorted_num_data = [test_lengths[x] for x in temp_indices]

    SNRs = [y[x][0] for y in temp_temp_data for x in y]
    alphas = [y[x][1] for y in temp_temp_data for x in y]

    if onsourceJob:
        onsourceRequiredString = "bknd_" + onsourceJob + ".mat"
        onsourceSNRs = [y[x][0] for y in temp_temp_data for x in y if onsourceRequiredString in x]
        onsourceAlphas = [y[x][1] for y in temp_temp_data for x in y if onsourceRequiredString in x]
        if check_mat_files_onsource:
            print([x for y in temp_temp_data for x in y if onsourceRequiredString in x])
            print(onsourceRequiredString)
        onsourceHighSNRs = [x for x in onsourceSNRs if x > threshold_SNR]
        onsourceHighAlphas = [onsourceAlphas[x] for x in range(len(onsourceAlphas)) if onsourceSNRs[x] > threshold_SNR]
        onsourceLowSNRs = [x for x in onsourceSNRs if x <= threshold_SNR]
        onsourceLowAlphas = [onsourceAlphas[x] for x in range(len(onsourceAlphas)) if onsourceSNRs[x] <= threshold_SNR]
    else:
        onsourceHighSNRs = None
        onsourceHighAlphas = None
        onsourceLowSNRs = None
        onsourceLowAlphas = None

    highSNRs = [x for x in SNRs if x > threshold_SNR]
    highAlphas = [alphas[x] for x in range(len(alphas)) if SNRs[x] > threshold_SNR]

    lowSNRs = [x for x in SNRs if x <= threshold_SNR]
    lowAlphas = [alphas[x] for x in range(len(alphas)) if SNRs[x] <= threshold_SNR]
    return [[sorted_percentiles, sorted_alphas_p, threshold_alphas, sorted_num_data], [highSNRs, highAlphas, lowSNRs, lowAlphas], [onsourceHighSNRs, onsourceHighAlphas, onsourceLowSNRs, onsourceLowAlphas]]

def normal_binomial_approximation_interval(proportion, confidence_level, number_samples):
    error_quantile = 1-confidence_level
    if 1-error_quantile/2 == 0.975:
        z_stat = 1.96
    else:
        print("error")
    delta = z_stat * np.sqrt(proportion*(1-proportion)/number_samples)
    return delta

def Wilson_score_interval(proportion, confidence_level, number_samples):
    error_quantile = 1-confidence_level
    if 1-error_quantile/2 == 0.975:
        z_stat = 1.96
    else:
        print("error")
    #z_stat = 1-error_quantile/2
    delta = z_stat * np.sqrt(proportion*(1-proportion)/number_samples + z_stat**2/(4*number_samples**2))
    upper_limit = (proportion + z_stat**2/(2*number_samples) + delta)/(1+z_stat**2/number_samples)
    lower_limit = (proportion + z_stat**2/(2*number_samples) - delta)/(1+z_stat**2/number_samples)
    return delta, upper_limit, lower_limit

def Wilson_score_interval_correction(proportion, confidence_level, number_samples):
    error_quantile = 1-confidence_level
    if 1-error_quantile/2 == 0.975:
        z_stat = 1.96
    else:
        print("error")
    #z_stat = 1-error_quantile/2
    delta = z_stat * np.sqrt(proportion*(1-proportion)/number_samples + z_stat**2/(4*number_samples**2))
    lower_limit = max([0, (2*number_samples*proportion + z_stat**2 - (z_stat*np.sqrt(z_stat**2 - 1/number_samples +4*number_samples*proportion*(1 - proportion) + (4*proportion - 2)) + 1))/(2*(number_samples+z_stat**2))])
    upper_limit = min([1, (2*number_samples*proportion + z_stat**2 + (z_stat*np.sqrt(z_stat**2 - 1/number_samples +4*number_samples*proportion*(1 - proportion) - (4*proportion - 2)) + 1))/(2*(number_samples+z_stat**2))])
    return delta, upper_limit, lower_limit

def frequentist_error_bars(proportion, number_samples):
    delta = np.sqrt(proportion*(1-proportion)/number_samples)
    return delta

def bayesian_error_bars(proportion, number_samples):
    number_found = number_samples*proportion
    expectation_proportion = (number_found + 1)/(number_samples + 2)
    variance = expectation_proportion*(1 - expectation_proportion)/(number_samples + 3)
    sigma = np.sqrt(variance)
    upper_limit = expectation_proportion + sigma
    lower_limit = expectation_proportion - sigma
    return sigma, upper_limit, lower_limit, expectation_proportion

def interpolate_threshold(proportions, alpha_values, threshold_proportion):
    if threshold_proportion in proportions:
        threshold_alpha = alpha_values[proportions.index(threshold_proportion)]
        interpolated = "Actual threshold"
    elif min(proportions) <= threshold_proportion <= max(proportions):
        proportion_above = min([x for x in proportions if x > threshold_proportion])
        proportion_below = max([x for x in proportions if x < threshold_proportion])
        alpha_above = alpha_values[proportions.index(proportion_above)]
        alpha_below = alpha_values[proportions.index(proportion_below)]
        log_h_above = np.log10(np.sqrt(alpha_above))
        log_h_below = np.log10(np.sqrt(alpha_below))
        #target_log_h = log_h_below + (log_h_above - log_h_below)/2
        difference = (threshold_proportion - proportion_below)*(log_h_above - log_h_below)/(proportion_above - proportion_below)
        target_log_h = log_h_below + difference
        threshold_alpha = np.power(10, target_log_h)**2
        # simple linear
        interpolated = "Interpolated threshold"
    else:
        threshold_alpha = None
        interpolated = "No threshold"
    return threshold_proportion, threshold_alpha, interpolated

def load_data(jsonPaths, name_tag, reloadJSONs=False):
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
    return temp_data_sets

def order_data(temp_data_sets, labels):
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
    return orderedData

def upper_limit_plot(ordered_data, threshold_percentages, labels, thresholdSNRs, data_info, outputPath, colours, name_tag, error_confidence_level, additional_plots=True, onsourceJob=None, pretty_version=True, save_plots=True, plot_mode="shaded", show_bayesian_average=False, plot_interpolated_points=False, xLimits=None, lockPlot=True):
    # if onsourceJob, set to actual onsource job number
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

def polarization_variation_plot():
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
