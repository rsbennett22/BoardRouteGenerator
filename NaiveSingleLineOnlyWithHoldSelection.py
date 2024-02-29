### Rafe Bennett 27/02/2024

'''
TODO:
    - Create data type to represent holds - done, implemented into what I already had
    - Randomly fill a grid with random holds / create a preset "wall" <- this will need some extra work - done
    - Generate a route that selects holds of a specific type
        - Want to be able to select a list of what hold types we want 
        - Need a method of choosing a hold in an area / finding the list of holds within an area
            - if multiple of type looking for, randomly choose one of them - done with random selection

    NEW TODO:
    - Amend algorithm to cater to going upwards more, amend the random selection to choose only ones where the y is greater or equal to the potential point
    - Fix not being able to generate if against wall - need to go back and select a different potential point
    - Fix next point y being smaller than the previous point y
    - Create verification methods
'''

from matplotlib import pyplot as plt
import math
from random import randint
from Components.Hold import Hold, HoldType
from Components.Wall import Wall

def plotHolds(holds, wall):
    wall.plotHolds()
    for hold in holds:
        plt.plot(hold.x, hold.y)
        # Plots the point as a red dot
        plt.plot(hold.x, hold.y, "ro")

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

    plt.xticks(range(0,11))
    plt.yticks(range(0,11))
    plt.show()


def createWall():
    wall = Wall([], [], [])
    wall.randomlyGenerateWall(10, 10)
    return wall


def generateRoute2():
    holds = []
    # Create a wall
    wall = createWall()
    # Create tree structure of wall
    gridWidth = 10
    gridHeight = 10
    wall.generateTreeRepresentation(gridWidth, gridHeight)
    # Generate a starting hold
    hold = Hold.generateStartHold(wall)

    while hold.y <= gridHeight:
        hold.print()
        holds.append(hold)
        potentialNextHoldLocation = Hold.generatePotentialHoldLocation(hold, 1, 10, 170, 10)
        hold = wall.selectHoldFromPotentialPoint(hold, potentialNextHoldLocation, 1.5)
        if hold == None:
            break

    plotHolds(holds, wall)
    plt.xticks(range(0,11))
    plt.yticks(range(0,11))
    plt.show()

# Run Program
#generateRoute()
generateRoute2()

'''
PAGES USED FOR HELP
'''