import matplotlib.pyplot as plt
from numpy import *
import csv

with open('C:/Users/leaye/Documents/Lea/Etudes/SeaTech/2A/Stage/prog/data/RGB/Subject001/03/09.csv') as csv_file:
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
        
        x_accel.append(float(row[1]))
        y_accel.append(float(row[2]))
        z_accel.append(float(row[3]))
    
        line_count += 1


plt.subplot(3, 1, 1)
plt.plot(normalised_timestamp, x_accel)
plt.title('Acceleration data')
plt.ylabel('X acceleration')

plt.subplot(3, 1, 2)
plt.plot(normalised_timestamp, y_accel)
plt.ylabel('Y acceleration')

plt.subplot(3, 1, 3)
plt.plot(normalised_timestamp, z_accel)
plt.xlabel('time (s)')
plt.ylabel('Z acceleration')

plt.show()