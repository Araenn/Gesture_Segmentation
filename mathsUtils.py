from scipy.ndimage import gaussian_filter1d
from typing import List, Tuple
from math import sqrt, pow
import readingUtils.csvUtils as CSV
import graphUtils as GRAPH
from enum import Enum, auto

class DetectionType(Enum):
    NONE = auto()
    TRUE_POS = auto()
    TRUE_NEG = auto()
    FALSE_POS = auto()
    FALSE_NEG = auto()


def derivative(normalised_timestamp_acc, x_accel):
    x_derivative = []
    t_i = normalised_timestamp_acc[0]
    for i in range(1, len(normalised_timestamp_acc)):
        t_i1 = normalised_timestamp_acc[i]
        a_x = (x_accel[i] - x_accel[i-1]) / (t_i1 - t_i)
        x_derivative.append(a_x)
        t_i = t_i1

    x_derivative.append(x_derivative[-1])

    return x_derivative


def simple_segmentation(timestamp, signal, sigma, threshold_multiplier):
    signal_derivative = signal

    # Filtering with Gaussian filter the derivated data
    norm_gaussian = gaussian_filter1d(signal_derivative, sigma)

    
    # Compute the adaptive envelopp using moving average and standard deviation
    abs_signal = abs(norm_gaussian)

    threshold = threshold_multiplier * max(abs_signal)

    # Find the indices of movement segments
    markers_begin, markers_end = find_bounds(timestamp, abs_signal, threshold)
    return signal_derivative, norm_gaussian, abs_signal, markers_begin, markers_end


def compute_norm(*signals: List[List[float]]):
    signal_amount = len(signals)
    min_len_signal = len(signals[0])
    for i in range(signal_amount):
        if len(signals[i]) < min_len_signal:
            min_len_signal = len(signals[i])
     
    norm = []
    for i in range(min_len_signal):
        res = 0
        for j in range(signal_amount):
            res += pow(signals[j][i], 2)
        norm.append(sqrt(res))

    return norm

def find_bounds(x, signal, threshold):
    markers_begin = []
    markers_end = []
    
    was_in_rect = False
    for i in range(0, len(signal)):
        in_rect = signal[i] >= threshold
        
        if in_rect:
            if not was_in_rect:
                was_in_rect = True
                markers_begin.append(x[i])
        else:
            if was_in_rect:
                was_in_rect = False
                markers_end.append(x[i])
    
    if was_in_rect:
        markers_end.append(x[-1])
    return markers_begin, markers_end

def non_max_suppression(seg_start_list, seg_end_list, threshold):
    selected_indices_start = []
    selected_indices_end = []
    
    selected_indices_start.append(seg_start_list[0])
    selected_indices_end.append(seg_end_list[0])
    
    for i in range(1, len(seg_start_list)):
        diff_start = abs(seg_end_list[i - 1] - seg_start_list[i])
        if diff_start <= threshold:
            selected_indices_end[-1] = max(seg_end_list[i], selected_indices_end[-1])
        else:
            selected_indices_start.append(seg_start_list[i])
            selected_indices_end.append(seg_end_list[i])
           
    return selected_indices_start, selected_indices_end

def is_supperposed(start_a:float, end_a:float, start_b:float, end_b:float) -> bool:
    Xa = max(start_a, start_b)
    Xb = min(end_a, end_b)
    return Xb - Xa > 0

def determine_detection(reals_start, dets_start, reals_end, dets_end) -> Tuple[List[Tuple[DetectionType, int]]]:
    assert len(reals_start) == len(reals_end)
    assert len(dets_start) == len(dets_end)

    real_n = len(reals_start)
    det_n = len(dets_start)
    reals_type = [DetectionType.NONE] * real_n
    dets_type = [DetectionType.NONE] * det_n

    for i_real in range(real_n):
        real_start = reals_start[i_real]
        real_end = reals_end[i_real]
        found = False
        was_count = False
        for i_det in range(det_n):
            det_start = dets_start[i_det]
            det_end = dets_end[i_det]

            if is_supperposed(real_start, real_end, det_start, det_end) and not was_count:
                #print(f"{i_real} est supperposé à {i_det}")
                reals_type[i_real] = (DetectionType.TRUE_POS, i_det)
                dets_type[i_det] = (DetectionType.TRUE_POS, i_real)
                found = True
                was_count = True
            elif is_supperposed(real_start, real_end, det_start, det_end) and was_count:
                dets_type[i_det] = (DetectionType.FALSE_POS, i_real)
                found = True
                was_count = True

        if not found:
            reals_type[i_real] = (DetectionType.FALSE_NEG, -1)
    
    for i_det in range(det_n):
        if dets_type[i_det] == DetectionType.NONE:
            dets_type[i_det] = (DetectionType.FALSE_POS, -1)

    return reals_type, dets_type

def precision_recall(reals_start, dets_start, reals_end, dets_end):
    _, dets_type = determine_detection(reals_start, dets_start, reals_end, dets_end)
    TP = 0
    FP = 0
    FN = 0
    for i in range(len(dets_type)):
        if dets_type[i][0] == DetectionType.TRUE_POS:
            TP += 1
        elif dets_type[i][0] == DetectionType.FALSE_NEG:
            FN += 1
        elif dets_type[i][0] == DetectionType.FALSE_POS:
            FP += 1

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    return precision, recall

def IOU(start_true, end_true, start_detected, end_detected):
    Xa = max(start_true, start_detected)
    Xb = min(end_true, end_detected)
    inter = max(0, Xb - Xa)
    union = max(end_true, end_detected) - min(start_true, start_detected)
    res = inter / union
    return res


def check_iou(reals_start, dets_start, reals_end, dets_end, num):
    assert len(reals_start) == len(reals_end)
    assert len(dets_start) == len(dets_end)

    reals_type, dets_type = determine_detection(reals_start, dets_start, reals_end, dets_end)
    n_reals = len(reals_start)

    iou = []
    
    for i_real in range(n_reals):
        detection_type, i_det = reals_type[i_real]
        if detection_type == DetectionType.TRUE_POS:
            iou.append(IOU(reals_start[i_real], 
                           reals_end[i_real],
                           dets_start[i_det],
                           dets_end[i_det]))


    print(f"iou : {iou}")
    CSV.write_to_csv(iou, f"results/iou{num}.csv")
    GRAPH.plots_data([x for x in range(len(iou))], 
                     f"IOU {num}", 
                     False, 
                     (iou, "iou"), 
                     ([0 for i in range(len(iou))], "0"), 
                     ([1 for i in range(len(iou))], "1")
                    )
    return iou