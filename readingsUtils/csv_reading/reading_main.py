import graphUtils as graph
import matplotlib.pyplot as plt
import csvUtils as CSV
import txtUtils as TXT


if __name__ == "__main__":

    #normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = CSV.reading_into_csv("../../data/RGB/Subject001/03/09.csv")
    normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
        "../../data/unsegmented/S1/Recorder_2019_04_03_16_10/data.txt")

    graph.plots_3_data(normalised_timestamp_acc, x_accel, y_accel, z_accel, 'Acceleration data', 'acceleration', 'times(s)')
    graph.plots_3_data(normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, 'Gyroscope data', 'gyroscope', 'times(s)')