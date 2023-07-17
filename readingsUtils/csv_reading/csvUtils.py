import csv

def reading_into_csv(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        timestamp_subject01_gesture09 = []
        normalised_timestamp = []
        x_accel = []
        y_accel = []
        z_accel = []

        x_gyros = []
        y_gyros = []
        z_gyros = []

        line_count = 0
        
        for row in csv_reader:
            timestamp_subject01_gesture09.append(row[0])
            normalised_timestamp.append(float(timestamp_subject01_gesture09[line_count]) - float(timestamp_subject01_gesture09[0]))
            
            x_accel.append(float(row[1]))
            y_accel.append(float(row[2]))
            z_accel.append(float(row[3]))

            x_gyros.append(float(row[4]))
            y_gyros.append(float(row[5]))
            z_gyros.append(float(row[6]))
        
            line_count += 1
    return normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros

"""
def labelise_date(path):
    normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = reading_into_csv(path)
    false_value = max(x_accel)
    count = 0
    for i in range(0, len(normalised_timestamp)):
        if normalised_timestamp[i] < 0:
            normalised_timestamp[i] = normalised_timestamp[i - 1] + 0.1
            count += 1
        if (x_accel[i] == 0 and y_accel[i] == 0 and z_accel[i] == 0) or (x_accel[i] == -1 and y_accel[i] == -1 and z_accel[i] == -1):
            x_accel[i] = false_value
            y_accel[i] = false_value
            z_accel[i] = false_value
            x_gyros[i] = false_value
            y_gyros[i] = false_value
            z_gyros[i] = false_value
    print(count/2)
    return normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros
    """

def labelise_data(path):
    normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = reading_into_csv(path)
    temp = []

    starting_timestamp = float(2 * normalised_timestamp[1] - normalised_timestamp[2])
    temp.append(0)
    for i in range(1, len(normalised_timestamp)):
        if normalised_timestamp[i] == 0:
            #print(normalised_timestamp[i + 2], normalised_timestamp[i - 1])
            temp.append(((normalised_timestamp[i + 1] + normalised_timestamp[i - 2]) / 2) - starting_timestamp)
        print(temp)

    return temp
