### Rafe Bennett 22/04/2024

import Helper
import RouteGenerationHelper
import matplotlib.pyplot as plt
from random import randint

class GenerateRouteAllHolds:
    def generateRoute(numOfMoves=8):
        print("Generating route with all holds selected...\n")

        '''
        TODO:
            - Rewrite random generation algorithm here
            - Create a generateRouteHelper class to hold shared code for every generation algorithm
            - Ensure modularity and easy updating for this algorithm as it will be the base for 
              different versions of generation
            - Generation works up to 12 holds
        '''
        POTENTIAL_HOLD_DISTANCE = int(1400 / numOfMoves)
        DEBUG = False

        generatedRoute = []

        Helper.setupPltPlotted([])

        holds = Helper.getHoldsFromFile()
        holds = Helper.sortHolds(holds)
        holds = set(holds)

        startHolds = RouteGenerationHelper.defineStartHolds(holds)
        finishHolds = RouteGenerationHelper.defineFinishHolds(holds)

        Helper.plotHoldsDebug(startHolds, "r", DEBUG)
        Helper.plotHoldsDebug(finishHolds, "b", DEBUG)

        treeAndCoOrds = RouteGenerationHelper.createCKDTree(holds)
        tree = treeAndCoOrds[0]
        coordinates = treeAndCoOrds[1]

        startHold = RouteGenerationHelper.chooseStartHold(startHolds)
        Helper.plotHolds([startHold], "b")

        startHold.debugPrint(DEBUG)

        score = RouteGenerationHelper.calculateInitialScore(startHold)
        Helper.debugPrint("Score: " + str(score), DEBUG)

        numOfHoldsGenerated = 0

        currentHold = startHold
        while(numOfHoldsGenerated < numOfMoves):

            # The bug is back for not generating the correct amount of holds, hopefully score will fix it
            # If not regenerate the route from scratch

            # Generate potential points and choose a random one from list
            potentialPoints = RouteGenerationHelper.generatePotentialHoldLocations(currentHold, POTENTIAL_HOLD_DISTANCE)
            Helper.debugPrint(("Length of potential points: " + str(len(potentialPoints)) + "\n"), DEBUG)

            # TODO point selection needs to be taking into account the score when randomly choosing a point
            point = potentialPoints[randint(0, len(potentialPoints)-1)]
            Helper.debugPrint(("Point: " + str(point)), DEBUG)
            Helper.plotPoint(point, "y", DEBUG)

            # Choose a random hold in surrounding area to point
            currentHold = RouteGenerationHelper.chooseHoldNearPotentialLocation(currentHold, holds, point, 
                                                                                tree, coordinates, DEBUG, POTENTIAL_HOLD_DISTANCE)
            currentHold.debugPrint(DEBUG)
            Helper.plotHolds([currentHold], "m")

            numOfHoldsGenerated = numOfHoldsGenerated + 1
        
        Helper.debugPrint("", DEBUG)
            
        plt.show()

        '''
        Get a set of holds from file
            - Ensure sorted
            - define start and finish holds
        Create a ckdTree representation
        Choose a random start hold
        Create a score for how likely the next hold won't be as high up the wall 
            - set higher or lower depending on the number of moves initially
        loop:
            Generate the collection of potential next holds at a set distance
            randomly choose a hold but with the current score taken into account
            if hold y > (max distance / 2) increase the score, else decrease it

            if on last loop, check if the hold is a finish hold, if it is -> finish, else select the nearest finish hold

        Verify route length is correct
        if route generation still doesn't create a route with the number of holds being correct,
        re-run the entire algorithm until it's true

        Display the route generated
        Done
        '''

GenerateRouteAllHolds.generateRoute()