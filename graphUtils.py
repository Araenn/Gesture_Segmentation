import matplotlib.pyplot as plt

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

def plots_3_data(x, y1, y2, y3, title, ylabel, xlabel):

    plt.plot(x, y1, x, y2, x, y3)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(f"./images_saved/{title}.png")
    plt.show()
    