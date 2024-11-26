import pytest
from app import app
from config import WORDS_FILE
from game.word_manager import load_words

# Set a known secret word for testing
SECRET_WORD = "shave"

@pytest.fixture
def client():
    """Create a Flask test client for testing."""
    with app.test_client() as client:
        yield client

def test_new_word(client):
    """Test the /api/new-word endpoint."""
    response = client.get('/api/new-word')
    assert response.status_code == 200

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "New word generated!"

def test_wordle_valid_guess(client):
    """Test /api/wordle with a valid guess (exact match)."""
    global SECRET_WORD
    SECRET_WORD = "shave"  # Ensure the word is predictable

    response = client.post('/api/wordle', json={"guess": "shave"})
    assert response.status_code == 200

    data = response.get_json()
    assert "feedback" in data
    assert data["feedback"] == ["green", "green", "green", "green", "green"]

def test_wordle_incorrect_guess(client):
    """Test /api/wordle with an incorrect guess (some correct letters)."""
    global SECRET_WORD
    SECRET_WORD = "shave"

    response = client.post('/api/wordle', json={"guess": "share"})
    assert response.status_code == 200

    data = response.get_json()
    assert "feedback" in data
    assert data["feedback"] == ["green", "green", "green", "gray", "green"]

def test_wordle_invalid_guess_length(client):
    """Test /api/wordle with a guess of invalid length."""
    response = client.post('/api/wordle', json={"guess": "longword"})
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid guess. Please enter a 5-letter word."

def test_wordle_non_alpha_guess(client):
    """Test /api/wordle with a guess containing non-alphabetic characters."""
    response = client.post('/api/wordle', json={"guess": "sh@ve"})
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid guess. Please enter a 5-letter word."

def test_wordle_all_incorrect_guess(client):
    """Test /api/wordle with a guess with no correct letters."""
    global SECRET_WORD
    SECRET_WORD = "shave"

    response = client.post('/api/wordle', json={"guess": "lucky"})
    assert response.status_code == 200

    data = response.get_json()
    assert "feedback" in data
    assert data["feedback"] == ["gray", "gray", "gray", "gray", "gray"]

def test_wordle_partial_correct_guess(client):
    """Test /api/wordle with a guess with letters in the wrong positions."""
    global SECRET_WORD
    SECRET_WORD = "shave"

    response = client.post('/api/wordle', json={"guess": "vases"})
    assert response.status_code == 200

    data = response.get_json()
    assert "feedback" in data
    assert data["feedback"] == ["yellow", "gray", "gray", "yellow", "gray"]

def test_wordle_no_guess_provided(client):
    """Test /api/wordle when no guess is provided."""
    response = client.post('/api/wordle', json={})
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No guess provided."

def test_wordle_case_insensitive_guess(client):
    """Test /api/wordle to ensure guesses are case-insensitive."""
    global SECRET_WORD
    SECRET_WORD = "shave"

    response = client.post('/api/wordle', json={"guess": "SHAVE"})
    assert response.status_code == 200

    data = response.get_json()
    assert "feedback" in data
    assert data["feedback"] == ["green", "green", "green", "green", "green"]
