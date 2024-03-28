### Rafe Bennett 22/04/2024

import Helper
import RouteGenerationHelper
import matplotlib.pyplot as plt
import random

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
        DEBUG = True

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
        MAX_POINT_DISTANCE = int((1500 - startHold.y) / numOfMoves)
        Helper.plotHolds([startHold], "b")

        startHold.debugPrint(DEBUG)

        score = 0 #RouteGenerationHelper.calculateInitialScore(startHold)
        numOfHoldsGenerated = 1
        currentHold = startHold

        # Generate all holds but finish hold
        while(numOfHoldsGenerated < numOfMoves):
            Helper.debugPrint("Start score: " + str(score), DEBUG)
            MAX_POINT_Y = (numOfHoldsGenerated * MAX_POINT_DISTANCE) + startHold.y
            tmp = MAX_POINT_DISTANCE
            if score > 3 or score < -3:
                score = 0
                MAX_POINT_DISTANCE = MAX_POINT_DISTANCE + 50
            # The bug is back for not generating the correct amount of holds, hopefully score will fix it
            # If not regenerate the route from scratch

            # Generate potential points and choose a random one from list
            potentialPoints = RouteGenerationHelper.generatePotentialHoldLocations(currentHold, MAX_POINT_DISTANCE)
            Helper.plotPoints(potentialPoints, "g", DEBUG)
            Helper.debugPrint(("Length of potential points: " + str(len(potentialPoints)) + "\n"), DEBUG)
            weights = RouteGenerationHelper.calculateWeightsForPoints(currentHold, potentialPoints, score, MAX_POINT_Y)

            point = random.choices(potentialPoints, weights)[0]
            Helper.plotPoint(point, "y", DEBUG)

            score = RouteGenerationHelper.adjustScore(score, point, currentHold, MAX_POINT_Y)
            Helper.debugPrint("Updated score: " + str(score), DEBUG)
            Helper.debugPrint(weights, DEBUG)

            currentHold = RouteGenerationHelper.chooseHoldNearPotentialLocation(currentHold, holds, point, tree, coordinates, MAX_POINT_DISTANCE)
            Helper.plotHolds([currentHold], "m")
            if MAX_POINT_DISTANCE != tmp:
                MAX_POINT_DISTANCE = tmp

                
            numOfHoldsGenerated += 1

            # Routes still not reaching the top, need to figure out why, maybe a rewrite is in order using a new
            # approach

            '''
            - set score initially to 0
            - generate start hold
            - generate list of potential point locations
            - randomly choose a point
            - compare start hold y to point y
            - if point y < max_y_point / 2 increase score
            - if greater then decrease score
            - generate hold near the point
            
            loop for holds other than start hold:
                generate list of potential hold locations
                create weights for each point using the score -> weight = weight + (weight * score) / 5
                randomly choose point using weights
                compare current hold to point, adjust weight accordingly as above
                generate random hold near this point
                repeat
            '''
            '''
            # TODO point selection needs to be taking into account the score when randomly choosing a point
            point = None
            if numOfHoldsGenerated != 1:
                # Choose point but use score to determine weights
                # Calculate expected max y for the new point

                point = RouteGenerationHelper.choosePoint(currentHold, score, potentialPoints, MAX_POINT_Y)
            else:
                # At a start hold, choose a random point from the generated
                Helper.debugPrint("At start hold, choosing random point.", DEBUG)
                point = potentialPoints[randint(0, len(potentialPoints)-1)]
                

            # Calculate the score
            score = RouteGenerationHelper.calculateScoreFromNewPoint(score, point, currentHold, MAX_POINT_Y)
            
            Helper.debugPrint(("Point: " + str(point)), DEBUG)
            Helper.plotPoint(point, "y", DEBUG)
            # Choose a random hold in surrounding area to point
            newHold = RouteGenerationHelper.chooseHoldNearPotentialLocation(currentHold, holds, point, 
                                                                                tree, coordinates, MAX_POINT_DISTANCE)
            newHold.debugPrint(DEBUG)
            #score = RouteGenerationHelper.calculateNewScore(currentHold, newHold, score)

            currentHold = newHold
            currentHold.debugPrint(DEBUG)
            Helper.plotHolds([currentHold], "m")

            numOfHoldsGenerated = numOfHoldsGenerated + 1

        
        Helper.debugPrint("", DEBUG)
        '''
            
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