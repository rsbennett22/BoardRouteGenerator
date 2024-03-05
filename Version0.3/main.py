### Rafe Bennett 04/03/2024

# This version is going to handle selecting holds on an actual wall, choosing the amount of holds to use, 
# and implementing the first iteration of a hold difficulty rating system

'''
TODO:
    - Create a way to plot the holds on a wall programmatically - done
    - Create the next iteration of the Hold class - done as part of above
        - include hold difficulty rating
    - Implement next iteration of route generation from scratch
        - need methods for generating the next hold
        - ability to choose amount of holds on the route
        - this is all to be done in the main method
'''

import pickle
from Hold import Hold

# Test load the data from file

with open("holds.txt", "rb") as file:
    holds = pickle.load(file)
    for hold in holds:
        hold.print()
        print()
