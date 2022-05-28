from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, NumberRange

class RequestForm(FlaskForm):
    cornerPoints = StringField('Insert a list of corner points:', validators=[InputRequired()])
    decimals = IntegerField('Round solution (decimal places): ', validators=[InputRequired(), NumberRange(0, max = 10)])
    cornerPoints = StringField('Insert a list of corner points:', validators=[InputRequired()])
    shape = StringField('Insert a tuple of (row, column) size dimensions:', validators=[InputRequired()])
    visualize = BooleanField('Graph the results?', default='checked')

class RequestFormEasy(FlaskForm):
    bottomLeftX = IntegerField('Bottom left corner: (', validators=[InputRequired(), NumberRange(-100, max = 100)])
    bottomLeftY = IntegerField(',', validators=[InputRequired(), NumberRange(-100, max = 100)])
    topRightX = IntegerField('Top Right Corner: (', validators=[InputRequired(), NumberRange(-100, max = 100)])
    topRightY = IntegerField(', ', validators=[InputRequired(), NumberRange(-100, max = 100)])
    decimals = IntegerField('Rounding places for solution (digits): ', validators=[InputRequired(), NumberRange(0, max = 10)])
    shapeM = IntegerField('Number of rows: ', validators=[InputRequired(), NumberRange(1, max = 100)])
    shapeN = IntegerField('Number of columns: ', validators=[InputRequired(), NumberRange(1, max = 100)])
    visualize = BooleanField('Graph the results?', default='checked')

class imageCompressForm(FlaskForm):
    imgRows = IntegerField('Number of rows: ', validators=[InputRequired(), NumberRange(512, max = 512)])
    imgCols = IntegerField('Number of columns: ', validators=[InputRequired(), NumberRange(512, max = 512)])
    varExplained = SelectField('Select post-compression quality', choices=[('.99', '99%'), ('.95', '95%'), ('.9', '90%'),
        ('.75', '75%'), ('.5', '50%'), ('.25', '25%')], validators=[InputRequired()])
    imgSelection = SelectField('Select image to compress', choices=[('application/static/images/lena_gray.raw', 'lena')], validators=[InputRequired()])
    