### Rafe Bennett 23/02/2024 Basic Approach To Line Generation From A Single Point

'''
TODO:
    - Create methods outlined in notebook
    - Learn how to display a grid system with points connected
'''


from random import uniform, randint
import math
from matplotlib import pyplot as plt



### Define classes needed
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(self.x)
        print(self.y)



### Define methods needed
def generateStartingPoint(gridWidth, gridHeight):
    # Limit x and y choices to be in a range

    limitX = gridWidth / 10
    limitY = gridHeight / 5

    randomX = uniform(limitX, gridWidth - limitX)
    randomY = uniform(0, limitY)

    return Point(randomX, randomY)



def generateNextPoint(point, distance, startAngle, endAngle, numToGenerate):
    # Generate arc of points in an arc of theta at a set distance from the point

    points = []
    angle = startAngle
    step = (endAngle - startAngle) / numToGenerate

    while angle <= endAngle:
        # Generate point on arc for the angle
        x = point.x + distance * math.cos(math.radians(angle))
        y = point.y + distance * math.sin(math.radians(angle))
        newPoint = Point(x, y)
        points.append(newPoint)
        angle += step
    
    # Randomly select a point in the list
    randomPoint = randint(0, len(points)-1)
    
    return points[randomPoint]



def plotPoints(points):
    xPoints = []
    yPoints = []

    for point in points:
        xPoints.append(point.x)
        yPoints.append(point.y)

    # Plots the points as connected lines
    plt.plot(xPoints, yPoints)
    # Plots the point as a red dot
    plt.plot(xPoints, yPoints, 'ro')



def generateRoute(pointsToGenerate):
    iteration = 0
    points = []
    point = generateStartingPoint(10, 10)
    while iteration <= pointsToGenerate:
        points.append(point)
        point = generateNextPoint(point, 1, 10, 170, 10)
        iteration += 1
    
    plotPoints(points)

    plt.xticks(range(0,10))
    plt.yticks(range(0,10))
    plt.show()

def generateRoute():
    points = []
    gridWidth = 10
    gridHeight = 10
    point = generateStartingPoint(gridWidth, gridHeight)
    while point.y < gridHeight:
        points.append(point)
        point = generateNextPoint(point, 1, 10, 170, 10)
    
    plotPoints(points)

    plt.xticks(range(0,10))
    plt.yticks(range(0,11))
    plt.show()


# Run program
#generateRoute(15)

# Method that generates until at the top
generateRoute()



### Basic test methods

def testGenerateStartingPoint():
    grid = Grid(10, 10)
    startingPoint = generateStartingPoint(grid)
    startingPoint.print()

#testGenerateStartingPoint()

def testGenerateNextPoint():
    startingPoint = generateStartingPoint(10, 10)
    secondPoint = generateNextPoint(startingPoint, 1, 10, 170, 10)
    secondPoint.print()

#testGenerateNextPoint()


'''
PAGES USED FOR HELP

- w3schools and geeks4geeks to get libs
- stack overflow for point on circle circumference
- wikipedia for parametric form

'''