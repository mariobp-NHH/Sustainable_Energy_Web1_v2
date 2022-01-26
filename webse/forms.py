from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from webse.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    course = SelectField('Course', validators=[DataRequired()],
                             choices=[('ENE425 Sustainable Energy and App Development', 'ENE425 Sustainable Energy and App Development'),
                                      ('Guest Course', 'Guest Course')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ChatFormUpdate(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Chat')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Annoucement')

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

#M2_Ch1: SE, Frame.
class ModulsForm_m2_ch1_e1(FlaskForm):
    type = SelectField(validators=[DataRequired(False)],
                       choices=[('Should include only environmental pollution, carbon emissions', 'Should include only environmental pollution, carbon emissions'),
                                ('Should include only poverty alleviation, gender equality', 'Should include only poverty alleviation, gender equality'),
                                ('Should include both', 'Should include both')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch1_e2(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Green Economy is more related to welfare and environmental economics', 'Green Economy is more related to welfare and environmental economics'),
                                ('Green Economy is more related to ecological economics', 'Green Economy is more related to ecological economics'),
                                ('Green Economy is more related to economics schools', 'Green Economy is more related to economics schools')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch1_q1(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Should only consider carbon emissions', 'Should only consider carbon emissions'),
                                ('Should only consider electrification', 'Should only consider electrification'),
                                ('Should also consider social aspects', 'Should also consider social aspects')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch1_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Pollution is a negative externality', 'Pollution is a negative externality'),
                                ('Sustainability and economy are a subsystem of the ecosystem', 'Sustainability and economy are a subsystem of the ecosystem'),
                                ('Research and technology are fundamental parts of agriculture development', 'Research and technology are fundamental parts of agriculture development')])
    submit = SubmitField('Submit')

#M2_Ch2: SE. Ch2. Ecological Footprint and Biocapacity
class ModulsForm_m2_ch2_e1(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('The ecological footprint should be charged to Norway', 'The ecological footprint should be charged to Norway'),
                                ('The ecological footprint should be charged to Spain', 'The ecological footprint should be charged to Spain'),
                                ('The ecological footprint should be charged partially to both countries', 'The ecological footprint should be charged partially to both countries')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_e2(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Land to capture carbon emissions', 'Land to capture carbon emissions'),
                                ('Cropland, grazing land, fishing grounds, and forest products land', 'Cropland, grazing land, fishing grounds, and forest products land'),
                                ('All the previous types of lands', 'All the previous types of lands')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_e3(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Land to capture carbon emissions', 'Land to capture carbon emissions'),
                                ('Cropland', 'Cropland'),
                                ('Fishing grounds', 'Fishing grounds')])
    submit = SubmitField('Submit')


class ModulsForm_m2_ch2_q1(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Biologically productive area it takes to satisfy the exporting demand', 'Biologically productive area it takes to satisfy the exporting demand'),
                                ('Biologically productive area it takes to satisfy the demands of people', 'Biologically productive area it takes to satisfy the demands of people'),
                                ('Biologically productive area it takes to satisfy the importing demand', 'Biologically productive area it takes to satisfy the importing demand')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Land and sea area available to provide the resources a population consumes and to absorb its wastes',
                                 'Land and sea area available to provide the resources a population consumes and to absorb its wastes'),
                                ('Land and sea area available for agriculture and fisheries',
                                 'Land and sea area available for agriculture and fisheries'),
                                ('Land area available for wildlife',
                                 'Land area available for wildlife')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q3(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Productive land required to absorb the carbon dioxide emissions',
                                'Productive land required to absorb the carbon dioxide emissions'),
                                ('Amount of carbon absorbed by oceans',
                                 'Amount of carbon absorbed by oceans'),
                                ('Both', 'Both')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q4(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Cropland, grazing land, fishing grounds (marine waters), forest, and built-up',
                                'Cropland, grazing land, fishing grounds (marine waters), forest, and built-up'),
                                ('Cropland, grazing land, fishing grounds (marine and inland waters), forest, and built-up',
                                 'Cropland, grazing land, fishing grounds (marine and inland waters), forest, and built-up'),
                                ('Cropland, grazing land, fishing grounds (marine and inland waters), and forest',
                                 'Cropland, grazing land, fishing grounds (marine and inland waters), and forest')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q5(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Reflect the relative productivity of a given land use type',
                                'Reflect the relative productivity of a given land use type'),
                                ('Reflect the relative productivity of cropland',
                                 'Reflect the relative productivity of cropland'),
                                ('Reflect the relative productivity of fishing grounds',
                                 'Reflect the relative productivity of fishing grounds')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q6(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Very suitable, suitable, moderately suitable, and marginally suitable',
                                'Very suitable, suitable, moderately suitable, and marginally suitable'),
                                ('Very suitable, suitable, marginally suitable, and not suitable',
                                 'Very suitable, suitable, marginally suitable, and not suitable'),
                                ('Very suitable, suitable, moderately suitable, marginally suitable, and not suitable',
                                 'Very suitable, suitable, moderately suitable, marginally suitable, and not suitable')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q7(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'In the 80s',
                                'In the 80s'),
                                ('In the 70s',
                                 'In the 70s'),
                                ('In the 90s',
                                 'In the 90s')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch2_q8(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'It represents the 50%','It represents the 50%'),
                                ('It represents the 40%','It represents the 40%'),
                                ('It represents the 60%', 'It represents the 60%')])
    submit = SubmitField('Submit')

#M2_Ch3: SE. Ch3. Human Development for the Anthropocene
class ModulsForm_m2_ch3_e1(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('The ecological footprint should be charged to Norway', 'The ecological footprint should be charged to Norway'),
                                ('The ecological footprint should be charged to Spain', 'The ecological footprint should be charged to Spain'),
                                ('The ecological footprint should be charged partially to both countries', 'The ecological footprint should be charged partially to both countries')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_e2(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Land to capture carbon emissions', 'Land to capture carbon emissions'),
                                ('Cropland, grazing land, fishing grounds, and forest products land', 'Cropland, grazing land, fishing grounds, and forest products land'),
                                ('All the previous types of lands', 'All the previous types of lands')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_e3(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Land to capture carbon emissions', 'Land to capture carbon emissions'),
                                ('Cropland', 'Cropland'),
                                ('Fishing grounds', 'Fishing grounds')])
    submit = SubmitField('Submit')


class ModulsForm_m2_ch3_q1(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Biologically productive area it takes to satisfy the exporting demand', 'Biologically productive area it takes to satisfy the exporting demand'),
                                ('Biologically productive area it takes to satisfy the demands of people', 'Biologically productive area it takes to satisfy the demands of people'),
                                ('Biologically productive area it takes to satisfy the importing demand', 'Biologically productive area it takes to satisfy the importing demand')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Land and sea area available to provide the resources a population consumes and to absorb its wastes',
                                 'Land and sea area available to provide the resources a population consumes and to absorb its wastes'),
                                ('Land and sea area available for agriculture and fisheries',
                                 'Land and sea area available for agriculture and fisheries'),
                                ('Land area available for wildlife',
                                 'Land area available for wildlife')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q3(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Productive land required to absorb the carbon dioxide emissions',
                                'Productive land required to absorb the carbon dioxide emissions'),
                                ('Amount of carbon absorbed by oceans',
                                 'Amount of carbon absorbed by oceans'),
                                ('Both', 'Both')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q4(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Cropland, grazing land, fishing grounds (marine waters), forest, and built-up',
                                'Cropland, grazing land, fishing grounds (marine waters), forest, and built-up'),
                                ('Cropland, grazing land, fishing grounds (marine and inland waters), forest, and built-up',
                                 'Cropland, grazing land, fishing grounds (marine and inland waters), forest, and built-up'),
                                ('Cropland, grazing land, fishing grounds (marine and inland waters), and forest',
                                 'Cropland, grazing land, fishing grounds (marine and inland waters), and forest')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q5(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Reflect the relative productivity of a given land use type',
                                'Reflect the relative productivity of a given land use type'),
                                ('Reflect the relative productivity of cropland',
                                 'Reflect the relative productivity of cropland'),
                                ('Reflect the relative productivity of fishing grounds',
                                 'Reflect the relative productivity of fishing grounds')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q6(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Very suitable, suitable, moderately suitable, and marginally suitable',
                                'Very suitable, suitable, moderately suitable, and marginally suitable'),
                                ('Very suitable, suitable, marginally suitable, and not suitable',
                                 'Very suitable, suitable, marginally suitable, and not suitable'),
                                ('Very suitable, suitable, moderately suitable, marginally suitable, and not suitable',
                                 'Very suitable, suitable, moderately suitable, marginally suitable, and not suitable')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q7(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'In the 80s',
                                'In the 80s'),
                                ('In the 70s',
                                 'In the 70s'),
                                ('In the 90s',
                                 'In the 90s')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q8(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'It represents the 50%','It represents the 50%'),
                                ('It represents the 40%','It represents the 40%'),
                                ('It represents the 60%', 'It represents the 60%')])
    submit = SubmitField('Submit')