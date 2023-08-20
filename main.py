import readingUtils.csvUtils as CSV
import signalUtils as SIGNAL
import mathsUtils as MATH

if __name__ == "__main__":

        #seq_to_read = "data/our_datas/non_gesture/Non-gesture_8_Lea.csv"
        seq_to_read = "data/our_datas/new/processed/seq2.csv"
        seq_to_labelise = "data/our_datas/new/raw/seq2.csv"

        normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros, fs = CSV.reading_into_csv(
                seq_to_read)


        # PARAMETERS FOR THE REST OF THE CODE
        # for new seq 13, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # for new seq 12, threshold = 0.5 and sigma = 10. For IOU, threshold = 2
        # for new seq 11, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # for new seq 10, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # for new seq 9, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # for new seq 8, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # for new seq 7, threshold = 0.3 and sigma = 10. For IOU, threshold = 2
        # same for the rest
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
        precision_classic = MATH.precision_recall(true_start, start_norm, true_end, end_norm)
        print(f"precision : {precision_classic}")
        iou = MATH.check_iou(true_start, start_norm, true_end, end_norm, 1)

        print("after merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, iou_threshold)
        precision_classic = MATH.precision_recall(true_start, new_start, true_end, new_end)
        print(f"precision : {precision_classic}")
        iou = MATH.check_iou(true_start, new_start, true_end, new_end, 2)


        """
        # ONLY X AND Y ACC
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 2)
        

        print("before merge : ")
        precision_only_acc, recall_only_acc = MATH.precision_recall(true_start, start_norm, true_end, end_norm)
        #print(f"only x and y acc : {precision_only_acc, recall_only_acc}")

        print("after merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, iou_threshold)
        precision_only_acc, recall_only_acc = MATH.precision_recall(true_start, new_start, true_end, new_end)
        #print(f"only x and y acc : {precision_only_acc, recall_only_acc}")

        
        # ALL ACC AND ALL GYR
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 3)
        
        print("before merge : ")
        precision_all, recall_all = MATH.precision_recall(true_start, start_norm, true_end, end_norm)
        #print(f"all acc and all gyr : {precision_all, recall_all}")

        print("after merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, iou_threshold)
        precision_all, recall_all = MATH.precision_recall(true_start, new_start, true_end, new_end)
        #print(f"all acc and all gyr : {precision_all, recall_all}")

        # X AND Y ACC AND ALL GYR
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 4)
        
        print("before merge : ")
        precision_acc_gyr, recall_acc_gyr = MATH.precision_recall(true_start, start_norm, true_end, end_norm)
        #print(f"all acc and all gyr : {precision_acc_gyr, recall_acc_gyr}")

        print("after merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, iou_threshold)
        precision_acc_gyr, recall_acc_gyr = MATH.precision_recall(true_start, new_start, true_end, new_end)
        #print(f"all acc and all gyr : {precision_acc_gyr, recall_acc_gyr}")
        """