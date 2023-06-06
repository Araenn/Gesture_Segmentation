import readingsUtils.csv_reading.txtUtils as TXT
import graphUtils as GRAPH
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
import mathsUtils as MATH
from math import sqrt, pow
import matplotlib.pyplot as plt
from scipy.fft import fftfreq, fft
import numpy as np
import time as time

normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
        "data/unsegmented/S1/Recorder_2019_04_03_16_35/data.txt")
freq = 100
"""
GRAPH.plots_3_data(normalised_timestamp_acc, x_accel, y_accel, z_accel, "Acceleration", "Value", "Time (sec)")

x_derivative, y_derivative, z_derivative = MATH.derivative(normalised_timestamp_acc, x_accel, y_accel, z_accel)
GRAPH.plots_3_data(normalised_timestamp_acc, x_derivative, y_derivative, z_derivative, "Derivative", "Value", "Time (sec)")

order = 20
polyn = 2
savgo_filtered = [savgol_filter(x_derivative, order, polyn), savgol_filter(y_derivative, order, polyn), savgol_filter(z_derivative, order, polyn)]

GRAPH.plots_3_data(normalised_timestamp_acc, savgo_filtered[0], savgo_filtered[1], savgo_filtered[2], "Savgol", "Value", "Times (sec)")

sigma = 20
gaussian_filtered = [gaussian_filter1d(x_derivative, sigma), gaussian_filter1d(y_derivative, sigma), gaussian_filter1d(z_derivative, sigma)]

GRAPH.plots_3_data(normalised_timestamp_acc, gaussian_filtered[0], gaussian_filtered[1], gaussian_filtered[2], "Gaussian", "Value", "Times (sec)")


"""
# norme accel * 0.3 + norme gyros * 0.7 puis normaliser
smoothing_factor = 12
sub_sampling_factor = freq // 30  # 125Hz to 30Hz
# Calculate the number of samples to keep
num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

# Smooth the data by taking the mean of every smoothing_factor frames
smoothed_x_accel = np.mean(np.array(x_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_accel = np.mean(np.array(y_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_accel = np.mean(np.array(z_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)

# Sub-sample the smoothed data
subsampled_x_accel = smoothed_x_accel[::sub_sampling_factor]
subsampled_y_accel = smoothed_y_accel[::sub_sampling_factor]
subsampled_z_accel = smoothed_z_accel[::sub_sampling_factor]

num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

# Smooth the data by taking the mean of every smoothing_factor frames
smoothed_x_gyros = np.mean(np.array(x_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_gyros = np.mean(np.array(y_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_gyros = np.mean(np.array(z_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)

# Sub-sample the smoothed data
subsampled_x_gyros = smoothed_x_gyros[::sub_sampling_factor]
subsampled_y_gyros = smoothed_y_gyros[::sub_sampling_factor]
subsampled_z_gyros = smoothed_z_gyros[::sub_sampling_factor]


# Calculate the corresponding timestamp for the subsampled data
original_timestamp = np.linspace(0, num_samples / freq, num_samples)
subsampled_timestamp = original_timestamp[::smoothing_factor][::sub_sampling_factor]

norm = []
for i in range(0, len(subsampled_x_accel)):
        norm.append(sqrt(pow(subsampled_x_accel[i], 2) + pow(subsampled_y_accel[i], 2) + pow(subsampled_z_accel[i], 2)))

plt.figure()
plt.plot(subsampled_timestamp, norm)

norm_derivative = MATH.derivative(subsampled_timestamp, norm)
fft_deri = fft(norm_derivative)

norm_derivative = MATH.derivative(subsampled_timestamp, norm_derivative)
fft_deri = fft(norm_derivative)

plt.figure()
plt.subplot(2,1,1)
plt.plot(subsampled_timestamp, norm_derivative)
plt.subplot(2,1,2)
plt.plot(fftfreq(len(fft_deri)), fft_deri.real)

sigma = 2
norm_gaussian = gaussian_filter1d(norm_derivative, sigma)
fft_gauss = fft(norm_gaussian)

plt.figure()
plt.subplot(2,1,1)
plt.plot(subsampled_timestamp, norm_gaussian)
plt.subplot(2,1,2)
plt.plot(fftfreq(len(fft_gauss)), fft_gauss.real)

plt.show()

# Define the parameters for adaptive envelopping
window_size = 20  # Size of the moving window for computing mean and standard deviation
envelopp_multiplier = 3  # Multiplier for the standard deviation to determine the envelopp
threshold_multiplier = 0.4

# Compute the absolute value of the filtered signal
abs_signal = np.abs(norm_gaussian)

# Compute the adaptive envelopp using moving average and standard deviation
mean_signal = np.convolve(abs_signal, np.ones(window_size) / window_size, mode='same')
std_signal = np.convolve((abs_signal - mean_signal)**2, np.ones(window_size) / window_size, mode='same')
envelopp = envelopp_multiplier * np.sqrt(std_signal)
threshold = threshold_multiplier * max(envelopp)

# Apply adaptive thresholding to identify movement segments
is_movement = envelopp > threshold

# Find the indices of movement segments
segment_start_indices = np.where(np.diff(is_movement.astype(int)) == 1)[0] + 1
segment_end_indices = np.where(np.diff(is_movement.astype(int)) == -1)[0] + 1

# Plot the filtered signal with adaptive envelopp
plt.figure()
plt.plot(abs_signal, label='Filtered Signal')
plt.plot(envelopp, label='Adaptive envelopp')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.legend()
plt.show()

# Print the segment start and end indices
for start, end in zip(segment_start_indices, segment_end_indices):
    print("Segment: Start={}, End={}".format(start, end))