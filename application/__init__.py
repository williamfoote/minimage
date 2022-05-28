from flask import Flask

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object('config.productionConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('config.testingConfig')
else:  
    app.config.from_object('config.developmentConfig')

from application.routes import baseViews
from application.routes import functionalViews