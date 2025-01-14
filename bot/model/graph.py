import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from xy import XY

def DrawGraph(xy : XY,longX:np.array ,predictions : list, symbol):
    plt.plot(xy.X, xy.Y, color="red")
    colors = ['blue', 'green']
    algs = ['lr', 'svr']
    index = 0
    for prediction in predictions:
        plt.plot(longX, prediction, color=colors[index], label=algs[index])
        index += 1
    plt.suptitle(symbol)
    plt.legend()
    plt.show()