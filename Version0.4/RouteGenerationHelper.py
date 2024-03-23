### Rafe Bennett 23/04/2024

import numpy as np
from scipy.spatial import cKDTree
import math
import random
from random import randint
import Helper

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

def createCKDTree(holds):
    # CDK tree of holds where y is greater than start hold
    coordinates = []
    for hold in holds:
        coordinates.append((hold.x, hold.y))
    
    tree = cKDTree(coordinates)
    coordinates = np.array(coordinates)
    return (tree, coordinates)

def chooseStartHold(startHolds):
    randomHold = random.randrange(0, len(startHolds)-1)
    return startHolds[randomHold]

def calculateInitialScore(startHold):
    score = 0
    if startHold.y > 520:
        score = 1
    return score

def generatePotentialHoldLocations(prevHold, distance, startAngle = 0, endAngle = 180, numPotentialPositions = 30):
    # Generate arc of points at a set distance from the hold co ordinates
    points = []
    angle = startAngle
    step = (endAngle - startAngle) / numPotentialPositions

    while angle <= endAngle:
        # Generate point on arc for the angle
        x = prevHold.x + distance * math.cos(math.radians(angle))
        y = prevHold.y + distance * math.sin(math.radians(angle))

        x = round(x)
        y = round(y)

        # Check where the x and y is to filter bad points
        if x <= 1100 and x >= 70 and y < 1500:
            points.append([x, y])
        
        angle += step
    
    return points


def chooseHoldNearPotentialLocation(currentHold, holds, point, tree, gridPoints, debug, maxHoldDist):
    # Find all the points in tree at radius r to the point
    radius = 100
    indicesInRadius = tree.query_ball_point(point, r=radius)
    while len(indicesInRadius) == 0:
        print("Increasing search radius")
        # Double search area
        radius = radius * 2
        indicesInRadius = tree.query_ball_point(point, r=radius)

    # Get the points in the grid from the indices found
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()

    if debug:
        for point in pointsInRadius:
            Helper.plotPoint(point, "k", debug)

    # Randomly choose a point in the list and return it
    nextHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
    nextHold = Helper.findHoldByCoordinate(holds, nextHoldLocation)
    distanceToCurrentHold = calculateDistanceBetweenTwoHolds(currentHold, nextHold)
    while distanceToCurrentHold < ((maxHoldDist / 1.4)):
        Helper.debugPrint("Generated hold too close to previous hold, generating another.", debug)
        pointsInRadius.remove(nextHoldLocation)
        nextHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
        nextHold = Helper.findHoldByCoordinate(holds, nextHoldLocation)
        distanceToCurrentHold = calculateDistanceBetweenTwoHolds(currentHold, nextHold)

    #nextHold = Helper.findHoldByCoordinate(holds, nextHoldLocation)
    return nextHold
    


def calculateDistanceBetweenTwoHolds(hold1, hold2):
     return math.sqrt((hold1.x - hold2.x)**2 + (hold1.y - hold2.y)**2)

def findClosestHold(hold, holds):
    shortestDistance = 9999
    closestHold = None
    for h in holds:
        distance = calculateDistanceBetweenTwoHolds(hold, h)
        if distance < shortestDistance:
            closestHold = h
            shortestDistance = distance

    return closestHold
