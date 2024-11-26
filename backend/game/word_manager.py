import json
import random


def load_words(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
def get_random_word(words):
    return random.choice(words)