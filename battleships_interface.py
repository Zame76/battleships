from os import system
import battleships_globals as g

# Print the map
def showmap(showall = False):
    position = ""
    ship = ""
    target = 0
    # Clear map
    system("cls")
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
            if showall == True and ship.hp > 0:                
                    print(f"    {g.COMPUTER}Health {ship.hp}/{ship.max}"," " * 2, end = "")                
            else:                
                if ship.hp > 0:
                    print(f"    {g.COMPUTER}{ship.status.capitalize()}{g.RESET}", end = "")        
                else:
                    print(f"    {g.HIT}{ship.status.upper()}{g.RESET}", end = "")        
        print(f"{g.RESET}")


# Print out error message
def errormsg(msg):
    print(f"ERROR! {msg}") 
    print("Or to see grids, write (M)ap")
    print("Or you can always stop playing by writing (Q)uit")   


# Print title screen
def title():
    system('cls')
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
    print(f"\n\tPress Enter to start{g.RESET}")
    input()


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