# Import libraries and functions
from os import system, name as os_name
import battleships_globals as g

# Check if windows or linux for the use of correct clear screen command
if os_name == "nt":
    # For Windows:
    clearscreen = "cls"
else:
    # For Linux 
    clearscreen = "clear"

# BATTLESHIPS_INTERFACE LIST:
#
# Function showmap(showall = False)                     - rows: 41-138
#   - print color coded map grids, ship status, log information
#   - showall has two different values, True and False (default)
#       - true shows all the map items, including computer ship positions
#       - usually shown at the end of the game
#       - global variable DEBUG is usually sent in every function call
#
# Function errormsg(msg)                                - rows: 141-145
#   - print custom error message with standard input info
#   - msg is the customizable error message, which tells what went wrong
#
# Function title()                                      - rows: 148-191
#   - print title screen and instructions at the start of the game
#   - let player change the rulesets between modern and tracitional rules
#       - show the information what eact ruleset does
#
# Function gameover(winner)                             - rows: 194-207
#   - print game over screen and show who was victorious
#   - ask if player wants to play again
#
# Function endgame()                                    - rows: 210-214
#   - player has decided to stop playing in the middle of the game
#   - print end game messages



# Print the map
def showmap(showall = False):
    position = ""
    ship = ""
    target = 0
    logno = g.counter
    # Clear map
    system(clearscreen)
    # Position player labels
    print(f"{g.PLAYER}PLAYER", " " * 79, f"{g.COMPUTER}COMPUTER") 
    # Print top axis info
    print(" " * 18, f"{g.PLAYER}A  B  C  D  E  F  G  H  I  J", " " * 7, f"{g.COMPUTER}A  B  C  D  E  F  G  H  I  J")
    for i in range(0,10):
        ship = g.ships_player[int(i/2)]
        # Print ship name on even row
        if (i % 2 == 0):
            print(f"{g.PLAYER}{ship.name.upper():15}", end="")            
        # Print ship health on odd row
        else:
            if ship.hp > 0:
                print(f"  {g.PLAYER}Health {ship.hp}/{ship.max}"," " * 2, end = "")
            else:                
                print(f"  {g.HIT}{ship.status.upper()}{g.RESET}", " " * 3, end = "")
        # A little bit of space between ship info and grid
        print(f"{i + 1:2} " , end = "")
        # Print colorcoded player grid
        for j in range(0,10):
            target = i * 10 + j
            # Unify all the ships as same symbol, if position has a ship in it
            if g.grid_player[target].content in "ABCDE":
                position = f"{g.PLAYER}O"
            # If there has been a miss
            elif g.grid_player[target].content == "x":        
                position = f"{g.RESET}x"
            # If ship has been hit
            elif g.grid_player[target].content == "*":
                position = f"{g.HIT}*"
            else:
                # If showall is true then show all the computer aiming aid spots
                if showall == True and g.grid_player[i * 10 + j].content == 'i':
                    position = f"{g.RESET}i"
                # Otherwise show just ocean
                else:
                    position = f"{g.OCEAN} "
            # Now print the color coded content of the grid           
            print(f"{g.OCEAN}[{position}{g.OCEAN}]", end = "")
           
        # Add a little bit of space between the grids and show computer y-axis
        print(" " * 3, f"{g.COMPUTER}{i + 1:2} " , end = "")
        # Print color coded computer grid
        for j in range(0,10):  
            target = i * 10 + j          
            # Show unified ship positions only if show all is true, other wise replace with ocean
            if g.grid_computer[target].content in "ABCDE":
                if showall == True:
                    position = f"{g.COMPUTER}O"
                else:
                    position = f"{g.OCEAN} "    
            # If position has been hit and missed
            elif g.grid_computer[target].content == "x":        
                position = f"{g.RESET}x"
            # If ship found and hit
            elif g.grid_computer[target].content == "*":
                position = f"{g.HIT}*"
            # Rest is just ocean
            else:                
                position = f"{g.OCEAN} "    
            print(f"{g.OCEAN}[{position}{g.OCEAN}]", end = "")            
        # Print computer ship names on even rows
        ship = g.ships_computer[int(i /2)]
        if (i % 2 == 0):
            print(f"  {g.COMPUTER}{ship.name.upper():15}", end="")
        # Print computer ship health on odd rows
        else:
            # Show active ship info only if showall is true
            if showall == True and ship.hp > 0:                
                    print(f"    {g.COMPUTER}Health {ship.hp}/{ship.max}{g.RESET}", end = "")                
            # Otherwise, show ships status
            else:                
                # Ship is active
                if ship.hp > 0:
                    print(f"    {g.COMPUTER}{ship.status.capitalize()}{g.RESET}", end = "")        
                # Ship is destroyed
                else:
                    print(f"    {g.HIT}{ship.status.upper()}{g.RESET}", end = "")  
        print()    
    # Show log, it there are values
    if len(g.log) != 0:                
        print(f"\n{g.WHITE}LOG OF LATEST EVENTS:{g.RESET}")
    # Show only latest five entries of log
    if g.counter < 5:
        j = 0
    else:
        j = g.counter - 5
    # Print log entries
    for i in range(j,g.counter):
        print(f"\tTurn {i + 1:2}: {g.log[i]}")
    print()    


