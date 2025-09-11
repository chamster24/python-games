#Battleship Version 1.0.0, poor bot AI.

import time, sys, random

STRIKET = "\033[9m"
CLEARSCREEN = "\033[2J\033[H"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def printboard(board):
    """Prints the game board with coordinates."""
    print("  1 2 3 4 5 6 7 8 9 10")
    for i, row in enumerate(board):
        # Print the row letter (A, B, C...)
        print(f"{chr(65 + i)} {' '.join(row)}")

def getpossiblerotations(start_coords, ship_length):
    """Gets possible rotations for a ship at a given coordinate."""
    try:
        # Convert the coordinate (e.g., "A5") to a row and column index (e.g., 0, 4)
        row = ord(start_coords[0].upper()) - ord('A')
        col = int(start_coords[1:]) - 1
    except (ValueError, IndexError):
        return []
    # Map rotation names to their row/col changes
    rotations = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    possible = [
        name for name, (dr, dc) in rotations.items()
        if 0 <= row + dr * (ship_length - 1) < 10 and 0 <= col + dc * (ship_length - 1) < 10
    ]
    return possible

def manualshipplacement():
    """Manually places a player's ships on the board."""
    global playergrid
    ships = ["Aircraft Carrier (5)", "Battleship (4)", "Cruiser (3)", "Submarine (3)", "Destroyer (2)"]
    placedships = []
    playergrid = []
    for i in range(10): #fills playergrid into empty
        playergrid.append([])
        for x in range(10):
            playergrid[i].append(".")
            
    while True:
        if len(placedships) == 5:
            break
        print(f"{CLEARSCREEN}- SHIP PLACEMENT -\n")
        printboard(playergrid)
        for ship in ships:
            if ship in placedships:
                print(f"{STRIKET}{ships.index(ship) + 1}. {ship}{RESET}")
            else:
                print(f"{ships.index(ship) + 1}. {ship}")
        userinput = getinput("Select a ship to place by it's number:")
        while True:
            if userinput.isnumeric(): #checks for number
                if int(userinput) >= 1 and int(userinput) <= 5: #checks for valid number
                    if ships[int(userinput) - 1] in placedships: #checks for already placedships
                        print("Ship already placed. Please select a different ship.")
                    else:
                        selectedship = int(userinput) - 1
                        break
                else:
                    userinput = getinput("Invalid number. Please try again.")
            else:
                userinput = getinput("Invalid input. Please try again.")
        print(f"{CLEARSCREEN}- SHIP PLACEMENT -\nPlacing ship: {ships[selectedship]}")
        printboard(playergrid)
        # Coordinate and rotation placement loop
        while True:
            print(f"{CLEARSCREEN}- SHIP PLACEMENT -\nPlacing ship: {ships[selectedship]}")
            printboard(playergrid)
            
            # Get starting coordinate
            userinput = getinput(f"Select the starting cordinate for {ships[selectedship]} (e.g., A5) or type 'RESET':")
            if userinput.lower() == "reset":
                # Clear all placed ships and reset the board
                placedships = []
                playergrid = []
                for i in range(10):
                    playergrid.append([])
                    for x in range(10):
                        playergrid[i].append(".")
                # Return to the start of manualshipplacement()
                return

            # Get all possible rotations for the coordinate
            ship_name = ships[selectedship]
            ship_length = int(ship_name.split("(")[1].strip(")"))
            
            possible_rotations = getpossiblerotations(userinput, ship_length)
            
            if not possible_rotations:
                print("Invalid coordinate. No rotations possible from here.")
                continue # Go back to the coordinate input prompt

            # Set a starting rotation and enter a new loop for rotation
            current_rotation_index = 0
            if "down" in possible_rotations:
                current_rotation_index = possible_rotations.index("down")

            while True:
                current_rotation = possible_rotations[current_rotation_index]
                
                # Create a temporary copy of the board to draw the preview on
                temp_board = [row[:] for row in playergrid]
                is_valid_placement = True

                # Get the row and col from the coordinate
                try:
                    row = ord(userinput[0].upper()) - ord('A')
                    col = int(userinput[1:]) - 1
                except (ValueError, IndexError):
                    is_valid_placement = False
                
                # Get the row/col changes for the current rotation
                rotations = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
                dr, dc = rotations[current_rotation]

                # Check and draw each part of the ship
                for i in range(ship_length):
                    current_row = row + dr * i
                    current_col = col + dc * i

                    if not (0 <= current_row < 10 and 0 <= current_col < 10) or playergrid[current_row][current_col] == '#':
                        is_valid_placement = False
                    
                    try:
                        # Draw the temporary ship on the board
                        if is_valid_placement:
                            temp_board[current_row][current_col] = f"{GREEN}█{RESET}"
                        else:
                            temp_board[current_row][current_col] = f"{RED}█{RESET}"
                    except IndexError:
                        pass # Ignore attempts to color out of bounds

                print(f"{CLEARSCREEN}- SHIP PLACEMENT -\nPlacing ship: {ships[selectedship]}")
                printboard(temp_board)
                print(f"Current rotation: {current_rotation}")

                user_choice = getinput("Press 'r' to rotate or Enter to confirm placement.")
                
                if user_choice.lower() == 'r':
                    current_rotation_index = (current_rotation_index + 1) % len(possible_rotations)
                else:
                    if is_valid_placement:
                        # Place the ship permanently
                        for i in range(ship_length):
                            current_row = row + dr * i
                            current_col = col + dc * i
                            playergrid[current_row][current_col] = '#'
                        
                        # Add the placed ship to the list and break out of the inner loop
                        placedships.append(ships[selectedship])
                        break
                    else:
                        print("Invalid placement. Please rotate or choose a new starting coordinate.")
                        break # Break out of the rotation loop to re-prompt for coordinates
            
            # If the ship was successfully placed, break out of the coordinate loop
            if ships[selectedship] in placedships:
                break

