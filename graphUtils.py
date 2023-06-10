from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def show_3_subplot(x, y1, y2, y3, title, ylabel, xlabel):
    plt.subplot(3, 1, 1)
    plt.plot(x, y1)
    plt.xlabel(xlabel)
    plt.ylabel('X ' + ylabel)

    plt.subplot(3, 1, 2)
    plt.plot(x, y2)
    plt.xlabel(xlabel)
    plt.ylabel('Y ' + ylabel)

    plt.subplot(3, 1, 3)
    plt.plot(x, y3)
    plt.xlabel(xlabel)
    plt.ylabel('Z ' + ylabel)

    plt.suptitle(title)
    plt.show()
    
def plot_simple_segmentation(downsampled_timestamp, signal, signal_derivative, norm_gaussian, abs_signal, envelopp, segment_start, segment_end):
    
    plt.figure()
    plots_data(downsampled_timestamp, 
               "Normalised acceleration data [sqrt(x+y+z)]",
               False,
               "Normalised_acceleration_data",
               (signal, "signal"))

    plt.figure()    
    plots_data(downsampled_timestamp, 
               "Derivative of the acceleration",
               False,
               "Derivative",
               (signal_derivative, "derivative"))

    plt.figure()
    plots_data(downsampled_timestamp,
               "Gaussian filtered derivative",
               False,
               "Gaussian",
               (norm_gaussian, "gaussian"))

    plt.figure()
    plots_data(downsampled_timestamp, 
               "Adaptative envelopp for the [abs(signal filtered)]",
               False,
               "Adaptative",
               (abs_signal, "abs"), (envelopp, "envelopp") )

    plots_rectangles(y_signal=norm_gaussian,
                     segment_start_indices=segment_start,
                     segment_end_indices=segment_end,
                     need_buffer=True)

def plots_data(x:List[float], title:str, need_buffered:bool, *functions:List[Tuple[List[float],str]], file_name:str=None):
    if file_name is None:
        file_name = title

    plt.xlabel("Times (s)")
    plt.ylabel("Value")
    plt.title(title)

    ploted = []
    legend = []
    for func in functions:
        ploted.append(x)
        ploted.append(func[0])
        legend.append(func[1])
    plt.plot(*ploted)
    legend = tuple(legend)

    plt.legend(legend)
    
    if not need_buffered:
        plt.savefig(f"./images_saved/{file_name}.png")
        plt.show()

def plots_rectangles(y_signal:List[float], segment_start_indices:List[float], segment_end_indices:List[float], need_buffer:bool):
    _, ax = plt.subplots()
    for start, end in zip(segment_start_indices, segment_end_indices):
        # for exception, allow to throw errors
        if start > end:
            temp = start
            start = end
            end = temp
        print("Segment : Start = {} seconds, End = {} seconds".format(start, end))
        norm_gaussian_part = y_signal[start:end]
        min_y = min(norm_gaussian_part)
        max_y = max(norm_gaussian_part)
        ax.add_patch(Rectangle((start, min_y), end-start, max_y - min_y, fill=False))
    plt.plot(y_signal, label="filtered signal")
    plt.legend()
    plt.title("Segmentation check")
    if not need_buffer:
        plt.savefig(f"./images_saved/Segmentation_check.png")
        plt.show()