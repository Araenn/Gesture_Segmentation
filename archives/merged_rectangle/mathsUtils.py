from scipy.ndimage import gaussian_filter1d
import numpy as np
from typing import List, Tuple
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


def simple_segmentation(downsampled_timestamp, signal, sigma, window_size, envelopp_multiplier, threshold_multiplier):
    # Derivate the normalised data
    signal_derivative = derivative(downsampled_timestamp, signal)
    signal_derivative = derivative(downsampled_timestamp, signal_derivative)

    # Filtering with Gaussian filter the derivated data
    norm_gaussian = gaussian_filter1d(signal_derivative, sigma)

    # Compute the adaptive envelopp using moving average and standard deviation
    abs_signal = np.abs(norm_gaussian)
    mean_signal = np.convolve(abs_signal, np.ones(window_size) / window_size, mode='same')
    std_signal = np.convolve((abs_signal - mean_signal)**2, np.ones(window_size) / window_size, mode='same')
    envelopp = envelopp_multiplier * np.sqrt(std_signal)
    threshold = threshold_multiplier * max(envelopp)

    # Apply adaptive thresholding to identify movement segments
    is_movement = envelopp > threshold

    # Find the indices of movement segments
    segment_start_indices = np.where(np.diff(is_movement.astype(int)) == 1)[0] + 1
    segment_end_indices = np.where(np.diff(is_movement.astype(int)) == -1)[0] + 1


    # Print the segment start and end indices
    start_output = []
    end_output = []
    for start, end in zip(segment_start_indices, segment_end_indices):
        # for exception, allow to throw errors
        if start > end:
            temp = start
            start = end
            end = temp
        #print("Segment : Start = {} seconds, End = {} seconds".format(start, end))
        start_output.append(start)
        end_output.append(end)
    return signal_derivative, norm_gaussian, abs_signal, envelopp, start_output, end_output

def smooth_signal(x_accel, y_accel, z_accel, smoothing_factor, down_sampling_factor):
    num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

    # Smooth the data by taking the mean of every smoothing_factor frames
    smoothed_x_accel = np.mean(np.array(x_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
    smoothed_y_accel = np.mean(np.array(y_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
    smoothed_z_accel = np.mean(np.array(z_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)

    # Down-sample the smoothed data
    downsampled_x_accel = smoothed_x_accel[::down_sampling_factor]
    downsampled_y_accel = smoothed_y_accel[::down_sampling_factor]
    downsampled_z_accel = smoothed_z_accel[::down_sampling_factor]

    return downsampled_x_accel, downsampled_y_accel, downsampled_z_accel, num_samples

def merge_rectangles(segment_start, segment_end):
    new_segment_end = []
    new_segment_start = []
    if segment_start[1] < segment_end[0]:
        new_segment_start = segment_start[0]
        new_segment_end = segment_end[1]
    elif segment_start[0] < segment_end[1]:
        new_segment_start = segment_start[1]
        new_segment_end = segment_end[0]
    return new_segment_start, new_segment_end

def rectangle_segmentation(segment_start: Tuple[List[float], List[float], List[float]], segment_end: Tuple[List[float], List[float], List[float]]):
    min_list = min(len(segment_start[0]), len(segment_start[1]), len(segment_start[2]))

    new_start = []
    new_end = []
    for i in range(0, min_list):
        if segment_start[0][i] != 0 and segment_start[1][i] != 0 and segment_start[2][i] != 0:
            min_x = min(segment_start[0][i], segment_start[1][i], segment_start[2][i])
            max_x = max(segment_end[0][i], segment_end[1][i], segment_end[2][i])
            new_start.append(min_x)
            new_end.append(max_x)

    return new_start, new_end

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