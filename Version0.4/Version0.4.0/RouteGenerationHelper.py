### Rafe Bennett 23/04/2024

import numpy as np
from scipy.spatial import cKDTree
import math
import random
from random import randint
import Helper

DEBUG = True

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

def calculateNewScore(prevHold, hold, score):
    if hold.y >= prevHold.y:
        Helper.debugPrint("Increasing score: ", DEBUG)
        score = score + 1
    # Maybe need to decrease it too?

    return score


def generatePotentialHoldLocations(prevHold, distance, startAngle = 10, endAngle = 170, numPotentialPositions = 30):
    # Generate arc of points at a set distance from the hold co ordinates
    points = []
    angle = startAngle
    step = (endAngle - startAngle) / (numPotentialPositions - 1)

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


def choosePoint(prevHold, score, points, maxDist):
    # Take into account the value of score to define likelihood of choosing a point higher up the wall
    '''
    Score being higher means greater chance to choose a point that's y is less than max y / 2
    Generate the weights for each point, then randomly choose based on weights
    '''
    #weights = calculateWeights(prevHold, score, points, maxDist)
    Helper.debugPrint("Calculated weights: " + str(weights), DEBUG)
    randomPoint = random.choices(points, weights)[0]
    Helper.debugPrint("Generated random point", DEBUG)
    return randomPoint


def calculateWeightsForPoints(hold, points, score, maxY):
    weights = []
    weight = 50
    print("MAX Y " + str(maxY))
    thresholdY = (hold.y + maxY) / 2
    print("Threshold: " + str(thresholdY))
    for point in points:
        if point[1] < thresholdY:
            weight = weight + ((weight * score) / 5)
        else:
            weight = weight - ((weight * score) / 5)
        
        weights.append(weight)
        weight = 50

    return weights

def adjustScore(score, point, hold, maxY):
    thresholdY = (hold.y + maxY) / 2
    if point[1] < thresholdY:
        score = score + 1
    else:
        score = score - 1
    return score


def chooseHoldNearPotentialLocation(currentHold, holds, point, tree, gridPoints, maxHoldDist):
    # Find all the points in tree at radius r to the point
    radius = 50
    indicesInRadius = tree.query_ball_point(point, r=radius)
    while len(indicesInRadius) == 0:
        print("Increasing search radius")
        # Double search area
        radius = radius * 2
        indicesInRadius = tree.query_ball_point(point, r=radius)

    # Get the points in the grid from the indices found
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()

    if DEBUG:
        for point in pointsInRadius:
            Helper.plotPoint(point, "k", DEBUG)

    # Find hold, check not too close, if exhaust list
            
    pointsCopy = pointsInRadius

    nextHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
    nextHold = Helper.findHoldByCoordinate(holds, nextHoldLocation)

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


def calculateScoreFromNewPoint(score, point, hold, maxDist):
    Helper.debugPrint("MAX DIST: " + str(maxDist), DEBUG)
    pointY = point[1]
    midY = (hold.y + maxDist) / 2
    Helper.debugPrint("Mid point y: " + str(midY), DEBUG)
    if pointY >= midY:
        Helper.debugPrint("Point greater than mid, increasing score.", DEBUG)
        score = score + 1
    else:
        Helper.debugPrint("Point less than mid, decreasing score.", DEBUG)
        score = score - 1

    return score


'''
https://www.geeksforgeeks.org/how-to-get-weighted-random-choice-in-python/
'''