from flask import Flask
from flask_bootstrap import Bootstrap
app = Flask(__name__, template_folder='templates')
Bootstrap(app)

from game_page.app import game

