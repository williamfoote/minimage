class cornersFromEasy(object):
    def __init__(self, bottomLeftX, bottomLeftY, topRightX, topRightY):
        self.xs = bottomLeftX, topRightX
        self.ys = bottomLeftY, topRightY
    def getSol(self):
        self.cornerPoints = [(x, y) for x in self.xs for y in self.ys]
        return self
        
