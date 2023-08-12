import readingUtils.csvUtils as CSV
import signalUtils as SIGNAL
import mathsUtils as MATH

if __name__ == "__main__":

        #seq_to_read = "data/our_datas/non_gesture/Non-gesture_8_Lea.csv"
        seq_to_read = "data/our_datas/new/processed/seq1.csv"
        seq_to_labelise = "data/our_datas/new/raw/seq1.csv"

        normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros, fs = CSV.reading_into_csv(
                seq_to_read)


        # PARAMETERS FOR THE REST OF THE CODE
        #maud_1 = trop brusque sur non mouvements
        #seq9 : sigma = 40, threshold = 0.1
        #seq8 : sigma = 1, threshold = 0.3 not working
        #seq7 : sigma = 30, threshold = 0.1
        #seq6 : sigma = 30, threshold = 0.1
        #seq5 : sigma = 30, threshold = 0.1
        #seq4 : sigma = 10, threshold = 0.1   not very effective
        #seq3 : sigma = 30, threshold = 0.1
        #seq2 : sigma = 30, threshold = 0.1
        #seq1 : sigma = 10, threshold = 0.1
        threshold_multiplier = 0.1 # if low (<0.2), detection is very harsh, else, detection is more smooth (overlapping gestures)

        sigma = 40


        # SEGMENTATION
        true_mvmt = CSV.labelise_data(seq_to_labelise)

        start_xgyros, end_xgyros, start_ygyros, end_ygyros, start_zgyros, end_zgyros, start_norm, end_norm = SIGNAL.all_calculations(
                x_gyros, y_gyros, z_gyros,
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs)
        
        true_start = true_mvmt[0]
        true_end = true_mvmt[1]

        for i in range(0, min(len(true_start), len(start_norm))):
            iou = MATH.IOU(true_start[i], true_end[i], start_norm[i], end_norm[i])
            print(iou)
        
