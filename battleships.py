from random import randint

import battleships_globals as g
import battleships_functions as f

class gridPosition():    
    ocean = " "
    __ships = "ABCDE"
    __hit = "*"
    __miss = "x"
    def __init__(self, pos):
        self.content = self.ocean
        self.gridpos = pos
        # North position
        if self.gridpos - 10 < 0:
            self.north = -1
        else:
            self.north = pos - 10
        # South position
        if pos + 10 > 99:
            self.south = -1
        else:
            self.south = pos + 10
        # West position        
        if (pos - 1) % 10 == 9:
            self.west = -1            
        else:
            self.west = pos - 1             
        # East position
        if (pos + 1) % 10 == 0:
            self.east = -1            
        else:
            self.east = pos + 1  
    def changecontent(self, char):
        self.content = char
    def checkplacement(self, user):
        if user == "computer":
            grid = g.grid_computer
        else:
            grid = g.grid_player
        value = north = south = west = east = False
        if self.content == self.ocean:            
            if self.north == -1 or grid[self.north].content == self.ocean:
                north = True
            if self.south == -1 or grid[self.south].content == self.ocean:
                south = True
            if self.west == -1 or grid[self.west].content == self.ocean:
                west = True
            if self.east == -1 or grid[self.east].content == self.ocean:
                east = True
            if north == south == west == east == True:
                value = True
        return value
    def gothit(self, user):        
        if self.content in self.__ships:           
            if user == "computer":
                g.hp_computer -= 1
                for i in g.ships_computer:
                    if i.grid == self.content:
                        i.hp -= 1                        
            else:
                g.hp_player -= 1
                for i in g.ships_player:
                    if i.grid == self.content:
                        i.hp -= 1
            value = self.content                        
            self.content = self.__hit            
        elif self.content in self.ocean:
            self.content = self.__miss            
            value = True
        else:
            value = False
        return value

# define class Ship with all the necessary attributes
class Ship():
    def __init__(self, hp) -> None:
        self.hp = hp
        self.max = hp
        self.status = "active"
        match hp:
            case 5:
                self.name = "Carrier"
                self.grid = "A"
            case 4:
                self.name = "Battleship"
                self.grid = "B"
            case 3:
                self.name = "Cruiser"
                self.grid = "C"
            case 2:
                self.name = "Submarine"
                self.grid = "D"
            case 1:
                self.name = "Destroyer"
                self.grid = "E"
    def stats(self):
        print(self.name, self.grid, self.hp, self.status)
    def hit(self):
        self.hp -= 1
        if self.hp == 0:
            self.status = "destroyed"




# Create map grid for player and computer        
for i in range(0,100):    
    g.grid_player.append(gridPosition(i))
    g.grid_computer.append(gridPosition(i))

# Create ships for player and computer
for i in range(5, 0, -1):
    g.ships_player.append(Ship(i))
    g.ships_computer.append(Ship(i))

# Place computers ships
f.placeships("computer")

# Print map grids for player to see
f.showmap(g.DEBUG)

# Ask player to place ships
f.placeships("player")

# Coin flip to see who starts
print("All ships have been placed, battle is ready to begin!")
# Coin flip: 0 = Computer, 1 = Player
turn = randint(0, 1)
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
list_targets = []
list_hit = []
while victory == 0:
    # Computer's turn
    if turn == 0:
        complete = 0
        while complete == 0:
            # If target list is empty, get random target
            if len(list_targets) == 0:
                target = randint(0,99)
            else:                
                # If there more than one hits on the same ship, clear up target list
                if len(list_hit) > 1:
                    # Get direction of ship
                    temp = list_hit[0] - list_hit[1]
                    if temp < 0:
                        temp *= -1
                    if temp == 1:
                        # East west ship
                        for i in list_hit:
                            if g.grid_player[i].north != -1:
                                if g.grid_player[i].north in list_targets:
                                    list_targets.remove(g.grid_player[i].north)
                                if g.grid_player[g.grid_player[i].north] == " ":
                                    g.grid_player[g.grid_player[i].north].content = 'i'
                            if g.grid_player[i].south != -1:
                                if g.grid_player[i].south in list_targets:
                                    list_targets.remove(g.grid_player[i].south)
                                if g.grid_player[g.grid_player[i].south].content == " ":
                                    g.grid_player[g.grid_player[i].south].content = 'i'
                    else:
                        # North south ship
                        for i in list_hit:
                            if g.grid_player[i].west != -1:
                                if g.grid_player[i].west in list_targets:
                                    list_targets.remove(g.grid_player[i].west)
                                if g.grid_player[g.grid_player[i].west] == " ":
                                    g.grid_player[g.grid_player[i].west].content = 'i'
                            if g.grid_player[i].east != -1:
                                if g.grid_player[i].east in list_targets:
                                    list_targets.remove(g.grid_player[i].east)
                                if g.grid_player[g.grid_player[i].east].content == " ":
                                    g.grid_player[g.grid_player[i].east].content = 'i'                    

                # Select random target list of targets
                rand = randint(0, len(list_targets) - 1)
                target = list_targets[rand]
            gridpos = g.grid_player[target].gothit("player")
            if gridpos == False:
                # Not a valid target, try again
                continue
            else:
                if g.grid_player[target].content == "*":
                    # Something got hit
                    list_hit.append(target)
                    if target in list_targets:
                        list_targets.remove(target)
                    temp = g.grid_player[target].north
                    if temp != -1 and g.grid_player[temp].content in " ABCDE":
                        list_targets.append(temp)
                    temp = g.grid_player[target].south
                    if temp != -1 and g.grid_player[temp].content in " ABCDE":
                        list_targets.append(temp)
                    temp = g.grid_player[target].west
                    if temp != -1 and g.grid_player[temp].content in " ABCDE":
                        list_targets.append(temp)
                    temp = g.grid_player[target].east
                    if temp != -1 and g.grid_player[temp].content in " ABCDE":
                        list_targets.append(temp)
                    # Check if target has been destroyed (WRONG POSITION, THIS CONTENT IS ALREADY * AT THIS POINT)                                  
                    for i in g.ships_player:
                        if i.grid == gridpos and i.hp == 0:
                            list_targets = []
                            # Need to loop through list_hit and mark appropriate directions from there to invalid spots
                            list_hit = []                                              
                # If miss and target found in target list, target needs to be removed from list
                else:
                    if target in list_targets:
                        list_targets.remove(target)
                complete = 1        
        turn = 1
        if g.hp_player == 0:
            # Player wins
            victory = 1
            winner = "computer"
    # Player's turn
    else:
        f.showmap(g.DEBUG)
        print("list hit:", list_hit)
        print("list_targets:", list_targets)            
        print("Please enter target coordinate, (Q)uit or (M)ap")
        target = input("> ").casefold()
        if target in ["q", "quit", "(q)", "(q)uit"]:
            f.endgame()
        elif target in ["m", "map", "(m)", "(m)ap"]:
            f.showmap(g.DEBUG)
            continue
        elif target not in g.map_grid:
            f.errormsg("Invalid target, please give a valid map coordinate")
            continue
        else:
            target = g.map_grid[target]
            test = g.grid_computer[target].gothit("computer")
            if test == False:
                f.errormsg("Invalid target, please give a valid map coordinate")
                continue
            # f.showmap(g.DEBUG)            
            turn = 0
        if g.hp_computer == 0:
            # Player wins
            victory = 1
            winner = "player"