import readingsUtils.csv_reading.txtUtils as TXT
import graphUtils as GRAPH
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import mathsUtils as MATH

normalised_timestamp_acc, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros = TXT.reading_into_txt(
        "data/unsegmented/S1/Recorder_2019_04_03_16_10/data.txt")


fourier = [fft(x_accel), fft(y_accel), fft(z_accel)]

freq = fftfreq(fourier[0].size)
GRAPH.plots_3_data(normalised_timestamp_acc, x_accel, y_accel, z_accel, "Acceleration", "Value", "Time (sec)")
GRAPH.plots_3_data(freq, fourier[0].real, fourier[1].real, fourier[2].real, "Accel FFT", "Amplitude", "Frequency (Hz)")

x_derivative, y_derivative, z_derivative = MATH.derivative(normalised_timestamp_acc, x_accel, y_accel, z_accel)
GRAPH.plots_3_data(normalised_timestamp_acc, x_derivative, y_derivative, z_derivative, "Derivative", "Value", "Time (sec)")
print(normalised_timestamp_acc)