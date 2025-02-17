# CLEMENTE, BRIAN MATTHEW E.

import random
import os

def getWords(filename):
    """Reads words from a file and returns them as a tuple."""
    full_path = os.path.join(script_dir, filename)
    try:
        with open(full_path, 'r') as file:
            words = [line.strip().upper() for line in file if line.strip()]
        if not words:
            print(f"Error: {filename} is empty. Expected file at {full_path}")
        return tuple(words)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Expected file at {full_path}")
        return ()
    
# Get the directory of the script (relative path)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use relative paths based on the script's directory
articles = getWords(os.path.join(script_dir, "articles.txt"))
nouns = getWords(os.path.join(script_dir, "nouns.txt"))
verbs = getWords(os.path.join(script_dir, "verbs.txt"))
prepositions = getWords(os.path.join(script_dir, "prepositions.txt"))

def sentence():
    """Builds and returns a sentence."""
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    """Builds and returns a noun phrase."""
    return random.choice(articles) + " " + random.choice(nouns)

def verbPhrase():
    """Builds and returns a verb phrase."""
    return random.choice(verbs) + " " + nounPhrase() + " " + \
           prepositionalPhrase()

def prepositionalPhrase():
    """Builds and returns a prepositional phrase."""
    return random.choice(prepositions) + " " + nounPhrase()

def main():
    """Allows the user to input the number of sentences to generate."""
    number = int(input("Enter the number of sentences: "))
    for _ in range(number):
        print(sentence())

# The entry point for program execution
if __name__ == "__main__":
    if not (articles and nouns and verbs and prepositions):
        print("Error: One or more vocabulary files are missing or empty.")
    else:
        main()  