import readingsUtils.csv_reading.txtUtils as TXT
import mathsUtils as MATH
import numpy as np
import signalUtils as SIGNAL
import graphUtils as GRAPH
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from math import sqrt

if __name__ == "__main__":

        normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
                "data/unsegmented/S1/Recorder_2019_04_03_16_10/data.txt")
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

        # SEGMENTATION
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel = SIGNAL.all_calculations(
                downsampled_x_accel, downsampled_y_accel, downsampled_z_accel,
                downsampled_timestamp, sigma, window_size,
                envelopp_multiplier, threshold_multiplier)

        SIGNAL.all_calculations(downsampled_x_gyros, downsampled_y_gyros, downsampled_z_gyros,
                                downsampled_timestamp, sigma, window_size,
                                envelopp_multiplier, threshold_multiplier)

        segment_start_indices = [start_xaccel, start_yaccel, start_zaccel]
        segment_end_indices = [end_xaccel, end_yaccel, end_zaccel]

        min_x = []
        max_x = []
        for i in range(0, min(len(start_xaccel), len(start_yaccel), len(start_zaccel))):
                min_x.append(min(start_xaccel[i], start_yaccel[i], start_zaccel[i]))
                max_x.append(max(end_xaccel[i], end_yaccel[i], end_zaccel[i]))

        print(min_x, max_x)

        _, ax = plt.subplots()
        plt.plot(downsampled_x_accel, label="x")
        plt.plot(downsampled_y_accel, label="y")
        plt.plot(downsampled_z_accel, label="z")

        
        for i in range(0, len(min_x)):
                norm_gaussian_part = downsampled_x_accel[int(min_x[i]):int(max_x[i])]
                min_y = min(norm_gaussian_part)
                max_y = max(norm_gaussian_part)
                
                rect = Rectangle((min_x[i], min_y), max_x[i] - min_x[i], max_y - min_y, fill=False, edgecolor="blue", linewidth=3)
                ax.add_patch(rect)
        plt.legend()
        plt.title("Merged rectangle with x, y and z channels")
        plt.savefig("./images_saved/Merged_rectanles.png")
        plt.show()

        _, ax = plt.subplots()
        norm = []
        for i in range(0, len(downsampled_x_accel)):
                norm.append(sqrt(pow(downsampled_x_accel[i], 2) + pow(downsampled_y_accel[i], 2) + pow(downsampled_z_accel[i], 2)))
        plt.plot(norm, label="norm")

        
        for i in range(0, len(min_x)):
                norm_gaussian_part = norm[int(min_x[i]):int(max_x[i])]
                min_y = min(norm_gaussian_part)
                max_y = max(norm_gaussian_part)
                
                rect = Rectangle((min_x[i], min_y), max_x[i] - min_x[i], max_y - min_y, fill=False, edgecolor="red", linewidth=3)
                ax.add_patch(rect)
        plt.legend()
        plt.title("Merged rectangle with the norm")
        plt.savefig("./images_saved/Merged_rectangle_norm.png")
        plt.show()