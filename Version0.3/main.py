### Rafe Bennett 04/03/2024

# This version is going to handle selecting holds on an actual wall, choosing the amount of holds to use, 
# and implementing the first iteration of a hold difficulty rating system

'''
TODO:
    - Create a way to plot the holds on a wall programmatically - done
    - Create the next iteration of the Hold class - done as part of above
        - include hold difficulty rating - done
        - implement into generation after it's done - TODO
    - Implement next iteration of route generation from scratch on the actual wall
        - need methods for generating the next hold - done
        - ability to choose amount of holds on the route - done
        - this is all to be done in the main method - done

    - Fix bug where a hold can't be generated - index out of bounds error
        - coming from: nextHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
        - suspect it's when the list length is already 1 - fixed
    
    - Implement choosing hold based on difficulty

    - Implement choosing hold based on hold type

    - Implement choosing last hold based on distance from current hold instead of randomly from list - done

    - Do these at very end!!!
    - Implement a method to save and load routes
        - Requires tracking all the moves into a list
        - Save to a file that the user names
        - Load from file by user typing in file name

    - Implement route history method, on every run the route is saved to a file
        - Implement method to select a route in the list of old routes and load it in / save it permanently

    - Next iteration will reduce chance of impossible moves
'''



import pickle, math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.spatial import cKDTree
from random import randint
from Hold import Hold


def defineAndPlotStartHolds(holds):
    # Start holds are holds at from the bottom to a height y
    startHolds = []
    for hold in holds:
        if hold.y < 580:
            startHolds.append(hold)
    plotHolds(startHolds, "g")
    return startHolds

def defineAndPlotFinishHolds(holds):
    # Finish holds are the holds at the very top of the wall
    finishHolds = []
    for hold in holds:
        if hold.y > 1450:
            finishHolds.append(hold)
    plotHolds(finishHolds, "b")
    return finishHolds

def chooseAndPlotStartHold(startHolds):
    randHold = startHolds[randint(0, len(startHolds)-1)]
    plotHolds([randHold], "m")
    return randHold

def createCKDTree(holds):
    # CDK tree of holds where y is greater than start hold
    coordinates = []
    for hold in holds:
        coordinates.append((hold.x, hold.y))
    
    tree = cKDTree(coordinates)
    coordinates = np.array(coordinates)
    return (tree, coordinates)

def generatePotentialHoldLocation(prevHold, startAngle = 15, endAngle = 165, numPotentialPositions = 20):
    # Generate arc of points at a set distance from the hold co ordinates
    distance = POTENTIAL_HOLD_DISTANCE

    points = []
    angle = startAngle
    step = (endAngle - startAngle) / numPotentialPositions

    while angle <= endAngle:
        # Generate point on arc for the angle
        x = prevHold.x + distance * math.cos(math.radians(angle))
        y = prevHold.y + distance * math.sin(math.radians(angle))
        
        points.append([x, y])
        angle += step
    
    # Randomly select a point in the list
    temp_points = points
    randomPoint = randint(0, len(points)-1)
    potentialPoint = points[randomPoint]
    while potentialPoint[0] >= 1100 or potentialPoint[0] <= 70 or potentialPoint[1] > 1500:
        print("Point x is too big / small, choosing another random point")
        if len(temp_points) > 1:
            temp_points.remove(potentialPoint)
            randomPoint = randint(0, len(temp_points)-1)
            potentialPoint = temp_points[randomPoint]
        else:
            break
    if len(temp_points) == 1:
        print("Randomly using a point")
        potentialPoint = points[randint(0, len(points)-1)]

    point_x = round(potentialPoint[0])
    point_y = round(potentialPoint[1])
    potentialPoint = (point_x, point_y)
    return potentialPoint