def autoshipplacement(user):
    """Automatically places ships for a player."""
    # Define ships
    ships_to_place = [
        {'name': 'Carrier', 'size': 5, 'coordinates': []},
        {'name': 'Battleship', 'size': 4, 'coordinates': []},
        {'name': 'Cruiser', 'size': 3, 'coordinates': []},
        {'name': 'Submarine', 'size': 3, 'coordinates': []},
        {'name': 'Destroyer', 'size': 2, 'coordinates': []}
    ]

    board = [["." for _ in range(10)] for _ in range(10)]
    ships_list = [ship.copy() for ship in ships_to_place]

    for ship in ships_list:
        while True:
            # Randomly select a starting coordinate and orientation
            direction = random.choice(["horizontal", "vertical"])
            row = random.randint(0, 9)
            col = random.randint(0, 9)

            # Check if the ship fits on the board
            if direction == "horizontal" and col + ship['size'] > 10:
                continue
            if direction == "vertical" and row + ship['size'] > 10:
                continue

            # Check for overlaps
            overlap = False
            ship['coordinates'] = []
            if direction == "horizontal":
                for i in range(ship['size']):
                    if board[row][col + i] == '#':
                        overlap = True
                        break
                    ship['coordinates'].append([row, col + i, 0])
            else:
                for i in range(ship['size']):
                    if board[row + i][col] == '#':
                        overlap = True
                        break
                    ship['coordinates'].append([row + i, col, 0])

            if not overlap:
                # Place the ship on the board
                for r, c, h in ship['coordinates']:
                    board[r][c] = '#'
                break
    return board, ships_list

def getinput(prompt): #REPLACES input()    managing fullquits
    """Gets user input while checking for quit commands."""
    while True:
        userinput = input(prompt)
        checkinput = userinput
        if checkinput.lower() == "quit":
            checkinput = input("Are you sure you want to quit? If so, type \"yes\"").lower()
            if checkinput == "yes":
                print("Exiting program...\n\nExitcode 7: Mid-program exit")
                sys.exit(7)
            else:
                userinput = input("Please reenter your command, as you have chosen not to quit the program.")
                return userinput
        elif checkinput.lower() == "forcequit" or checkinput.lower() == "fullquit":
            print("\nExitcode 8: Force-quit")
            sys.exit(8)
        else:
            return userinput

# --- Main Game Sequence ---

print("d8888b.  .d8b.  d888888b d888888b db      d88888b .d8888. db   db d888888b d8888b. \n88  `8D d8' `8b `~~88~~' `~~88~~' 88      88'     88'  YP 88   88   `88'   88  `8D \n88oooY' 88ooo88    88       88    88      88ooooo `8bo.   88ooo88    88    88oodD' \n88~~~b. 88~~~88    88       88    88      88~~~~~   `Y8b. 88~~~88    88    88~~~   \n88   8D 88   88    88       88    88booo. 88.     db   8D 88   88   .88.   88      \nY8888P' YP   YP    YP       YP    Y88888P Y88888P `8888Y' YP   YP Y888888P 88")
input("\n BATTLESHIP - Press ANY KEY to Play:")

