import matplotlib.pyplot as plt

from typing import List, Optional

def buffer_plot(x:List[float], y:List[float], name:Optional[str]=None) -> None:
    plt.plot(x, y, label=name)

def buffer_line(x:List[float], y:int) -> None:
    plt.plot(x, [y] * len(x), label=f"y={y}")

def plot_buffered() -> None:
    plt.legend()
    plt.show()