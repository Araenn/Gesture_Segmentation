import readingsUtils.csv_reading.txtUtils as TXT
import readingsUtils.csv_reading.csvUtils as CSV
import matplotlib.pyplot as plt
import numpy as np
import signalUtils as SIGNAL
import graphUtils as GRAPH
from math import sqrt

if __name__ == "__main__":

        normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, x_accel, y_accel, z_accel = CSV.reading_into_csv(
                "data/our_datas/non_gesture/Non-gesture_8_Lea.csv")

        # PARAMETERS FOR THE REST OF THE CODE
        window_size = 5  # Size of the moving window for computing mean and standard deviation
        envelopp_multiplier = 3  # Multiplier for the standard deviation to determine the envelopp
        threshold_multiplier = 0.5 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

        sigma = 0.1


        # SEGMENTATION
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel = SIGNAL.all_calculations(
                x_accel, y_accel, z_accel,
                normalised_timestamp_acc, sigma, window_size,
                envelopp_multiplier, threshold_multiplier)

        start_xgyros, end_xgyros, start_ygyros, end_ygyros, start_zgyros, end_zgyros = SIGNAL.all_calculations(
                x_gyros, y_gyros, z_gyros,
                normalised_timestamp_acc, sigma, window_size,
                envelopp_multiplier, threshold_multiplier)


        # MERGED RECTANGLES
        x_coordinates_accel = list(zip(start_xaccel, end_xaccel))
        y_coordinates_accel = list(zip(start_yaccel, end_yaccel))
        z_coordinates_accel = list(zip(start_zaccel, end_zaccel))

        SIGNAL.rectangle_extraction(x_coordinates_accel, y_coordinates_accel, z_coordinates_accel,
                                    x_accel, y_accel, z_accel,
                                    "acceleration")

        x_coordinates_gyros = list(zip(start_xgyros, end_xgyros))
        y_coordinates_gyros = list(zip(start_ygyros, end_ygyros))
        z_coordinates_gyros = list(zip(start_zaccel, end_zgyros))

        SIGNAL.rectangle_extraction(x_coordinates_gyros, y_coordinates_gyros, z_coordinates_gyros,
                                    x_gyros, y_gyros, z_gyros,
                                    "gyroscope")
