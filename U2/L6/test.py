user_input = ""
numbers = []
while user_input != "-1":
    user_input = input("Enter a positive integer, -1 to end: ")
    if user_input != "-1":
        numbers.insert(0, int(user_input))

print(f"Your numbers:\n{numbers}")
print(f"Sum: {sum(numbers)}")
print(f"Average: {sum(numbers) / len(numbers)}")
print(f"max: {max(numbers)}")