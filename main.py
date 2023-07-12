import readingsUtils.csv_reading.txtUtils as TXT
import readingsUtils.csv_reading.csvUtils as CSV
import numpy as np
import signalUtils as SIGNAL

if __name__ == "__main__":

        normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, x_accel, y_accel, z_accel = CSV.reading_into_csv(
                "data/our_datas/non_gesture/Non-gesture_8_Lea.csv")

        # PARAMETERS FOR THE REST OF THE CODE
        threshold_multiplier = 0.3 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

        sigma = 0.1


        # SEGMENTATION
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel = SIGNAL.all_calculations(
                x_accel, y_accel, z_accel,
                normalised_timestamp_acc, sigma, threshold_multiplier)

        """
        start_xgyros, end_xgyros, start_ygyros, end_ygyros, start_zgyros, end_zgyros = SIGNAL.all_calculations(
                x_gyros, y_gyros, z_gyros,
                normalised_timestamp_acc, sigma, window_size,
                envelopp_multiplier, threshold_multiplier)
        """