def chooseHoldNearPotentialPoint(point, tree, gridPoints):
    # Find all the points in tree at radius r to the point
    #print("POINT")
    #print(point)
    radius = 100
    indicesInRadius = tree.query_ball_point(point, r=radius)
    while len(indicesInRadius) == 0:
        print("Increasing search radius")
        # Increase double search area
        radius = radius * 2
        indicesInRadius = tree.query_ball_point(point, r=radius)
    #print(indicesInRadius)

    # Get the points in the grid from the indices found
    pointsInRadius = gridPoints[indicesInRadius]
    pointsInRadius = pointsInRadius.tolist()
    #print("POINTS IN RADIUS")
    #print(pointsInRadius)

    # Plot for testing
    #for point in pointsInRadius:
    #    plotPoint(point, "k")

    # Randomly choose a point in the list and return it
    if len(pointsInRadius) > 1:
        nextHoldLocation = pointsInRadius[randint(0, len(pointsInRadius)-1)]
        return nextHoldLocation
    else:
        return pointsInRadius[0]
    
def findNearestFinishHold(currentHold, finishHolds):
    smallestDist = 99999999
    nearestFinishHold = None
    for hold in finishHolds:
        dist = math.sqrt((currentHold.x - hold.x)**2 + (currentHold.y - hold.y)**2)
        if dist < smallestDist:
            smallestDist = dist
            nearestFinishHold = hold
    return nearestFinishHold


def generateRoute(numOfMoves):
    '''
    Generate a start hold
    Number of moves wanted dictates the likelihood of choosing a closer hold
    Generate the next hold
    Repeat until at a top hold, or number of holds is num of moves - 1 -> then choose a top hold
    '''
    
    # Set up plt
    applyImageToPlt()

    # Get holds from file, sort and plot them
    holds = getHoldsFromFile()
    holds = sortHolds(holds)
    plotHolds(holds, "r")

    # Create ckd representation of the holds
    ckd_tree = createCKDTree(holds)
    tree = ckd_tree[0]
    holdCoOrdinates = ckd_tree[1]

    # Plot where start and finish holds are
    startHolds = defineAndPlotStartHolds(holds)
    finishHolds = defineAndPlotFinishHolds(holds)

    # Generate a start hold
    currentHold = chooseAndPlotStartHold(startHolds)

    # Create a loop until at num of moves

    currentMove = 0
    while currentMove < numOfMoves - 1:
        # generate the next hold
        centerPoint = generatePotentialHoldLocation(currentHold)
        #plotPoint(centerPoint, "y")
        nextHoldLocation = chooseHoldNearPotentialPoint(centerPoint, tree, holdCoOrdinates)
        currentHold = Hold(nextHoldLocation[0], nextHoldLocation[1], "hold", 0)
        if checkIfHoldInFinishHolds(currentHold, finishHolds):
            print("Hold is a finish hold, breaking out early")
            break
        if currentMove != 7:
            plotHolds([currentHold], 'm')
        currentMove += 1
    
    # Choose a finish hold, TODO case of already on one
    if checkIfHoldInFinishHolds(currentHold, finishHolds):
        plotHolds([currentHold], 'm')
    else:
        print("Last hold was not a finish hold, selecting nearest finish hold instead")
        finishHold = findNearestFinishHold(currentHold, finishHolds)
        plotHolds([finishHold], "m")
    
    

def checkIfHoldInFinishHolds(hold, finishHolds):
    holdLocation = (hold.x, hold.y)
    for finishHold in finishHolds:
        finishHoldLocation = (finishHold.x, finishHold.y)
        if finishHoldLocation == holdLocation:
            return True
    return False

def applyImageToPlt():
    img = mpimg.imread('../img/stokt_board.jpg')
    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])
    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])

def getHoldsFromFile():
    with open("holds.txt", "rb") as file:
        holds = pickle.load(file)
        return holds

def plotHolds(holds, colour):
    for hold in holds:
        plt.plot(round(hold.x), round(hold.y), colour+"o")

def plotPoint(point, colour):
    plt.plot(point[0], point[1], colour+"o")

def sortHolds(holds):
    return sorted(holds, key=lambda k: [k.y, k.x])


NUM_OF_MOVES = 8
POTENTIAL_HOLD_DISTANCE = int(1500 / NUM_OF_MOVES)

generateRoute(NUM_OF_MOVES)
plt.show()


'''
Sites used:

https://stackoverflow.com/questions/37111798/how-to-sort-a-list-of-x-y-coordinates

'''