### Rafe Bennett 04/03/2024

# This version is going to handle selecting holds on an actual wall, choosing the amount of holds to use, 
# and implementing the first iteration of a hold difficulty rating system

'''
TODO:
    - Rewrite most of code, maybe try refactoring into different service classes

    - Plot all holds with hold type
        - Ughhhh the painnnn

    - Make new generation algorithm
        - Make it clearer how it works
        - Tidy it up into more functions, maybe a helper class
        - Make it work up to 20 moves, requires backtracking
        - No clustering weirdly

    - Implement generation accounting hold type
        - Make it so it has to choose a specific hold type, the backtracking will be useful here
'''



import pickle, math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backend_bases import MouseButton
import numpy as np
from scipy.spatial import cKDTree
from random import randint
from Hold import Hold
import Helper


NUM_OF_MOVES = 10
GENERATED_ROUTES = []

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

def chooseAndPlotStartHold(startHolds):
    randHold = startHolds[randint(0, len(startHolds)-1)]
    Helper.plotHolds([randHold], "m")
    return randHold

def createCKDTree(holds):
    # CDK tree of holds where y is greater than start hold
    coordinates = []
    for hold in holds:
        coordinates.append((hold.x, hold.y))
    
    tree = cKDTree(coordinates)
    coordinates = np.array(coordinates)
    return (tree, coordinates)

def generatePotentialHoldLocation(prevHold, distance, startAngle = 15, endAngle = 165, numPotentialPositions = 20):
    # Generate arc of points at a set distance from the hold co ordinates

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
    
    route = []
    # Set up plt
    Helper.applyImageToPlt()

    # Get holds from file, sort and plot them
    global holds
    holds = Helper.sortHolds(holds)
    #plotHolds(holds, "r")

    # Create ckd representation of the holds
    ckd_tree = createCKDTree(holds)
    tree = ckd_tree[0]
    holdCoOrdinates = ckd_tree[1]

    # Plot where start and finish holds are
    startHolds = defineStartHolds(holds)
    finishHolds = defineFinishHolds(holds)
    #plotHolds(startHolds, "g")
    #plotHolds(finishHolds, "b")

    # Generate a start hold
    currentHold = chooseAndPlotStartHold(startHolds)
    POTENTIAL_HOLD_DISTANCE = int(1400 / NUM_OF_MOVES)
    route.append(currentHold)

    # Create a loop until at num of moves

    currentMove = 0
    while currentMove < numOfMoves:
        # generate the next hold
        centerPoint = generatePotentialHoldLocation(currentHold, POTENTIAL_HOLD_DISTANCE)
        #plotPoint(centerPoint, "y")
        nextHoldLocation = chooseHoldNearPotentialPoint(centerPoint, tree, holdCoOrdinates)
        currentHold = Hold(nextHoldLocation[0], nextHoldLocation[1], "hold", 0)
        if checkIfHoldInFinishHolds(currentHold, finishHolds):
            print("Hold is a finish hold, breaking out early")
            break
        if currentMove != 7:
            Helper.plotHolds([currentHold], 'm')
            route.append(currentHold)
        currentMove += 1
    
    # Choose a finish hold
    if checkIfHoldInFinishHolds(currentHold, finishHolds):
        Helper.plotHolds([currentHold], 'm')
        route.append(currentHold)
    else:
        print("Last hold was not a finish hold, selecting nearest finish hold instead")
        finishHold = findNearestFinishHold(currentHold, finishHolds)
        Helper.plotHolds([finishHold], "m")
        route.append(finishHold)

    GENERATED_ROUTES.append(route)
    

def checkIfHoldInFinishHolds(hold, finishHolds):
    holdLocation = (hold.x, hold.y)
    for finishHold in finishHolds:
        finishHoldLocation = (finishHold.x, finishHold.y)
        if finishHoldLocation == holdLocation:
            return True
    return False

def plotPoint(point, colour):
    plt.plot(point[0], point[1], colour+"o")

def on_click(event):
    if event.button is MouseButton.LEFT:
        print("Generating new route")
        plt.close()
        generateRoute(NUM_OF_MOVES)
        plt.connect('button_press_event', on_click)
        plt.show()

    if event.button is MouseButton.RIGHT:
        print("Saving the route to file")
        with open("routes.txt", "ab") as file:
            routeName = input("Enter route name: ")
            pickle.dump((routeName, GENERATED_ROUTES[len(GENERATED_ROUTES)-1]), file)
 
    if event.button is MouseButton.MIDDLE:
        print("Loading routes from file")
        with open("routes.txt", "rb") as file:
            routes_with_name = []
            while True:
                try:
                    routes_with_name.append(pickle.load(file))
                except EOFError:
                    break

            print("Route names:")
            routeNames = []
            routes = []
            for route in routes_with_name:
                routeNames.append(route[0])
                routes.append(route[1])
                # Print each route name
                print(route[0])

            routeName = input("What route to load? ")
            while (routeName not in routeNames) and (routeName != "cancel"):
                routeName = input("What route to load? ")

            if routeName != "cancel":
                # Display the route
                print("Loading " + routeName)
                plt.close()
                Helper.applyImageToPlt()
                index = routeNames.index(routeName)
                route = routes[index]
                Helper.plotHolds(route, 'm')
                plt.connect('button_press_event', on_click)
                plt.show()

holds = Helper.getHoldsFromFile()
plt.connect('button_press_event', on_click)
plt.show()

'''
Sites used:

https://stackoverflow.com/questions/37111798/how-to-sort-a-list-of-x-y-coordinates
https://stackoverflow.com/questions/12761991/how-to-use-append-with-pickle-in-python

'''