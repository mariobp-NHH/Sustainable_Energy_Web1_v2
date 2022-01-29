from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Optional
from webse.models import User


class ChatFormUpdate(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Chat')

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
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('At the beginning of the Agricultural Revolution 12.000–15.000 years ago',
                                 'At the beginning of the Agricultural Revolution 12.000–15.000 years ago'),
                                ('In 1945 after the detonation of the first atomic bomb',
                                 'In 1945 after the detonation of the first atomic bomb'),
                                ('At the beginning of the Industrial Revolution',
                                 'At the beginning of the Industrial Revolution')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_e2(FlaskForm):
    type = SelectField(validators=[DataRequired()],
                       choices=[('Carbon emissions', 'Carbon emissions'),
                                ('Ecological Footprint', 'Ecological Footprint'),
                                ('Both', 'Both')])
    submit = SubmitField('Submit')



class ModulsForm_m2_ch3_q1(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('At the beginning of the Agricultural Revolution 12.000–15.000 years ago', 'At the beginning of the Agricultural Revolution 12.000–15.000 years ago'),
                                ('In 1945 after the detonation of the first atomic bomb', 'In 1945 after the detonation of the first atomic bomb'),
                                ('The debate about the starting date of the Antrophocene is still open', 'The debate about the starting date of the Antrophocene is still open')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q2(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('Homogenization of flora and fauna',
                                 'Homogenization of flora and fauna'),
                                ('One species (humans) consuming 25–40 percent of land net primary productivity',
                                 'One species (humans) consuming 25–40 percent of land net primary productivity'),
                                ('Increasing impact of new technologies as the biosphere interacts with the technosphere',
                                 'Increasing impact of new technologies as the biosphere interacts with the technosphere'),
                                ('Increase in arid areas',
                                 'Increase in arid areas')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q3(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Those elements do not interact with humans, and do not determine the relations of power and culture',
                                'Those elements do not interact with humans, and do not determine the relations of power and culture'),
                                ('Those elements do not interact with humans, and determine the relations of power and culture',
                                 'Those elements do not interact with humans, and determine the relations of power and culture')])
    submit = SubmitField('Submit')



class ModulsForm_m2_ch3_q4(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Chemical pollution, and ocean acidification',
                                'Chemical pollution, and ocean acidification'),
                                ('Freshwater use, and phosphorus cycle',
                                 'Freshwater use, and phosphorus cycle'),
                                ('Biodiversity loss, climate crisis, and nitrogen cycle',
                                 'Biodiversity loss, climate crisis, and nitrogen cycle')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q5(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('They are two independent imbalances that operate independently',
                                 'They are two independent imbalances that operate independently'),
                                ('They are two interdependent imbalances that reinforce each other',
                                 'They are two interdependent imbalances that reinforce each other')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q6(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'The cost of carbon in 2030 will be $75 per tonne of carbon dioxide in 2017 US dollars',
                                'The cost of carbon in 2030 will be $75 per tonne of carbon dioxide in 2017 US dollars'),
                                ('The cost of carbon in 2030 will be $50 per tonne of carbon dioxide in 2017 US dollars',
                                 'The cost of carbon in 2030 will be $50 per tonne of carbon dioxide in 2017 US dollars'),
                                ('The cost of carbon in 2030 will be $85 per tonne of carbon dioxide in 2017 US dollars',
                                 'The cost of carbon in 2030 will be $85 per tonne of carbon dioxide in 2017 US dollars')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q7(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'Multiplying the HDI by the social cost of carbon emissions',
                                'Multiplying the HDI by the social cost of carbon emissions'),
                                ('Multiplying the HDI by the ecological footprint',
                                 'Multiplying the HDI by the ecological footprint'),
                                ('Multiplying the HDI by the arithmetic mean of the social cost of carbon emissions and the ecological footprint',
                                 'Multiplying the HDI by the arithmetic mean of the social cost of carbon emissions and the ecological footprint')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q8(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'The PHDI in country B is larger','The PHDI in country B is larger'),
                                ('The PHDI in country A is larger','The PHDI in country A is larger'),
                                ('The PHDI does not depend on carbon emissions', 'The PHDI does not depend on carbon emissions')])
    submit = SubmitField('Submit')

class ModulsForm_m2_ch3_q9(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[(
                                'It is increasing the gap with the HDI','It is increasing the gap with the HDI'),
                                ('It is closing the gap with the HDI','It is closing the gap with the HDI'),
                                ('The gap between both indexes remains the same', 'The gap between both indexes remains the same')])
    submit = SubmitField('Submit')