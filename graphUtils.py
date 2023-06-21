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
               "Normalised data [sqrt(x+y+z)]",
               False,
               "Normalised_data",
               (signal, "signal"))

    plt.figure()    
    plots_data(downsampled_timestamp, 
               "Derivative",
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

    plt.figure()
    plt.subplot(4)
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

def plots_rectangles(y_signals: List[Tuple[List[float],str]], segment_start_indices: List[List[float]], segment_end_indices: List[List[float]], need_buffer: bool):
    _, ax = plt.subplots()
    patches = []
    lines = []

    for i, (y_signal, start_indices, end_indices) in enumerate(zip(y_signals, segment_start_indices, segment_end_indices)):
        line, = plt.plot(y_signal[0], label=y_signal[1])
        lines.append(line)
        for start, end in zip(start_indices, end_indices):
            if start > end:
                start, end = end, start
            norm_gaussian_part = y_signal[0][int(start):int(end)]
            min_y = min(norm_gaussian_part)
            max_y = max(norm_gaussian_part)
            rect = Rectangle((start, min_y), end - start, max_y - min_y, fill=False, edgecolor=line.get_color(), linewidth=3)
            ax.add_patch(rect)
            patches.append(rect)
        
        
    plt.legend()
    plt.title("Segmentation check")

    if not need_buffer:
        plt.savefig("./images_saved/Segmentation_check.png")
        plt.show()


def test(signals: List[Tuple[List[float], str]], rectangles: List[Tuple[float, float]], need_buffer: bool):
    _, ax = plt.subplots()
    patches = []
    lines = []

    for i in range(len(signals)):
        y_signal, label = signals[i]
        x_min, x_max = rectangles[i]

        line, = plt.plot(y_signal, label=label)
        lines.append(line)

        if len(y_signal) > 0:
            min_y = min(y_signal)
            max_y = max(y_signal)
            rect = Rectangle((x_min, min_y), x_max - x_min, max_y - min_y, fill=False, edgecolor=line.get_color(), linewidth=3)
            ax.add_patch(rect)
            patches.append(rect)

    plt.legend()
    plt.title("Merged Rectangles")

    if not need_buffer:
        plt.savefig("./images_saved/Merged_rectangle.png")
        plt.show()



