# BATTLESHIPS_GLOBALS
# Contains all the global variables to be used in the game
# Also has the color code constants
# Creates two dictionaries to map coordinates to grid positions and vice versa 

# Change this to true to see everything on maps during game play
DEBUG = True

# Default rules, modern is default, traditional is the othe options
rules = "modern"

# Hitpoints
hp_player = 17
hp_computer = 17
# Ship hitpoints
hp_carrier = 5
hp_battleship = 4
hp_cruiser = 3
hp_submarine = 3
hp_destroyer = 2

# Lists to hold ship-objects
ships_computer = []
ships_player = []

# Lists to hold grid-objects
grid_player = []
grid_computer = []

# Lists to aid in computer targeting
shadow_map = set()
list_targets = set()
list_hit = []

# Turn-counter and -log
counter = 0
log = []

# Color coding: (search for ANSI color codes)
HIT       = "\033[1;31m" # red 
OCEAN     = "\033[1;34m" # blue
COMPUTER  = "\033[1;36m" # cyan
PLAYER    = "\033[1;32m" # green
WHITE     = "\033[1;37m" # white
RESET     = "\033[0;0m"  # reset to default


# Create dictionarys to map coordinates to corresponding gridpoints and vice versa
map_grid = {}
map_coordinate = {}
k = 0
for i in range(1, 11):
    for j in "abcdefghij":
        map_grid[j + str(i)] = k
        map_coordinate[k] = j + str(i)
        k += 1
# Result of these will handle this
#    A  B  C  D  E  F  G  H  I  J
# 1  00 01 02 03 04 05 06 07 08 09
# 2  10 11 12 13 14 15 16 17 18 19
# 3  20 21 22 23 24 25 26 27 28 29
# 4  30 31 32 33 34 35 36 37 38 39
# 5  40 41 42 43 44 45 46 47 48 49
# 6  50 51 52 53 54 55 56 57 58 59
# 7  60 61 62 63 64 65 66 67 68 69
# 8  70 71 72 73 74 75 76 77 78 79
# 9  80 81 82 83 84 85 86 87 88 89
# 10 90 91 92 93 94 95 96 97 98 99
