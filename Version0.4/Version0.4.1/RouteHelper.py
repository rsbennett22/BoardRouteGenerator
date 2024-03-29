### Rafe Bennett 25/04/2024

import logging
import numpy as np
from scipy.spatial import cKDTree
import math
import random
from random import randint
import matplotlib.image as mpimg
import GlobalHelper


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

img = None

def getImg():
    global img
    img = mpimg.imread('../../img/stokt_board.jpg')

def defineStartHolds(holds):
    # Start holds are holds at from the bottom to a height y
    startHolds = []
    for hold in holds:
        if hold.y < 580:
            startHolds.append(hold)
    return startHolds



def defineFinishHolds(holds):
    # Finish holds are the holds at the very top of the wall
    finishHolds = []
    for hold in holds:
        if hold.y > 1450:
            finishHolds.append(hold)
    return finishHolds


def generateCkdTreeWithHoldPoints(holds):
    # CDK tree of holds where y is greater than start hold
    holdPoints = []
    for hold in holds:
        holdPoints.append((hold.x, hold.y))
    
    tree = cKDTree(holdPoints)
    holdPoints = np.array(holdPoints)
    return (tree, holdPoints)


def randomlySelectStartHold(startHolds):
    randomHold = randint(0, len(startHolds)-1)
    return startHolds[randomHold]


def randomlySelectFinishHold(finishHolds):
    randomHold = randint(0, len(finishHolds)-1)
    return finishHolds[randomHold]


def createMidHold(hold1, hold2, holds, tree, gridPoints, generatedRoute):
    midPointX = (hold1.x + hold2.x) / 2
    midPointY = (hold1.y + hold2.y) / 2

    # TODO: Add some variation to this point here

    midPoint = (midPointX, midPointY)

    GlobalHelper.plotPoint(midPointX, midPointY, "y")
    # Find an area of holds around the midpoint
    midHold = generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints)
    while midHold in generatedRoute:
        print("GENERATED HOLD ALREADY IN ROUTE, CHOOSING ANOTHER")
        midHold = generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints)
    return midHold
    



def generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints):
    # Find all the points in tree at radius r to the point
    radius = 50
    indicesInRadius = tree.query_ball_point(midPoint, r=radius)
    
    # Increasing this makes the route spread out more as more holds to choose from randomly
    while len(indicesInRadius) < 15:
        print("Increasing search radius")
        # Double search area
        radius = radius + 25
        indicesInRadius = tree.query_ball_point(midPoint, r=radius)

    # Get the points in the grid from the indices found
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()

    # Debug stuff
    #for point in pointsInRadius:
    #    GlobalHelper.plotPoint(point[0], point[1], "k")

    midHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
    midHold = getHoldAtLocation(midHoldLocation, holds)
    return midHold


def getHoldAtLocation(point, holds):
    for hold in holds:
            if hold.x == point[0] and hold.y == point[1]:
                return hold
            

def generateMidpoints(generatedRoute):
    midPoints = []

    # NOTE: May not want to check start and finish hold at a certain point
        # Check if start hold at a wall
    '''
    startHold = generatedRoute[0]
    finishHold = generatedRoute[len(generatedRoute)-1]
    startHoldMidPoint = generateStartHoldMidpoint(startHold)
    if startHoldMidPoint != None:
        midPoints.append(startHoldMidPoint)

     # Check if finish hold at a wall
    finishHoldMidpoint = generateFinishHoldMidpoint(finishHold)
    if finishHoldMidpoint != None:
        midPoints.append(finishHoldMidpoint)
    '''
    # Generate midpoints between holds
    for i in range(0, len(generatedRoute)-1):
        hold1 = generatedRoute[i]
        hold2 = generatedRoute[i + 1]

        midPoint = (hold1.x + hold2.x) / 2
        midPoints.append(midPoint)
    
    return midPoints

def generateStartHoldMidpoint(startHold):
    if checkHoldNotAtWall(startHold):
        print("Start hold not at wall")
        closestWallLimitValue = findNearestWall(startHold.x)
        midPoint = (startHold.x + closestWallLimitValue) / 2
        return midPoint
    else:
        return None
    
def generateFinishHoldMidpoint(finishHold):
    if checkHoldNotAtWall(finishHold):
        closestWallLimitValue = findNearestWall(finishHold.x)
        midPoint = (finishHold.x + closestWallLimitValue) / 2
        return midPoint
    else:
        return None

def checkHoldNotAtWall(hold):
    if hold.x <= 1100 and hold.x >= 70:
        return True
    return False

def findNearestWall(x):
    distToLeft = x - 70
    distToRight = 1100 - x
    if distToLeft < distToRight:
        return "L"
    else:
        return "R"


def randomlyChooseMidpoint(midPoints):
    return midPoints[randint(0, len(midPoints)-1)]

def areStartAndFinishInLine(startHold, finishHold):
    if (startHold.x >= finishHold.x - 200) and (startHold.x <= finishHold.x + 200):
        return True
    else:
        return False
    

def findLargestDistanceBetweenHolds(generatedRoute):
    # This finds the pair of holds with largest distance between them and returns them both

    holdDistances = []
    for i in range(0, len(generatedRoute) - 1):
        hold1 = generatedRoute[i]
        hold2 = generatedRoute[i+1]
        distance = calculateDistanceBetweenTwoHolds(hold1, hold2)
        holdDistances.append(distance)
    print("HOLD DISTANCES: " + str(holdDistances))
    
    largestDistancePos = -1
    largestDistance = -1
    if len(holdDistances) > 1:
        for i in range(0, len(holdDistances)):
            if holdDistances[i] > largestDistance:
                print("Found bigger dist: " + str(holdDistances[i]))
                largestDistance = holdDistances[i]
                largestDistancePos = i
    else:
        largestDistance = holdDistances[i]
        largestDistancePos = i
    
    return (generatedRoute[largestDistancePos], generatedRoute[largestDistancePos + 1], largestDistancePos)


def calculateDistanceBetweenTwoHolds(hold1, hold2):
    return math.sqrt((hold1.x - hold2.x)**2 + (hold1.y - hold2.y)**2)


def generateMidpoint(hold1, hold2, maxDist):
    midPointX = (hold1.x + hold2.x) / 2
    midPointY = randint(hold1.y, hold1.y + maxDist + 50)

    return (midPointX, midPointY)

def checkIfLessThanTwoHoldsWanted(numOfHolds):
    if numOfHolds <= 2:
        return True
    else:
        return False