# accept an integer value from the user and convert it to celsius, rounded to the nearest whole number


fahrenheit = int(input("Enter degrees in fahrenheit: "))
print(f"{fahrenheit} degrees fahrenheit is {round((int(fahrenheit) - 32) * 5 / 9)} degrees celsius")