while True:
    userinput = getinput(f"{CLEARSCREEN}BATTLESHIP\n\n- MENU -\n\n1. Play against BOT\n\n Please select an option: (Type \"quit\" at any time to quit.)")
    if userinput == "1":
        gamemode = 1
        print("Selected: Match against BOT.")
        time.sleep(1)
        break
    else:
        print("Invalid option.")
        time.sleep(1)

# Ship placement selection screen
userinput = getinput(f"{CLEARSCREEN}Option selection: Press 1 to automate your ship placement, and any other key to place your ships manually.")
if userinput == "1":
    playergrid, player_ships = autoshipplacement("player")
else:
    manualshipplacement()

# Create boards and ships for the bot
botgrid, bot_ships = autoshipplacement("bot")

# --- Main Game Loop ---
print("BATTLESHIP - Ships Set Up. May the games begin!")
playerdefendgrid = [row[:] for row in playergrid]
botdefendgrid = [["." for _ in range(10)] for _ in range(10)]

time.sleep(2)
turn = 1
while True:  # main game loop
    # Player's turn
    if turn % 2 == 1:
        print(f"{CLEARSCREEN}Your board:")
        printboard(playerdefendgrid)
        print("\nOpponent's board:")
        printboard(botdefendgrid)

        # Coordinate validation and wasted shot check loop
        while True:
            userinput = getinput("\nIt's your turn. Select a coordinate to attack. ")
            try:
                row = ord(userinput[0].upper()) - ord('A')
                col = int(userinput[1:]) - 1

                if not (0 <= row <= 9 and 0 <= col <= 9):
                    print("Invalid input. Please try again.")
                    continue
                if botdefendgrid[row][col] != ".":
                    print("You already fired at that spot! Try again.")
                    continue
                else:
                    break
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        # Hit or miss logic
        if botgrid[row][col] == "#":
            botdefendgrid[row][col] = "X"
            print(f"\n{GREEN}HIT!{RESET}")
            for ship in bot_ships:
                is_hit = False
                for coord in ship['coordinates']:
                    if coord[0] == row and coord[1] == col:
                        coord[2] = 1
                        is_hit = True
                        if all(c[2] == 1 for c in ship['coordinates']):
                            print(f"{GREEN}You sank the opponent's {ship['name']}!{RESET}")
                            for c in ship['coordinates']:
                                botdefendgrid[c[0]][c[1]] = f"{RED}█{RESET}"
                        break
                if is_hit:
                    break

            # Check for a win
            if all(all(c[2] == 1 for c in ship['coordinates']) for ship in bot_ships):
                print(f"{CLEARSCREEN}{GREEN}CONGRATULATIONS! You have sunk all the opponent's ships! You win!{RESET}")
                print("\nOpponent's board:")
                printboard(botdefendgrid)
                input("\n\nPress any key to exit:")
                quit()
        else:
            botdefendgrid[row][col] = "O"
            print(f"\n{RED}MISS!{RESET}")

        input("Press Enter to continue...")
        turn += 1

    else:  # Bot's turn
        print(f"\nIt's your opponent's turn.")
        time.sleep(1)

        # Bot shot logic
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if playerdefendgrid[row][col] == ".":
                break

        # Check for hit/miss
        if playergrid[row][col] == "#":
            playerdefendgrid[row][col] = "X"
            print(f"Opponent hit your ship at {chr(65 + row)}{col + 1}!")
            for ship in player_ships:
                is_hit = False
                for coord in ship['coordinates']:
                    if coord[0] == row and coord[1] == col:
                        coord[2] = 1
                        is_hit = True
                        if all(c[2] == 1 for c in ship['coordinates']):
                            print(f"{RED}Your {ship['name']} has been sunk!{RESET}")
                            for c in ship['coordinates']:
                                playerdefendgrid[c[0]][c[1]] = f"{RED}█{RESET}"
                        break
                if is_hit:
                    break
            
            # Check for a loss
            if all(all(c[2] == 1 for c in ship['coordinates']) for ship in player_ships):
                print(f"{CLEARSCREEN}{RED}All of your ships have been sunk! You lose!{RESET}")
                print("\nYour board:")
                printboard(playerdefendgrid)
                input("\n\nPress any key to exit:")
                quit()
        else:
            playerdefendgrid[row][col] = "O"
            print(f"Opponent missed at {chr(65 + row)}{col + 1}.")
            
        input("Press Enter to continue...")
        turn += 1
