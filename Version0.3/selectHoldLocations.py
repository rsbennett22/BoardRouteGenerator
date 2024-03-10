### Rafe Bennett 04/03/2024

'''
TODO:
    - Set the background on matplot lib to picture of depot wall - done
        - Figure out a way to easily get the co-ords of each hold / plot them myself in the program
    - implement method to input data about that hold while plotting it
        - create new hold data type - done
        - on click, display the point, ask for hold information wanted for new hold data type - done
        - save this data to a file - done
'''

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import matplotlib.image as mpimg
import pickle
from Hold import Hold

holds = []
isPlotting = False

def on_click(event):
    global isPlotting
    x = event.xdata
    y = event.ydata
    if x == None or y == None:
        return
    if event.button is MouseButton.LEFT and not isPlotting:
        isPlotting = True
        x = int(event.xdata)
        y = int(event.ydata)
        plt.plot(x, y, "ro")
        plt.show()
        holdType = input("Enter the holdType: ")
        #difficulty = input("Enter hold difficulty: ")
        hold = Hold(x, y, "hold", 0)
        holds.append(hold)
        isPlotting = False

    
    if event.button is MouseButton.RIGHT:
        # Remove the last point
        removeLastPoint()

    if event.button is MouseButton.MIDDLE:
        saveHoldCoOrdinates()

def removeLastPoint():
    print("Removing last hold.")
    holds.pop()
    createGraph()
    for hold in holds:
        plt.plot(hold.x, hold.y, "ro")

    plt.show()

def saveHoldCoOrdinates():
    print("Writing holds to file.")
    with open("holds_with_holdType_and_difficulty.txt", 'wb') as file:
        pickle.dump(holds, file)

def createGraph():
    plt.close()
    img = mpimg.imread('../img/stokt_board.jpg')

    # Display the image
    plt.imshow(img, extent=[0, img.shape[1], 0, img.shape[0]])

    # Adjust axis limits to start from 0
    plt.xlim(0, img.shape[1])
    plt.ylim(0, img.shape[0])
    plt.connect('button_press_event', on_click)

# Save this data to a new file

createGraph()
plt.show()


'''
PAGES USED FOR HELP

- https://stackoverflow.com/questions/34458251/plot-over-an-image-background-in-python

'''