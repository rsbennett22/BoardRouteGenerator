### Rafe Bennett 27/02/2024

'''
TODO:
    - Create data type to represent holds - done, implemented into what I already had
    - Randomly fill a grid with random holds / create a preset "wall" <- this will need some extra work
    - Generate a route that selects holds of a specific type
        - Want to be able to select a list of what hold types we want 
    - Create verification methods
'''


from random import uniform, randint
import math
from matplotlib import pyplot as plt
from Components.Hold import Hold
from Components.HoldType import HoldType

def plotHolds(holds):
    xHolds = []
    yHolds = []

    for hold in holds:
        xHolds.append(hold.x)
        yHolds.append(hold.y)

    # Plots the points as connected lines
    plt.plot(xHolds, yHolds)
    # Plots the point as a red dot
    plt.plot(xHolds, yHolds, 'ro')

def generateRoute():
    holds = []
    gridWidth = 10
    gridHeight = 10
    distance = 1
    startAngle = 10
    endAngle = 170
    numPotentialPositions = 10
    hold = Hold.generateStartHold(gridWidth, gridHeight, HoldType.JUG)
    while hold.y < gridHeight:
        holds.append(hold)
        hold = hold.generateNextHold(HoldType.CRIMP, distance, startAngle, endAngle, numPotentialPositions)
    
    plotHolds(holds)

    plt.xticks(range(0,10))
    plt.yticks(range(0,11))
    plt.show()


# Run Program
generateRoute()



### Basic test methods



'''
PAGES USED FOR HELP
'''