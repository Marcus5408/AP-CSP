import random
import json
from colorama import init, Fore, just_fix_windows_console

# initialize colorama and various text formatting things
init()
just_fix_windows_console()
RED, YELLOW, GREEN, BLUE, RESET = Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.RESET
MAGENTA, CYAN, WHITE = Fore.MAGENTA, Fore.CYAN, Fore.WHITE
CLEARLINE = "\033[2K"  # clears the current line


def clear_previous_lines(num_lines_to_clear: int) -> None:
    if num_lines_to_clear == 0:
        return

    for _ in range(num_lines_to_clear):
        print(f"{CLEARLINE}\033[F", end=CLEARLINE, flush=True)
        # \033[F moves the cursor to the beginning of the previous line


def pick_secret_word(category: str = "none", difficulty: str = "none") -> str:
    # get words from json, sanitize inputs
    words_file_path = f"{__file__.replace("__init__.py", "")}words.json"
    with open(words_file_path, "r", encoding="utf-8") as words_file:
        words = json.load(words_file)
    category = category.lower()
    difficulty = difficulty.lower()

    # make sure the category & difficulty is valid
    valid_categories = [category_words["category"].lower() for category_words in words]
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
    return list(secret_word.upper())


def create_guessed_letter_list(secret_word_list: list) -> list:
    return ["__" for _ in secret_word_list]


def print_guessed_letters(guessed_letters: list or str) -> None:
    for letter in guessed_letters:
        print(letter, end=" ")
    print()


def check_letter(secret_word_list: list, letter: str) -> bool:
    return letter in secret_word_list


def update_guessed_letters(secret_word_list: list, guessed_letters: list, letter: str) -> list:
    for index, secret_letter in enumerate(secret_word_list):
        if secret_letter == letter:
            guessed_letters[index] = letter

    return guessed_letters


def is_word_guessed(guessed_letters: list) -> bool:
    return "__" not in guessed_letters


def show_menu(options: dict) -> int:
    # print menu
    for number, option_name in options.items():
        print(f"{GREEN}[{number}] {BLUE}{option_name}{' ' * 15}", flush=True)

    # get user input
    menu_selection = ""
    invalid_selections = 0
    while menu_selection not in options or menu_selection == "":
        menu_selection = input(f"{CYAN}Please enter an option: {RESET}")
        invalid_selections += 1 if menu_selection not in options else 0
    menu_selection = 1 if menu_selection == "" else int(menu_selection)

    return menu_selection, invalid_selections


def show_main_menu() -> int:
    print(f"{CLEARLINE}{MAGENTA}Main Menu")
    main_menu = {
        "1": "Play Hangman",
        "2": "Game Options",
        "3": "Exit"
    }
    selection, invalids = show_menu(main_menu)
    selection = 1 if selection == "" else int(selection)

    return selection, invalids


def play_hangman(settings: dict, program_state:str) -> bool:
    if program_state == "main_menu":
        clear_previous_lines(5)
    elif program_state == "settings_menu":
        clear_previous_lines(0)

    print(f"{MAGENTA}Hangman Game")
    hangman_life = settings["lives"]
    secret_word = pick_secret_word(settings["category"], settings["difficulty"])
    secret_word_list = create_secret_word_list(secret_word)
    guessed_letters = create_guessed_letter_list(secret_word_list)
    wrong_guesses = []
    correctly_guessed = False
    while hangman_life != 0:
        print(f"{CYAN}The hangman has {BLUE}{hangman_life}{CYAN} chances left.\n{GREEN}")
        print_guessed_letters(guessed_letters)

        # format wrong guesses and print them
        print(f"\r{RED}Wrong guesses: ")
        wrong_guesses_total_len = sum([len(wrong_guess) for wrong_guess in wrong_guesses])
        beginning_and_ending = f"+{'-' * (wrong_guesses_total_len * 2 + 2)}+"
        formatted_wrong_guesses = (" ".join(wrong_guesses) + " ") if len(wrong_guesses) > 0 else ""
        print(f"{beginning_and_ending}\n| {formatted_wrong_guesses} |\n{beginning_and_ending}")

        # game logic, see if user guesses correctly
        guess = input(f"{CYAN}Please enter a letter: {RESET}").upper()
        if len(guess) == 1:
            if check_letter(secret_word_list, guess):
                update_guessed_letters(secret_word_list, guessed_letters, guess)
            else:
                wrong_guesses.append(guess.upper())
                hangman_life -= 1
        else:
            for letter in guess:
                if check_letter(secret_word_list, letter):
                    update_guessed_letters(secret_word_list, guessed_letters, letter)
                else:
                    wrong_guesses.append(letter.upper())
                    hangman_life -= 1

        clear_previous_lines(8)  # move cursor up 5 lines, clear lines
        if is_word_guessed(guessed_letters):
            print(f"{GREEN}You guessed the word correctly!")
            correctly_guessed = True
            break

    if not correctly_guessed:
        print(f"{RED}The hangman's specter claims another soul in the void of your defeat.")
        print(f"The elusive word you sought to unveil was {secret_word}.{RESET}")

    return correctly_guessed


