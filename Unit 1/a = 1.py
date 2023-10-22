def print_item(title, items):
    if title: print (title)
    if type(items) == str:
        length = len(items) + 4
        print(f"|{'-' * length}|")
        print(f"| {items}   |")
        print(f"|{'-' * length}|")
    elif type(items) == list:
        length = 0
        for item in items:
            if len(item) > length: length = len(item) + 4
        print(f"|{'-' * length}|")
        for item in items:
            print(f"| {item}{' ' * (length - len(item) - 2)} |")
            print(f"|{'-' * length}|")
    print()

personal_info = ["Issac Liu", "New York City, New York"]
print_item("Personal Information:", personal_info)
print_item("Interesting fact about me:", "I like reading Asian web novels and webtoons.")
print_item ("MY SLOGAN:", "It be like that")