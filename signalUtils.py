import graphUtils as GRAPH
from math import sqrt
import mathsUtils as MATH
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import numpy as np

def all_calculations(downsampled_x_accel, downsampled_y_accel, downsampled_z_accel, downsampled_timestamp, sigma, window_size, envelopp_multiplier, threshold_multiplier):
    # Normalise the acceleration data

    xaccel_derivative, xaccel_gaussian, abs_xaccel, envelopp_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_x_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    yaccel_derivative, yaccel_gaussian, abs_yaccel, envelopp_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_y_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    zaccel_derivative, zaccel_gaussian, abs_zaccel, envelopp_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_z_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    
    norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative)
    norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian)

    abs_norm = np.abs(norm_gaussian)
    mean_norm = np.convolve(abs_norm, np.ones(window_size) / window_size, mode='same')
    std_norm = np.convolve((abs_norm - mean_norm)**2, np.ones(window_size) / window_size, mode='same')
    envelopp_norm = envelopp_multiplier * np.sqrt(std_norm)
    threshold_norm = threshold_multiplier * max(envelopp_norm)

    # Apply adaptive thresholding to identify movement segments
    is_movement = envelopp_norm > threshold_norm

    # Find the indices of movement segments
    segment_start_indices = np.where(np.diff(is_movement.astype(int)) == 1)[0] + 1
    segment_end_indices = np.where(np.diff(is_movement.astype(int)) == -1)[0] + 1


    # Print the segment start and end indices
    start_norm = []
    end_norm = []
    for start, end in zip(segment_start_indices, segment_end_indices):
        # for exception, allow to throw errors
        if start > end:
            temp = start
            start = end
            end = temp
        #print("Segment : Start = {} seconds, End = {} seconds".format(start, end))
        start_norm.append(start)
        end_norm.append(end)


    GRAPH.plots_data(downsampled_timestamp, 
                    "Derivative",
                    False,
                    (xaccel_derivative, "x"), 
                    (yaccel_derivative, "y"), 
                    (zaccel_derivative, "z"), 
                    (norm_derivative, "norm"))

    GRAPH.plots_data(downsampled_timestamp,
                    "Gaussian filtered",
                    False,
                    (xaccel_gaussian, "x"),
                    (yaccel_gaussian, "y"),
                    (zaccel_gaussian, "z"),
                    (norm_gaussian, "norm"))

    plt.subplot(4,1,1)
    GRAPH.plots_data(downsampled_timestamp, "X", True, (abs_xaccel, "abs"), (envelopp_xaccel, "envelopp"))
    plt.subplot(4,1,2)
    GRAPH.plots_data(downsampled_timestamp, "Y", True, (abs_yaccel, "abs"), (envelopp_yaccel, "envelopp"))
    plt.subplot(4,1,3)
    GRAPH.plots_data(downsampled_timestamp, "Z", True, (abs_zaccel, "abs"), (envelopp_zaccel, "envelopp"))
    plt.subplot(4,1,4)
    GRAPH.plots_data(downsampled_timestamp, "Norm", False, (abs_norm, "abs"), (envelopp_norm, "envelopp"))


    GRAPH.plots_rectangles([ (xaccel_gaussian, "x"), (yaccel_gaussian, "y"), (zaccel_gaussian, "z"), (norm_gaussian, "norm") ],
                            [start_xaccel,start_yaccel, start_zaccel, start_norm],
                            [end_xaccel, end_yaccel, end_zaccel, end_norm],
                            False)
    
    return start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel

def rectangle_extraction(x_coordinates, y_coordinates, z_coordinates, x_accel, y_accel, z_accel, type):
        movement_ranges = []

        for x_start, x_end in x_coordinates:
                for y_start, y_end in y_coordinates:
                        for z_start, z_end in z_coordinates:
                        # Check if at least 2 axes have crossing rectangles
                                if (x_end > y_start or y_end > x_start) and (x_end > z_start or z_end > x_start):
                                        # Determine the overlapping range
                                        overlapping_start = max(x_start, y_start, z_start)
                                        overlapping_end = min(x_end, y_end, z_end)
                                        movement_ranges.append(((overlapping_start, overlapping_end), (y_start, y_end), (z_start, z_end)))

        x = []
        y = []
        z = []
        for x_range, y_range, z_range in movement_ranges:
                x.append(x_range)
                y.append(y_range)
                z.append(z_range)
                #print(f"X: {x_range}  Y: {y_range}  Z: {z_range}")

        new_start = []
        new_end = []
        for i in range(0, int(len(x))):
                new_start.append(min(x[i][0], y[i][0], z[i][0]))
                new_end.append(max(x[i][1], y[i][1], z[i][1]))

        _, ax = plt.subplots()
        plt.plot(x_accel, label="x")
        plt.plot(y_accel, label="y")
        plt.plot(z_accel, label="z")

        colorList = ["blue", "red", "green", "cyan", "magenta", "yellow", "orange", "purple", "brown"]
        for i in range(0, len(new_start)):
                rectangleColor = random.choice(colorList)
                norm_gaussian_part = x_accel[int(new_start[i]):int(new_end[i])]
                min_y = min(norm_gaussian_part)
                max_y = max(norm_gaussian_part)
                
                rect = Rectangle((new_start[i], min_y), new_end[i] - new_start[i], max_y - min_y, fill=False, edgecolor=rectangleColor, linewidth=3)
                ax.add_patch(rect)
        plt.legend()
        plt.title(f"Merged rectangle for {type} with x, y and z channels")
        plt.savefig(f"./images_saved/results/Merged_rectangles_{type}.png")
        plt.show()

        _, ax = plt.subplots()
        norm = MATH.compute_norm(x_accel, y_accel, z_accel)
        plt.plot(norm, label="norm")


        for i in range(0, len(new_start)):
                rectangleColor = random.choice(colorList)
                norm_gaussian_part = norm[int(new_start[i]):int(new_end[i])]
                min_y = min(norm_gaussian_part)
                max_y = max(norm_gaussian_part)
                
                rect = Rectangle((new_start[i], min_y), new_end[i] - new_start[i], max_y - min_y, fill=False, edgecolor=rectangleColor, linewidth=3)
                ax.add_patch(rect)
        plt.legend()
        plt.title(f"Merged rectangle for {type} with the norm")
        plt.savefig(f"./images_saved/results/Merged_rectangles_{type}_norm.png")
        plt.show()