def configure_game_settings(game_settings: dict, program_mode:str) -> dict:
    clear_previous_lines(5 if program_mode == "main_menu" else 0)
    settings_menu = {
        "1": "Category",
        "2": "Difficulty",
        "3": "Lives",
        "4": "Reset Settings",
        "5": "Show Settings",
        "6": "Go Back"
    }
    while True:
        print(f"{CLEARLINE}{MAGENTA}Game Options")
        settings_selection, lines_to_clear = show_menu(settings_menu)
        clear_previous_lines(8 + lines_to_clear)
        if settings_selection == 1:
            print(f"{MAGENTA}Game Options - Category")
            category_options = {}

            # get possible categories
            words_json = f"{__file__.replace("__init__.py", "")}words.json"
            with open(words_json, "r", encoding="utf-8") as words_file:
                words = json.load(words_file)
            for index, category_words in enumerate(words):
                category_options[str(index + 1)] = category_words["category"]
            category_options[str(len(words) + 1)] = "Random"  # allow for "random" category
            category_options[str(len(words) + 2)] = "Go back to Game Options"  # add go back option

            # show menu, update settings if updated
            settings_selection, lines_to_clear = show_menu(category_options)
            if settings_selection <= (len(words) + 1):
                game_settings["category"] = category_options[str(settings_selection)]
                print(f"{GREEN}Category set to {BLUE}{game_settings['category']}{GREEN}.")
            else:
                print(f"{GREEN}Category not changed ({BLUE}{game_settings['category']}{GREEN}).")
            
            input(f"{YELLOW}Press enter to go back to the settings menu.")
            clear_previous_lines(len(category_options) + 4 + lines_to_clear)
        elif settings_selection == 2:
            print(f"{MAGENTA}Game Options - Difficulty")
            difficulty_options = {
                "1": "Easy",
                "2": "Medium",
                "3": "Hard",
                "4": "Random",
                "5": "Go Back to Game Options"
            }
            settings_selection, lines_to_clear = show_menu(difficulty_options)
            if settings_selection <= 4:
                game_settings["difficulty"] = difficulty_options[str(settings_selection)]
                print(f"{GREEN}Difficulty set to {BLUE}{game_settings['difficulty']}{GREEN}.")
            else:
                print(f"{GREEN}Difficulty not changed ({BLUE}{game_settings['difficulty']}{GREEN}).")

            input(f"{YELLOW}Press enter to go back to the settings menu.")
            clear_previous_lines(len(difficulty_options) + 4 + lines_to_clear)
        elif settings_selection == 3:
            print(f"{MAGENTA}Game Options - Lives")
            lives_options = {
                "1": "Enter a number of lives",
                "2": "Reset to default (6)",
                "3": "Go back to Game Options"
            }
            selection, lines_to_clear = show_menu(lives_options)
            if selection == 1:
                lives_input = ""
                while not lives_input.isdigit():
                    lives_input = input(f"{CYAN}Please enter a number of lives: {RESET}")
                    lines_to_clear += 1 if not lives_input.isdigit() else 0

                game_settings["lives"] = lives_input
                print(f"{GREEN}Lives set to {BLUE}{game_settings['lives']}{GREEN}.")
            elif selection == 2:
                game_settings["lives"] = 6
                print(f"{GREEN}Lives reset to {BLUE}6{GREEN}.")
            else:
                print(f"{GREEN}Lives not changed ({BLUE}{game_settings['lives']}{GREEN}).")

            input(f"{YELLOW}Press enter to go back to the settings menu.")
            clear_previous_lines(len(lives_options) + 5 + lines_to_clear)
        elif settings_selection == 4:
            print(f"{MAGENTA}Game Options - Reset Settings")
            reset_options = {
                "1": "Reset all settings",
                "2": "Reset category",
                "3": "Reset difficulty",
                "4": "Reset lives",
                "5": "Go back to Game Options"
            }
            selection, lines_to_clear = show_menu(reset_options)
            if selection == 1:
                game_settings["category"] = "random"
                game_settings["difficulty"] = "random"
                game_settings["lives"] = 6
                print(f"{GREEN}All settings reset to default:")
                print(f"Category: {BLUE}Random{GREEN}")
                print(f"Difficulty: {BLUE}Random{GREEN}")
                print(f"Lives: {BLUE}Random{GREEN}")
                lines_to_clear += 3
            elif selection == 2:
                game_settings["category"] = "random"
                print(f"{GREEN}Category reset to default {BLUE}Random{GREEN}.")
            elif selection == 3:
                game_settings["difficulty"] = "random"
                print(f"{GREEN}Difficulty reset to default {BLUE}Random{GREEN}.")
            elif selection == 4:
                game_settings["lives"] = 6
                print(f"{GREEN}Lives reset to default {BLUE}6{GREEN}.")
            else:
                print(f"{GREEN}Settings not changed.")

            input(f"{YELLOW}Press enter to go back to the settings menu.")
            clear_previous_lines(len(reset_options) + 4 + lines_to_clear)
        elif settings_selection == 5:
            print(f"{MAGENTA}Game Options - Show Settings")
            print(f"{GREEN}Current settings:")
            print(f"Category: {BLUE}{game_settings['category']}{GREEN}")
            print(f"Difficulty: {BLUE}{game_settings['difficulty']}{GREEN}")
            print(f"Lives: {BLUE}{game_settings['lives']}{GREEN}")
            input(f"{YELLOW}Press enter to go back to the settings menu.")
            clear_previous_lines(6)
        elif settings_selection == 6:
            return game_settings


