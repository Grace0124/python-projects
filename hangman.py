# Problem Set 2, hangman.py
# Name: Grace Liu
# Collaborators: Kaylee Sweet
# Time spent: 2.5 hours

import random
import string

# -----------------------------------
# HELPER CODE
# -----------------------------------

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    returns: list, a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(" ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------
# END OF HELPER CODE
# -----------------------------------


# Load the list of words to be accessed from anywhere in the program
wordlist = load_words()

def has_player_won(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: boolean, True if all the letters of secret_word are in letters_guessed,
        False otherwise
    """
    win = True
    for letter in secret_word:
        if letter in letters_guessed:
            pass
        else:
            win = False
    return win


def get_word_progress(secret_word, letters_guessed):
    """
    secret_word: string, the lowercase word the user is guessing
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters and asterisks (*) that represents
        which letters in secret_word have not been guessed so far
    """
    #get secret_word
    #if a letter in secret_word is not in letters_guessed, add *
    #if a letter in secret_word is in letters_guessed, add the letter
    word_reveal = ''
    for letter in secret_word:
        if letter in letters_guessed:
            word_reveal += letter
        else:
            word_reveal += '*'
    return word_reveal


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of lowercase letters), the letters that have been
        guessed so far

    returns: string, comprised of letters that represents which
      letters have not yet been guessed. The letters should be returned in
      alphabetical order
    """
    #create an empty string
    #if the letter is not in letter_guessed, add it to the string
    available_letters = ''
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters

def choose_letter(secret_word, available_letters):
    """
    secret_word: string, the lowercase word the user is guessing
    available_letters: string, all letters that haven't been guessed yet
    
    returns: string, one letter in secret_word to be revealed
    """
    choose_from = ''
    for letter in string.ascii_lowercase:
        if letter in secret_word and letter in available_letters:
            choose_from += letter
    new = random.randint(0, len(choose_from)-1)
    revealed_letter = choose_from[new]
    return revealed_letter

def unique(secret_word):
    """
    secret_word: string, the lowercase word the user is guessing
    
    returns: int, number of unique letters in secret_word
    """
    unique_letters = ''
    for letter in secret_word:
        if letter not in unique_letters:
            unique_letters += letter
    return len(unique_letters)
    
def hangman(secret_word, with_help):
    """
    secret_word: string, the secret word to guess.
    with_help: boolean, this enables help functionality if true.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses they start with.

    * The user should start with 10 guesses.

    * Before each round, you should display to the user how many guesses
      they have left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a single letter (or help character '!'
      for with_help functionality)

    * If the user inputs an incorrect consonant, then the user loses ONE guess,
      while if the user inputs an incorrect vowel (a, e, i, o, u),
      then the user loses TWO guesses.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    -----------------------------------
    with_help functionality
    -----------------------------------
    * If the guess is the symbol !, you should reveal to the user one of the
      letters missing from the word at the cost of 3 guesses. If the user does
      not have 3 guesses remaining, print a warning message. Otherwise, add
      this letter to their guessed word and continue playing normally.

    Follows the other limitations detailed in the problem write-up.
    """
    guesses = 10
    letters_guessed = ''
    vowels = 'aeiou'
    print("Welcome to Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')

    
    while guesses > 0 and not has_player_won(secret_word, letters_guessed): 
        print('--------------')
        print(f'You have {guesses} guesses left.')
        available_letters = get_available_letters(letters_guessed)
        print(f'Available letters: {available_letters}')
        current_letter = input('Please guess a letter: ')
        current_letter = current_letter.lower()
        word_progress = get_word_progress(secret_word, letters_guessed)
        
        if len(current_letter) != 1 or current_letter not in string.ascii_letters:
            #check for help
            if current_letter == '!' and with_help == True:
                if guesses < 3: 
                    #can't ask for help if guesses are less than 3
                    print(f'Oops! Not enough guesses left: {word_progress}')
                else:
                    #choose a letter, reveal it, and add it to the word
                    revealed_letter = choose_letter(secret_word, available_letters)
                    print(f'Letter revealed: {revealed_letter}')
                    letters_guessed += revealed_letter
                    word_progress = get_word_progress(secret_word, letters_guessed)
                    print(word_progress)
                    guesses -= 3
            #check if guess is 1 letter and in the alphabet
            else:
                print(f'Oops! That is not a valid letter. Please input a letter from \
                          the alphabet: {word_progress}')
        elif current_letter in letters_guessed:
            #check if guess is already guessed
            print(f"Oops! You've already guessed that letter: {word_progress}")
        else:
            letters_guessed += current_letter
            word_progress = get_word_progress(secret_word, letters_guessed)
            if current_letter in secret_word:
                print(f'Good guess: {word_progress}')
            else:
                #wrong guesses
                if current_letter in vowels:
                    guesses -= 2
                else:
                    guesses -= 1
                print(f'Oops! That letter is not in my word: {word_progress}')
    if has_player_won(secret_word, letters_guessed):
        #winning condition
        num_unique_letters = unique(secret_word)
        total_score = guesses + 4*num_unique_letters + 3*len(secret_word)
        print("--------------")
        print("Congratulations, you won!")
        print(f'Your total score for this game is: {total_score}')
    else:
        #losing condition
        print("--------------")
        print(f'Sorry, you ran out of guesses. The word was {secret_word}.')

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the lines to test

if __name__ == "__main__":
    # To test your game, uncomment the following three lines.

    secret_word = "wildcard"
    with_help = True
    hangman(secret_word, with_help)

    # After you complete with_help functionality, change with_help to True
    # and try entering "!" as a guess!

    ###############

    # SUBMISSION INSTRUCTIONS
    # -----------------------
    # It doesn't matter if the lines above are commented in or not
    # when you submit your pset. However, please run ps2_student_tester.py
    # one more time before submitting to make sure all the tests pass.
    pass

