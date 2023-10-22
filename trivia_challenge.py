import math
import random

from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()
RED, GREEN, BLUE, YELLOW, CYAN = Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL + Fore.RESET
name = input(f"{CYAN}Enter your name: {RESET}")
print(f"{CYAN}Welcome to the trivia game, {BLUE}{name}{CYAN}!")
print(f"{CYAN}What type of questions do you want?")
game_mode = input(f"{GREEN}[1] Trivia Questions\n[2] Math Questions\n{CYAN}> {RESET}")
options = {"1": "trivia", "2": "math"}
while game_mode not in options:
    game_mode = input(f"{CYAN}> {RESET}")
game_mode = options[game_mode]

print(f"{CYAN}What difficulty?")
hard_mode = input(f"{GREEN}[1] Easy\n[2] Hard\n{CYAN}> {RESET}")
while hard_mode not in ["1", "2"]:
    hard_mode = input(f"{CYAN}> {RESET}")
hard_mode = True if hard_mode == "2" else False

if game_mode == "trivia":
    if hard_mode == False:
        questions = [
            {"question": "What is the capital of France? ", "answer": "paris"},
            {"question": "What is the largest planet in our solar system? ", "answer": "jupiter"},
            {"question": "What is the name of the world's largest ocean? ", "answer": "pacific"},
            {"bonus": "What is the smallest country in the world? ", "answer": "vatican city"},
        ]
    else:
        questions = [
            {"question": "How many moons does the planet Saturn have? ", "answer": "83"},
            {"question": "What is the total number of keys on a standard piano, including both black and white keys? ", "answer": "88"},
            {"question": "What is the value of the Riemann Zeta function at s = 1? ", "answer": "infinity"},
            {"bonus": "In particle physics, what is approximately the mass of the Higgs boson in GeV/c^2 (gigaelectronvolts / speed of light^2)? Do not include units in your answer. ", "answer": "125.1"},
        ]
    
    # initial 3 questions
    num_correct = 0
    for question in questions[:3]:
        answer = input(f"{GREEN}{question['question']}{RESET}")
        if question["answer"] in answer.lower():
            print(f"{YELLOW}Correct!")
            num_correct += 1
        else:
            print(f"{RED}Wrong!")

    # Print final results and handle bonus round
    number_color = GREEN if num_correct >= 2 else RED
    print(f"{CYAN}You got {number_color}{num_correct}{CYAN} out of 3 questions correct. Good job, {name}!")
    if num_correct == 3:
        print(f"You are now entering the {YELLOW}{BOLD}BONUS ROUND!{RESET}")
        answer = input(f"{YELLOW}{BOLD}{questions[3]['bonus']}{RESET}")
        if questions[3]["answer"] in answer.lower():
            num_correct += 1
            print(f"{YELLOW}{BOLD}Congratulations! You got 4 out of 4 questions correct!")
        else:
            print(f"{RED}{BOLD}Sorry, you only got 3 out of 4 questions correct. Better luck next time!")
            
else:
    print(f"{CYAN}{BOLD}NOTE{RESET}{CYAN}: If an answer contains decimal places, round to the hundredths place.")
    if hard_mode == False:
        # basic addition, subtraction, multiplication, and division
        def ask_math_question():
            question = {
                "number_1": random.randint(1,10),
                "operation": random.choice(["+", "-", "*", "/"]),
                "number_2": random.randint(1,10)
            }
            formatted_question = str(question['number_1']) + question['operation'] + str(question['number_2'])
            correct_answer = eval(formatted_question)
            if "." in str(correct_answer):
                correct_answer = round(correct_answer, 2)
            answer = ""
            while isinstance(answer, float) == False:
                answer = float(input(f"What is {formatted_question}? "))
            return True if answer == correct_answer else False
        
    else:
        print(f"{CYAN}{BOLD}NOTE{RESET}{CYAN}: It is possible to have no real roots. In such cases, enter 'None'. If there are two real roots, you only need to enter one.")
        # quadratic equations
        def ask_math_question():
            MAGENTA = Fore.MAGENTA
            quadratic = {
                "a": random.randint(-10,10),
                "b": random.randint(-10,10),
                "c": random.randint(-10,10)
            }
            # solve for roots of quadratic equation
            discriminant = (quadratic["b"]**2) - (4*quadratic["a"]*quadratic["c"])
            if discriminant < 0: roots = [None]
            elif discriminant == 0: roots = [-quadratic["b"] / (2*quadratic["a"])]
            else:
                x1 = (-quadratic["b"] + math.sqrt(discriminant)) / (2*quadratic["a"])
                x2 = (-quadratic["b"] - math.sqrt(discriminant)) / (2*quadratic["a"])
                # round to the hundredths place ONLY IF the number has decimal places
                if "." in str(x1): x1 = round(x1, 2)
                if "." in str(x2): x2 = round(x2, 2)
                roots = [x1, x2]
            # ask user for answer and check if it is correct
            formatted_question = f"{quadratic['a']}x^2 {'+' if quadratic['b'] >= 0 else '-'} {abs(quadratic['b'])}x {'+' if quadratic['c'] >= 0 else '-'} {abs(quadratic['c'])} = 0"
            answer = ""
            while isinstance(answer, float) == False:
                answer = input(f"{GREEN}In the equation {MAGENTA}{formatted_question}{GREEN}, what is the value of {MAGENTA}x{GREEN}?{RESET} ")
                if "none" in answer.lower():
                    return True if None in roots else False
                else:
                    try: answer = float(answer)
                    except ValueError: answer = ""
            return True if answer in roots else False
    
    # initial 3 questions
    num_correct = 0
    for i in range(3):
        if ask_math_question() == True:
            print(f"{YELLOW}Correct!")
            num_correct += 1
        else:
            print(f"{RED}Wrong!")

    # Print final results and handle bonus round
    number_color = GREEN if num_correct >= 2 else RED
    print(f"{CYAN}You got {number_color}{num_correct}{CYAN} out of 3 questions correct. Good job, {name}!")
    if num_correct == 3:
        print(f"{CYAN}You are now entering the {YELLOW}{BOLD}BONUS ROUND!{RESET}")
        if ask_math_question() == True:
            num_correct += 1
            print(f"{YELLOW}{BOLD}Congratulations! You got 4 out of 4 questions correct!")
        else:
            print(f"{RED}{BOLD}Sorry, you only got 3 out of 4 questions correct. Better luck next time!")