# tests are in tests/__init__.py
if __name__ == "__main__":
    hangman_ascii = __file__.replace("__init__.py", "") + "hangman_ascii.txt"
    with open(hangman_ascii, "r", encoding="utf-8") as f:
        ascii_art = f.read()
        print(f"{YELLOW}{ascii_art}")
    del hangman_ascii, ascii_art
    print(f"{'-' * 8} Hangman, but with more Python {'-' * 8}")
    user_settings = {
        "category": "random",
        "difficulty": "random",
        "lives": 6,
    }
    game_won = None
    lines_to_clear = 0
    previous_state = "main_menu"
    while True:
        main_menu_selection, invalid_menu_selections = show_main_menu()
        lines_to_clear += invalid_menu_selections
        lines_to_clear += 2 if previous_state == "hangman_game" else 0
        clear_previous_lines(lines_to_clear)
        lines_to_clear = 0
        if main_menu_selection == 1:
            game_won = play_hangman(user_settings, previous_state)
            lines_to_clear += 5 if game_won else 6
            previous_state = "hangman_game"
        elif main_menu_selection == 2:
            user_settings = configure_game_settings(user_settings, previous_state)
            lines_to_clear += 5
            main_menu_selection = 0
            previous_state = "settings_menu"
        else:
            print(f"{YELLOW}Goodbye!")
            exit()
