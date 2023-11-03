from os import system
from random import randint 
import battleships_globals as g

# Print the map
def showmap(showall = False):
    position = ""
    # Clear map
    system("cls")
    # Position player labels
    print(f"{g.PLAYER}PLAYER", " " * 79, f"{g.COMPUTER}COMPUTER") 
    # Print top axis info
    print(" " * 18, f"{g.PLAYER}A  B  C  D  E  F  G  H  I  J", " " * 7, f"{g.COMPUTER}A  B  C  D  E  F  G  H  I  J")
    for i in range(0,10):
        # Print ship name on even row
        if (i % 2 == 0):
            print(f"{g.PLAYER}{g.ships_player[int(i / 2)].name.upper():15}", end="")
        # Print ship health on odd row
        else:
            print(f"  {g.PLAYER}Health {g.ships_player[int(i / 2)].hp}/{g.ships_player[int(i / 2)].max}"," " * 2, end = "")
        # A little bit of space between ship info and grid
        print(f"{i + 1:2} " , end = "")
        # Print colorcoded player grid
        for j in range(0,10):
            # Unify all the ships as same symbol, if position has a ship in it
            if g.grid_player[i * 10 + j].content in "ABCDE":
                position = f"{g.PLAYER}O"
            # If there has been a miss
            elif g.grid_player[i * 10 + j].content == "x":        
                position = f"{g.RESET}x"
            # If ship has been hit
            elif g.grid_player[i * 10 + j].content == "*":
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
            # Show unified ship positions only if show all is true, other wise replace with ocean
            if g.grid_computer[i * 10 + j].content in "ABCDE":
                if showall == True:
                    position = f"{g.COMPUTER}O"
                else:
                    position = f"{g.OCEAN} "    
            # If position has been hit and missed
            elif g.grid_computer[i * 10 + j].content == "x":        
                position = f"{g.RESET}x"
            # If ship found and hit
            elif g.grid_computer[i * 10 + j].content == "*":
                position = f"{g.HIT}*"
            # Rest is just ocean
            else:                
                position = f"{g.OCEAN} "    
            print(f"{g.OCEAN}[{position}{g.OCEAN}]", end = "")
        # Print computer ship names on even rows
        if (i % 2 == 0):
            print(f"  {g.COMPUTER}{g.ships_computer[int(i / 2)].name.upper():15}", end="")
        # Print computer ship health on odd rows
        else:
            if showall == True:
                print(f"    {g.COMPUTER}Health {g.ships_computer[int(i / 2)].hp}/{g.ships_computer[int(i / 2)].max}"," " * 2, end = "")        
        print(f"{g.RESET}")



