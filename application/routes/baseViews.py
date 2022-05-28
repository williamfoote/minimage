from application import app

from flask import render_template

#########################################################################
########################### Base Pages ##################################
#########################################################################

# Defining the home page of our site
@app.route("/") # Defines the url address for this page
def home():
	return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/documentation")
def documentation():
    return render_template("documentation.html")

#########################################################################
########################### Error Pages #################################
#########################################################################

@app.errorhandler(404)
def page_not_found(e):
    return(render_template('404.html')), 404

@app.errorhandler(500)
def page_not_found(e):
    return(render_template('500.html')), 404