# Print out error message
def errormsg(msg):
    print(f"ERROR! {msg}") 
    print("Or to see grids, write (M)ap")
    print("Or you can always stop playing by writing (Q)uit")   


# Print title screen
def title():
    system(clearscreen)
    print(f"{g.PLAYER}")
    print("\t ____        _   _   _           _     _")
    print("\t|  _ \\      | | | | | |         | |   (_)           ")
    print("\t| |_) | __ _| |_| |_| | ___  ___| |__  _ _ __  ___")
    print("\t|  _ < / _` | __| __| |/ _ \\/ __| '_ \\| | '_ \\/ __|")
    print("\t| |_) | (_| | |_| |_| |  __/\\__ \\ | | | | |_) \\__ \\")
    print("\t|____/ \\__,_|\\__|\\__|_|\\___||___/_| |_|_| .__/|___/")
    print("\t                                        | |")
    print("\t                                        |_|")
    print(" " * 45, "Version 2.0")
    print("\n\tPlay a game of battleships against a computer.")
    print("\n\tDuring the game, you can print current (M)ap")
    print("\tOr you can use (Q)uit to end the game")
    print("\tType (C)hange to use different rules")
    print(f"\n\tCurrent ruleset: {g.COMPUTER}{g.rules.capitalize()}{g.PLAYER}")
    print(f"\n\tPress Enter to start or (C)hange ruleset{g.RESET}")
    ruleset = input("> ").casefold()
    if ruleset in ["c", "(c)", "change", "(c)hange"]:
        system(clearscreen)        
        if g.rules == "modern":
            g.rules = "traditional"
            print(f"\n{g.PLAYER}Rules changed to {g.COMPUTER}Traditional{g.PLAYER}")
            print("Carrier size is 5")
            print("Battleship size is 4")
            print("Cruiser size is 3")
            print("Submarine size is 2")
            print("Destroyer size is 1")
        else:
            g.rules = "modern"
            print(f"\n{g.PLAYER}Rules changed to {g.COMPUTER}Modern{g.PLAYER}")
            print("Carrier size is 5")
            print("Battleship size is 4")
            print("Cruiser size is 3")
            print("Submarine size is 3")
            print("Destroyer size is 2")
        print("\nPress enter to continue")
        input()
        title()
    elif ruleset in ["q", "(q)", "quit", "(q)uit"]:
        print("\nThank you for playing!\n")
        exit()


# Print game over text
def gameover(winner):
    print("\nGame is over!")
    if winner == "player":
        print(f"\n{g.PLAYER}Congratulations! You have won the game!{g.RESET}")
    else:
        print(f"\n{g.COMPUTER}Sorry, but computer beat you this time.{g.RESET}")
    print("Would you like to play again? Type (Y)es for new game, otherwise game ends")
    game = input("> ")
    if game not in ['y', '(y)', 'yes', '(y)es']:
        newgame = False
    else:
        newgame = True
    return newgame


# Exit game
def endgame():
    showmap(True)
    print("\nThank you for playing!\n")
    exit()    