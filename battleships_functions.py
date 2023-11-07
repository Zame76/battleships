# Import libraries and functions
from random import randint 
from battleships_interface import showmap, errormsg, endgame
import battleships_globals as g

# BATTLESHIPS_FUNCTIONS LIST:
#
# Function reset()                                  - rows: 44-72
#   - resets all the global variables for a new game
#
# Function placeships(user)                         - rows: 75-155
#   - places ships on the map   
#   - user is "computer" or "player"
#
#   Subfunction get_position(user)                  - rows: 158-187
#       - main function: placeships(user)
#       - get starting position for ship placement
#       - user is "computer" or "player"
#       - computer get's random position
#       - player gets to choose starting position
#   
#   Subfunction ship_placement(user, suggestions)   - rows: 190-273
#       - main function: placeships(user)
#       - returns list of valid ship placement positions
#       - user is "computer" or "player"
#       - suggestions is list of possible placement suggestions lists
#       - computer chooses one suggestion randomly from the list
#       - player is shown possible directions for the ship to choose from
#
# Function turn_computer()                          - rows: 276-361
#   - handles computer targeting
#   - list_targets set contains all the positions that are priorized for the next shot
#   - list_hit set contains all the current target ship positions that have already been hit
#   - uses shadow map, which contains all map positions
#       - after computer has made shot, target position will be removed from map
#       - also when computer determines the direction of the ship hit, removes all invalid positions around it
# 
# Function turn_player(msg = "")                    - rows: 364-415
#   - handles player's turn
#   - asks for target coordinate and checks the validity
#   - prints map with log and possible error messages for player to see


# Reset global variables
def reset():
    if g.rules == "modern":
        g.hp_player = 17
        g.hp_computer = 17
        # Ship hitpoints
        g.hp_carrier = 5
        g.hp_battleship = 4
        g.hp_cruiser = 3
        g.hp_submarine = 3
        g.hp_destroyer = 2
    else:
        g.hp_player = 15
        g.hp_computer = 15
        # Ship hitpoints
        g.hp_carrier = 5
        g.hp_battleship = 4
        g.hp_cruiser = 3
        g.hp_submarine = 2
        g.hp_destroyer = 1
    g.ships_player = []
    g.ships_computer = []
    g.grid_player = []
    g.grid_computer = []
    g.shadow_map = set()
    g.list_targets = set()
    g.list_hit = []
    g.counter = 0
    g.log = []


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
                if placeship == False:
                    suggestions = []
                    continue
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
    endpoint = " " 
    valid = 0    
    # Select random suggestion for computer
    if user == "computer":
        rand = randint(0,len(suggestions) - 1) 
        value = suggestions[rand]
    # Ask for correct suggestion from player
    else:        
        # Loop until valid choice has been made
        while valid == 0:
            # Player has cancelled ship placement, return the get new starting position                                
            if endpoint == "c":                                  
                 value = False
                 break            
            # Reset directional lists
            n = []
            s = []
            w = []
            e = []       
            # If ship size is 1 (ie. first entry in list is same as last entry), no direction can be used, so ask player to press enter     
            if suggestions[0] == suggestions[-1]:
                print("\tPress Enter to accept placement or (C)ancel")
            # Ship has clear start and end, so provide list of choices
            else:
                print("\nSelect end point or (C)ancel")            
            # Loop through suggestions and provide endpoint options
            for suggestion in suggestions:                                
                # If suggestion has only one item, grab it and break from loop
                if len(suggestion) == 1:                    
                    e = suggestion
                    break
                # Otherwise, check for possible directions 
                else:
                    # North direction
                    if suggestion[0] - 10 == suggestion[1]:
                        print("\t(N)orth",end = "")
                        n = suggestion                        
                    # South direction
                    if suggestion[0] + 10 == suggestion[1]:
                        print("\t(S)outh",end = "")
                        s = suggestion
                    # West direction
                    if suggestion[0] - 1 == suggestion[1]:
                        print("\t(W)est",end = "")
                        w = suggestion
                    # East direction
                    if suggestion[0] + 1 == suggestion[1]:
                        print("\t(E)ast",end = "")                    
                        e = suggestion            
            # Possible direction options are shown, ask player to select one
            while endpoint not in ["c", "n", "s", "w", "e"]:                               
                endpoint = input("\n> ").casefold()
                # If player wants to cancel this placement
                if endpoint in ["c", "cancel", "(c)", "(c)ancel"]:
                    endpoint = "c"
                    break                                
                # If player selects north and it is valid direction
                elif endpoint in ["n", "(n)", "north", "(n)orth"] and len(n) > 0:
                    endpoint = "n"
                    value = n
                # If player selects south and it is valid direction
                elif endpoint in ["s", "(s)", "south", "(s)outh"] and len(s) > 0:
                    endpoint = "s"
                    value = s
                # If player selects west and it is valid direction
                elif endpoint in ["w", "(w)", "west", "(w)est"] and len(w) > 0:
                    endpoint = "w"
                    value = w
                # If player selects east and it is valid direction                    
                elif endpoint in ["e", "(e)", "east", "(e)ast", ""] and len(e) > 0:
                    endpoint = "e"                    
                    value = e           
                # Got invalid direction, print error and ask again
                else:
                    errormsg("Invalid direction, please give a valid direction")
                    continue                            
                # If valid choices have been made, exit question loop
                valid = 1
    # Return chosen position list for actual ship placement
    return value


