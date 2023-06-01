import csv_reading.graphUtils as graph
import matplotlib.pyplot as plt
import csv_reading.csvUtils as CSV


if __name__ == "__main__":

    normalised_timestamp_acc, x_accel, y_accel, z_accel = CSV.reading_into_csv("data/RGB/Subject001/03/09.csv", 1, 2, 3)
    normalised_timestamp_gyr, x_gyr, y_gyr, z_gyr = CSV.reading_into_csv("data/RGB/Subject001/03/09.csv", 4, 5, 6)


    plt.figure(1)
    graph.show_3_subplot(normalised_timestamp_acc, x_accel, y_accel, z_accel, 'Acceleration data', 'acceleration', 'times(s)')
    plt.figure(2)
    graph.show_3_subplot(normalised_timestamp_gyr, x_gyr, y_gyr, z_gyr, 'Gyroscope data', 'gyroscope', 'times(s)')

    plt.show()