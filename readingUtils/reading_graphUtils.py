from typing import List, Tuple

import matplotlib.pyplot as plt

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