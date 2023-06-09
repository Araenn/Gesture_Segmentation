import readingsUtils.csv_reading.txtUtils as TXT
from scipy.ndimage import gaussian_filter1d
import mathsUtils as MATH
from math import sqrt, pow
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
        "data/unsegmented/S1/Recorder_2019_04_03_16_35/data.txt")
freq = 100 # based on documentaion
smoothing_factor = 12
down_sampling_factor = freq // 30  # 100Hz to 30Hz

# PARAMETERS FOR THE REST OF THE CODE
window_size = 20  # Size of the moving window for computing mean and standard deviation
envelopp_multiplier = 3  # Multiplier for the standard deviation to determine the envelopp
threshold_multiplier = 0.4 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

sigma = 2

"""
For the Recorder_2019_04_03_16_10, best config is respectively 20, 3, 0.4 and 2.
For the Recorder_2019_04_03_16_23, best is 20, 3, 0.4, 2
Does not work for Recorder_2019_04_03_16_35
"""

# COMPUTATION
# Calculate the number of samples to keep
num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

# Smooth the data by taking the mean of every smoothing_factor frames
smoothed_x_accel = np.mean(np.array(x_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_accel = np.mean(np.array(y_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_accel = np.mean(np.array(z_accel[:num_samples]).reshape(-1, smoothing_factor), axis=1)

# Down-sample the smoothed data
downsampled_x_accel = smoothed_x_accel[::down_sampling_factor]
downsampled_y_accel = smoothed_y_accel[::down_sampling_factor]
downsampled_z_accel = smoothed_z_accel[::down_sampling_factor]

num_samples = (len(x_accel) // smoothing_factor) * smoothing_factor

"""
# Same for the gyros
smoothed_x_gyros = np.mean(np.array(x_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_y_gyros = np.mean(np.array(y_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)
smoothed_z_gyros = np.mean(np.array(z_gyros[:num_samples]).reshape(-1, smoothing_factor), axis=1)

downsampled_x_gyros = smoothed_x_gyros[::down_sampling_factor]
downsampled_y_gyros = smoothed_y_gyros[::down_sampling_factor]
downsampled_z_gyros = smoothed_z_gyros[::down_sampling_factor]
"""


# Calculate the corresponding timestamp for the downsampled data
original_timestamp = np.linspace(0, num_samples / freq, num_samples)
downsampled_timestamp = original_timestamp[::smoothing_factor][::down_sampling_factor]

# Normalise the acceleration data
norm = []
for i in range(0, len(downsampled_x_accel)):
        norm.append(sqrt(pow(downsampled_x_accel[i], 2) + pow(downsampled_y_accel[i], 2) + pow(downsampled_z_accel[i], 2)))

# Derivate the normalised data
norm_derivative = MATH.derivative(downsampled_timestamp, norm)

norm_derivative = MATH.derivative(downsampled_timestamp, norm_derivative)


# Filtering with Gaussian filter the derivated data
norm_gaussian = gaussian_filter1d(norm_derivative, sigma)


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

        
# PLOTS
plt.figure()
plt.plot(downsampled_timestamp, norm)
plt.title("Normalised acceleration data [sqrt(x+y+z)]")
plt.savefig(f"./images_saved/Normalised_acc.png")

plt.figure()
plt.plot(downsampled_timestamp, norm_derivative)
plt.title("Derivative of the acceleration")
plt.savefig(f"./images_saved/Derivative.png")

plt.figure()
plt.plot(downsampled_timestamp, norm_gaussian)
plt.title("Gaussian filtered derivative")
plt.savefig(f"./images_saved/Gaussian_filtered.png")
plt.show()

plt.figure()
plt.plot(abs_signal, label='Filtered Signal')
plt.plot(envelopp, label='Adaptive envelopp')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.legend()
plt.title("Adaptative envelopp for the [abs(signal filtered)]")
plt.savefig(f"./images_saved/Adaptative_envelopp.png")
plt.show()

# Print the segment start and end indices, and plot them (with rectangles)
fig, ax = plt.subplots()
for start, end in zip(segment_start_indices, segment_end_indices):
    # for exception, allow to throw errors
    if start > end:
          temp = start
          start = end
          end = temp
    print("Segment : Start = {} seconds, End = {} seconds".format(start, end))
    norm_gaussian_part = norm_gaussian[start:end]
    min_y = min(norm_gaussian_part)
    max_y = max(norm_gaussian_part)
    ax.add_patch(Rectangle((start, min_y), end-start, max_y - min_y, fill=False))
plt.plot(norm_gaussian, label="filtered signal")
plt.legend()
plt.title("Segmentation check")
plt.savefig(f"./images_saved/Segmentation_check.png")
plt.show()
