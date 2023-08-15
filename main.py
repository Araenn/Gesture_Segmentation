import readingUtils.csvUtils as CSV
import signalUtils as SIGNAL
import mathsUtils as MATH

if __name__ == "__main__":

        #seq_to_read = "data/our_datas/non_gesture/Non-gesture_8_Lea.csv"
        seq_to_read = "data/our_datas/new/processed/seq3.csv"
        seq_to_labelise = "data/our_datas/new/raw/seq3.csv"

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


        # SEGMENTATION
        true_mvmt = CSV.labelise_data(seq_to_labelise)


        #CLASSIC
        start_xgyros, end_xgyros, start_ygyros, end_ygyros, start_zgyros, end_zgyros, start_norm, end_norm = SIGNAL.all_calculations(
                (x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 1)
        
        true_start = true_mvmt[0]
        true_end = true_mvmt[1]

        print("avant merge : ")
        for i in range(0, min(len(true_start), len(start_norm))):
            iou = MATH.IOU(true_start[i], true_end[i], start_norm[i], end_norm[i])
            print(iou)

        print("apres merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, 2)
        for i in range(0, min(len(true_start), len(new_start))):
            iou = MATH.IOU(true_start[i], true_end[i], new_start[i], new_end[i])
            print(iou)



        # ONLY X AND Y ACC
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 2)
        
        true_start = true_mvmt[0]
        true_end = true_mvmt[1]

        print("avant merge : ")
        for i in range(0, min(len(true_start), len(start_norm))):
            iou = MATH.IOU(true_start[i], true_end[i], start_norm[i], end_norm[i])
            print(iou)

        print("apres merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, 2)
        for i in range(0, min(len(true_start), len(new_start))):
            iou = MATH.IOU(true_start[i], true_end[i], new_start[i], new_end[i])
            print(iou)


        # ALL ACC AND ALL GYR
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 3)
        
        print("avant merge : ")
        for i in range(0, min(len(true_start), len(start_norm))):
            iou = MATH.IOU(true_start[i], true_end[i], start_norm[i], end_norm[i])
            print(iou)

        print("apres merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, 2)
        for i in range(0, min(len(true_start), len(new_start))):
            iou = MATH.IOU(true_start[i], true_end[i], new_start[i], new_end[i])
            print(iou)

        # X AND Y ACC AND ALL GYR
        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel, start_norm, end_norm = SIGNAL.all_calculations(
                (x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros),
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs, 4)
        
        print("avant merge : ")
        for i in range(0, min(len(true_start), len(start_norm))):
            iou = MATH.IOU(true_start[i], true_end[i], start_norm[i], end_norm[i])
            print(iou)

        print("apres merge : ")
        new_start, new_end = MATH.non_max_suppression(start_norm, end_norm, 2)
        for i in range(0, min(len(true_start), len(new_start))):
            iou = MATH.IOU(true_start[i], true_end[i], new_start[i], new_end[i])
            print(iou)