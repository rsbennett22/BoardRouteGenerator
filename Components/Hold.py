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
        print(HoldType.convertHoldTypeToString(self.holdType))
        print(self.x)
        print(self.y)

    def generateStartHold(wall):
        # Randomly select a hold from first 4 rows on wall
        return wall.holds[randint(0, 19*4)]
    
    def generatePotentialHoldLocation(prevHold, distance, startAngle, endAngle, numPotentialPositions):
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
        randomPoint = randint(0, len(points)-1)
        
        return points[randomPoint]

class HoldType:
    JUG, CRIMP, SLOPER, PINCH, POCKET = range(5)

    def convertHoldTypeToString(num):
        match num:
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
            
    def convertToColourCode(num):
        match num:
            case HoldType.JUG:
                return 'g'
            case HoldType.CRIMP:
                return 'b'
            case HoldType.SLOPER:
                return 'y'
            case HoldType.PINCH:
                return 'm'
            case HoldType.POCKET:
                return 'k'

    def generateRandomHoldType():
        randomNum = randint(0, 4)
        match randomNum:
            case 0:
                return HoldType.JUG
            case 1:
                return HoldType.CRIMP
            case 2:
                return HoldType.SLOPER
            case 3:
                return HoldType.PINCH
            case 4:
                return HoldType.POCKET
            
'''
TESTING

TODO: Tidy up into test methods

hold = Hold.generateStartHold(10, 10, HoldType.JUG)
hold.print()
print("\n")
secondHold = Hold.generateNextHold(hold, HoldType.CRIMP, 1, 10, 170, 10)
secondHold.print()
'''