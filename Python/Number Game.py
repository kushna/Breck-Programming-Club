import random


guesses = 5
num = random.randint(0,100)
print("Guess the random number from 1-99! You have " + str(guesses) + " guesses")


while True:
    guess = int(input())

    if guess == num:
        print("You win!")
        win == 1
        break

    if guesses == 0:
        print("You've run out of guesses. The answer was " + str(num) + ".")
        break
    
    if guess > num:
        print("Too high. Guess again. You have " + str(guesses) + " guesses left")
    else:
        print("Too low. Guess again. You have " + str(guesses) + " guesses left")

    guesses = guesses - 1

    
