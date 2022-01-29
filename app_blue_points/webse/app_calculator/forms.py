from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from webse.models import User

###############################
###   App Calculator form   ###
###############################
class AddRecordForm(FlaskForm):
    kms = FloatField("Kilometers", [InputRequired()])
    transport_type = SelectField("Type of Transport",
                                 [InputRequired()],
                                 choices=[
                                     ('Bus', 'Bus'),
                                     ('Car', 'Car'),
                                     ('Plane', 'Plane'),
                                     ('Ferry', 'Ferry'),
                                     ('Scooter', 'E-Scooter'),
                                     ('Bicycle', 'Bicycle'),
                                     ('Motorbike', "Motorbike"),
                                     ('Walk', 'Walk')
                                 ])

    fuel_type = SelectField("Fuel Type",
                            validators=[InputRequired()], choices=[])

    gas = FloatField("kg/passenger km", [Optional()], description='Add CO2 kg/passenger km if known. \
                  Otherwise, leave blank and a default corresponding to the fuel \
                 type and vehicle average from "UK Government GHG Conversion Factors for Company Reporting" will be used')

    submit = SubmitField("Submit")