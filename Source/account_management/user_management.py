from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo


# Represent the Flask login form - will be passed into flask bootstrap at routing
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),
                                                   Length(min=4, max=50)
                                                   ])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=80)
                                                     ])
    remember = BooleanField('Remember me')


# Represent the Flask user registration form - will be passed into flask bootstrap at routing
class RegistrationForm(FlaskForm):
    email_message = "Please enter a valid email address"
    password_length_message = "Password must be between 8-80 characters"
    password_confirm_message = "Passwords do not match"
    username = StringField('Username - up to 10 characters', validators=[InputRequired(),
                                                   Length(min=4, max=10),
                                                   ])
    email = StringField('Email', validators=[InputRequired(),
                                             Email(message=str(email_message)),
                                             Length(min=4, max=50, message=email_message)
                                             ])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=80,
                                                            message=password_length_message),
                                                     EqualTo('confirm_password',
                                                             message=password_message)
                                                     ])
    confirm_password = PasswordField('Repeat Password')

