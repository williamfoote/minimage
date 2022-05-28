from application import app
from flask import Flask, redirect, render_template, url_for
import ast
import numpy as np

from application.packages import cornersFromEasy, graphItMPL, graphItPlotly, imagePixels
from application.packages.forms import RequestForm, RequestFormEasy, imageCompressForm

#########################################################################
########################### Demo Pages ##################################
#########################################################################

@app.route("/demo2D", methods = ('GET', 'POST'))
def demo2D():
    # Set these values all to None on the page refresh
    shape, visualize, cornerPoints, ipObject, solution, graphJSON = [None] * 6
    # Set decimals to zero for default integer-rounding
    decimals = 0
    # Set done = False if they haven't filled out form. Change if they submit form.
    done = False
    form = RequestForm()
    if form.validate_on_submit():
        # If they submitted, change done to True for rendering the page
        done = True
        decimals = form.decimals.data
        cornerPoints = ast.literal_eval(form.cornerPoints.data)
        shape = ast.literal_eval(form.shape.data)
        visualize = form.visualize.data
        ipObject = imagePixels.imagePixels(cornerPoints=cornerPoints,
            shape = shape)
        # Round array values using np.around() for text display
        # Convert back to a list to output the commas
        solution = np.around(ipObject.getGrid(), decimals = decimals).tolist()
        imagePixelsInfo = ({'cornerPoints': cornerPoints,
                              'shape': shape,
                              'visualize': visualize,
                              'solution':solution
                              })
        graphJSON = graphItPlotly.graphIt(imagePixelsInfo, dimension=2).ggjWrapper()
    return render_template('demo2D.html', form = form, graphJSON = graphJSON,
    solution = solution, visualize = visualize, done = done)

@app.route("/demo2DEasy", methods = ('GET', 'POST'))
def demo2DEasy():
    # Set these values all to None on the page refresh
    shape, visualize, cornerPoints, ipObject, solution, graphJSON, = [None] * 6
    bottomLeftX, bottomLeftY, topRightX, topRightY = [None] * 4
    # Set done = False if they haven't filled out form. Change if they submit form.
    done = False
    # Set decimals to zero for default integer-rounding
    decimals = 0
    form = RequestFormEasy()
    if form.validate_on_submit():
        # If they submitted, change done to True for rendering the page
        done = True
        bottomLeftX = form.bottomLeftX.data
        bottomLeftY = form.bottomLeftY.data
        topRightX = form.topRightX.data
        topRightY = form.topRightY.data
        cornerPoints = (cornersFromEasy.cornersFromEasy(bottomLeftX, bottomLeftY, topRightX, topRightY)).getSol().cornerPoints
        shape = (form.shapeM.data, form.shapeN.data)
        visualize = form.visualize.data
        ipObject = imagePixels.imagePixels(cornerPoints=cornerPoints,
            shape = shape)
        # Convert back to a list to output the commas
        solution = np.around(ipObject.getGrid(), decimals = decimals).tolist()
        imagePixelsInfo = ({'cornerPoints': cornerPoints,
                              'shape': shape,
                              'visualize': visualize,
                              'solution':solution
                              })
        graphJSON = graphItPlotly.graphIt(imagePixelsInfo, dimension=2).ggjWrapper()
    return render_template('demo2D-easy.html', form = form, graphJSON = graphJSON,
    solution = solution, visualize = visualize, done = done)

@app.route("/imageCompressor", methods = ('GET', 'POST'))  # this sets the route to the PCA page
def imageCompressor():
    data, rows, columns, n_components, n_components_prt, imgFilePath, kwargs, temp = [None] * 8
    form = imageCompressForm()
    if form.validate_on_submit():
        rows = form.imgRows.data 
        columns = form.imgCols.data
        # Coerce from str (SubmitField is always string value) to float
        n_components = float(form.varExplained.data)
        imgFilePath = form.imgSelection.data
        kwargs = {'rows':rows, 'columns':columns, 'imgFilePath':imgFilePath}
        temp = graphItMPL.mplGraphs(**kwargs)
        data = temp.buildFoundation().doPCA(n_components=n_components).makeMPLPlots()
        n_components_prt = str(n_components * 100) + '%'
    return render_template("imageCompressor.html", data = data, form = form, n_components_prt = n_components_prt)