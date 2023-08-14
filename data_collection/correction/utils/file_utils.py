import os

from sequence_gesture import SequenceGesture
from typing import List

def file_exist(file_path_name:str) -> bool:
    return os.path.exists(file_path_name)

def get_gesture_file_content(file_path_name:str) -> SequenceGesture:
    if not file_exist(file_path_name):
        raise ValueError(f"The file \"{file_path_name}\" do not exist.")
    
    file = open(file_path_name, "r")
    file_lines:List[str] = file.readlines()
    file.close()
    
    timestamps = []
    gyrs_x = []
    gyrs_y = []
    gyrs_z = []
    accs_x = []
    accs_y = []
    accs_z = []

    for file_line in file_lines:
        file_line_infos = file_line.split(",")
        timestamps.append(float(file_line_infos[0]))

        gyr_x = float(file_line_infos[1])
        gyr_y = float(file_line_infos[2])
        gyr_z = float(file_line_infos[3])

        acc_x = float(file_line_infos[4])
        acc_y = float(file_line_infos[5])
        acc_z = float(file_line_infos[6])

        accs_x.append(acc_x)
        accs_y.append(acc_y)
        accs_z.append(acc_z)
        gyrs_x.append(gyr_x)
        gyrs_y.append(gyr_y)
        gyrs_z.append(gyr_z)

    return SequenceGesture(timestamps, gyrs_x, gyrs_y, gyrs_z, accs_x, accs_y, accs_z)



