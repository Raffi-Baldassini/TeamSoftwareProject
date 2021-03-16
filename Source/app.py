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
from Source import friendsChart


# Configure and instantiate the flask app
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (username, password, server, db_name)
app.config['SECRET_KEY'] = 'secret_key'

# Instantiates the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Loads bootstrap and sqlalchemy into flask app
Bootstrap(app)
db = SQLAlchemy(app)


# Represents user credentials by modelling mySQL columns
# Provides default implementations for the methods that Flask-Login expects user objects to have
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    pword = db.Column(db.String(80), unique=True)


# Global variable used to keep track of a user id if logged in
userID = None


# Connects flask_login 'abstract' users to users that are defined in the DB
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Flask routes
# home page
@app.route('/', methods=['POST', 'GET'])
def index():
    global userID

    # Returns the user login-form with validated fields
    login_form = um.LoginForm()

    # If the form can be validated
    if login_form.validate_on_submit():
        submitted_user = User.query.filter_by(email=login_form.email.data).first()
        # If the email provided in the form matches stored email
        if submitted_user:
            # If hashed form password == hashed stored password
            if check_password_hash(submitted_user.pword, login_form.password.data):
                userID = submitted_user.id
                login_user(submitted_user, remember=login_form.remember.data)
                flash("Successfully logged in!")
                return redirect(url_for('profile'))
            else:
                flash("Invalid login details!")
    return render_template('index.html', form=login_form)


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    cursor = DB.get_cursor()
    global userID

    username_statement = "SELECT `uname` FROM `user` WHERE id = %s;" % userID
    cursor.execute(username_statement)
    username_response = cursor.fetchall()[0][0]

    solo_game_statement = "SELECT `solo_games` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(solo_game_statement)
    solo_game_response = cursor.fetchall()[0][0]

    online_game_statement = "SELECT `online_games` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(online_game_statement)
    online_game_response = cursor.fetchall()[0][0]

    words_statement = "SELECT `words` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(words_statement)
    words_response = cursor.fetchall()[0][0]

    chars_statement = "SELECT `chars` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(chars_statement)
    chars_response = cursor.fetchall()[0][0]

    wpm_statement = "SELECT `wpm` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(wpm_statement)
    wpm_response = cursor.fetchall()[0][0]

    accuracy_statement = "SELECT `accuracy` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(accuracy_statement)
    accuracy_response = cursor.fetchall()[0][0]

    acc_best_statement = "SELECT `acc_best` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(acc_best_statement)
    acc_best_response = cursor.fetchall()[0][0]

    acc_worst_statement = "SELECT `acc_worst` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(acc_worst_statement)
    acc_worst_response = cursor.fetchall()[0][0]

    wpm_best_statement = "SELECT `wpm_best` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(wpm_best_statement)
    wpm_best_response = cursor.fetchall()[0][0]

    wpm_worst_statement = "SELECT `wpm_worst` FROM `stats` WHERE id = %s;" % userID
    cursor.execute(wpm_worst_statement)
    wpm_worst_response = cursor.fetchall()[0][0]
  
    (wpmChartJSON, accChartJSON) = friendsChart.get_charts(userID)
    return render_template('profile.html', uname = username_response, data1 = solo_game_response, data2 = online_game_response, data3 = words_response, data4 = chars_response, data5 = wpm_response, data6 = accuracy_response, data7 = wpm_best_response, data8 = wpm_worst_response, data9 = acc_best_response, data10 = acc_worst_response, wpmChartJSON = wpmChartJSON, accChartJSON = accChartJSON)


# signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    reg_form = um.RegistrationForm()
    login_form = um.LoginForm()

    # If form is submitted
    if reg_form.validate_on_submit():
        # Generates a password hash which will be stored in the DB
        password_hash = generate_password_hash(reg_form.password.data, method='sha256')
        # Creates User class which will be used to populate the D, if successful
        new_user = User(uname=reg_form.username.data.lower(),
                        email=reg_form.email.data.lower(),
                        pword=password_hash
                        )

        # Query if username/email already exist and provide appropriate error messages
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


# Login page route - same login procedure as with 'index'
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
                return redirect(url_for('profile'))
            else:
                flash("Invalid login details!")
    return render_template('login.html', form=login_form)


# logout page - hardcoded logout function
@app.route('/logout')
@login_required
def logout():
    form = um.LoginForm
    global userID
    userID = None
    logout_user()
    flash("Logout successful!")
    return redirect(url_for('index'))


# Practice page for non-authenticated user
@app.route('/practice', methods=['POST', 'GET'])
def practice():
    # Ensure paths are correct for Windows and linux - only necessary for local testing
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

    output = generate_random_paragraph(wordDictionary, 10)
    output = " ".join([str(word) for word in output])

    return render_template('practice.html', generated_text=output)

#obtain a fresh text set to be used in the game in JSON formatr
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

    output = generate_random_paragraph(wordDictionary, 10)
    output = " ".join([str(word) for word in output])

    return jsonify({'reply':output})

#receive statistics from a played game, associate them with a user
#and forward them to the method upload_game() in the DB class
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

#obtain the id and day-best and all-time-best WPM for userID in JSON format
@app.route('/loggedinidwpm',methods=['GET'])
def ifLoggedInSendIDandWPM():
    global userID
    if userID != None:
        wpms = DB.getBestWPM(userID)
        return jsonify({'reply':'yes','id':userID,'wpm_day':wpms[0],'wpm_best':wpms[1]})
    return jsonify({'reply':''})


# Run the applications
if __name__ == '__main__':
    app.run(port=16932, host='0.0.0.0')
