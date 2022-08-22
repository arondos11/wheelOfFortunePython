from pickle import TRUE
import random
from threading import Timer
from config import finalPrize
from config import dictionaryLoc

class Player:
    def __init__(self, name, roundBank, totalBank, roundWin):
        self.name = name
        self.roundBank = roundBank
        self.totalBank = totalBank
        self.roundWin = roundWin

def gameSetup():
    global p1
    global p2
    global p3
    p1 = Player("Player 1", 0, 0, 0)
    p2 = Player("Player 2", 0, 0, 0)
    p3 = Player("Player 3", 0, 0, 0)

def buyVowel(playerTurn):
    if playerOrder[playerTurn].roundBank >= vowelCost:
        playerOrder[playerTurn].roundBank = playerOrder[playerTurn].roundBank - vowelCost
        vowelCheck = True
    else:
        vowelCheck = False
    return vowelCheck

def roundEnding():
    if p1.roundWin == 1:
        p1.totalBank = p1.roundBank + p1.totalBank
        p1.roundBank = 0
        p1.roundWin = 0
        p2.roundBank = 0
        p3.roundBank = 0
    elif p2.roundWin == 1:
        p2.totalBank = p2.roundBank + p2.totalBank
        p2.roundBank = 0
        p2.roundWin = 0
        p1.roundBank = 0
        p3.roundBank = 0
    else:
        p3.totalBank = p1.roundBank + p1.totalBank
        p3.roundBank = 0
        p3.roundWin = 0
        p1.roundBank = 0
        p2.roundBank = 0

def getWord():
    global correctWord
    global guessedLetters
    global correctLetters
    global unguessedLetters
    global vowels
    vowels = ['a', 'e', 'i', 'o', 'u']
    correctWord = random.choice(open(dictionaryLoc,"r").read().split())
    guessedLetters = set()
    correctLetters = set()
    for letter in correctWord:
        correctLetters.add(letter)
    unguessedLetters = correctLetters

def newRoundStart():
    global playerOrder
    startPlayer = random.randint(1,3)
    if startPlayer == 1:
        playerOrder = [p1, p2, p3]
        print("Welcome to Wheel of Fortune, Player 1 Starts")
    if startPlayer == 2:
        playerOrder = [p2, p3, p1]
        print("Welcome to Wheel of Fortune, Player 2 Starts")
    if startPlayer == 3:
        playerOrder = [p3, p1, p2]
        print("Welcome to Wheel of Fortune, Player 3 Starts")   
    getWord()

def wofRound():
    global vowelCost
    vowelCost = 250
    roundEnd = 0
    print("Make sure to use all lowercase")
    while roundEnd == 0:
        playerTurn = 0
        while playerTurn <= 2:
            if(set(unguessedLetters).issubset(set(vowels))):
                vowelCost = 0
            print(playerOrder[playerTurn].name + "'s Turn")
            currentState = ""
            for letter in correctWord:
                if letter in guessedLetters:
                    currentState += letter + " "
                else:
                    currentState += "_ "
            print(currentState)
            print("")

            spin = random.randint(1, 19)
            if spin == 1:
                playerOrder[playerTurn].roundBank = 0
                print(playerOrder[playerTurn].name + "Went Bankrupt, Next Players Turn")
                playerTurn = playerTurn + 1
            elif spin == 2:
                print(playerOrder[playerTurn].name + "Lost Their Turn, Next Players Turn")
                playerTurn = playerTurn + 1
            else:
                print(spin*100)
                guessedLetter = input("Guess a Letter, Vowels Cost $250, press 1 to guess the word")
                if guessedLetter.lower() in ('a', 'e', 'i', 'o', 'u'):
                    if buyVowel(playerTurn) == True:
                        if guessedLetter in correctLetters:
                            guessedLetters.add(guessedLetter)
                            unguessedLetters.remove(guessedLetter)
                            playerOrder[playerTurn].roundBank = playerOrder[playerTurn].roundBank + spin * 100
                        else:
                            print(playerOrder[playerTurn].name + "Guessed Incorrectly, Next Players Turn")
                            playerTurn = playerTurn + 1
                    else:
                            print("Not enough money, guess a consonant")
                elif guessedLetter == '1':
                    roundGuess = input("Enter Your Guess:")
                    if roundGuess == correctWord:
                        print(correctWord)
                        print("Congratulations, you win!")
                        playerOrder[playerTurn].roundWin = 1
                        roundEnding()
                        roundEnd = 1
                        break
                    else:
                        print("Incorrect Guess")
                        playerTurn = playerTurn + 1
                else:
                    if guessedLetter in correctLetters:
                        guessedLetters.add(guessedLetter)
                        unguessedLetters.remove(guessedLetter)
                        playerOrder[playerTurn].roundBank = playerOrder[playerTurn].roundBank + spin * 100
                    else:
                        print(playerOrder[playerTurn].name + "Guessed Incorrectly, Next Players Turn")
                        playerTurn = playerTurn + 1
                

