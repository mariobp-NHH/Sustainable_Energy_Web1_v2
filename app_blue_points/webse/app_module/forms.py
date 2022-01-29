from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from webse.models import User

#Chat
class ChatFormUpdate(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Chat')

#M1_Ch1
class ModulsForm_m1_ch1_q1(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Python', 'Python'),
                                ('HTML', 'HTML')])
    submit = SubmitField('Programming Language')

class ModulsForm_m1_ch1_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('GitHub', 'GitHub'),
                                ('Heroku', 'Heroku')])
    submit = SubmitField('Server')

class ModulsForm_m1_ch1_q3(FlaskForm):
    type = RadioField(choices=['Easy', 'Medium', 'Difficult'],
                       validators=[InputRequired()])
    submit = SubmitField('Implementation')

#M1_Ch2
class ModulsForm_m1_ch2_q1(FlaskForm):
    identifier = StringField()
    question_str = StringField('App Module, Chapter 2, Question 1', validators=[DataRequired()])
    submit1 = SubmitField('Check')

class ModulsForm_m1_ch2_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('wind', 'wind'),
                                ('solar', 'solar')])
    submit = SubmitField('Type Energy')

class ModulsForm_m1_ch2_q3(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('income', 'income'),
                                        ('expense', 'expense')])
    submit = SubmitField('Type Income')

class ModulsForm_m1_ch2_q4(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('university', 'university'),
                                        ('school', 'school')])
    submit = SubmitField('Type Work')

class ModulsForm_m1_ch2_q5(FlaskForm):
    type = RadioField('Level',
                       choices=['Petrol', 'Electric', 'Hydrogen'],
                       validators=[InputRequired()])
    submit = SubmitField('Type type')
