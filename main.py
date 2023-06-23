import readingsUtils.csv_reading.txtUtils as TXT
import readingsUtils.csv_reading.csvUtils as CSV
import mathsUtils as MATH
import numpy as np
import signalUtils as SIGNAL

if __name__ == "__main__":

        normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, x_accel, y_accel, z_accel = CSV.reading_into_csv(
                "data/our_datas/non_gesture/Non-gesture_8_Lea.csv")
        freq = 100 # based on documentaion

        # PARAMETERS FOR THE REST OF THE CODE
        window_size = 20  # Size of the moving window for computing mean and standard deviation
        envelopp_multiplier = 3  # Multiplier for the standard deviation to determine the envelopp
        threshold_multiplier = 0.4 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

        sigma = 2

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
        segment_start_indices = [start_xaccel, start_yaccel, start_zaccel]
        segment_end_indices = [end_xaccel, end_yaccel, end_zaccel]

        SIGNAL.rectangle_extraction(x_accel, y_accel, z_accel,
                                    start_xaccel, start_yaccel, start_zaccel,
                                    end_xaccel, end_yaccel, end_zaccel,
                                    "acceleration")
        
        SIGNAL.rectangle_extraction(x_gyros, y_gyros, z_gyros,
                                    start_xgyros, start_ygyros, start_zgyros,
                                    end_xgyros, end_ygyros, end_zgyros,
                                    "gyroscope")