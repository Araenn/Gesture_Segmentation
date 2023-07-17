from scipy.ndimage import gaussian_filter1d
import numpy as np
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


def simple_segmentation(downsampled_timestamp, signal, sigma, threshold_multiplier):
    # Derivate the normalised data
    signal_derivative = derivative(downsampled_timestamp, signal)
    signal_derivative = derivative(downsampled_timestamp, signal_derivative)

    # Filtering with Gaussian filter the derivated data
    norm_gaussian = gaussian_filter1d(signal_derivative, sigma)

    # Compute the adaptive envelopp using moving average and standard deviation
    abs_signal = np.abs(norm_gaussian)

    threshold = threshold_multiplier * max(abs_signal)

    # Find the indices of movement segments
    markers_begin, markers_end = find_bounds(downsampled_timestamp, abs_signal, threshold)

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
    for i in range(len(x)):
        x_i = x[i]
        y_i = signal[i]

        in_rect = y_i > threshold
        
        if in_rect:
            if not was_in_rect:
                was_in_rect = True
                markers_begin.append(x_i)
        else:
            if was_in_rect:
                was_in_rect = False
                markers_end.append(x_i)
    
    if was_in_rect:
        markers_end.append(signal[-1])
            
    return markers_begin, markers_end