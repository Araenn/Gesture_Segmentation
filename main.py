import simple_method
import readingsUtils.csv_reading.csvUtils as CSV
import graphUtils as graph

normalised_timestamp_acc, x_accel, y_accel, z_accel = CSV.reading_into_csv("data/RGB/Subject001/03/09.csv", 1, 2, 3)

graph.plots_3_data(normalised_timestamp_acc, x_accel, y_accel, z_accel, "Accelerometer data", "time", "value")