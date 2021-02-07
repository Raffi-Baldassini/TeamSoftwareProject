from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user as LoginUser, login_required, logout_user, current_user
from random import randint

import user_management as um
from db_setup import username, password, server, db_name


"""
TO DO:
    - Split all functionality into different packages/files
    - Encrypt SQL login details (read them in indirectly)
    - Set up secret key generation - consider key rotation?
    - Registration should check for unique emails and username - currently does not
        - Also does not include an option to input DOB
            - DOB should be checked for certain age - over 12 or something?
    - Implement email confirmation to register an account!
    - Implement user id generation - maybe just auto-increment in SQL (simple but not secure)
    
TO TEST:
    - Run script and go to http://127.0.0.1:5000/ in browser to view flask app
        - This will be index.html or home
    - Click sign up and complete the registration with fake details
        - The username and email are not validated for uniqueness yet so this does not matter
    - Go to: http://127.0.0.1:5000/secret_page
        - This is only visible when logged in
    - Go to: http://127.0.0.1:5000/logout
    - Then back to http://127.0.0.1:5000/ and http://127.0.0.1:5000/secret_page
        - The login screen should pop up
"""


# Configure and instantiate the flask app
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (username, password, server, db_name)
app.config['SECRET_KEY'] = 'asecretkey'

# Instantiates the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Loads bootstrap and sqlalchemy into flask app
Bootstrap(app)
db = SQLAlchemy(app)


# Represents user credentials
# UserMixin provides default implementations for the methods that Flask-Login expects user objects to have
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    pword = db.Column(db.String(80), unique=True)


# Connects flask_login 'abstract' users to users that are defined in the DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Flask routes
# home page
@app.route('/')
def index():
    return render_template('index.html')


# signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    reg_form = um.RegistrationForm()
    if reg_form.validate_on_submit():
        password_hash = generate_password_hash(reg_form.password.data, method='sha256')
        new_user = User(uname=reg_form.username.data.lower(),
                        email=reg_form.email.data.lower(),
                        pword=password_hash,
                        id=randint(0, 5000)
                        )
        db.session.add(new_user)
        db.session.commit()
        return '<h1>Thank you for creating an account, %s.</h1>' % reg_form.username.data
    return render_template('signup.html', form=reg_form)


# login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = um.LoginForm()

    if login_form.validate_on_submit():
        login_user = User.query.filter_by(email=login_form.email.data).first()
        if login_user:
            if check_password_hash(login_user.pword, login_form.password.data):
                LoginUser(login_user, remember=login_form.remember.data)
                return '<h1>Successfully logged in.</h1>'
        return '<h1>Invalid username/password!</h1>'
    return render_template('login.html', form=login_form)


# logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Test page for private pages that require authentication
@app.route('/secret_page', methods=['POST', 'GET'])
@login_required
def secret_page():
    return "<h1>Test Page - Only logged in users should see this message</h1>"


# Run the applications
if __name__ == '__main__':
    app.run(debug=True)
