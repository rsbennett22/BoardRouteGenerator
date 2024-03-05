### Rafe Bennett 05/03/2024

'''
TODO:
    - Create fresh implementation of hold datatype - done
    - Doesn't need any methods other than getters or setters and print - done
'''

class Hold:
    def __init__(self, x, y, holdType, difficulty):
        self.x = x
        self.y = y
        self.holdType = holdType
        self.difficulty = difficulty
    
    def print(self):
        print(self.x)
        print(self.y)
        print(self.holdType)
        print(self.difficulty)