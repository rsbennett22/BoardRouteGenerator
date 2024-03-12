### Rafe Bennett 12/04/2024

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
    fileNames = ["holds.txt", "holds_with_holdType.txt"]
    fileNum = int(input("What file would you like to load: \n" + str(fileNames)))
    while fileNum not in [0,1]:
        fileNum = input("What file would you like to load: \n" + str(fileNames))

    with open(fileNames[fileNum], "rb") as file:
        holds = pickle.load(file)
        return holds
    
def applyImageToPlt():
    img = mpimg.imread('../img/stokt_board.jpg')
    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])
    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])