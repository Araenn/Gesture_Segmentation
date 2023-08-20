import graphUtils as GRAPH
import mathsUtils as MATH
import matplotlib.pyplot as plt
import numpy as np

def all_calculations(signal, timestamp, sigma, threshold_multiplier, true_mvmt, fs, choice):
    x_accel = signal[0]
    y_accel = signal[1]
    z_accel = signal[2]

    if choice == 2: #only x and y acc
        z_accel = [0] * len(z_accel) 
        xaccel_derivative, xaccel_gaussian, abs_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            timestamp, x_accel, sigma, threshold_multiplier)
        yaccel_derivative, yaccel_gaussian, abs_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
                timestamp, y_accel, sigma, threshold_multiplier)
        zaccel_derivative, zaccel_gaussian, abs_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
                timestamp, z_accel, sigma, threshold_multiplier)
        
        norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative)
        norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian)

        name = "x_y_acc"
    elif choice == 3: #merge all acc and gyros
        xaccel_derivative, xaccel_gaussian, abs_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            timestamp, x_accel, sigma, threshold_multiplier)
        yaccel_derivative, yaccel_gaussian, abs_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
                timestamp, y_accel, sigma, threshold_multiplier)
        zaccel_derivative, zaccel_gaussian, abs_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
                timestamp, z_accel, sigma, threshold_multiplier)
        
        xgyros_derivative, xgyros_gaussian, abs_xgyros, start_xgyros, end_xgyros = MATH.simple_segmentation(
            timestamp, signal[3], sigma, threshold_multiplier)
        ygyros_derivative, ygyros_gaussian, abs_ygyros, start_ygyros, end_ygyros = MATH.simple_segmentation(
                timestamp, signal[4], sigma, threshold_multiplier)
        zgyros_derivative, zgyros_gaussian, abs_zgyros, start_zgyros, end_zgyros = MATH.simple_segmentation(
                timestamp, signal[5], sigma, threshold_multiplier)
        
        norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative, 
                                            xgyros_derivative, ygyros_derivative, zgyros_derivative)
        norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian,
                                          xgyros_gaussian, ygyros_gaussian, zgyros_gaussian)
        
        name = "all"
    elif choice == 4: #merge x and y acc and gyros
        z_accel = [0] * len(z_accel) 
        xaccel_derivative, xaccel_gaussian, abs_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            timestamp, x_accel, sigma, threshold_multiplier)
        yaccel_derivative, yaccel_gaussian, abs_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
                timestamp, y_accel, sigma, threshold_multiplier)
        zaccel_derivative, zaccel_gaussian, abs_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
                timestamp, z_accel, sigma, threshold_multiplier)
        
        xgyros_derivative, xgyros_gaussian, abs_xgyros, start_xgyros, end_xgyros = MATH.simple_segmentation(
            timestamp, signal[3], sigma, threshold_multiplier)
        ygyros_derivative, ygyros_gaussian, abs_ygyros, start_ygyros, end_ygyros = MATH.simple_segmentation(
                timestamp, signal[4], sigma, threshold_multiplier)
        zgyros_derivative, zgyros_gaussian, abs_zgyros, start_zgyros, end_zgyros = MATH.simple_segmentation(
                timestamp, signal[5], sigma, threshold_multiplier)
        
        norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative, 
                                            xgyros_derivative, ygyros_derivative, zgyros_derivative)
        norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian,
                                          xgyros_gaussian, ygyros_gaussian, zgyros_gaussian)
        
        name = "x_y_acc_all_gyr"
    else:
        xaccel_derivative, xaccel_gaussian, abs_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            timestamp, x_accel, sigma, threshold_multiplier)
        yaccel_derivative, yaccel_gaussian, abs_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
                timestamp, y_accel, sigma, threshold_multiplier)
        zaccel_derivative, zaccel_gaussian, abs_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
                timestamp, z_accel, sigma, threshold_multiplier)
        
        norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative)
        norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian)

        name = "classic"

 
    threshold = threshold_multiplier * max(norm_gaussian)

    # Find the indices of movement segments
    markers_begin, markers_end = MATH.find_bounds(timestamp, norm_gaussian, threshold)

    """
    GRAPH.plots_data(timestamp, 
                    "Derivative",
                    False,
                    (xaccel_derivative, "x"), 
                    (yaccel_derivative, "y"), 
                    (zaccel_derivative, "z"), 
                    (norm_derivative, "norm"))

    GRAPH.plots_data(timestamp,
                    "Gaussian filtered",
                    False,
                    (xaccel_gaussian, "x"),
                    (yaccel_gaussian, "y"),
                    (zaccel_gaussian, "z"),
                    (norm_gaussian, "norm"))

    plt.subplot(4,1,1)
    GRAPH.plots_data(timestamp, "X", True, (abs_xaccel, "abs"))
    plt.subplot(4,1,2)
    GRAPH.plots_data(timestamp, "Y", True, (abs_yaccel, "abs"))
    plt.subplot(4,1,3)
    GRAPH.plots_data(timestamp, "Z", True, (abs_zaccel, "abs"))
    plt.subplot(4,1,4)
    GRAPH.plots_data(timestamp, "Norm", False, (norm_gaussian, "abs"))

    
    GRAPH.plots_rectangles(timestamp,
                           [ (xaccel_gaussian, "x"), (yaccel_gaussian, "y"), (zaccel_gaussian, "z"), (norm_gaussian, "norm") ],
                            [start_xaccel, start_yaccel, start_zaccel, markers_begin],
                            [end_xaccel, end_yaccel, end_zaccel, markers_end], fs,
                            False)
    
    """
    GRAPH.plot_checking(timestamp,
                        [ (xaccel_gaussian, "x"), (yaccel_gaussian, "y"), (zaccel_gaussian, "z"), (norm_gaussian, "norm") ],
                        [start_xaccel, start_yaccel, start_zaccel, markers_begin],
                        [end_xaccel, end_yaccel, end_zaccel, markers_end],
                        true_mvmt, fs, "raw", name)
    
    iou_threshold = 1

    new_start_norm, new_end_norm = MATH.non_max_suppression(markers_begin, markers_end, iou_threshold)
    new_start_x, new_end_x = MATH.non_max_suppression(start_xaccel, end_xaccel, iou_threshold)
    new_start_y, new_end_y = MATH.non_max_suppression(start_yaccel, end_yaccel, iou_threshold)
    new_start_z, new_end_z = MATH.non_max_suppression(start_zaccel, end_zaccel, iou_threshold)

    
    GRAPH.plot_checking(timestamp,
                        [(xaccel_gaussian, "x"), (yaccel_gaussian, "y"), (zaccel_gaussian, "z"), (norm_gaussian, "norm")],
                        [new_start_x, new_start_y, new_start_z, new_start_norm],
                        [new_end_x, new_end_y, new_end_z, new_end_norm],
                        true_mvmt,
                        fs, "corrected", name)
    
    return start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, markers_begin, markers_end
    