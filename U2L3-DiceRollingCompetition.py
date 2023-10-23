import random
import time

rounds = int(input("How many rounds do you want to play? "))

player_points = 0
point_map = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, -100]
player_rolls, cpu_rolls = []

for i in range(0, rounds):
    print(f"\nROUND {i + 1}!")
    cpu_roll = random.randint(1, 20)
    cpu_rolls.append(cpu_roll)
    print(f"The computer rolled a {cpu_roll}")
    round_roll, round_total, round_tries = 0, 0, 0
    round_tied = False

    while round_roll < (cpu_roll + 1) and round_tries < 10:
        round_roll = random.randint(1, 20)
        player_rolls.append(round_roll)
        print(f"Player roll {round_tries + 1}: {round_roll}")
        round_total += round_roll
        round_tries += 1
        if round_roll == cpu_roll: round_tied = True
    
    if round_roll > cpu_roll:
        player_points += (point_map[round_tries - 1])
        print(f"Player wins and gets {point_map[round_tries - 1]} points!")
    elif round_tied:
        print(f"Player got a tie! No points gained or lost")
    else:
        print(f"Player loses and loses 100 points!")

print(f"\n\nTotal points: {player_points}")
print(f"Average points per round: {round(player_points / rounds)}")
print(f"Average player roll: {round(sum(player_rolls) / len(player_rolls))}")
print(f"Average computer roll: {round(sum(cpu_rolls) / len(cpu_rolls))}")