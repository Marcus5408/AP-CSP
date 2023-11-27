import random
import json
from typing import List, Type, Union


class HangmanHung(Exception):
    # custom exception for when the hangman is hung due to user error
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def validate_input(input_to_check: any, valid_inputs: Union[type, List[Type], List[str]]) -> None:
    # check if input is a valid type
    if valid_inputs is List[Type]:
        valid_input = False
        for valid_type in valid_inputs:
            if isinstance(input_to_check, valid_type):
                valid_input = True
        if not valid_input:
            raise TypeError(f"input must be one of the following types: {valid_inputs}")
    else:
        if not isinstance(input_to_check, valid_inputs):
            raise TypeError(f"input must be one of the following types: {valid_inputs}")


def pick_secret_word(category: str = "none", difficulty: str = "none") -> str:
    # get words from json, sanitize inputs
    with open(f"{__file__.replace("__init__.py", "")}words.json", "r", encoding="utf-8") as f:
        words = json.load(f)
    category = category.lower()
    difficulty = difficulty.lower()

    # make sure the category & difficulty is valid
    valid_categories = [category_words["category"].lower() for index, category_words in enumerate(words)]
    valid_categories.append("none")  # allow for "random" category
    if category not in valid_categories:
        raise HangmanHung("You entered an invalid category. The hangman has been sent to the gallows.")
    if difficulty not in ["easy", "medium", "hard"]:
        raise HangmanHung("You entered an invalid difficulty. The hangman has been sent to the gallows.")

    # if all is well, pick a word
    words = words[valid_categories.index(category)]["words"][difficulty]
    return random.choice(words).upper()


def create_secret_word_list(secret_word: str) -> list:
    if not isinstance(secret_word, str):
        raise TypeError("secret_word must be a string")
    return list(secret_word.upper())


def create_guessed_letter_list(secret_word_list: list) -> list:
    if not isinstance(secret_word_list, list):
        raise TypeError("secret_word_list must be a list")
    return ["__" for _ in secret_word_list]


def print_guessed_letters(guessed_letters: list or str) -> None:
    for letter in guessed_letters:
        print(letter, end=" ") 
    print()


def check_letter(secret_word_list: list, letter: str) -> bool:
    # check if secret_word_list is a list of letters
    if not isinstance(secret_word_list, list):
        raise TypeError("secret_word_list must be a list")
    # check if letter is a string and is only one character
    if not isinstance(letter, str):
        raise TypeError("letter must be a string")
    if len(letter) != 1:
        raise ValueError("letter must be a single character")

    return letter in secret_word_list


def update_guessed_letters(secret_word_list: list, guessed_letters: list, letter: str) -> list:
    # check list inputs are valid
    validate_input(secret_word_list, list)
    validate_input(guessed_letters, list)
    # check if letter is a string and is only one character
    if not isinstance(letter, str):
        raise TypeError("letter must be a string")
    if len(letter) != 1:
        raise ValueError("letter must be a single character")
    
    # actual function
    for index, secret_letter in enumerate(secret_word_list):
        if secret_letter == letter:
            guessed_letters[index] = letter

    return guessed_letters


def is_word_guessed(guessed_letters):
    return 0

# past tests are in tests/__init__.py

t1_word = ["B", "I", "Y", "O", "O"]
t1_guessed = ["__", "__", "Y", "__", "__"]
t1_letter = "O"
t1_guessed_new = update_guessed_letters(t1_word, t1_guessed, t1_letter)
print(t1_guessed_new)


# if __name__ == "__main__":
#     chosen_secret_word = pick_secret_word("People", "Easy")
# 
#     print(f"Secret word is {chosen_secret_word}")
#     print(create_secret_word_list(chosen_secret_word))
