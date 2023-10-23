from random import randint

print("""Welcome to Guess My Secret Number!
Guess a number between 1 and 20
-------------------------------""")

secret = randint(1, 20)
guess, tries, max_tries = 0, 0, 5

while guess != secret and tries < max_tries:
    guess = int(input("Enter a guess: "))
    if guess != secret:
        tries += 1
    else:
        break
    print("Too high!" if guess > secret else "Too low!")

print(f"You guessed it! My number was {secret}\nIt took you {tries} guesses\nGame over, goodbye!" if guess == secret else "Out of guesses, game over!")