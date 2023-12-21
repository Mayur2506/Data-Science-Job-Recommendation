from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo

class PersonalForm(FlaskForm) :
    #username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=50)])
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    middle_name = StringField('Middle Name', validators=[Length(max=20)])
    last_name = StringField('Last Name', validators=[Length(max=20)])
    student_address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=20)])
    isNRI = BooleanField('Do you belong to NRI quota?')
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=10)])
    submit = SubmitField('Update')

class LoginForm(FlaskForm) :
    #username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=50)])
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm) :
    MIS = StringField('MIS ID', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class RecommendForm(FlaskForm) :
    years_of_experience = IntegerField('Years of Experience', validators=[DataRequired()])
    skills = StringField('skills', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JrecommendForm(FlaskForm) :
    userid = IntegerField('user id', validators=[DataRequired()])
    submit = SubmitField('Submit')