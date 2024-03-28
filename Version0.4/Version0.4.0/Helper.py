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

def plotHoldsDebug(holds, colour, debug):
    if debug:
        plotHolds(holds, colour)

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

def setupPltPlotted(holds):
    plt.close()
    applyImageToPlt()
    plotHolds(holds, "r")

def plotPoint(point, colour, debug):
    if debug:
        plt.plot(point[0], point[1], colour+"o")

def plotPoints(points, colour, debug):
    if debug:
        for point in points:
            plotPoint(point, colour, debug)

def debugPrint(message, debug):
    if debug:
        print(message)

def findHoldByCoordinate(holds, coordinate):
        for hold in holds:
            if hold.x == coordinate[0] and hold.y == coordinate[1]:
                return hold