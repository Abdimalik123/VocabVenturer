from flask import Flask, jsonify, request
from game.word_manager import load_words, get_random_word
from game.logic import check_guess
from config import WORDS_FILE
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
WORDS = load_words(WORDS_FILE)

SECRET_WORD = get_random_word(WORDS)

@app.route('/')
def home():
    return "Welcome to Wordle! Use the '/api/new-word' endpoint to generate a new word."


@app.route('/api/new-word', methods=['GET'])
def new_word():
    global SECRET_WORD
    SECRET_WORD = get_random_word(WORDS)
    return jsonify({"message": "New word generated"})

@app.route('/api/wordle', methods = ['POST'])
def wordle():
    data = request.get_json()
    guess = data.get('guess')
    
    if not guess or len(guess) != 5:
        return jsonify({"error": "Invalid guess. Please enter a 5-letter word"}, 400)
    
    result = check_guess(guess, SECRET_WORD)
    return jsonify(result)

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "An internal server error occurred."}, 500)

if __name__=='__main__':
    app.run(debug=True)
    