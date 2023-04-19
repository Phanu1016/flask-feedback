from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf, Length

class RegisterAccountForm(FlaskForm):
    """ Register form for new users """
    username = StringField("Username: ",  validators=[InputRequired(message="Username cannot be empty."), Length(max=20)])
    password = PasswordField("Password: ",  validators=[InputRequired(message="Password cannot be empty.")])
    email = EmailField("Email: ",  validators=[InputRequired(message="Email cannot be empty."), Length(max=50)])
    first_name = StringField("First Name: ",  validators=[InputRequired(message="First name cannot be empty."), Length(max=30)])
    last_name = StringField("Last Name: ",  validators=[InputRequired(message="Last name cannot be empty."), Length(max=30)])

class LoginAccountForm(FlaskForm):
    """ Login an user """
    username = StringField("Username: ",  validators=[InputRequired(message="Username cannot be empty."), Length(max=20)])
    password = PasswordField("Password: ",  validators=[InputRequired(message="Password cannot be empty.")])

class FeedbackForm(FlaskForm):
    """ Add/update a feedback """
    title = StringField("Title: ",  validators=[InputRequired(message="Title cannot be empty."), Length(max=100)])
    content = StringField("Content: ",  validators=[InputRequired(message="Content cannot be empty.")])