### Rafe Bennett 29/04/2024

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


def randomlySelectHoldFromList(holds, holdType):
    holdsOfHoldType = []
    for hold in holds:
        if hold.holdType == holdType:
            holdsOfHoldType.append(hold)
    if holdType == "all":
        return holds[randint(0, len(holds)-1)]
    else:
        return holdsOfHoldType[randint(0, len(holdsOfHoldType)-1)]


def createMidHold(hold1, hold2, holds, tree, gridPoints, finishHolds, generatedRoute, holdType):
    midPointX = (hold1.x + hold2.x) / 2
    midPointY = (hold1.y + hold2.y) / 2

    # TODO: Add some variation to this point here? Kind of resolved in generateRandomMidhold 

    # Check if start and finish in line, if so vary the first midpoint generated's x point
    if len(generatedRoute) == 2:
        if checkIfStartAndFinishInLine(hold1, hold2):
            # Vary the x point
            varyMidPoint = input("Vary the midpoint: [y/n]")
            if varyMidPoint == "y":
                print("Varying midpoint!")
                midPointX = varyMidPointX(hold1.x, hold2.x)
            else:
                pass

    midPoint = (midPointX, midPointY)

    #Debug stuff
    #GlobalHelper.plotPoint(midPointX, midPointY, "y")

    # Find an area of holds around the midpoint
    midHold = generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints, holdType)
    isMidHoldSuitable = checkIfMidHoldSuitable(midHold, finishHolds, generatedRoute)
    
    while not isMidHoldSuitable:
        midHold = generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints, holdType)
        isMidHoldSuitable = checkIfMidHoldSuitable(midHold, finishHolds, generatedRoute)

    return midHold
    

def generateRandomMidHoldAroundMidPoint(midPoint, holds, tree, gridPoints, holdType):
    # Find all the points in tree at radius r to the point
    radius = 50
    indicesInRadius = tree.query_ball_point(midPoint, r=radius)
    
    # Increasing this makes the route spread out more as more holds to choose from randomly
    while len(indicesInRadius) < 15 or not checkIfHoldOfHoldTypeInGeneratedHolds(gridPoints, indicesInRadius, holds, holdType):
        # Double search area
        print("Increasing search radius")
        radius = radius + 25
        indicesInRadius = tree.query_ball_point(midPoint, r=radius)

    # Get the points in the grid from the indices found
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()

    # Debug stuff
    #for point in pointsInRadius:
    #    GlobalHelper.plotPoint(point[0], point[1], "k")

    # Convert list of points to holds
    generatedHolds = []
    for point in pointsInRadius:
        generatedHolds.append(getHoldAtLocation(point, holds))

    # Check what the holdType is
    if holdType != "all":
        holdsOfHoldType = []
        for hold in generatedHolds:
            if hold.holdType == holdType:
                holdsOfHoldType.append(hold)
        return holdsOfHoldType[randint(0, len(holdsOfHoldType)-1)]
    else:
        return generatedHolds[randint(0, len(generatedHolds)-1)]


def getHoldAtLocation(point, holds):
    for hold in holds:
            if hold.x == point[0] and hold.y == point[1]:
                return hold
            

def checkIfStartAndFinishInLine(startHold, finishHold):
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
        distance = calculateDistanceBetweenPoints(hold1.x, hold1.y, hold2.x, hold2.y)
        holdDistances.append(distance)
    
    largestDistancePos = -1
    largestDistance = -1
    if len(holdDistances) > 1:
        for i in range(0, len(holdDistances)):
            if holdDistances[i] > largestDistance:
                largestDistance = holdDistances[i]
                largestDistancePos = i
    else:
        largestDistance = holdDistances[0]
        largestDistancePos = 0
    
    return (generatedRoute[largestDistancePos], generatedRoute[largestDistancePos + 1], largestDistancePos)


def calculateDistanceBetweenPoints(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def checkIfLessThanTwoHoldsWanted(numOfHolds):
    if numOfHolds <= 2:
        return True
    else:
        return False
    

def checkIfGeneratedHoldTooCloseToAnyHoldInRoute(generatedRoute, newHold):
    # Prevent bunching of holds by forcing at least 1 hold of distance
    for hold in generatedRoute:
        distance = calculateDistanceBetweenPoints(hold.x, hold.y, newHold.x, newHold.y)

        # Vary this value to increase / decrease distances between holds on route
        if distance <= 100:
            return True
    return False


def checkIfMidHoldInList(holds, newHold):
    for hold in holds:
        if newHold == hold:
            return True
    return False


def checkIfMidHoldSuitable(midHold, finishHolds, generatedRoute):
    isTooClose = checkIfGeneratedHoldTooCloseToAnyHoldInRoute(generatedRoute, midHold)
    isAFinishHold = checkIfMidHoldInList(finishHolds, midHold)
    isInGeneratedRoute = checkIfMidHoldInList(generatedRoute, midHold)

    if not isTooClose and not isAFinishHold and not isInGeneratedRoute:
        return True
    return False


def varyMidPointX(x1, x2):
    distanceToLeft = -1
    distanceToRight = -1
    maxX = -1
    # Get distances to both walls based on both holds
    if x1 < x2:
        # Closer to left
        distanceToLeft = x1
        distanceToRight = 1100 - x2
        # Was originally divided by 3, testing out increasing variation area, same for else statement
        maxX = x2 + (distanceToRight / 2)
    else:
        distanceToLeft = x2
        distanceToRight = 1100 - x1
        maxX = x1 + (distanceToRight / 2)

    # Calculate the bounds to randomise the distance in, split each dist into 3 and get closest third to mid
    #minX = (2 * distanceToLeft) / 3
        
    # Smaller minX
    minX = distanceToLeft / 2

    #GlobalHelper.plotPoint(minX, 300, "r")
    #GlobalHelper.plotPoint(maxX, 300, "r")

    # Generate and return random x between these points
    return randint(int(minX), int(maxX))


def checkIfHoldOfHoldTypeInGeneratedHolds(gridPoints, indicesInRadius, holds, holdType):
    if holdType == "all":
        return True
    
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()

    # Convert list of points to holds
    generatedHolds = []
    for point in pointsInRadius:
        generatedHolds.append(getHoldAtLocation(point, holds))

    for hold in generatedHolds:
        if hold.holdType == holdType:
            return True
    return False