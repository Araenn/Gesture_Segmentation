from scipy.ndimage import gaussian_filter1d
from typing import List
from math import sqrt, pow, atan, pi
import numpy as np

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
    # WARNING, MAYBE NOT DERIVATING
    signal_derivative = derivative(timestamp, signal)
    #signal_derivative = derivative(timestamp, signal_derivative)
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


def IOU(start_true, end_true, start_detected, end_detected):
    Xa = max(start_true, start_detected)
    Xb = min(end_true, end_detected)
    inter = max(0, Xb - Xa)
    union = max(end_true, end_detected) - min(start_true, start_detected)
    res = inter / union
    return res

def true_false_positive_negative(iou:float, is_gesture:bool):
    threshold = 0.5

    true_positiv = 0
    false_positiv = 0
    true_negativ = 0
    false_negativ = 0
    
    if iou > threshold and is_gesture:
        true_positiv += 1
    elif iou > threshold and not is_gesture:
        false_positiv += 1
    elif iou < threshold and is_gesture:
        false_negativ += 1
    elif iou > threshold and not is_gesture:
        true_negativ += 1

    return true_positiv, true_negativ, false_positiv, false_negativ

def mean(data):
    return sum(data)/len(data)

def build_angles(accs_x, accs_y, accs_z, gyrs_x, gyrs_y, gyrs_z, timestamps):
    n = len(timestamps)
    acc_angles_x = [0] * n
    acc_angles_y = [0] * n
    for i in range(len(timestamps)):
        acc_angles_x[i] = atan(accs_y[i] / sqrt(pow(accs_x[i], 2) + pow(accs_z[i], 2))) * 180 / pi
        acc_angles_y[i] = atan(-1 * accs_x[i] / sqrt(pow(accs_y[i], 2) + pow(accs_z[i], 2))) * 180 / pi

    gyro_angles_x = [0] * n
    gyro_angles_y = [0] * n
    dt = timestamps[1] - timestamps[0]
    current_gyro_angle_x = 0.0
    current_gyro_angle_y = 0.0
    current_gyro_angle_x = gyrs_x[0] * dt
    current_gyro_angle_y = gyrs_y[0] * dt
    gyro_angles_x[0] = current_gyro_angle_x
    gyro_angles_y[0] = current_gyro_angle_y

    yaws = [0] * n
    rolls = [0] * n
    pitchs = [0] * n
    current_yaw = 0
    current_yaw = gyrs_z[0] + dt
    yaws[0] = current_yaw

    total_time = 0
    ERROR_YAW = 0
    ERROR_ROLL = 0
    ERROR_PITCH = 0
    for i in range(1, n):
        dt = timestamps[i] - timestamps[i - 1]
        total_time += dt
        current_gyro_angle_x += gyrs_x[i] * dt
        current_gyro_angle_y += gyrs_y[i] * dt
        gyro_angles_x[i] = current_gyro_angle_x
        gyro_angles_y[i] = current_gyro_angle_y

        current_yaw += gyrs_z[i] * dt
        yaws[i] = current_yaw
        rolls[i] = gyro_angles_x[i]
        pitchs[i] = gyro_angles_y[i]
        
    ERROR_YAW = yaws[-1] / total_time
    ERROR_ROLL = rolls[-1] / total_time
    ERROR_PITCH = pitchs[-1] / total_time

    total_time = 0
    current_yaw = 0
    current_yaw = gyrs_z[0] + dt
    for i in range(1, n):
        dt = timestamps[i] - timestamps[i - 1]
        total_time += dt
        current_gyro_angle_x += gyrs_x[i] * dt
        current_gyro_angle_y += gyrs_y[i] * dt
        gyro_angles_x[i] = current_gyro_angle_x
        gyro_angles_y[i] = current_gyro_angle_y

        yaws[i] -= ERROR_YAW * total_time
        rolls[i] -= ERROR_ROLL * total_time
        pitchs[i] -= ERROR_PITCH * total_time
    return rolls, pitchs, yaws

def init_norms(timestamps, accs_x, accs_y, accs_z):
        norms = []
        n = len(timestamps)
        for i in range(n):
            norms.append(sqrt(accs_x[i] * accs_x[i] + accs_y[i] * accs_y[i] + accs_z[i] * accs_z[i]))
        return norms

def compensate_gravity(timestamps, accs_x, accs_y, accs_z, gyrs_x, gyrs_y, gyrs_z):
    alpha = 0.6
    rolls, pitchs, yaws = build_angles(accs_x, accs_y, accs_z, gyrs_x, gyrs_y, gyrs_z, timestamps)
    for i in range(len(timestamps)):
        # Intégration des valeurs du gyroscope pour estimer l'angle d'inclinaison
        roll = rolls[i] / 180 * pi
        pitch = pitchs[i] / 180 * pi
        yaw = yaws[i] / 180 * pi

        # Projection de l'accélération sur les axes du référentiel du capteur
        # selon l'angle d'inclinaison estimé
        R_x = np.array([[1, 0, 0],
                        [0, np.cos(roll), -np.sin(roll)],
                        [0, np.sin(roll), np.cos(roll)]])
        R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])
        R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])

        accel = np.array([accs_x[i], accs_y[i], accs_z[i]]).reshape(-1, 1)
        projected_accel = np.dot(R_z, np.dot(R_y, np.dot(R_x, accel)))

        # Compensation de la gravité
        compensated_accel = projected_accel - np.array([0, 0, 1]).reshape(-1, 1)

        # Filtre complémentaire pour combiner l'accélération compensée et non compensée
        compensated_accel = alpha * compensated_accel + (1 - alpha) * np.array([accs_x[i], accs_y[i], accs_z[i]]).reshape(-1, 1)

        accs_x[i] = float(compensated_accel[0][0])
        accs_y[i] = float(compensated_accel[1][0])
        accs_z[i] = float(compensated_accel[2][0])

    return accs_x, accs_y, accs_z