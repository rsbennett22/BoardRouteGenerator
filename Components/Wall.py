### Rafe Bennett 29/02/2024

'''
TODO:
    - Create a wall class that will store info on the holds
    - Create methods to generate a "wall"
        - Random hold, uniformed, set sequence
    - Create a method to plot the holds onto the wall
'''

from matplotlib import pyplot as plt
from scipy.spatial import cKDTree
import numpy as np
from random import randint
from Components.Hold import Hold, HoldType

class Wall:
    # In this version holds are uniformly spaced along the wall of size 10, 10

    def __init__(self, holds, tree, gridPoints):
        self.holds = holds
        self.tree = tree
        self.gridPoints = gridPoints

    def generateTreeRepresentation(self, gridWidth, gridHeight):
        gridWidth = gridWidth - (gridWidth / 10)
        x = np.arange(0, gridWidth, 0.5)
        y = np.arange(0, gridHeight, 0.5)
        xx, yy = np.meshgrid(x, y)
        gridPoints = np.column_stack((xx.ravel(), yy.ravel()))
        tree = cKDTree(gridPoints)
        self.tree = tree
        self.gridPoints = gridPoints

    def selectHoldFromPotentialPoint(self, prevHold, point, radius):
        indicesInRadius = self.tree.query_ball_point(point, r=radius)
        # Randomly choose hold in this
        pointsInRadius = self.gridPoints[indicesInRadius]
        print("POINTS IN RADIUS")
        print(pointsInRadius)
        # Randomly select a hold
        nextHold = pointsInRadius[randint(0, len(pointsInRadius)-1)]
        # Return the hold from the wall
        for hold in self.holds:
            if hold.x == nextHold[0] and hold.y == nextHold[1] and hold != prevHold:
                return hold

    def randomlyGenerateWall(self, gridWidth, gridHeight):
        # This generates a list of randomly selected holds
        holds = []
        gridWidth = gridWidth - (gridWidth / 10)
        y = 0
        while y <= gridHeight:
            x = 0
            while x <= gridWidth:
                holdType = HoldType.generateRandomHoldType()
                hold = Hold(x, y, holdType)
                holds.append(hold)
                x += 0.5
                
            y += 0.5

        self.holds = holds
        return self

    def plotHolds(self):
       for hold in self.holds:
           holdColour = HoldType.convertToColourCode(hold.holdType)
           plt.plot(hold.x, hold.y, "ko")
