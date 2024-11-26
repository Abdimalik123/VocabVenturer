import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the words of the JSON file
WORDS_FILE = os.path.join(BASE_DIR, 'static', 'words.json')

DEBUG = True
SECRET_KEY = 'your-secret-key'

ENV = os.getenv('FLASK_ENV', 'development')

WORD_LENGTH = 5
MAX_ATTEMPTS = 6