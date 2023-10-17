
# name = input("Enter your name: ")
# color = input("What is your favorite color? ")
# age = input("How old are you? ")
# print(f"Welcome, {name}! Your favorite color is {color}.")
# print(f"You are {age} years old.")
# print(f"Next year, you will be {int(age) + 1} years old.")

from colorama import Fore

# setup
GREEN = Fore.GREEN
CYAN = Fore.CYAN
RESET = Fore.RESET
print(f"{GREEN}Versus Blåhaj{RESET}")
print("-------------")

# ask for info required to compare
options = ["[1] Normal (100 cm)", "[2] Small (55 cm)"]
print(f"{CYAN}What size Blåhaj are you comparing to?")
for option in options:
    print(f"{GREEN}{option}{RESET}")
blåhaj_size = ""
while blåhaj_size not in ["1", "2"]:
    blåhaj_size = input(f"{CYAN}> {RESET}")
blåhaj_size = "normal" if blåhaj_size == "1" else "small"

item_name = input(f"{CYAN}What's the name of the item you're comparing to a Blåhaj? {RESET}")

options = ["[1] Price", "[2] Width", "[3] Height", "[4] Length", "[5] Weight"]
print(f"{CYAN}What are you comparing to Blåhaj?")
for option in options: 
    print(f"{GREEN}{option}{RESET}")
compare_type = ""
while compare_type not in ["1", "2", "3", "4", "5"]:
    compare_type = input(f"{CYAN}> {RESET}")
options = {"1": "price", "2": "width", "3": "height", "4": "length", "5": "weight"}
compare_type = options[compare_type]
del options

item_value = ""
while not isinstance(item_value, (int, float)):
    item_value = input(f"{CYAN}What is the {compare_type} of the {item_name}? {RESET}")
    try:
        item_value = int(item_value)
    except ValueError:
        try:
            item_value = float(item_value)
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{RESET}")

# set up non-user data required for comparison
blåhaj_data = {
    "normal": {
        "price": 29.99, 
        "width": 54,
        "height": 23,
        "length": 99,
        "weight": 0.64,
    },
    "small": {
        "price": 7.99, 
        "width": 17,
        "height": 16,
        "length": 55,
        "weight": 0.19,
    },
}
result_messages = {
    "price": {
        "unit": "dollars",
        "less": "cheaper than",
        "more": "more expensive than",
        "equal": "the same price as",
    },
    "weight": {
        "unit": "kg",
        "less": "lighter than",
        "more": "heavier than",
        "equal": "the same weight as",
    }
}
size_messages = {
    "unit": "cm",
    "less": "smaller than",
    "more": "larger than",
    "equal": "the same size as",
}
result_messages.update(dict.fromkeys(["width", "height", "length"], size_messages))
del size_messages

# actually compare the data and output the result
metric_difference = float(f"{blåhaj_data[blåhaj_size][compare_type] - float(item_value):.2f}")
difference_percent = f"{((float(item_value) / blåhaj_data[blåhaj_size][compare_type]) * 100):.2f}"
metric = result_messages[compare_type]["unit"]

if metric_difference < 0:
    result_message = result_messages[compare_type]["more"]
elif metric_difference > 0:
    result_message = result_messages[compare_type]["less"]
else:
    result_message = result_messages[compare_type]["equal"]

print(f"{GREEN}{item_name} is {abs(metric_difference)} {metric} {result_message} Blåhaj's {compare_type}.")
if metric_difference != 0:
    print(f"{GREEN}It is {difference_percent}% Blåhaj's {compare_type}.{RESET}")