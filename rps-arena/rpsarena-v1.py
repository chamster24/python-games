#Rock-Paper-Scissors Arena V1
import random
import time

P_Mwins, P_Rwins, OP_Mwins, OP_Rwins, currentmatch, currentround = 0, 0, 0, 0, 1, 1
options = ["rock", "paper", "scissors"]
winning_rules = {"rock": "scissors", "scissors": "paper", "paper": "rock"}

def matchsetup(): #setup for matches inside of tournament after the round setup to avoid conflict
    global matches
    userinput = input("\n Select the number of matches:")
    while True:
        if userinput.isnumeric() and userinput != "0":
            matches = int(userinput)
            print(f"Set to {matches} matches.")
            time.sleep(1)
            break
        else:
            userinput = input("That's not a valid number.")

def tournamentdisplay():
    global P_Rwins, OP_Rwins, P_Mwins, OP_Mwins, currentround, currentmatch
    if currentmatch > matches:
        if P_Mwins > OP_Mwins: #P wins round
            P_Rwins += 1
            print("You've won this round!")
        if P_Mwins < OP_Mwins: #BOT wins round
            OP_Rwins += 1
            print("You've lost this round.")
        if P_Mwins == OP_Mwins:
            print("You've tied, so we're leaving your victory to a coin flip...")
            time.sleep(0.5)
            if random.randint(1,2) == 1:
                print("And you've won the coin flip - and this round!")
                P_Rwins += 1
            else:
                print("You lost the coin flip - and this round.")
                OP_Rwins += 1
        currentmatch, P_Mwins, OP_Mwins, currentround = 1, 0, 0, currentround + 1
        time.sleep(1)
        
    if currentround > rounds:
        if P_Rwins > OP_Rwins: #P wins round
            print("\nAnd with that, you've won the game!")
            print(f"Final score: {P_Rwins}/{OP_Rwins}")
            time.sleep(3)
            quit()
        if P_Rwins < OP_Rwins: #BOT wins round
            print("\nAnd with that, you've lost the game.")
            print(f"Final score: {P_Rwins}/{OP_Rwins}")
            time.sleep(3)
            quit()
        if P_Rwins == OP_Rwins:
            print("\nYou ended up with a tie!")
            print(f"Final score: {P_Rwins}/{OP_Rwins}")
            time.sleep(3)
            quit()
        
    print(f"\n\nTOURNAMENT   Round {currentround}/{rounds}   Match {currentmatch}/{matches}")
    print(f"\nRound Wins: {P_Rwins} - {OP_Rwins}\nMatch Wins: {P_Mwins} - {OP_Mwins}")
    
def runmatch():
    global playeroption, userinput, currentround, currentmatch, P_Mwins, OP_Mwins
    userinput = input("\nSELECT RPS - TYPE THE FIRST LETTER, THE FULL WORD, OR THE CORRESPONDING NUMBER OF YOUR CHOICE")
    while True: #input check
        if userinput.isnumeric(): #Number check
            if int(userinput) > 0 and int(userinput) < 4: #within range
                playeroption = options[int(userinput) - 1]
                print(f"You've selected {playeroption.upper()}.")
                break
            else:
                userinput = input(f"\"{userinput}\" is not a valid numerical option. Please try again.")
        
        elif len(userinput) == 1 and not userinput.isnumeric(): #letter check
            validletters = {"r":"rock", "p":"paper", "s":"scissors"}
            if userinput.lower() in validletters:
                playeroption = validletters[userinput.lower()]
                print(f"You've selected {playeroption.upper()}.")
                break
            else:
                userinput = input(f"\"{userinput}\" is not a valid letter option. Please try again.")
        
        elif userinput.lower() in options: #word check
            playeroption = userinput.lower()
            print(f"You've selected {playeroption.upper()}.")
            break
        elif userinput.lower() == "exit":
            print("Exiting program...")
            quit()
        
        else: #failsafe
            userinput = input(f"\"{userinput}\" is not a valid option. Please try again.")
        
    time.sleep(1)
    botoption = options[random.randint(0,2)]
    print(f"\nBot picks {botoption.upper()}.")
    time.sleep(0.5)
    if playeroption == botoption:
        print("It's a tie! Both sides get 1 point.")
        P_Mwins += 1
        OP_Mwins += 1
        currentmatch += 1
    elif winning_rules[playeroption] == botoption:
        print(f"You win! {playeroption} beats {botoption}.")
        P_Mwins += 1
        currentmatch += 1
    else:
        print(f"You lose! {playeroption} was beaten by {botoption}.")
        OP_Mwins += 1
        currentmatch += 1
        
    input("Press any key to continue:")
    
    
    
    


userinput = input("Welcome to the Rock-Paper-Scissors Arena!\nPress 1 to play in a tournament, any other key to play casually, or \"exit\" to exit.")

if userinput == "1":
    gamemode = 1
elif userinput.lower() == "exit":
    print("We hope you enjoyed RPS Arena. Have a great day!")
    quit()
else:
    gamemode = 2
    currentmatch = 1
    currentround = 1


if gamemode == 1: # tournament setup
    userinput = input("\nTournament setup - press \"A\" to go with the regular setup (3 rounds of 5 matches).\n\nRounds: A series of matches where the winner of the most matches wins the round.\n Match: A single game of Rock-Paper-Scissors.\n\nSelect the number of rounds:")
    while True:
        if userinput.isnumeric() and userinput != "0":
            rounds = int(userinput)
            print(f"Set to {rounds} rounds.")
            time.sleep(1)
            matchsetup()
            currentmatch = 1
            currentround = 1
            break
        elif userinput.upper() == "A":
            rounds = 3
            matches = 5
            print(f"Set to {rounds} rounds and {matches} matches.")
            time.sleep(1)
            break
        else:
            userinput = input("That's not a valid number.")

while True:
    if gamemode == 1:
        tournamentdisplay()
    else:
        print(f"\nScore: {P_Mwins}/{OP_Mwins}     Type \"exit\" to exit.")
    runmatch()
