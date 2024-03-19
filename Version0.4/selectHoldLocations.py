### Rafe Bennett 04/03/2024

'''
TODO:
    - Rewrite most of code making it clearer, tidy into helpers etc
    - Implement edit mode again but showing what hold has been changed
        - Make sure it saves the updated colour!!!
'''

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import matplotlib.image as mpimg
from scipy.spatial import cKDTree
import pickle
import numpy as np
from Hold import Hold
import Helper

holds = []
isPlotting = False
PROGRAM_MODE = "EDITING"

def on_click(event):
    global isPlotting
    global PROGRAM_MODE
    global holds
    x = event.xdata
    y = event.ydata
    if x == None or y == None:
        return
    if event.button is MouseButton.LEFT and not isPlotting and PROGRAM_MODE == "PLOTTING":
        isPlotting = True
        plt.plot(int(x), int(y), "ro")
        plt.show()
        holdType = input("Enter the holdType: ")
        #difficulty = input("Enter hold difficulty: ")
        hold = Hold(x, y, "hold", 0)
        holds.append(hold)
        isPlotting = False
    
    if event.button is MouseButton.LEFT and PROGRAM_MODE == "EDITING":
        '''
        Methods required for editing
        - Sorting the holds - done on every code path
        - Adding all the holds to a cKDTree - done
        - Finding the nearest hold to a left click, change it's colour
        - Get the hold from the list
            - Ask for user input for the holdType value (add in difficulty later)
        '''
        coordinates = []

        for hold in holds:
            coordinates.append((hold.x, hold.y))
        
        coordinates = np.array(coordinates)

        tree = cKDTree(coordinates)
        # Got x and y
        # Query tree, slowly increase radius until find points
        # Query against all points found to see which is nearest
        print([x, y])
        nearestPoints = tree.query_ball_point([x, y], r=1)
        radius = 1
        while len(nearestPoints) == 0:
            nearestPoints = tree.query_ball_point([x,y], r=radius)
            radius = radius + 1
        
        print(nearestPoints)
        nearestHoldLocations = coordinates[nearestPoints]
        nearestHoldLocation = []
        if len(nearestHoldLocations) == 1:
            # Convert location to coordinate
            nearestHoldLocation = nearestHoldLocations[0]
            nearestHoldLocation = [nearestHoldLocation[0], nearestHoldLocation[1]]
        
            # Iterate list of holds to find coordinate
            for hold in holds:
                holdLocation = [hold.x, hold.y]
                if holdLocation == nearestHoldLocation:
                    print("Found hold")
                    hold.print()
                    holdType = input("Enter new hold type: ")
                    hold.holdType = holdType
                    print("Successfully updated hold")
                    Helper.plotHolds([hold], "b")
                    plt.show()
                    break

    
    if event.button is MouseButton.RIGHT and PROGRAM_MODE == "PLOTTING":
        # Remove the last point
        removeLastPoint()

    if event.button is MouseButton.MIDDLE:
        loadOrSaveOrMode = input("Load existing file, save, or change mode? ")
        if loadOrSaveOrMode == "load":
            print("Loading file")
            # Load in the file
            plt.close()
            createGraph()
            plt.show()

        if loadOrSaveOrMode == "save":
            holds = Helper.sortHolds(holds)
            saveHoldCoOrdinates()

        if loadOrSaveOrMode == "edit":
            PROGRAM_MODE = "EDITING"
            holds = Helper.sortHolds(holds)
            print("Changed mode to: "+ PROGRAM_MODE)

        if loadOrSaveOrMode == "plot":
            PROGRAM_MODE = "PLOTTING"
            print("Changed mode to: "+ PROGRAM_MODE)

def removeLastPoint():
    print("Removing last hold.")
    holds.pop()
    createGraph()
    for hold in holds:
        plt.plot(hold.x, hold.y, "ro")

    plt.show()

def saveHoldCoOrdinates():
    with open("holds_with_holdType.txt", 'wb') as file:
        pickle.dump(holds, file)
    print("Saved file")

def createGraph():
    plt.close()
    global holds
    holds = Helper.getHoldsFromFile()

    Helper.applyImageToPlt()
    Helper.plotHolds(holds, "r")
    holds = Helper.sortHolds(holds)

    plt.connect('button_press_event', on_click)

# Save this data to a new file

createGraph()
plt.show()


'''
PAGES USED FOR HELP

- https://stackoverflow.com/questions/34458251/plot-over-an-image-background-in-python

'''