### Rafe Bennett 22/04/2024

'''
TODO:
    - Rewrite random route generation algorithm to work up to 12 moves
        - Needs to be modular, clear, easy to update
    
    - Create route generation algorithms based on hold type
        - All, just random alg
        - One to All holdType

    - Add click functionality:
        - for generating a new route
        - fpr changing what type of generation
'''

from generateRouteAllHolds import GenerateRouteAllHolds
from generateRouteCustomHoldSelection import GenerateRouteCustomHoldSelection

HOLD_TYPES = ["c", "j", "p", "s"]
SELECTED_HOLD_TYPES = set() 

def generateRoute(selectedHoldTypes):
    # This method asks the user what holds they want on the route
    # Then chooses the appropiate algorithm based on the user's input
    holdPreferences = input("Enter what hold type you want on the route (enter done when finished selecting): ")
    
    if len(holdPreferences) > 1 and holdPreferences != "done":
        handleEnterHoldTypeError()
    
    while holdPreferences != "done" or len(selectedHoldTypes) != 4:
        if holdPreferences in HOLD_TYPES:
            selectedHoldTypes.add(holdPreferences)
            holdPreferences = input("Enter what hold type you want on the route (enter done when finished selecting): ")
        else:
            if holdPreferences == "done":
                if len(selectedHoldTypes) == 0:
                    selectedHoldTypes = set(HOLD_TYPES)
                    print("All hold types selected for route generation.")
                break
            else:
                handleEnterHoldTypeError()
    
    print("Selected hold types:" + str(selectedHoldTypes))
    # Call generation algorithm that handles multiple hold types up to 3

    if len(selectedHoldTypes) == 4:
        # Call generate with all hold types algorithm (the random one)
        GenerateRouteAllHolds.generateRoute()
    else:
        # Call generate route with 1-3 hold types algorithm
        GenerateRouteCustomHoldSelection.generateRoute(selectedHoldTypes)


def handleEnterHoldTypeError():
    print("Invalid input. Hold types are: " + str(HOLD_TYPES))
    generateRoute()


generateRoute(SELECTED_HOLD_TYPES)