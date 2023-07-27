import numpy as np
import utils.plot_utils as plot_utils
import matplotlib.pyplot as plt

from math import sqrt, atan, pow, pi
from scipy.ndimage import gaussian_filter1d

class SequenceGesture:

    def __init__(self, timestamps=[], gyrs_x=[], gyrs_y=[], gyrs_z=[], accs_x=[], accs_y=[], accs_z=[]) -> None:
        self.timestamps = timestamps
        self.gyrs_x = gyrs_x
        self.gyrs_y = gyrs_y
        self.gyrs_z = gyrs_z
        self.accs_x = accs_x
        self.accs_y = accs_y
        self.accs_z = accs_z
        self.norms = None
        self.moyenne = None
        self.acc_angles_x = None
        self.acc_angles_y = None
        self.gyro_angles_x = None
        self.gyro_angles_y = None
        self.yaws = None
        self.rolls = None
        self.pitchs = None



    def build_angles(self):
        n = len(self.timestamps)
        self.acc_angles_x = [0] * n
        self.acc_angles_y = [0] * n
        for i in range(len(self.timestamps)):
            self.acc_angles_x[i] = atan(self.accs_y[i] / sqrt(pow(self.accs_x[i], 2) + pow(self.accs_z[i], 2))) * 180 / pi
            self.acc_angles_y[i] = atan(-1 * self.accs_x[i] / sqrt(pow(self.accs_y[i], 2) + pow(self.accs_z[i], 2))) * 180 / pi

        self.gyro_angles_x = [0] * n
        self.gyro_angles_y = [0] * n
        dt = self.timestamps[1] - self.timestamps[0]
        current_gyro_angle_x = 0.0
        current_gyro_angle_y = 0.0
        current_gyro_angle_x = self.gyrs_x[0] * dt
        current_gyro_angle_y = self.gyrs_y[0] * dt
        self.gyro_angles_x[0] = current_gyro_angle_x
        self.gyro_angles_y[0] = current_gyro_angle_y

        self.yaws = [0] * n
        self.rolls = [0] * n
        self.pitchs = [0] * n
        current_yaw = 0
        current_yaw = self.gyrs_z[0] + dt
        self.yaws[0] = current_yaw

        total_time = 0
        ERROR_YAW = 0
        ERROR_ROLL = 0
        ERROR_PITCH = 0
        for i in range(1, n):
            dt = self.timestamps[i] - self.timestamps[i - 1]
            total_time += dt
            current_gyro_angle_x += self.gyrs_x[i] * dt
            current_gyro_angle_y += self.gyrs_y[i] * dt
            self.gyro_angles_x[i] = current_gyro_angle_x
            self.gyro_angles_y[i] = current_gyro_angle_y

            current_yaw += self.gyrs_z[i] * dt
            self.yaws[i] = current_yaw
            self.rolls[i] = self.gyro_angles_x[i]
            self.pitchs[i] = self.gyro_angles_y[i]
           
        ERROR_YAW = self.yaws[-1] / total_time
        ERROR_ROLL = self.rolls[-1] / total_time
        ERROR_PITCH = self.pitchs[-1] / total_time

        total_time = 0
        current_yaw = 0
        current_yaw = self.gyrs_z[0] + dt
        for i in range(1, n):
            dt = self.timestamps[i] - self.timestamps[i - 1]
            total_time += dt
            current_gyro_angle_x += self.gyrs_x[i] * dt
            current_gyro_angle_y += self.gyrs_y[i] * dt
            self.gyro_angles_x[i] = current_gyro_angle_x
            self.gyro_angles_y[i] = current_gyro_angle_y

            self.yaws[i] -= ERROR_YAW * total_time
            self.rolls[i] -= ERROR_ROLL * total_time
            self.pitchs[i] -= ERROR_PITCH * total_time
           
        print(total_time)
        print("yaw error", self.yaws[-1] / total_time)
        print("roll error", self.rolls[-1] / total_time)
        print("pitch error", self.pitchs[-1] / total_time)

    def shift_timestamp(self):
        n = len(self.timestamps)
        if n == 0:
            print("Unable to use shift_timestamp function when the time stamp array lenght equals to 0")
            return
        
        shift_value = self.timestamps[0]
        for i in range(n):
            self.timestamps[i] -= shift_value

    def init_norms(self):
        self.norms = []
        n = len(self.timestamps)
        for i in range(n):
            self.norms.append(sqrt(self.accs_x[i] * self.accs_x[i] + self.accs_y[i] * self.accs_y[i] + self.accs_z[i] * self.accs_z[i]))

    def remove_gravity(self):
        norm_0 = self.norms[0]
        accx_0 = self.accs_x[0]
        accy_0 = self.accs_y[0]
        accz_0 = self.accs_z[0]

        to_remove_x = sqrt(norm_0**2 - (accy_0**2 + accz_0**2))
        to_remove_y = sqrt(norm_0**2 - (accx_0**2 + accz_0**2))
        to_remove_z = sqrt(norm_0**2 - (accx_0**2 + accy_0**2))

        for i in range(len(self.timestamps)):
            self.accs_x[i] -= to_remove_x
            self.accs_y[i] -= to_remove_y
            self.accs_z[i] -= to_remove_z

    def moyenne_acc(self):
        n = len(self.timestamps)
        self.moyenne = [0] * n
        for i in range(n):
            self.moyenne[i] = (self.accs_x[i] + self.accs_y[i] + self.accs_z[i]) / 3
        
        

    # Fonction pour la compensation de la gravité
    def compensate_gravity(self):
        alpha = 0.96
        for i in range(len(self.timestamps)):
            # Intégration des valeurs du gyroscope pour estimer l'angle d'inclinaison
            roll = self.rolls[i] / 180 * pi
            pitch = self.pitchs[i] / 180 * pi
            yaw = self.yaws[i] / 180 * pi

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

            accel = np.array([self.accs_x[i], self.accs_y[i], self.accs_z[i]]).reshape(-1, 1)
            projected_accel = np.dot(R_z, np.dot(R_y, np.dot(R_x, accel)))

            # Compensation de la gravité
            compensated_accel = projected_accel - np.array([0, 0, 1]).reshape(-1, 1)

            # Filtre complémentaire pour combiner l'accélération compensée et non compensée
            compensated_accel = alpha * compensated_accel + (1 - alpha) * np.array([self.accs_x[i], self.accs_y[i], self.accs_z[i]]).reshape(-1, 1)

            self.accs_x[i] = float(compensated_accel[0][0])
            self.accs_y[i] = float(compensated_accel[1][0])
            self.accs_z[i] = float(compensated_accel[2][0])


    def filter_gaussian(self, sigma=5):
        self.accs_x = gaussian_filter1d(self.accs_x, sigma)
        self.accs_y = gaussian_filter1d(self.accs_y, sigma)
        self.accs_z = gaussian_filter1d(self.accs_z, sigma)

    def plot(self):
        plt.figure(1)
        plot_utils.buffer_plot(self.timestamps, self.accs_x, "accs_x")
        plot_utils.buffer_plot(self.timestamps, self.accs_y, "accs_y")
        plot_utils.buffer_plot(self.timestamps, self.accs_z, "accs_z")
        if self.norms is not None:
            plot_utils.buffer_plot(self.timestamps, self.norms, "norms")
        if self.moyenne is not None:
            plot_utils.buffer_plot(self.timestamps, self.moyenne, "moyenne")
        plot_utils.buffer_line(self.timestamps, 0)
        plt.legend()

        plt.figure(2)
        plot_utils.buffer_plot(self.timestamps, self.rolls, "roll")
        plot_utils.buffer_plot(self.timestamps, self.pitchs, "pitch")
        plot_utils.buffer_plot(self.timestamps, self.yaws, "yaw")

        plot_utils.plot_buffered() 
