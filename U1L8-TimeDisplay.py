from colorama import Fore, just_fix_windows_console

just_fix_windows_console()
GREEN, YELLOW, CYAN, RESET = Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.RESET

# set up the necessary info for processing
seconds = int(input(f"{CYAN}How much time in seconds? {RESET}"))
print(f"{CYAN}What display type do you want? ")
display_type = input(f"{GREEN}[1] Type 1\n[2] Type 2\n[3] Type 3\n[4] See examples\n{CYAN}> {RESET}")
while display_type not in ["1", "2", "3"]:
    if display_type == "4":
        print(f"{CYAN}Type [1]: {GREEN}21h, 11m, 5s")
        print(f"{CYAN}Type [2]: \n{GREEN}21 hours\n11 minutes\n5 seconds")
        print(f"{CYAN}Type [3]: {GREEN}21:04:01")
        print(f"{CYAN}What display type do you want? ")
    display_type = input(f"{CYAN}> {RESET}")

# parse seconds to hours, minutes, seconds
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = seconds % 60

# format the hours, minutes, seconds based on the display type
if display_type == "1":
    print(f"{CYAN}The total time is:\n{YELLOW}{hours}h, {minutes}m, {seconds}s{RESET}")
elif display_type == "2":
    print(f"{CYAN}The total time is:\n{YELLOW}{hours}{' hour' if hours == 1 else ' hours'}\n{minutes}{' minute' if minutes == 1 else ' minutes'}\n{seconds}{' second' if seconds == 1 else ' seconds'}{RESET}")
else:
    print(f"{CYAN}The total time is:\n{YELLOW}{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
