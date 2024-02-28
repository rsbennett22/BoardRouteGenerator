### Rafe Bennett 27/02/2024

class HoldType:
    JUG, CRIMP, SLOPER, PINCH, POCKET, NONE = range(6)

    def convertToString(self):
        match self:
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