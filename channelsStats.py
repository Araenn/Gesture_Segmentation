import readingsUtils.csv_reading.csvUtils as CSV
import signalUtils as SIGNAL
import mathsUtils as MATH

if __name__ == "__main__":

        seq_to_read = "data/our_datas/gestures/processed/seq3.csv"
        seq_to_labelise = "data/our_datas/gestures/raw/seq3.csv"
        normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, x_accel, y_accel, z_accel, fs = CSV.reading_into_csv(
                seq_to_read)

        # PARAMETERS FOR THE REST OF THE CODE
        #seq7 : sigma = 47, threshold = 0.3, turn 
        #seq6 : sigma = 47, threshold = 0.3, up down
        #seq5 : sigma = 70, threshold = 0.4, s left right
        #seq4 : sigma = 46, threshold = 0.3, right left
        #seq3 : sigma = 11, threshold = 0.3, v right left
        threshold_multiplier = 0.1 # if too low (<0.4), detection check shows ungesture instead of gesture, if too high, gesture are too much segmented

        sigma = 10


        # SEGMENTATION
        true_mvmt = CSV.labelise_data(seq_to_labelise)

        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel = SIGNAL.all_calculations(
                x_accel, y_accel, z_accel,
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs)
        
        higher_channel = SIGNAL.channels_stats(x_accel, y_accel, z_accel)
        print(f"higher chan is : {higher_channel}")