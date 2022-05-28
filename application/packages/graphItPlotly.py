import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np

class graphIt(object):
    """Class for extracting important info from imagePixelsInfo dict for processing.
    Be able to output the solution as a dataframe and visually in 2D or 3D"""
    def __init__(self, imagePixelsInfo, dimension):
        self.imagePixelsInfo = imagePixelsInfo # This has all the data from the solutions page
        # Variables (keys) include: visualize, shape, cornerPoints, and the solution to the problem
        self.dimension = dimension # whether this is 2D or 3D
    def getInfo(self):
        """For processing the imagePixelsInfo including unpacking the shape tuple"""
        self.m, self.n = self.imagePixelsInfo['shape']
        self.numPixels = self.m * self.n
        # Later I will use np.reshape by (numPixels, dimension) to turn the solution as a list into a
        # dataframe
        return self

    def getGraphJSON(self):
        solution = self.imagePixelsInfo['solution']
        numPixels = self.numPixels
        dimension = self.dimension
        asArrayReshaped = np.array(solution).reshape((numPixels, dimension))
        if dimension == 2:
            self.df = pd.DataFrame(asArrayReshaped, columns = ['x', 'y'])
            self.fig = px.scatter(self.df, x='x', y='y').update_yaxes(
                                    scaleanchor = "x",
                                    scaleratio = 1,
                                  )
        graphJSON = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
    def ggjWrapper(self):
        """A wrapper for an existing, instantiated graphIt object"""
        return self.getInfo().getGraphJSON()