# Handle computers turn
def turn_computer():
    complete = 0    
    while complete == 0:
        # If target list is empty, get random target from shadow_map
        if len(g.list_targets) == 0:
            target = list(g.shadow_map)[randint(0,len(g.shadow_map) - 1)]
        else:                
            # If there more than one hits on the same ship, clean up target list
            if len(g.list_hit) > 1:
                # Get direction of ship
                temp = g.list_hit[0] - g.list_hit[1]                
                if temp in [1, -1]:
                    # East west ship
                    for i in g.list_hit:
                        # Remove possible north and south locations from target list
                        if g.grid_player[i].north != -1:
                            # Remove north location from shadow map and target list
                            g.shadow_map.discard(g.grid_player[i].north)                            
                            g.list_targets.discard(g.grid_player[i].north)                                
                        if g.grid_player[i].south != -1:
                            # Remove south location from shadow map and target list
                            g.shadow_map.discard(g.grid_player[i].south)                            
                            g.list_targets.discard(g.grid_player[i].south)  
                else:
                    # North south ship
                    for i in g.list_hit:
                        if g.grid_player[i].west != -1:
                            # Remove west location from shadow map and target list
                            g.shadow_map.discard(g.grid_player[i].west)
                            g.list_targets.discard(g.grid_player[i].west)
                        if g.grid_player[i].east != -1:
                            # Remove east location from shadow map and target list
                            g.shadow_map.discard(g.grid_player[i].east)
                            g.list_targets.discard(g.grid_player[i].east)                                
            # Select random target from list of targets
            rand = randint(0, len(g.list_targets) - 1)
            target = list(g.list_targets)[rand]
        gridpos = g.grid_player[target].gothit("player")
        # If not a valid target, try again
        if gridpos == False:            
            continue
        else:
            # Remove location from shadow_map, so computer will not try to randomly hit it again
            g.shadow_map.discard(target)
            # If shot hit
            if g.grid_player[target].content == "*":
                for ship in g.ships_player:
                    if ship.grid == gridpos:
                        msg = f"{g.COMPUTER}Computer hit your {g.PLAYER}{ship.name}{g.COMPUTER} at {g.map_coordinate[target].upper()}{g.RESET}"
                # Mark location it in list_hit
                g.list_hit.append(target)                
                # Remove location from targets                
                g.list_targets.discard(target)
                # Add adjacent locations to target list if they are valid                    
                directions = [g.grid_player[target].north, g.grid_player[target].south, g.grid_player[target].west, g.grid_player[target].east]
                for dir in directions:
                    # If position in this direction is valid and is marked as an ocean or as a ship 
                    if dir != -1 and dir not in g.list_targets and g.grid_player[dir].content in " ABCDE":
                        g.list_targets.add(dir)
                # Check if target has been destroyed (WRONG POSITION, THIS CONTENT IS ALREADY * AT THIS POINT)                                  
                for ship in g.ships_player:
                    if ship.grid == gridpos and ship.hp == 0:
                        # Player ship has been destroyed
                        msg += f" {g.COMPUTER}and {g.HIT}destroyed{g.COMPUTER} your {g.PLAYER}{ship.name}{g.RESET}"
                        # Empty target list
                        g.list_targets = set()
                        # Need to loop through list_hit and mark appropriate directions from there to invalid spots
                        for target in g.list_hit:
                            directions = [g.grid_player[target].north, g.grid_player[target].south, g.grid_player[target].west, g.grid_player[target].east]
                            for dir in directions:
                                # If direction is valid and marked as ocean, remove value from shadow map
                                if dir != -1 and g.grid_player[dir].content == " ":
                                    g.shadow_map.discard(dir)
                        # Reset hit list for the next hit
                        g.list_hit = []
                
            # If shot missed 
            else:                
                # If target is in target list, remove target from the list                
                g.list_targets.discard(target)
                msg = f"{g.COMPUTER}Computer missed at {g.map_coordinate[target].upper()}{g.RESET}"
            complete = 1
            g.counter += 1
            g.log.append(msg)
            return msg
              

# Handle players turn
def turn_player(msg = ""):
    value = False
    # Print map to show player what's happening
    showmap(g.DEBUG)  
    # If player made invalid input in earlier iteration, show error      
    if msg == "error":
        errormsg("Invalid target, please give a valid map coordinate")
    # Ask for target coordinate
    print("Please enter target coordinate, (Q)uit or (M)ap")
    target = input("> ").casefold()
    # If player wants to quit
    if target in ["q", "quit", "(q)", "(q)uit"]:
        endgame()
    # If player wants to see map
    elif target in ["m", "map", "(m)", "(m)ap"]:
        showmap(g.DEBUG)
        value = False
    # if player made invalid choice
    elif target not in g.map_grid:        
        value = "error"
    # So far so good, let's check the target
    else:    
        # Change target coordinate to grid position
        target = g.map_grid[target]
        # Check if player made a hit or miss
        test = g.grid_computer[target].gothit("computer")
        # If player shot a position that has already been shot
        if test == False:            
            value = "error"
        else:
            # Test has return value of true, which is a miss
            if test == True:
                # Prepare log message
                msg = f"{g.PLAYER}You missed at {g.map_coordinate[target].upper()}{g.RESET}"
            # Test has return value of ship grid id that got hit
            else:
                # Prepare log message
                msg = f"{g.PLAYER}You hit enemy ship at {g.map_coordinate[target].upper()}{g.RESET}"
                # Check if ship has been sunk
                for ship in g.ships_computer:
                    if ship.grid == test and ship.hp == 0:
                        # Ship destroyed, add this information to log message
                        msg += f" {g.PLAYER}and {g.HIT}destroyed {g.COMPUTER}{ship.name.capitalize()}{g.RESET}"
            # Increase turn count
            g.counter += 1
            # Write log entry
            g.log.append(msg)
            # Player turn is over, return true
            value = True    
    return value
