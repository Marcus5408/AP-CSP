import random
import json
from re import M
from typing import List, Type, Union
from colorama import init, Fore
from matplotlib import use

# initialize colorama
init()
RED, YELLOW, GREEN, BLUE, RESET = Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.RESET


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


def is_word_guessed(guessed_letters: list) -> bool:
    return "__" not in guessed_letters


def show_menu(options: dict) -> int:
    # check if options is a dictionary
    if not isinstance(options, dict):
        raise TypeError("options must be a dictionary")

    # print menu
    for option, menu_item in options.items():
        print(f"{GREEN}[{option}] {BLUE}{menu_item}")

    # get user input
    user_input = None
    while True:
        if user_input in options:
            break
        user_input = input(f"{YELLOW}Please enter an option: {RESET}")

    return user_input


# tests are in tests/__init__.py
if __name__ == "__main__":
    with open(f"{__file__.replace("__init__.py", "")}ascii_art.txt", "r", encoding="utf-8") as f:
        ascii_art = f.read()
        print(f"{RED}{ascii_art}")

    print(f"{YELLOW}{'-' * 13} Welcome to Hangman! {'-' * 13}")
    print("The hangman is currently alive and well.")
    main_menu = {
        "1": "Play Hangman",
        "2": "Options",
        "3": "Exit"
    }
    for option, menu_item in main_menu.items():
        print(f"{GREEN}[{option}] {BLUE}{menu_item}")
    
    user_input = None
    while True:
        if user_input in main_menu:
            break
        user_input = input(f"{YELLOW}Please enter an option: {RESET}")

    chosen_secret_word = pick_secret_word("People", "Easy")
