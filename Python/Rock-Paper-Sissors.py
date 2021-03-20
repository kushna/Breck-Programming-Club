import random

#Dictionary: will automatically change our number inputs to corresponding choice
game = {"1": "rock", "2": "paper", "3": "scissors"}

#defining our variables (start out with no wins or losses and 3 turns)
wins = 0
losses = 0
turns = 3

#tell user the rules
print("1 = rock, 2 = paper, 3 = scissors. Best of 3!")

#repeats until no turns are left
for i in range(turns):

    #user inputs choice
    play1 = input()

    #computer randomly chooses
    comp = game[str(random.randint(1,3))]

    #if the user types something other 1, 2, or 3, make them retry
    while play1 != "1" and play1 != "2" and play1 != "3":
        print("Please type in a '1,' '2,' or '3.'")
        play1 = input()

    #converts the user's input to corrresponding choice in our dictionary (ex. '1' changes to 'rock')          
    play = game[play1]

    #Tell user their choice, tell computer's choice,
    print("You: " + play)
    print("Computer: " + comp)

    #if user wins, tell them and add 1 to win variable
    if (play == "rock" and comp == "scissors") or (play == "paper" and comp == "rock") or (play == "scissors" and comp == "paper"): 
        print("You win!")
        wins = wins + 1

    #if user draws, tell them 
    elif play == comp:
        print("Draw")

    #if user loses, tell them and add 1 to lose variable            
    else:
        print("You lose")
        losses = losses + 1

    #for loop repeats
    

#tell user if they won and what the score was
if wins > losses:
    print("You Won " + str(wins) + " to " + str(losses) + "!")
if wins < losses:
    print("You Lost " + str(wins) + " to " + str(losses))
