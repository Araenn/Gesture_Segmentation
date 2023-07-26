from scipy.ndimage import gaussian_filter1d
from typing import List
from math import sqrt, pow

def derivative(normalised_timestamp_acc, x_accel):
    x_derivative = []
    t_i = normalised_timestamp_acc[0]
    for i in range(1, len(normalised_timestamp_acc)):
        t_i1 = normalised_timestamp_acc[i]
        a_x = (x_accel[i] - x_accel[i-1]) / (t_i1 - t_i)
        x_derivative.append(a_x)
        t_i = t_i1

    x_derivative.append(x_derivative[-1])

    return x_derivative


def simple_segmentation(timestamp, signal, sigma, threshold_multiplier):
    # Derivate the normalised data
    signal_derivative = derivative(timestamp, signal)
    signal_derivative = derivative(timestamp, signal_derivative)

    # Filtering with Gaussian filter the derivated data
    norm_gaussian = gaussian_filter1d(signal_derivative, sigma)

    
    # Compute the adaptive envelopp using moving average and standard deviation
    abs_signal = abs(norm_gaussian)

    threshold = threshold_multiplier * max(abs_signal)

    # Find the indices of movement segments
    markers_begin, markers_end = find_bounds(timestamp, abs_signal, threshold)
    return signal_derivative, norm_gaussian, abs_signal, markers_begin, markers_end


def compute_norm(*signals: List[List[float]]):
    signal_amount = len(signals)
    min_len_signal = len(signals[0])
    for i in range(signal_amount):
        if len(signals[i]) < min_len_signal:
            min_len_signal = len(signals[i])
     
    norm = []
    for i in range(min_len_signal):
        res = 0
        for j in range(signal_amount):
            res += pow(signals[j][i], 2)
        norm.append(sqrt(res))

    return norm

def find_bounds(x, signal, threshold):
    markers_begin = []
    markers_end = []
    
    was_in_rect = False
    for i in range(0, len(signal)):
        in_rect = signal[i] >= threshold
        
        if in_rect:
            if not was_in_rect:
                was_in_rect = True
                markers_begin.append(x[i])
        else:
            if was_in_rect:
                was_in_rect = False
                markers_end.append(x[i])
    
    if was_in_rect:
        markers_end.append(x[-1])
    return markers_begin, markers_end

def non_max_suppression(seg_start_list, seg_end_list, threshold):
    selected_indices_start = []
    selected_indices_end = []
    n = len(seg_start_list)

    i = 0
    while i < n - 1:
        end_i = seg_end_list[i]
        j = i + 1
        while j < n - 1:
            if ((threshold > 0 and -end_i + seg_start_list[j] < threshold)
                or (threshold <= 0 and end_i - seg_start_list[j] > threshold)):
                j += 1
            else:
                break
        selected_indices_start.append(seg_start_list[i])
        selected_indices_end.append(seg_end_list[j])
        i = j + 1
    """
    for i in range(1, len(seg_start_list)):
        diff_start = seg_end_list[i - 1] - seg_start_list[i]
        if diff_start <= threshold:
            selected_indices_start.append(min(seg_start_list[i - 1], seg_start_list[i]))
            selected_indices_end.append(max(seg_end_list[i - 1], seg_end_list[i]))
    """
            
    return selected_indices_start, selected_indices_end

def normalize_data(data):
    min_val = min(data)
    max_val = max(data)
    normalized_data = [(x - min_val) / (max_val - min_val) for x in data]
    normalized_scaled_data = [2 * x - 1 for x in normalized_data]
    return normalized_scaled_data
