### Rafe Bennett 25/04/2024

import logging
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def sortHolds(holds):
    return sorted(holds, key=lambda k: [k.y, k.x])

def roundHoldCoordinates(holds):
    roundedHolds = holds
    for hold in roundedHolds:
        hold.x = round(hold.x)
        hold.y = round(hold.y)
    return roundedHolds

def plotHolds(holds, colour="r"):
    for hold in holds:
        plt.plot(hold.x, hold.y, colour+"o")


def getHoldsFromFile():
    with open("holds.txt", "rb") as file:
        holds = pickle.load(file)
        holds = sortHolds(holds)
        holds = roundHoldCoordinates(holds)
        return holds
    

def applyImageToPlt():
    img = mpimg.imread('../img/stokt_board.jpg')
    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])
    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])


def askUserForNumOfHolds():
    numOfHolds = -1
    while numOfHolds not in [range(0, 16)]:
        try:
            numOfHolds = int(input("Enter the number of holds wanted in the route: [0 - 15]"))
            return numOfHolds
        except ValueError:
            print("Invalid number")


def plotPoint(x, y, colour):
    plt.plot(x, y, colour+"o")


def askUserForHoldTypeWanted():
    holdTypes = ["j", "c", "p", "s", "all"]
    holdType = input("Enter hold type wanted: " + str(holdTypes))
    while holdType not in holdTypes:
        holdType = input("Enter hold type wanted: " + str(holdTypes))
    
    return holdType

