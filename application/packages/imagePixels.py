import numpy as np
class imagePixels(object):
    # I will create a class that has the necessary objects and methods to achieve the goals of the project
    # I use classes and objects (i.e. an Object-Oriented Programming approach) mostly for cleanliness of
    # code and reproducibility. If there's a bug in my code, it should be easy to address as well. By 
    # distributing my functions across multiple methods, I should be able to isolate an issue to one
    # method rather than having to decipher my code line by line out of a thousand lines later. Just my
    # personal preference, though.
    
    # The tradeoff is that the code needs to be ran in order, but on the backend
    # this should be fine – as the user won't be running the code manually anyway.
    def __init__(self, cornerPoints, shape):
        """Instantiate the object"""
        # Inputs: 
        # 1) Corner points are a list of four two-element tuples which are the corners of the rectangle
        # 2) shape is the mxn shape of the rectangle in terms of equally distances (in euclidian distance)
        # rows and columns
        # Uses:
        # 1) I will make a function getCorners which organizes the given corner points to give me
        # 2) The minimum and maximum of each x and y (four total values)
        
        # Use pt. 2: I'll then use list comprehension and numpy.linspace to turn these corner points
        # I've gotten with getCorners into an m x n x 2 list which is the output requested. 
        self.cornerPoints = cornerPoints
        self.shape = shape
        
    def getCorners(self):
        """Get the corners of the image"""
        # First, isolate the x and y values from the input using list comprehension. This is helpful in
        # A) isolating the x and y's and B) giving an easy to use data structure (list) for the next step.
        # Second, use min and max methods for lists to get the points I want (i.e. x_min, x_max, y_min, y_max).
        
        # Goal: This helper method will get the necessary extrema (mins and maxes) in getExtrema which will 
        # be the penultimate step to getGriddy – which outputs the final solution.
        self.exes = [x for x, y in self.cornerPoints]
        # An interesting note is that I use tuple unpacking but only want the respective element of the tuple
        # In the list I'm making. Recall each element of self.corner_points is a tuple, but we only want the 
        # First element for now (and the second later).
        self.whys = [y for x, y in self.cornerPoints]
        return self
        
    def getExtrema(self):
        """Get the minimum and maxiums of the x and y's of the image"""
        # This is pretty self explanatory. This method just gets the min and max of x and y, respectively.
        # We can use list comprehension with np.linspace(min_i, max_i, shape_j) where i = x, y
        # and j are the two shape_elements originally inputted in __init__
        self.xMin = min(self.exes)
        self.xMax = max(self.exes)
        self.yMin = min(self.whys)
        self.yMax = max(self.whys)
        return self
        
    def getGriddy(self):
        """Get the final grid for the image's pixel locations"""
        # Putting everything together, we need to make a cartesian-esque grid of the points within the 
        # rectangle we are trying to plot.
        
        # Note 1: the shape of the solution is (m x n x 2) (m rows and n columns of 2-element tuples)
        # Note 2: I did the y's on the middle (of three) list because of the convention of the solution.
        # I just wanted to copy the solution's output. It also makes logical sense because this makes
        # y's constant across the columns and x's constant across the rows
        self.solution = [[[x, y] for y in np.linspace(self.yMin, self.yMax, self.shape[1])]
         for x in np.linspace(self.xMin, self.xMax, self.shape[0])]
        return self.solution
    
    def getGrid(self):
        """Wrapper for the above functions"""
        # This is just the wrapper version of the above three
        # Takes in an unmodified imagePixels() object and outputs the solution
        return self.getCorners().getExtrema().getGriddy()