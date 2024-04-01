### Rafe Bennett 25/04/2024

import logging
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def sortHolds(holds):
    return sorted(holds, key=lambda k: [k.y, k.x])

def roundHoldCoordinates(holds):
    roundedHolds = holds
    for hold in roundedHolds:
        hold.x = round(hold.x)
        hold.y = round(hold.y)
    return roundedHolds

def plotHolds(holds, colour="r"):
    for hold in holds:
        plt.plot(hold.x, hold.y, colour+"o")


def getHoldsFromFile(fileName = "holds.txt"):
    with open(fileName, "rb") as file:
        holds = pickle.load(file)
        holds = sortHolds(holds)
        holds = roundHoldCoordinates(holds)
        return holds
    

def applyImageToPlt():
    img = mpimg.imread('../img/stokt_board.jpg')
    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])
    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])


def askUserForNumOfHolds():
    numOfHolds = -1
    while numOfHolds not in list(range(0, 16)):
        try:
            numOfHolds = int(input("Enter the number of holds wanted in the route: [0 - 15]"))
        except ValueError:
            print("Invalid number")

    return numOfHolds


def plotPoint(x, y, colour):
    plt.plot(x, y, colour+"o")


def askUserForHoldTypeWanted():
    holdTypes = ["j", "c", "p", "s", "all"]
    holdType = input("Enter hold type wanted: " + str(holdTypes))
    while holdType not in holdTypes:
        holdType = input("Enter hold type wanted: " + str(holdTypes))
    
    return holdType

def askUserToLoadOrGenerateRoute():
    loadOrGenerate = ""
    while loadOrGenerate not in ["l", "g"]:
        loadOrGenerate = str(input("Load existing route or generate a new one: [l, g]"))
    
    return loadOrGenerate


def askUserSaveRoute():
    saveRoute = ""
    while saveRoute not in ["y", "n"]:
        saveRoute = str(input("Save generated route? [y/n]"))

    return saveRoute


def saveRoute(route):
    with open("routes.txt", "ab") as file:
        routeName = input("Enter route name: ")
        pickle.dump((routeName, route), file)


def loadRoute():
    with open("routes.txt", "rb") as file:
        routes = []
        while True:
            try:
                routes.append(pickle.load(file))
            except EOFError:
                break
    
    if len(routes) > 0:
        routeNames = []
        for route in routes:
            # Print each route name
            routeNames.append(route[0])
            print(route[0])
        
        routeName = askUserWhichRouteToLoad(routeNames)
        
        for route in routes:
            if route[0] == routeName:
                return route[1]

    else:
        print("No routes saved!")
        return []

    

def askUserWhichRouteToLoad(routeNames):
    routeName = ""
    while routeName not in routeNames:
        routeName = str(input("Enter route name to load"))

    return routeName