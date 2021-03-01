from flask import render_template
from game_page.app import app
from flask_bootstrap import Bootstrap
from ..RandomWordMarkovGenerator import read_frequency_JSON, generate_random_paragraph

@app.route('/')
@app.route('/index')
def index():
    wordDictionary = read_frequency_JSON('TextGeneration\\FrankensteinWordFrequency.JSON')

    output = generate_random_paragraph(wordDictionary, 20)

    output = " ".join([str(word) for word in output])

    return render_template('game.html', generated_text = output)