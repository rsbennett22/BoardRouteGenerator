### Rafe Bennett 30/03/2024

'''
TODO:
    - BUG: Editing a hold and then switching back to plotting, plotting a hold and then deleting deleted the last edited hold too
    - Needs a rewrite bad!! 
    - Undo doesn't work due to holds being constantly sorted, only works for last plotted point, maybe change behaviour to this
    - Worked for now with being able to edit plotted holds :)
'''

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import matplotlib.image as mpimg
from scipy.spatial import cKDTree
import pickle
import numpy as np
from Hold import Hold
import GlobalHelper

holds = set()
isPlotting = False
PROGRAM_MODE = "PLOTTING"
lastPlottedHold = None
lastEditedHold = None
lastDeletedHold = None
tmpHold = None
isChangingLocation = False
positionChangeHold = None

def on_click(event):
    global isPlotting
    global PROGRAM_MODE
    global holds
    global lastPlottedHold
    global lastEditedHold
    global lastDeletedHold
    global positionChangeHold

    global isChangingLocation 

    x = event.xdata
    y = event.ydata
    if x == None or y == None:
        return
    if event.button is MouseButton.LEFT and not isPlotting and PROGRAM_MODE == "PLOTTING" and not isChangingLocation:
        isPlotting = True
        plt.plot(int(x), int(y), "ro")
        plt.show()
        holdType = input("Enter the holdType: ")
        #difficulty = input("Enter hold difficulty: ")
        hold = Hold(x, y, holdType)
        holds.add(hold)
        isPlotting = False
        saveHoldCoOrdinates()
    
    if event.button is MouseButton.LEFT and PROGRAM_MODE == "EDITING":

        if isChangingLocation:
            positionChangeHold.x = x
            positionChangeHold.y = y
            holds.add(positionChangeHold)
            print("Successfully changed hold location")
            createGraph()
            holds = set(GlobalHelper.sortHolds(holds))
            GlobalHelper.plotHolds(holds)
            GlobalHelper.plotHolds([positionChangeHold], "b")
            positionChangeHold = None
            isChangingLocation = False
            saveHoldCoOrdinates()
            plt.show()
        else:
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

                '''
                ASK USER FOR INPUT ON WHAT PROPERTY THEY WANT TO EDIT
                IF CO-ORDINATES OF THE HOLD THEN ASK FOR USER TO CLICK WHERE
                '''

                foundHold = None
                for hold in holds:
                    holdLocation = [hold.x, hold.y]
                    if holdLocation == nearestHoldLocation:
                        print("Found hold")
                        hold.print()
                        foundHold = hold
                        break

                holds.remove(foundHold)
                property = input("What property do you want to change: ")
                if property == "position":
                    isChangingLocation = True
                    positionChangeHold = foundHold
                    print("Click where you want the new location to be...")
                    
                if property == "holdType":
                    holdType = input("Enter new hold type: ")
                    foundHold.holdType = holdType
                    holds.add(foundHold)

                    print("Successfully updated hold")
                    createGraph()
                    holds = set(GlobalHelper.sortHolds(holds))
                    GlobalHelper.plotHolds(holds, "r")
                    GlobalHelper.plotHolds([foundHold], "b")
                    saveHoldCoOrdinates()
                    plt.show()

    if event.button is MouseButton.LEFT and PROGRAM_MODE == "DELETE" and not isChangingLocation:
        pass

    if event.button is MouseButton.RIGHT and not isChangingLocation:
        # Undo method
        if PROGRAM_MODE == "PLOTTING":
            removeOrRestore = input("Remove or restore removed hold? ")
            if removeOrRestore == "remove":
                removeLastPlottedPoint()
            if removeOrRestore == "restore":
                if lastPlottedHold != None:
                    restoreLastPlottedPoint()  

            

    if event.button is MouseButton.MIDDLE and not isChangingLocation:
        loadOrSaveOrMode = input("Load existing file, save, or change mode? ")
        if loadOrSaveOrMode == "load":
            print("Loading file")
            # Load in the file
            holds = GlobalHelper.getHoldsFromFile()
            holds = set(holds)
            print("TYPE: "+ str(type(holds)))
            createGraph()
            GlobalHelper.plotHolds(holds, "r")
            isPlotting = False
            PROGRAM_MODE = "PLOTTING"
            lastPlottedHold = None
            lastEditedHold = None
            lastDeletedHold = None
            plt.show()

        if loadOrSaveOrMode == "save":
            holds = GlobalHelper.sortHolds(holds)
            saveHoldCoOrdinates()

        if loadOrSaveOrMode == "edit":
            PROGRAM_MODE = "EDITING"
            holds = set(GlobalHelper.sortHolds(holds))
            print("Changed mode to: "+ PROGRAM_MODE)

        if loadOrSaveOrMode == "plot":
            PROGRAM_MODE = "PLOTTING"
            print("Changed mode to: "+ PROGRAM_MODE)
        if loadOrSaveOrMode == "delete":
            PROGRAM_MODE = "DELETE"
            print("Changed mode to "+ PROGRAM_MODE)

def removeLastPlottedPoint():
    global lastPlottedHold
    print("Removing last hold.")
    if len(holds) > 0:
        lastPlottedHold = holds.pop()
    createGraph()
    GlobalHelper.plotHolds(holds, "r")
    plt.show()
    print("Removed last hold")

def restoreLastPlottedPoint():
    global lastPlottedHold
    holds.add(lastPlottedHold)
    createGraph()
    GlobalHelper.plotHolds(holds, "r")
    plt.show()
    print("Restored last deleted hold")

def saveHoldCoOrdinates():
    with open("holds.txt", 'wb') as file:
        pickle.dump(GlobalHelper.sortHolds(holds), file)
    print("Saved file")

def createGraph():
    plt.close()
    GlobalHelper.applyImageToPlt()
    plt.connect('button_press_event', on_click)

# Save this data to a new file
createGraph()
plt.show()


'''
PAGES USED FOR HELP

- https://stackoverflow.com/questions/34458251/plot-over-an-image-background-in-python

'''