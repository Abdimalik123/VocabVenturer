import React, { useState } from "react";
import axios from "axios";

const WordleGame = () => {
  const [guess, setGuess] = useState("");
  const [feedback, setFeedback] = useState([]);
  const [message, setMessage] = useState("");
  const [userId, setUserId] = useState("user123"); // Example user ID

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (guess.length !== 5) {
      setMessage("Please enter a valid 5-letter word.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/wordle", {
        guess: guess,
        user_id: userId,
      });
      setFeedback(response.data.feedback);
      setMessage("");
    } catch (error) {
      setMessage("Error submitting guess. Please try again.");
    }
  };

  const handleNewGame = async () => {
    try {
      await axios.get("http://127.0.0.1:5000/api/new-word");
      setFeedback([]);
      setGuess("");
      setMessage("New word generated!");
    } catch (error) {
      setMessage("Error starting a new game. Please try again.");
    }
  };

  return (
    <div>
      <h1>Wordle Game</h1>
      <button onClick={handleNewGame}>Start New Game</button>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={guess}
          onChange={(e) => setGuess(e.target.value)}
          maxLength="5"
          placeholder="Enter your guess"
        />
        <button type="submit">Submit Guess</button>
      </form>
      {message && <p>{message}</p>}
      {feedback.length > 0 && (
        <div>
          <h3>Feedback</h3>
          <ul>
            {feedback.map((color, index) => (
              <li key={index} style={{ color: color }}>
                {guess[index]}: {color}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default WordleGame;