# Place ships on map
def placeships(user):
    # Determine whose ships are we placing
    if user == "computer":
        grid = g.grid_computer
        ships = g.ships_computer
    else:
        grid = g.grid_player
        ships = g.ships_player
    # Needed lists
    possibility = []    # Growing list of possible locations
    suggestions = []    # If possible location is valid, it will be transferred to suggestions
    placeship = []      # From suggestions, one suggestion will be chosen and ship is placed 
    # Go through all the ships
    for ship in ships:
        # Need to go through as many times as it takes to place the current ship
        placement = False
        while placement == False:                        
            # Get random position for computer or ask for position from player with subfunction
            position = get_position(user)                                        
            # Now we loop through all possible directions to find if placement is possible
            for direction in range(0,4):
                # To preserve the original position, use temp variable to do calculations
                temp = position
                # Need to loop through the whole ship length
                for length in range(0,ship.hp):               
                    # If temp-value is out of bounds, no need to go further with checks
                    if temp > 99 or temp < 0:
                        break            
                    # If neighboring positions make placement invalid, break out
                    if (grid[temp].checkplacement(user) == False):
                        break
                    # This position is fine, add it to the possibility list
                    possibility.append(temp)
                    # Move to the next location 
                    if direction == 0:
                        # Going north, unless it is invalid position
                        if grid[temp].north == -1:
                            break
                        temp -= 10
                    elif direction == 1:
                        # Going south, unless it is invalid position
                        if grid[temp].south == -1:
                            break
                        temp += 10
                    elif direction == 2:
                        # Going west, unless it is invalid position
                        if grid[temp].west == -1:
                            break
                        temp -= 1
                    else:
                        # Going east, unless it is invalid position
                        if grid[temp].east == -1:
                            break
                        temp += 1
                # Now that we have reached this point, ensure that possibility list has enough positions
                if len(possibility) == ship.hp:
                    # Possibility list is ok, add it to suggestions
                    suggestions.append(possibility)
                # Reset possibility list for the next round
                possibility = []        
            # Now that we have gone through all possibilities, check if there are any listed on suggestions list
            if len(suggestions) != 0:
                # Randomly select one possibility for computer or ask from player to choose, needs to get list of grid positions
                placeship = ship_placement(user, suggestions)
                # Insert ship to the valid grid positions
                for i in placeship:                                
                    grid[i].changecontent(ship.grid)
                # Ship has been placed, clear suggestions list for the next round and go to next ship placement
                suggestions = []    
                placement = True
                if user == "player":
                    showmap(g.DEBUG)
                    print(f"\n{g.PLAYER}Your {ship.name} has been placed.{g.RESET}")
            # No possible placement, computer will try again and for player, print error message to inform
            else:
                if user == "player":
                    errormsg("Unfortunately, this ship cannot be placed on this location")


# Get_position subfunction returns valid position for starting point to placeships function
def get_position(user):
    valid = 0
    value = 0
    # For computer return random map position
    if user == "computer":
        value = randint(0,99)
    # Otherwise ask player to provide map coordinate
    else:
        # Check for options for quitting, showing map or coordinate
        while valid == 0:
            print("\nPlease, select starting point:")
            position = input("> ").casefold()
            # Player wants to quit
            if position in ["q", "quit", "(q)", "(q)uit"]:
                endgame()
            # Player wants to see the map
            elif position in ["m", "map", "(m)", "(m)ap"]:
                showmap(g.DEBUG)
                continue
            # Player made invalid choice
            elif position not in g.map_grid:                
                errormsg("Invalid start point, please give a valid map coordinate")
                continue
            else:
                # Convert map coordinate to grid position
                value = g.map_grid[position]
                # Exit loop
                valid = 1
    print("value: ", value)
    return value


# Ship_placement option goes through a list of suggested locations and returns one them
def ship_placement(user, suggestions):
    # Initialize 
    value = []    
    endpoint = "" 
    valid = 0
    # Select random suggestion for computer
    if user == "computer":
        rand = randint(0,len(suggestions) - 1) 
        value = suggestions[rand]
    # Ask for correct suggestion from player
    else:
        # Loop until valid choice has been made
        while valid == 0:            
            # Get list of valid endpoint options
            print("\nSelect end point or (C)ancel")
            # Loop through suggestions and provide endpoint options
            test = -1
            for i in suggestions: 
                if test != i[-1]:
                    print(f"\t{g.map_coordinate[i[-1]].upper()}",end = "")
                    test = i[-1]
            endpoint = input("\n> ").casefold()
            # If player wants to cancel this position
            if endpoint in ["c", "cancel", "(c)", "(c)ancel"]:
                break
            elif endpoint not in g.map_grid:
                errormsg("Invalid end point, please give a valid map coordinate")
                continue
            else:
                for i in suggestions:                    
                    if i[-1] == g.map_grid[endpoint]:
                        value = i
                        valid = 1
                        break
    return value


# Print out error message
def errormsg(msg):
    print(f"ERROR! {msg}") 
    print("Or to see grids, write (M)ap")
    print("Or you can always stop playing by writing (Q)uit")   


# Exit game
def endgame():
    showmap(True)
    print("\nThank you for playing!\n")
    exit()    
