# The Plan

## Variables

- rounds: an integer that stores the number of rounds the player wants to play.
- player_points: an integer that stores the total points accumulated by the player.
- point_map: a list of integers that maps the number of tries it took to beat the computer's roll to the points earned by the player.
- player_rolls: a list of integers that stores the rolls made by the player in each round.
- cpu_rolls: a list of integers that stores the rolls made by the computer in each round.
- round_roll: an integer that stores the roll made by the player in the current round.
- round_total: an integer that stores the total of the rolls made by the player in the current round.
- round_tries: an integer that stores the number of tries made by the player in the current round.
- round_tied: a boolean that is set to True if the player's roll is tied with the computer's roll in the current round.

## Loops

- for loop: iterates over the range of rounds specified by the player.
- while loop: iterates until the player has made 10 rolls or has beaten the computer's roll.

## Plan

1. Ask the user for the number of rounds to be played and store it in rounds.
2. Initialize the player_points, player_rolls, and cpu_rolls variables to 0 and empty lists, respectively.
3. Create a point_map list that maps the number of tries to the points earned by the player.
4. For every round specified by the user:
    1. Print the round number.
    2. Generate a random roll for the computer and store it in the cpu_roll variable.
    3. Append the cpu_roll to the cpu_rolls list.
    4. Initialize the round_roll, round_total, and round_tries variables to 0.
    5. Initialize the round_tied variable to False.
    6. While the round_roll is less than the cpu_roll plus 1 and the round_tries is less than 10:
        1. Generate a random roll for the player and store it in the round_roll variable.
        2. Append the round_roll to the player_rolls list.
        3. Add the round_roll to the round_total variable.
        4. Increment the round_tries variable.
        5. If the round_roll is equal to the cpu_roll, set the round_tied variable to True.
    7. If the round_roll is greater than the cpu_roll:
        1. Add the points earned by the player to the player_points variable.
        2. Print the points earned by the player.
    8. If the round_tied variable is True, print that the player got a tie.
    9. If the round_roll is less than or equal to the cpu_roll and the round_tied variable is False:
        3. Deduct 100 points from the player_points variable.
        4. Print that the player loses and lost 100 points.
    10. Pause for 5 seconds.
5. Print the total points earned by the player.
6. Print the average points earned per round.
7. Print the average roll made by the player and computer.