def wofFinalRound():
    vowelCount = 0
    consonantCount = 0
    print("Final Round")
    print("Make sure to use all lowercase")
    if max(p1.totalBank, p2.totalBank, p3.totalBank) == p1.totalBank:
        print("Player 1 has the most money and will move on to the final round.")
    elif max(p1.totalBank, p2.totalBank, p3.totalBank) == p2.totalBank:
        print("Player 2 has the most money and will move on to the final round.")
    else:
        print("Player 3 has the most money and will move on to the final round.")
    print("The final contestant will be given a chance to guess 3 words and 1 vowel, and then 5 seconds to guess the full word.")
    getWord()
    if 'r' in correctLetters:
        guessedLetters.add('r')
    if 's' in correctLetters:
        guessedLetters.add('s')
    if 't' in correctLetters:
        guessedLetters.add('t')
    if 'l' in correctLetters:
        guessedLetters.add('l')
    if 'n' in correctLetters:
        guessedLetters.add('n')
    if 'e' in correctLetters:
        guessedLetters.add('e')
        
    while vowelCount == 0:
        currentState = ""
        for letter in correctWord:
            if letter in guessedLetters:
                currentState += letter + " "
            else:
                currentState += "_ "
        print(currentState)
        print("")
        guessedLetter = input("Guess a vowel")

        if guessedLetter.lower() in ('a', 'e', 'i', 'o', 'u'):
            if guessedLetter in correctLetters:
                guessedLetters.add(guessedLetter)
                vowelCount = vowelCount + 1
                print("Nice Guess!")
            else:
                vowelCount = vowelCount + 1
                print("Incorrect Guess")
        else:
            print("Not a vowel")
    while consonantCount < 3:
        currentState = ""
        for letter in correctWord:
            if letter in guessedLetters:
                currentState += letter + " "
            else:
                currentState += "_ "
        print(currentState)
        print("")
        guessedLetter = input("Guess 3 consonants")
        
        if guessedLetter.lower() in ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'):
            if guessedLetter in correctLetters:
                guessedLetters.add(guessedLetter)
                consonantCount = consonantCount + 1
                print("Nice Guess!")
            else:
                consonantCount = consonantCount + 1
                print("Incorrect Guess")
        else:
            print("Not a constant")
        if consonantCount == 3:
            currentState = ""
            for letter in correctWord:
                if letter in guessedLetters:
                    currentState += letter + " "
                else:
                    currentState += "_ "
            print(currentState)
            print("")

    print(currentState)

    timeout = 5
    t = Timer(timeout, print, ['Sorry, times up!'])
    t.start()
    finalGuess = input('Enter you final guess within 5 seconds!')
    t.cancel()
    if finalGuess == correctWord:
        print("Congratulations, you win the final round and " + finalPrize)
    else:
        print("You Lose.")


def main():
    gameSetup()    

    for i in range(0,3):
        if i in [0,1]:
            print("New Round")
            newRoundStart()
            wofRound()    
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    