### Rafe Bennett 25/04/2024

import logging
import RouteHelper
import GlobalHelper
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GENERATED_ROUTE = []
holds = None
startHolds = []
finishHolds = []
startHold = None
finishHold = None
tree = None
holdPoints = None
WIDEN_ROUTE = False
MAX_DIST = 230


def setup():
    global GENERATED_ROUTE
    global holds
    global startHolds
    global finishHolds
    global startHold
    global finishHold
    global tree
    global holdPoints
    global WIDEN_ROUTE
    GlobalHelper.applyImageToPlt()
    holds = GlobalHelper.getHoldsFromFile()
    treeAndHoldPoints = RouteHelper.generateCkdTreeWithHoldPoints(holds)
    tree = treeAndHoldPoints[0]
    holdPoints = treeAndHoldPoints[1]
    startHolds = RouteHelper.defineStartHolds(holds)
    finishHolds = RouteHelper.defineFinishHolds(holds)
    startHold = RouteHelper.randomlySelectHoldFromList(startHolds)
    finishHold = RouteHelper.randomlySelectHoldFromList(finishHolds)
    GENERATED_ROUTE.append(startHold)
    GENERATED_ROUTE.append(finishHold)


def algorithm(numOfHolds):
    global GENERATED_ROUTE
    global tree
    global holdPoints
    global finishHolds

    currentHold = 0
    midHold = None

    # Check if 0, 1 or 2 holds chosen
    lessThanTwoHoldsWanted = RouteHelper.checkIfLessThanTwoHoldsWanted(numOfHolds)

    if (lessThanTwoHoldsWanted):
        if numOfHolds == 0:
            # Empty board
            GENERATED_ROUTE = []
        if numOfHolds == 1:
            # One hold wanted
            GENERATED_ROUTE = [GENERATED_ROUTE[0]]

    # Increase current hold by 2 as start hold and finish hold been generated already
    currentHold = 2
    while currentHold < numOfHolds and not lessThanTwoHoldsWanted:
        
        # Find the hold with the largest distance to the next hold in list
        largestDistHolds = RouteHelper.findLargestDistanceBetweenHolds(GENERATED_ROUTE)
        hold1 = largestDistHolds[0]
        hold2 = largestDistHolds[1]
        hold1Pos = largestDistHolds[2]

        # Generate the midHold and insert into route
        midHold = RouteHelper.createMidHold(hold1, hold2, holds, tree, holdPoints, finishHolds, GENERATED_ROUTE)
        GENERATED_ROUTE.insert(hold1Pos+1, midHold)
        
        currentHold += 1
    


def runProgram():
    global GENERATED_ROUTE
    global holds

    setup()
    numOfHolds = GlobalHelper.askUserForNumOfHolds()
    algorithm(numOfHolds)
    GlobalHelper.plotHolds(GENERATED_ROUTE, "b")
    plt.show()


runProgram()


def testAlgorithmGeneratesExpectedLengthRoutes():
    # Generate 10 routes for each route length 0 - 15, verify the route length is correct
    global GENERATED_ROUTE
    numFailed = 0
    numPassed = 0

    for i in range(15):
        for y in range(50):
            setup()
            # Generate 10 routes per route length i
            algorithm(i)
            if (len(GENERATED_ROUTE) != i):
                numFailed += 1
            else:
                numPassed += 1
            GENERATED_ROUTE = []
    print("FAILED: " + str(numFailed) + "\nPASSED: " + str(numPassed))

#testAlgorithmGeneratesExpectedLengthRoutes()
