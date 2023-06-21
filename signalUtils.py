import graphUtils as GRAPH
from math import sqrt
import mathsUtils as MATH
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def all_calculations(downsampled_x_accel, downsampled_y_accel, downsampled_z_accel, downsampled_timestamp, sigma, window_size, envelopp_multiplier, threshold_multiplier):
    # Normalise the acceleration data
    norm = []
    for i in range(0, len(downsampled_x_accel)):
            norm.append(sqrt(pow(downsampled_x_accel[i], 2) + pow(downsampled_y_accel[i], 2) + pow(downsampled_z_accel[i], 2)))

    norm_derivative, norm_gaussian, abs_norm, envelopp_norm, start_norm, end_norm = MATH.simple_segmentation(
            downsampled_timestamp, norm, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    xaccel_derivative, xaccel_gaussian, abs_xaccel, envelopp_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_x_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    yaccel_derivative, yaccel_gaussian, abs_yaccel, envelopp_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_y_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)
    zaccel_derivative, zaccel_gaussian, abs_zaccel, envelopp_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
            downsampled_timestamp, downsampled_z_accel, sigma, window_size, envelopp_multiplier, threshold_multiplier)

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

def rectangle_extraction(downsampled_x_accel, downsampled_y_accel, downsampled_z_accel, start_xaccel, start_yaccel, start_zaccel, end_xaccel, end_yaccel, end_zaccel, type):
        min_x = []
        max_x = []
        for i in range(0, min(len(start_xaccel), len(start_yaccel), len(start_zaccel))):
                min_x.append(min(start_xaccel[i], start_yaccel[i], start_zaccel[i]))
                max_x.append(max(end_xaccel[i], end_yaccel[i], end_zaccel[i]))

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
        plt.title(f"Merged rectangle for {type} with x, y and z channels")
        plt.savefig(f"./images_saved/Merged_rectangles_{type}.png")
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
        plt.title(f"Merged rectangle for {type} with the norm")
        plt.savefig(f"./images_saved/Merged_rectangles_{type}_norm.png")
        plt.show()