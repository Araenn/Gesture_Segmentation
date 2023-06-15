import readingsUtils.csv_reading.txtUtils as TXT
import mathsUtils as MATH
import numpy as np
import signalUtils as SIGNAL

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

# COMPUTATION
downsampled_x_accel, downsampled_y_accel, downsampled_z_accel, num_samples = MATH.smooth_signal(x_accel, y_accel, z_accel,
                                                                                                smoothing_factor, down_sampling_factor)
downsampled_x_gyros, downsampled_y_gyros, downsampled_z_gyros, num_samples = MATH.smooth_signal(x_gyros, y_gyros, z_gyros,
                                                                                                smoothing_factor, down_sampling_factor)


# Calculate the corresponding timestamp for the downsampled data
original_timestamp = np.linspace(0, num_samples / freq, num_samples)
downsampled_timestamp = original_timestamp[::smoothing_factor][::down_sampling_factor]

SIGNAL.all_calculations(downsampled_x_accel, downsampled_y_accel, downsampled_z_accel,
                        downsampled_timestamp, sigma, window_size,
                        envelopp_multiplier, threshold_multiplier)

SIGNAL.all_calculations(downsampled_x_gyros, downsampled_y_gyros, downsampled_z_gyros,
                        downsampled_timestamp, sigma, window_size,
                        envelopp_multiplier, threshold_multiplier)