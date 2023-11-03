
from random import randint 
from battleships_interface import showmap, errormsg, endgame
import battleships_globals as g



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


# Handle computers turn
def turn_computer():
    complete = 0    
    while complete == 0:
        # If target list is empty, get random target
        if len(g.list_targets) == 0:
            target = randint(0,99)
        else:                
            # If there more than one hits on the same ship, clear up target list
            if len(g.list_hit) > 1:
                # Get direction of ship
                temp = g.list_hit[0] - g.list_hit[1]
                if temp < 0:
                    temp *= -1
                if temp == 1:
                    # East west ship
                    for i in g.list_hit:
                        # Remove possible north and south locations from target list
                        if g.grid_player[i].north != -1:
                            if g.grid_player[i].north in g.list_targets:
                                g.list_targets.remove(g.grid_player[i].north)                                
                        if g.grid_player[i].south != -1:
                            if g.grid_player[i].south in g.list_targets:
                                g.list_targets.remove(g.grid_player[i].south)                                
                else:
                    # North south ship
                    for i in g.list_hit:
                        if g.grid_player[i].west != -1:
                            if g.grid_player[i].west in g.list_targets:
                                g.list_targets.remove(g.grid_player[i].west)                                
                        if g.grid_player[i].east != -1:
                            if g.grid_player[i].east in g.list_targets:
                                g.list_targets.remove(g.grid_player[i].east)                                
            # Select random target from list of targets
            rand = randint(0, len(g.list_targets) - 1)
            target = g.list_targets[rand]
        gridpos = g.grid_player[target].gothit("player")
        if gridpos == False:
            # Not a valid target, try again
            continue
        else:
            # If shot hit
            if g.grid_player[target].content == "*":
                msg = f"Computer made a hit at {g.map_coordinate[target].upper()}"
                # Mark location it in list_hit
                g.list_hit.append(target)
                # Remove location from targets
                if target in g.list_targets:
                    g.list_targets.remove(target)
                # Add adjacent locations to target list if they are valid                    
                directions = [g.grid_player[target].north, g.grid_player[target].south, g.grid_player[target].west, g.grid_player[target].east]
                for dir in directions:
                    if dir != -1 and dir not in g.list_targets and g.grid_player[dir].content in " ABCDE":
                        g.list_targets.append(dir)
                # Check if target has been destroyed (WRONG POSITION, THIS CONTENT IS ALREADY * AT THIS POINT)                                  
                for ship in g.ships_player:
                    if ship.grid == gridpos and ship.hp == 0:
                        msg += f" and destroyed your {ship.name}"
                        g.list_targets = []
                        # Need to loop through list_hit and mark appropriate directions from there to invalid spots
                        for target in g.list_hit:
                            directions = [g.grid_player[target].north, g.grid_player[target].south, g.grid_player[target].west, g.grid_player[target].east]
                            for dir in directions:
                                if dir != -1 and g.grid_player[dir].content == " ":
                                    g.grid_player[dir].content = "i"
                        g.list_hit = []
                
            # If miss and target found in target list, target needs to be removed from list
            else:
                if target in g.list_targets:
                    g.list_targets.remove(target)
                msg = f"Computer missed at {g.map_coordinate[target].upper()}"
            complete = 1
            return msg
              

# Handle players turn
def turn_player(msg = ""):
    value = False
    showmap(g.DEBUG)  
    if msg != "":
        print(msg, "\n")             
    print("Please enter target coordinate, (Q)uit or (M)ap")
    target = input("> ").casefold()
    if target in ["q", "quit", "(q)", "(q)uit"]:
        endgame()
    elif target in ["m", "map", "(m)", "(m)ap"]:
        showmap(g.DEBUG)
        value = False
    elif target not in g.map_grid:
        errormsg("Invalid target, please give a valid map coordinate")
        value = False
    else:
        target = g.map_grid[target]
        test = g.grid_computer[target].gothit("computer")
        if test == False:
            errormsg("Invalid target, please give a valid map coordinate")
            value = False
        else:
            value = True
    return value
