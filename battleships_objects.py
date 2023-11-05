import battleships_globals as g

# Create map grip position object
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
                        i.hit()
            else:
                g.hp_player -= 1
                for i in g.ships_player:
                    if i.grid == self.content:
                        i.hit()
            value = self.content                        
            self.content = self.__hit            
        elif self.content in self.ocean:
            self.content = self.__miss            
            value = True
        else:
            value = False
        return value


# Create ship object
class Ship():
    def __init__(self, grid) -> None:
        self.status = "active"
        match grid:
            case "A":
                self.name = "Carrier"
                self.grid = "A"
                self.hp = g.hp_carrier
                self.max = g.hp_carrier
            case "B":
                self.name = "Battleship"
                self.grid = "B"
                self.hp = g.hp_battleship
                self.max = g.hp_battleship
            case "C":
                self.name = "Cruiser"
                self.grid = "C"
                self.hp = g.hp_cruiser
                self.max = g.hp_cruiser
            case "D":
                self.name = "Submarine"
                self.grid = "D"
                self.hp = g.hp_submarine
                self.max = g.hp_submarine
            case "E":
                self.name = "Destroyer"
                self.grid = "E"
                self.hp = g.hp_destroyer
                self.max = g.hp_destroyer
    def stats(self):
        print(self.name, self.grid, self.hp, self.status)
    def hit(self):
        self.hp -= 1
        if self.hp == 0:
            self.status = "destroyed"
