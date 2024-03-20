### Rafe Bennett 19/04/2024

import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backend_bases import MouseButton

def sortHolds(holds):
    return sorted(holds, key=lambda k: [k.y, k.x])

def plotHolds(holds, colour):
    for hold in holds:
        plt.plot(round(hold.x), round(hold.y), colour+"o")

def getHoldsFromFile():
    with open("holds.txt", "rb") as file:
        holds = pickle.load(file)
        return holds
    
def applyImageToPlt():
    img = mpimg.imread('../img/stokt_board.jpg')
    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])
    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])