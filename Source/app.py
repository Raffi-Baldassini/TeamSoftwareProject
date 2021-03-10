from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from random import choice
import platform
import pymysql
import os

import Source.user_management as um
from Source.db_setup import username, password, server, db_name
from Source.RandomWordMarkovGenerator import read_frequency_JSON, generate_random_paragraph
from Source.db_interaction import DB
"""
TO DO:
    - Encrypt SQL login details (read them in indirectly)
    - Set up secret key generation - consider key rotation?
    
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

userID = None

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    pword = db.Column(db.String(80), unique=True)


# Connects flask_login 'abstract' users to users that are defined in the DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Flask routes
# home page
@app.route('/', methods=['POST', 'GET'])
def index():
    global userID
    login_form = um.LoginForm()

    if login_form.validate_on_submit():
        submitted_user = User.query.filter_by(email=login_form.email.data).first()
        # If form email matches stored email
        if submitted_user:
            # If hashed form password == hashed stored password
            if check_password_hash(submitted_user.pword, login_form.password.data):
                userID = submitted_user.id
                login_user(submitted_user, remember=login_form.remember.data)
                flash("Successfully logged in!")
                return render_template('index.html', form=login_form)
            else:
                flash("Invalid login details!")
    return render_template('index.html', form=login_form)


# signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    reg_form = um.RegistrationForm()
    login_form = um.LoginForm()

    # If form is submitted
    if reg_form.validate_on_submit():
        password_hash = generate_password_hash(reg_form.password.data, method='sha256')
        new_user = User(uname=reg_form.username.data.lower(),
                        email=reg_form.email.data.lower(),
                        pword=password_hash
                        )

        check_email = User.query.filter_by(email=reg_form.email.data).first()
        check_username = User.query.filter_by(uname=reg_form.username.data).first()

        if check_email:
            flash("An account is already registered with that email address!")
        elif check_username:
            flash("An account is already registered with that username!")
        else:
            db.session.add(new_user)
            db.session.commit()
            flash("Thank you for creating an account!")
            return render_template('index.html', form=login_form)
    return render_template('signup.html', form=reg_form)


# Login page route
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = um.LoginForm()
    if login_form.validate_on_submit():
        submitted_user = User.query.filter_by(email=login_form.email.data).first()
        # If form email matches stored email
        if submitted_user:
            # If hashed form password == hashed stored password
            if check_password_hash(submitted_user.pword, login_form.password.data):
                login_user(submitted_user, remember=login_form.remember.data)
                flash("Successfully logged in!")
                return render_template('practice.html')
            else:
                flash("Invalid login details!")
    return render_template('login.html', form=login_form)


# logout page
@app.route('/logout')
@login_required
def logout():
    global userID
    userID = None
    logout_user()
    flash("Logout successful!")
    return redirect(url_for('index'))


# Test page for private pages that require authentication
@app.route('/secret_page', methods=['POST', 'GET'])
@login_required
def secret_page():
    return "<h1>Test Page - Only logged in users should see this message</h1>"


# Practice page for non-authenticated user
@app.route('/practice', methods=['POST', 'GET'])
def practice():
    
    if platform.system() == 'Linux':
        Frequency_dicts = os.listdir('TextGeneration/FrequencyDictionaries')
        Frequency_dicts.remove('LetterFrequency.json')
        filepath = choice(Frequency_dicts)
        wordDictionary = read_frequency_JSON(f'TextGeneration/FrequencyDictionaries/{filepath}')
    elif platform.system() == 'Windows':
        Frequency_dicts = os.listdir('TextGeneration\\FrequencyDictionaries')
        Frequency_dicts.remove('LetterFrequency.json')
        filepath = choice(Frequency_dicts)
        wordDictionary = read_frequency_JSON(f'TextGeneration\\FrequencyDictionaries\\{filepath}')

    output = generate_random_paragraph(wordDictionary, 6)
    output = " ".join([str(word) for word in output])

    return render_template('practice.html', generated_text=output)
    
@app.route('/reset', methods=['GET'])
def reset():
    if platform.system() == 'Linux':
        Frequency_dicts = os.listdir('TextGeneration/FrequencyDictionaries')
        Frequency_dicts.remove('LetterFrequency.json')
        filepath = choice(Frequency_dicts)
        wordDictionary = read_frequency_JSON(f'TextGeneration/FrequencyDictionaries/{filepath}')
    elif platform.system() == 'Windows':
        Frequency_dicts = os.listdir('TextGeneration\\FrequencyDictionaries')
        Frequency_dicts.remove('LetterFrequency.json')
        filepath = choice(Frequency_dicts)
        wordDictionary = read_frequency_JSON(f'TextGeneration\\FrequencyDictionaries\\{filepath}')

    output = generate_random_paragraph(wordDictionary, 6)
    output = " ".join([str(word) for word in output])

    return jsonify({'reply':output})

@app.route('/stats',methods=['POST'])
def store_stats():
    global userID
    if userID:
        stats=request.args.get('value').split(",")
        for i in range(len(stats)):
            stats[i] = int(stats[i].strip())
        stats = [userID] + stats
        DB.upload_game(stats)
    return jsonify({'reply':'success'})
    
@app.route('/isloggedin',methods=['GET'])
def ifLoggedInSendID():
    global userID
    if userID != None:
        return jsonify({'reply':'yes','id':userID})
    return jsonify({'reply':''})


# Run the applications
if __name__ == '__main__':
    app.run(port=16932, host='0.0.0.0')
