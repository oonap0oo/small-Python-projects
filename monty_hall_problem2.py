# Monty Hall problem simulation using Monte Carlo Method
# ------------------------------------------------------

import random # this code only uses the random library of Python

# perform a given number of simulated games
# the player either always switches to another door or always stayes
# with his choice, this is controlled by a boolean argument
# the function returns the number of wins
def run_games(number_of_games, player_switches_doors):
    player_wins = 0
    doors = [1,2,3] # the three doors in the game
    for _ in range(number_of_games):
        # one random door hides a car, two other doors a goat
        position_car = random.randint(1,3)
        
        # the player randomly selects one of three doors, door stays closed for now
        player_choice = random.randint(1,3)

        # host opens a door, always one with a goat and
        # different from the one selected by the player
        host_options = [door for door in doors if door != position_car and door != player_choice]
        door_opened_by_host = random.choice(host_options) # either 1 or 2 remaining options

        # the player can switch to the remaining closed door or keep initial choice
        # this choice is given as argument to this function
        if player_switches_doors == True: # player decides to switch
            player_options = [door for door in doors if door != player_choice and door != door_opened_by_host]
            player_choice = player_options[0] # one remaining option = new choice of player
            
        # does the player win the car? 
        if player_choice == position_car:
            player_wins += 1 # add a win

    return player_wins


random.seed()

# number of simulated games in each run
number_of_games = 100000

print(f"""Monty Hall problem simulation using Monte Carlo Method
------------------------------------------------------
The Monty Hall problem is a probability puzzle in which three closed doors are presented.
Behind one door the price (a car) is hidden, behind the other two a goat awaits.
A contestant chooses one of three doors, and the host, who knows where
the prize is (a car), opens a different door revealing a goat.

The contestant is then offered the chance to switch to
the remaining unopened door.
The correct strategy is to always switch,
as this doubles your chances of winning the prize from 1/3 to 2/3.

A Monte Carlo simulation is a computerized mathematical technique
that uses repeated random sampling to predict the probable outcomes
of uncertain events, providing a range of possible results and
their probabilities.

Simulating {number_of_games} games.
One set in which the player always switches his choice of doors,
a second set in which the player never switches.""")

# run simulation with switching choice
wins_with_switch = run_games(number_of_games, True)
ratio_wins_total_with_switch = wins_with_switch / number_of_games
print(f"\nBy always switching to the other door, the player won {wins_with_switch} out of {number_of_games} games")
print(f"This means the player won {ratio_wins_total_with_switch:.2%} of the games by switching doors")

# run simulation without switching choice
wins_without_switch = run_games(number_of_games, False)
ratio_wins_total_without_switch = wins_without_switch / number_of_games
print(f"\nBy always staying with the initial choice, the player won {wins_without_switch} out of {number_of_games} games")
print(f"This means the player won {ratio_wins_total_without_switch:.2%} of the games by keeping initial choice")

improvement = ratio_wins_total_with_switch / ratio_wins_total_without_switch
print(f"\nSwitching improved the players wins by factor {improvement:.2f} in this simulation")
