import random
from colorama import Fore, just_fix_windows_console

just_fix_windows_console()
CYAN, YELLOW, GREEN, RESET = Fore.CYAN, Fore.YELLOW, Fore.GREEN, Fore.RESET

print(f"{CYAN}What would you like to do?")
mode = input(f"{GREEN}[1] Enter a point\n[2] Generate a random point\n[3] Generate a random point based on a bound\n{CYAN}> {RESET}")
while mode not in ["1","2","3"]:
    mode = input(f"{CYAN}> {RESET}")
mode = int(mode)

def coords_to_quadrant(x:int, y:int):
    # map the coordinates to 0-2, so pos. nums = 2, neg. nums = 0, 0 = 1
    x = int((x / abs(x)) + 1 if x != 0 else 1)
    y = int((y / abs(y)) + 1 if y != 0 else 1)

    map = [
        ["Quadrant III", "On the y axis", "Quadrant IV"],
        ["On the x axis", "Point is on the origin", "On the x axis"],
        ["Quadrant II", "On the y axis", "Quadrant I"]
    ]
    return map[int(y)][int(x)]

if mode == 1:
    x = int(input(f"{CYAN}Enter the x coordinate: {RESET}"))
    y = int(input(f"{CYAN}Enter the y coordinate: {RESET}"))
elif mode == 2:
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    print(f"{CYAN}Randomly generated x-y point: ({GREEN}{x}{CYAN}, {GREEN}{y}{CYAN})\n")
else:
    bound = 0
    while bound < 1: bound = int(input(f"{CYAN}Enter your bound: {RESET}"))

    print(f"{CYAN}Generating a random x-y coordinate from {GREEN}-{bound}{CYAN} to {GREEN}{bound}")
    x = random.randint(-bound, bound)
    y = random.randint(-bound, bound)
    print(f"{CYAN}Randomly generated x-y point: ({GREEN}{x}{CYAN}, {GREEN}{y}{CYAN})\n")

print(f"{YELLOW}{coords_to_quadrant(x, y)}{RESET}")