



def check_guess(guess, secret_word):
    
    feedback = []
    
    secret_word_chars = list(secret_word)
    
    # Mark green (correct position)
    for i, char in enumerate(guess):
        if char == secret_word_chars[i]:
            feedback.append("green")
            secret_word_chars[i] = None # Mark as used
        else:
            feedback.append(None)
    
    # Mark yellow or gray
    for i, char in enumerate(guess):
        if feedback[i] is None:
            if char in secret_word_chars:
                feedback[i] = "yellow"
                secret_word_chars[secret_word_chars.index(char)] = None # Mark as used
            else:
                feedback[i] = "gray"
    return {"guess": guess, "feedback":feedback}
            
    