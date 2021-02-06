from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


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
    username = StringField('Username', validators=[InputRequired(),
                                                   Length(min=4, max=10),
                                                   ])
    email = StringField('Email', validators=[InputRequired(),
                                             Email(message=str(email_message)),
                                             Length(max=50)
                                             ])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=8, max=80)
                                                     ])

