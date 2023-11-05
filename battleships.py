# from random import randint
from battleships_interface import title, gameover
import battleships_objects as o
import battleships_globals as g
import battleships_functions as f

# Initialize game loop
game = True

# Play as long game is true
while game == True:    
    # Print title screen
    title()
    # Reset the global variables
    f.reset()

    # Create map grid for player and computer        
    for i in range(0,100):    
        g.grid_player.append(o.gridPosition(i))
        g.grid_computer.append(o.gridPosition(i))

    # Create ships for player and computer
    for i in "ABCDE":
        g.ships_player.append(o.Ship(i))
        g.ships_computer.append(o.Ship(i))

    # Create shadow map to make computer aiming a bit easier
    for i in range(0,100):
        g.shadow_map.add(i) 

    # Place computers ships
    f.placeships("computer")

    # Print map grids for player to see
    f.showmap(g.DEBUG)

    # Ask player to place ships
    f.placeships("player")

    # Coin flip to see who starts
    print("All ships have been placed, battle is ready to begin!")
    # Coin flip: 0 = Computer, 1 = Player
    turn = f.randint(0, 1)
    # Inform the result
    if turn == 0:
        print(f"{g.COMPUTER}Computer won the coin flip, so it has the first turn.{g.RESET}")
    else:
        print(f"{g.PLAYER}You won the coin flip, so you will start.{g.RESET}")    
    # Wait for player to start the game
    print ("\nPress enter to continue...")
    input()

    # Loop until game ends
    victory = 0
    complete = 0
    gridpos = False
    target = ""
    temp = 0
    directions = []
    msg = ""

    while victory == 0:
        # Computer's turn
        if turn == 0:
            msg = f.turn_computer()
            turn = 1
            if g.hp_player == 0:
                # Player wins
                victory = 1
                winner = "computer"
        # Player's turn
        else:
            if (f.turn_player(msg) == True):
                turn = 0
            else:
                continue    
            if g.hp_computer == 0:
                # Player wins
                victory = 1
                winner = "player"

    # Game ends
    f.showmap(True)

    # Print game over screen
    game = gameover(winner)
    
print("\nThank you for playing")
