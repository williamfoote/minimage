import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import base64
from io import BytesIO
from matplotlib.figure import Figure
from .imagePixels import imagePixels
import copy
from math import cos, sin, pi


greyToHex = pd.read_csv('application/static/hexToGrey.csv', index_col = 0)

class mplGraphs(object):
    '''For processing image files for PCA dimensionality reduction'''
    def __init__(self, rows, columns, imgFilePath):
        '''Instantiate the object'''
        self.rows = rows
        self.columns = columns
        # Make the actual file name from the choice
        # Note: might change this if they select Lena/Baboon from a dropdown
        self.imgFilePath = imgFilePath
    def getInfrastructure(self):
        '''Need the attributes to self to plot the points'''
        fin = open(self.imgFilePath)
        # dtype is because of type of file. Haven't added functionality for other
        # types with numpy limitations.
        img = np.fromfile(fin, dtype = np.uint8,
                count = self.rows * self.columns)
        # Want a deep copy of img we'll use it in two ways
        # 1) we want 2D version to do PCA on
        # 2) we want 1D version to concatenate with x, y coordinates
        # The dataframe from (2) would have shape (x*y, 3) at this point
        self.img2D = copy.deepcopy(img)
        self.img2D.shape = (self.img2D.size // self.columns, self.columns)
        # R is the rotational matrix to reflect across the Y
        # For some reason np reads it in rotated 90 degrees counterclockwise.
        # I account for that here
        theta = pi/2
        self.R = np.around(np.array((cos(theta), sin(theta),
                                     -sin(theta), cos(theta))).reshape(2, 2))
        return self
    def integrateImagePixels(self):
        '''Using the information from above, turn this into an imagePixels object
        and get the x, y values'''
        # Note this is a different shape than above in img.shape
        shape = (self.rows, self.columns)
        # To use with arange to get cornerPoints from shape information
        # Note, I've decided this range starts from 1 if we upload our own picture
        rowUpperLim = (self.rows * 2) - 1
        colUpperLim = (self.columns * 2) - 1
        cornerPoints = [(x, y)
                            for x in np.arange(1, rowUpperLim, self.rows - 1)
                                for  y in np.arange(1, colUpperLim, self.columns - 1)]
        self.imagePixels = imagePixels(cornerPoints, shape)
        return self
    def getCoords(self):
        '''use the imagePixels.getGrid() method to get the xy values as an array
        Then, unpack these into XY values'''
        # First, get the "solution" (per the assignment instructions) which is in a
        # (rows, cols, 2) shape right now. We'll unpack this with numpy
        # and use pandas to get a (rows * cols, 2)-shaped array.
        solution = self.imagePixels.getGrid()
        arr = np.array(solution).reshape(self.rows * self.columns, 2)
        self.arr = arr
        return self
    def doPCA(self, n_components):
        '''Take image array information and do Principal Components Analysis (PCA)
        using sklearn after scaling the data. Output a 1D-array to concatenate with
        x, y values. Note: this step can be skipped if just plotting the original
        image without PCA.'''
        img2D = self.img2D
        # create scaler and pca objects to fit to the data
        scaler = StandardScaler()
        pca = PCA(n_components=n_components)
        # Transform/fit data
        scaled = scaler.fit_transform(img2D)
        pca.fit(scaled)
        # Based on PCA results, transform the scaled data to new values
        transformed = pca.transform(scaled)
        # Inverse the transformations to get back on (0, 255) scale
        mined_img = pca.inverse_transform(transformed)
        final = scaler.inverse_transform(mined_img).astype('uint8')
        # Reshape the data to one-dimensional array
        final2 = final
        final2.shape = (-1, 1)
        # Note, important to swtich back to ('uint8') format
        self.img = final
        return self
    def rotXY(self):
        '''Reflect XY values. Due to how numpy reads in the image, it led
        to the images being reflected vertically (i.e. upside down).'''
        xy = self.arr
        self.arr = (self.R @ xy.transpose()).transpose()
        return self
    def concatItems(self):
        '''Concatenate the two arrays of xy values and greyscale color info (i.e. img).
        Should have 3-column dataframe after this'''
        combnDF = pd.DataFrame(np.concatenate([self.arr, self.img], axis = 1),
                columns = ['x', 'y', 'grey'])
        self.combnDF = combnDF
        return self
    def makeGrey(self):
        '''Create row by row grayscale info to convert from (0, 255) to hex'''
        # Use simply dataframe.merge method for this to left join grey to hex
        # on greyscale information (both are 'grey' in the respective dataframe)
        updatedDF = self.combnDF.merge(greyToHex, how = 'left', on = 'grey')
        self.combnDF = updatedDF
        return self
    def makeGraphs(self):
        df = self.combnDF
        fig = Figure()
        ax = fig.subplots()
        ax.scatter(df.x, df.y, marker = '.', c = df.hexCode, s = 1)
        ax.axis('off')
        ax.set_aspect('equal')
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight')
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
    def buildFoundation(self):
        return self.getInfrastructure().integrateImagePixels().getCoords()
    def makeMPLPlots(self):
        return self.rotXY().concatItems().makeGrey().makeGraphs()