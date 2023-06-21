import graphUtils as GRAPH
from math import sqrt
import mathsUtils as MATH
import matplotlib.pyplot as plt

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