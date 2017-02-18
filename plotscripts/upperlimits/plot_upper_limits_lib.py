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
def get_info(ordered_data, threshold_SNR, temp_temp_data, waveform_label):
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
