### Rafe Bennett 05/03/2024

'''
TODO:
    - Create hold classification standard
'''

class Hold:
    def __init__(self, x, y, holdType, holdSize="", angle="", difficulty="", holdColour="r"):
        self.x = x
        self.y = y
        self.holdType = holdType
        self.holdSize = holdSize
        self.angle = angle
        self.difficulty = difficulty
        self.holdColour = holdColour
    
    def print(self):
            print("holdType: " + str(self.holdType))
            print("x: " + str(self.x))
            print("y: " + str(self.y))
            print("holdSize: " + str(self.holdSize))
            print("angle: " + str(self.angle))
            print("difficulty: " + str(self.difficulty))
            print("holdColour: " + str(self.holdColour))

    def calculateDifficulty(self, prevHolds, hand, routeGrade):
        # Calculates the difficulty level given to the hold outlined below
        pass

    def calculateAngle(self):
        # Use computer vision to calculate the angle?
        pass

'''
Hold classification:
    - Hold type: Jug, Crimp, Pinch, Sloper
    - Hold size: Micro, Small, Medium, Large, this is the edge size
        - Micro: >= 8mm
        - Small: < 8mm to 14mm
        - Medium: < 14mm to 20mm
        - Large: < 20mm / Jug gets this automatically
    - Angle: How far from horizontal it is
    - Difficulty: 0, 1, 2, 3, 4, 5
        - 0 for V0-1
        - 1 for V1-3
        - 2 for V3-5
        - 3 for V5-7
        - 4 for V7-9
        - 5 for V9+
        This should be calculated by:
            - the previous hold parameters, take into account every hold already generated,
            - the overall difficulty of the route
            - how far from the previous hold
            - what hand it's for
            - the aims of the route
                - e.g more crimpy smaller edges at a specific grade changes what hold can be selected massively from 
                  V3 compared to V6 for example

    - USE THE BOLT HOLES TO CALCULATE THE ANGLE OF THE HOLD!!!
'''