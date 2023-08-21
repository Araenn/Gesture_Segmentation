import readingUtils.csvUtils as CSV
import signalUtils as SIGNAL
import mathsUtils as MATH

if __name__ == "__main__":

        #seq_to_read = "data/our_datas/non_gesture/Non-gesture_8_Lea.csv"
        seq_to_read = "data/our_datas/new/processed/seq12.csv"
        seq_to_labelise = "data/our_datas/new/raw/seq12.csv"

        normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros, fs = CSV.reading_into_csv(
                seq_to_read)


        # PARAMETERS FOR THE REST OF THE CODE
        threshold_multiplier = 0.3 # if low (<0.2), detection is very harsh, else, detection is more smooth (overlapping gestures)

        sigma = 10
        iou_threshold = 1

        # SEGMENTATION
        true_mvmt = CSV.labelise_data(seq_to_labelise)


        #CLASSIC
        start_xgyros, end_xgyros, start_ygyros, end_ygyros, start_zgyros, end_zgyros, start_norm, end_norm = SIGNAL.all_calculations(
                (x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 1)
        
        true_start = true_mvmt[0]
        true_end = true_mvmt[1]

        print("before merge : ")
        precision_classic, recall_classic = MATH.precision_recall(true_start, start_norm, true_end, end_norm)
        print(f"precision : {precision_classic}, recall = {recall_classic}")
        iou = MATH.check_iou(true_start, start_norm, true_end, end_norm, 1)

        print("after merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, iou_threshold)
        precision_classic, recall_classic = MATH.precision_recall(true_start, new_start, true_end, new_end)
        print(f"precision : {precision_classic}, recall = {recall_classic}")