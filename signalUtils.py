import graphUtils as GRAPH
import mathsUtils as MATH
import matplotlib.pyplot as plt

def all_calculations(x_accel, y_accel, z_accel, timestamp, sigma, threshold_multiplier, true_mvmt, fs):
    # Normalise the acceleration data

    xaccel_derivative, xaccel_gaussian, abs_xaccel, start_xaccel, end_xaccel = MATH.simple_segmentation(
            timestamp, x_accel, sigma, threshold_multiplier)
    yaccel_derivative, yaccel_gaussian, abs_yaccel, start_yaccel, end_yaccel = MATH.simple_segmentation(
            timestamp, y_accel, sigma, threshold_multiplier)
    zaccel_derivative, zaccel_gaussian, abs_zaccel, start_zaccel, end_zaccel = MATH.simple_segmentation(
            timestamp, z_accel, sigma, threshold_multiplier)
    
    norm_derivative = MATH.compute_norm(xaccel_derivative, yaccel_derivative, zaccel_derivative)
    norm_gaussian = MATH.compute_norm(xaccel_gaussian, yaccel_gaussian, zaccel_gaussian)
    threshold = threshold_multiplier * max(norm_gaussian)

    # Find the indices of movement segments
    markers_begin, markers_end = MATH.find_bounds(timestamp, norm_gaussian, threshold)

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
    
    print(f"x rectangle amount : {len(start_xaccel)}")
    print(f"y rectangle amount : {len(start_yaccel)}")
    print(f"z rectangle amount : {len(start_zaccel)}")
    print(f"norm rectangle amount : {len(markers_begin)}")

    GRAPH.plot_checking(timestamp,
                        [ (xaccel_gaussian, "x"), (yaccel_gaussian, "y"), (zaccel_gaussian, "z"), (norm_gaussian, "norm") ],
                        [start_xaccel, start_yaccel, start_zaccel, markers_begin],
                        [end_xaccel, end_yaccel, end_zaccel, markers_end],
                        true_mvmt, fs)
    return start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel