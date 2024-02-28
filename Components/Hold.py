### Rafe Bennett 27/02/2024

'''
TODO:
    - Create Hold data type
    - Create enum for hold types
    - Create method to generate a hold
'''

import math
from random import uniform, randint

class Hold:
    def __init__(self, x, y, holdType):
        self.x = x
        self.y = y
        self.holdType = holdType

    def print(self):
        print(HoldType.convertToString(self.holdType))
        print(self.x)
        print(self.y)

    def generateStartHold(gridWidth, gridHeight, holdType):
    # Limit x and y choices to be in a range

        limitX = gridWidth / 10
        limitY = gridHeight / 5

        randomX = uniform(limitX, gridWidth - limitX)
        randomY = uniform(0, limitY)

        return Hold(randomX, randomY, holdType)
    
    def generateNextHold(self, holdType, distance, startAngle, endAngle, numPotentialPositions):
    # Generate arc of points at a set distance from the hold co ordinates

        holds = []
        angle = startAngle
        step = (endAngle - startAngle) / numPotentialPositions

        while angle <= endAngle:
            # Generate point on arc for the angle
            x = self.x + distance * math.cos(math.radians(angle))
            y = self.y + distance * math.sin(math.radians(angle))
            
            newHold = Hold(x, y, holdType)
            holds.append(newHold)
            angle += step
        
        # Randomly select a point in the list
        randomHold = randint(0, len(holds)-1)
        
        return holds[randomHold]

class HoldType:
    JUG, CRIMP, SLOPER, PINCH, POCKET = range(5)

    def convertToString(holdType):
        match holdType:
            case 0:
                return "JUG"
            case 1:
                return "CRIMP"
            case 2:
                return "SLOPER"
            case 3:
                return "PINCH"
            case 4:
                return "POCKET"
            case 5:
                return "NONE"

            
'''
TESTING

TODO: Tidy up into test methods

hold = Hold.generateStartHold(10, 10, HoldType.JUG)
hold.print()
print("\n")
secondHold = Hold.generateNextHold(hold, HoldType.CRIMP, 1, 10, 170, 10)
secondHold.print()
'''