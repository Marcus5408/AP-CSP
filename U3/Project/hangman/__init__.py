import random
import json
from typing import List, Type, Union
from colorama import init, Fore

# initialize colorama
init()
RED, YELLOW, GREEN, BLUE, RESET = Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.RESET
CYAN = Fore.CYAN

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
    valid_categories.append("random")  # allow for "random" category
    if category not in valid_categories:
        print(f"{RED}You entered an invalid category. The hangman has been sent to the gallows.")
    if difficulty not in ["easy", "medium", "hard", "random"]:
        print(f"{RED}You entered an invalid difficulty. The hangman has been sent to the gallows.")

    # if all is well, pick a word
    if category == "random":
        valid_categories.remove("random")
        category = random.choice(valid_categories)

    if difficulty == "random":
        difficulty = random.choice(["easy", "medium", "hard"])

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
    for number, option_name in options.items():
        print(f"{GREEN}[{number}] {BLUE}{option_name}")

    # get user input
    selection = ""
    while selection not in options or selection == "":
        selection = input(f"{YELLOW}Please enter an option: {RESET}")
    selection = 1 if selection == "" else selection

    return selection


def show_main_menu() -> int:
    with open(f"{__file__.replace("__init__.py", "")}ascii_art.txt", "r", encoding="utf-8") as f:
        ascii_art = f.read()
        print(f"{RED}{ascii_art}")

    print(f"{YELLOW}{'-' * 13} Welcome to Hangman! {'-' * 13}")
    print("The hangman is currently alive and well.")
    main_menu = {
        "1": "Play Hangman",
        "2": "Game Options",
        "3": "Exit"
    }
    selection = show_menu(main_menu)
    selection = 1 if selection == "" else int(selection)

    return selection


def play_hangman(settings: dict) -> None:
    print("Starting game...")
    hangman = 0
    lives = settings["lives"]
    secret_word = pick_secret_word(settings["category"], settings["difficulty"])
    secret_word_list = create_secret_word_list(secret_word)
    guessed_letters = create_guessed_letter_list(secret_word_list)
    wrong_guesses = []
    correctly_guessed = False
    while hangman < lives:
        print(f"{CYAN}The hangman has {BLUE}{lives - hangman}{CYAN} chances left.\n{GREEN}")
        print_guessed_letters(guessed_letters)
        print(f"\r{RED}Wrong guesses: {' '.join(wrong_guesses)}", flush=True)
        letter = input(f"{YELLOW}Please enter a letter: {RESET}").upper()
        if check_letter(secret_word_list, letter):
            update_guessed_letters(secret_word_list, guessed_letters, letter)
        else:
            wrong_guesses.append(letter.upper())
            hangman += 1

        print("\r\033[A" * 5, end="", flush=True)  # move cursor up 5 lines, clear lines
        if is_word_guessed(guessed_letters):
            print(f"{GREEN}You guessed the word correctly!")
            correctly_guessed = True
            break
    
    if not correctly_guessed:
        print(f"{RED}The hangman's specter claims another soul in the void of your defeat.")
        print(f"The elusive word you sought to unveil was {secret_word}.{RESET}")


def configure_game_settings() -> dict:
    print("Game Options")
    settings_menu = {
        "1": "Category",
        "2": "Difficulty",
        "3": "Lives",
        "4": "Go Back"
    }
    while True:
        selection = show_menu(settings_menu)
        print("\r\033[A" * 5, end="", flush=True)
        if selection == 1:
            # multiple choice

        if selection == 4:
            break

    return None


# tests are in tests/__init__.py
if __name__ == "__main__":
    game_settings = {
        "category": "random",
        "difficulty": "random",
        "lives": 6
    }
    while True:
        main_menu_selection = show_main_menu()
        if main_menu_selection == 1:
            play_hangman(game_settings)
        elif main_menu_selection == 2:
            configure_game_settings()
        else:
            print(f"{YELLOW}Goodbye!")
            exit()


    chosen_secret_word = pick_secret_word("People", "Easy")
