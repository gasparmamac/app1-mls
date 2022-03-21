from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[Length(min=6), Email(message='Enter a valid email.'), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[InputRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')
