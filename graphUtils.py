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
    plt.plot(downsampled_timestamp, signal)
    plt.title("Normalised acceleration data [sqrt(x+y+z)]")
    plt.savefig(f"./images_saved/Normalised_acc.png")

    plt.figure()
    plt.plot(downsampled_timestamp, signal_derivative)
    plt.title("Derivative of the acceleration")
    plt.savefig(f"./images_saved/Derivative.png")

    plt.figure()
    plt.plot(downsampled_timestamp, norm_gaussian)
    plt.title("Gaussian filtered derivative")
    plt.savefig(f"./images_saved/Gaussian_filtered.png")
    plt.show()

    plt.figure()
    plt.plot(abs_signal, label='Filtered Signal')
    plt.plot(envelopp, label='Adaptive envelopp')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.legend()
    plt.title("Adaptative envelopp for the [abs(signal filtered)]")
    plt.savefig(f"./images_saved/Adaptative_envelopp.png")
    plt.show()

    # Print the segment start and end indices, and plot them (with rectangles)
    fig, ax = plt.subplots()
    for i in range(0, len(segment_start)):
        start = segment_start[i]
        end = segment_end[i]
        norm_gaussian_part = norm_gaussian[start:end]
        min_y = min(norm_gaussian_part)
        max_y = max(norm_gaussian_part)
        ax.add_patch(Rectangle((start, min_y), end-start, max_y - min_y, fill=False))
    plt.plot(norm_gaussian, label="filtered signal")
    plt.legend()
    plt.title("Segmentation check")
    plt.savefig(f"./images_saved/Segmentation_check.png")
    plt.show()

def plots_data(x:List[float], title:str, *functions:List[Tuple[List[float],str]]):

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
    plt.savefig(f"./images_saved/{title}.png")
    plt.show()