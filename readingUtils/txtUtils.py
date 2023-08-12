import csv

def reading_into_txt(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        date = []
        timestamp = []
        normalised_timestamp = []
        x_accel = []
        y_accel = []
        z_accel = []

        x_gyros = []
        y_gyros = []
        z_gyros = []

        line_count = 0
        
        for row in csv_reader:
            date = row[0].split(";")[1] # keep only second part, after ;
            hours, min, sec = map(float, date.split(":"))
            timestamp.append(hours * 3600 + min * 60 + sec)
            normalised_timestamp.append(float(timestamp[line_count]) - float(timestamp[0]))
            
            x_accel.append(float(row[1]))
            y_accel.append(float(row[2]))
            z_accel.append(float(row[3]))

            x_gyros.append(float(row[4]))
            y_gyros.append(float(row[5]))
            z_gyros.append(float(row[6]))
        
            line_count += 1
    return normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros