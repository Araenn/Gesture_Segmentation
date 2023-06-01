import matplotlib.pyplot as plt

def show_3_subplot(y, x1, x2, x3, title, ylabel, xlabel):
    plt.subplot(3, 1, 1)
    plt.plot(y, x1)
    plt.xlabel(xlabel)
    plt.ylabel('X ' + ylabel)

    plt.subplot(3, 1, 2)
    plt.plot(y, x2)
    plt.xlabel(xlabel)
    plt.ylabel('Y ' + ylabel)

    plt.subplot(3, 1, 3)
    plt.plot(y, x3)
    plt.xlabel(xlabel)
    plt.ylabel('Z ' + ylabel)

    plt.suptitle(title)