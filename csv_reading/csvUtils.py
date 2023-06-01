import csv
from numpy import *

def reading_into_csv(path, colX, colY, colZ):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        timestamp_subject01_gesture09 = []
        normalised_timestamp = []
        x_accel = []
        y_accel = []
        z_accel = []

        line_count = 0
        
        for row in csv_reader:
            timestamp_subject01_gesture09.append(row[0])
            normalised_timestamp.append(double(timestamp_subject01_gesture09[line_count]) - double(timestamp_subject01_gesture09[0]))
            
            x_accel.append(float(row[colX]))
            y_accel.append(float(row[colY]))
            z_accel.append(float(row[colZ]))
        
            line_count += 1
    return normalised_timestamp, x_accel, y_accel, z_accel