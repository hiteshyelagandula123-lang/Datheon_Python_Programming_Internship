
import random

WORDS = [
    "PYTHON", "COMPUTER", "DEVELOPER", "KEYBOARD",
    "PROGRAM", "SOFTWARE", "GITHUB", "PROJECT"
]

MAX_ATTEMPTS = 6

HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ========="""
]


def display_game(word, guessed, wrong):
    print(HANGMAN_STAGES[wrong])

    masked = [
        letter if letter in guessed else "_"
        for letter in word
    ]

    print("\nWord:", " ".join(masked))
    print("Incorrect guesses remaining:", MAX_ATTEMPTS - wrong)
    print("Guessed letters:", ", ".join(sorted(guessed)) or "None")


def play_game():
    word = random.choice(WORDS)
    guessed = set()
    wrong = 0

    print("\n=== HANGMAN WORD GUESSING GAME ===")
    print("Guess the word one letter at a time!")

    while wrong < MAX_ATTEMPTS:
        display_game(word, guessed, wrong)

        guess = input("\nEnter one letter: ").strip().upper()

        if len(guess) != 1 or not guess.isascii() or not guess.isalpha():
            print("Invalid input! Enter one English letter (A-Z).")
            continue

        if guess in guessed:
            print("You already guessed that letter. No penalty!")
            continue

        guessed.add(guess)

        if guess in word:
            print("Correct guess!")
        else:
            wrong += 1
            print("Wrong guess!")

        if all(letter in guessed for letter in word):
            display_game(word, guessed, wrong)
            print("\nCONGRATULATIONS! YOU WON!")
            print("The word was:", word)
            return

    display_game(word, guessed, wrong)
    print("\nGAME OVER! YOU LOST.")
    print("The word was:", word)


def main():
    while True:
        play_game()

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
