from colorama import Fore, Style, init
import random
import math

# Initialize colorama
init(autoreset=True)

# Define constants for colors and styles
CYAN, GREEN, YELLOW, RED, MAGENTA, BLUE = Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.BLUE
BOLD, RESET = Style.BRIGHT, Style.RESET_ALL + Fore.RESET

# Define question dictionaries
TRIVIA_QUESTIONS = [
    {"question": "What is the capital of France? ", "answer": "paris"},
    {"question": "What is the largest planet in our solar system? ", "answer": "jupiter"},
    {"question": "What is the name of the world's largest ocean? ", "answer": "pacific"},
    {"bonus": "What is the smallest country in the world? ", "answer": "vatican city"},
]

MATH_QUESTIONS = [
    {"question": "How many moons does the planet Saturn have? ", "answer": "83"},
    {"question": "What is the total number of keys on a standard piano, including both black and white keys? ", "answer": "88"},
    {"question": "What is the value of the Riemann Zeta function at s = 1? ", "answer": "infinity"},
    {"bonus": "In particle physics, what is approximately the mass of the Higgs boson in GeV/c^2 (gigaelectronvolts / speed of light^2)? Do not include units in your answer. ", "answer": "125.1"},
]

# Functions for asking trivia and math questions
def ask_trivia_question(question):
    user_answer = input(f"{GREEN}{question['question']}{RESET}")
    return question["answer"] in user_answer.lower()

def ask_math_question(question):
    discriminant = (question["b"] ** 2) - (4 * question["a"] * question["c"])
    if discriminant < 0:
        roots = [None]
    elif discriminant == 0:
        roots = [-question["b"] / (2 * question["a"])]
    else:
        x1 = (-question["b"] + math.sqrt(discriminant)) / (2 * question["a"])
        x2 = (-question["b"] - math.sqrt(discriminant)) / (2 * question["a"])
        roots = [round(x1, 2) if "." in str(x1) else x1, round(x2, 2) if "." in str(x2) else x2]
    formatted_question = f"{question['a']}x^2 {'+' if question['b'] >= 0 else '-'} {abs(question['b'])}x {'+' if question['c'] >= 0 else '-'} {abs(question['c'])} = 0"
    user_answer = input(f"{GREEN}In the equation {MAGENTA}{formatted_question}{GREEN}, what is the value of {MAGENTA}x{GREEN}?{RESET} ").lower()
    return "none" in user_answer or float(user_answer) in roots

# Function to play a round of the game
def play_game(name, questions):
    num_correct = 0
    for question in questions[:3]:
        if ask_trivia_question(question) or ask_math_question(question):
            print(f"{YELLOW}{BOLD}Correct!{RESET}")
            num_correct += 1
        else:
            print(f"{RED}{BOLD}Wrong!{RESET}")

    number_color = GREEN if num_correct >= 2 else RED
    print(f"{CYAN}You got {number_color}{num_correct}{CYAN} out of 3 questions correct. Good job, {name}!")

    if num_correct == 3:
        print(f"You are now entering the {YELLOW}{BOLD}BONUS ROUND!{RESET}")
        if ask_trivia_question(questions[3]) or ask_math_question(questions[3]):
            num_correct += 1
            print(f"{YELLOW}{BOLD}Congratulations! You got 4 out of 4 questions correct!")
        else:
            print(f"{RED}{BOLD}Sorry, you only got 3 out of 4 questions correct. Better luck next time!")

# Main program
name = input(f"{CYAN}Enter your name: {RESET}")
print(f"{CYAN}Welcome to the trivia game, {BLUE}{name}{CYAN}!")
print(f"{CYAN}What type of questions do you want?")
game_mode = input(f"{GREEN}[1] Trivia Questions\n[2] Math Questions\n{CYAN}> {RESET}")

if game_mode == "1":
    questions = TRIVIA_QUESTIONS
else:
    questions = MATH_QUESTIONS

print(f"{CYAN}What difficulty?")
hard_mode = input(f"{GREEN}[1] Easy\n[2] Hard\n{CYAN}> {RESET}")
hard_mode = hard_mode == "2"

if game_mode == "1":
    print(f"{CYAN}{BOLD}NOTE{RESET}{CYAN}: If an answer contains decimal places, round to the hundredths place.")
else:
    print(f"{CYAN}{BOLD}NOTE{RESET}{CYAN}: It is possible to have no real roots. In such cases, enter 'None'.")

play_game(name, questions)