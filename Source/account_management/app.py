from random import randint

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required,\
    logout_user
from db_setup import username, password, server, db_name
import user_management as um


"""
TO DO:
    - Encrypt SQL login details (read them in indirectly)
    - Set up secret key generation - consider key rotation?
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'\
                                        % (username, password, server, db_name)
app.config['SECRET_KEY'] = 'secret_key'

# Instantiates the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Loads bootstrap and sqlalchemy into flask app
Bootstrap(app)
db = SQLAlchemy(app)


# Represents user credentials
# Provides default implementations for the methods that Flask-Login expects user objects to have
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

    # If form is submitted
    if reg_form.validate_on_submit():
        password_hash = generate_password_hash(reg_form.password.data, method='sha256')
        new_user = User(uname=reg_form.username.data.lower(),
                        email=reg_form.email.data.lower(),
                        pword=password_hash,
                        id=randint(0, 5000))
        check_email = User.query.filter_by(email=reg_form.email.data).first()
        check_username = User.query.filter_by(uname=reg_form.username.data).first()
        if check_email:
            return "<h1>An account is already registered with that email address!</h1>"
        elif check_username:
            return "<h1>An account is already registered with that username!</h1>"

        db.session.add(new_user)
        db.session.commit()
        return '<h1>Thank you for creating an account, %s.</h1>' % reg_form.username.data
    return render_template('signup.html', form=reg_form)


# login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = um.LoginForm()

    # User submits the form
    if login_form.validate_on_submit():
        submitted_user = User.query.filter_by(email=login_form.email.data).first()
        # If form email matches stored email
        if submitted_user:
            # If hashed form password == hashed stored password
            if check_password_hash(submitted_user.pword, login_form.password.data):
                login_user(submitted_user, remember=login_form.remember.data)
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


# Profile page privatised by user
@app.route('/private_page', methods=['POST', 'GET'])
@login_required
def search_user():
    search_form = um.SearchForm()
    curr_user = current_user.id
    if search_form.validate_on_submit():
        submitted_user = User.query.filteby(uname=search_form.username.data.first())
        submitted_user_id = submitted_user.id
        # Need to add load user call
        if db.session.query(User.user.status).filter(User.user.uname == submitted_user):
            if db.session.query(User.friends.id, User.friends.friend_id).filter(User.friends.id == submitted_user_id).filter(User.friends.friend_id == curr_user):
                return "<h1>Test Page - only logged in and added friend users should see this message</h1>"
        else:
            return "<h1>Test Page - only logged in users should see this message</h1>"


# Practice as guest page
@app.route('/practice', methods=['POST', 'GET'])
def practice():
    return render_template('practice.html')


# Run the applications
if __name__ == '__main__':
    app.run(debug=True)
