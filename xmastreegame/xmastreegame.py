import threading
import RPi.GPIO as GPIO
from time import sleep, time
from ThreadedTree import XmasTree
from random import getrandbits, randint
from os.path import isfile

#CONSTANTS
#leds
L0 = 1
L1 = 2
L2 = 4
L3 = 8
L4 = 16
L5 = 32
L6 = 64
ALL = 1+2+4+8+16+32+64
#leds as a list
LEDS = [L0,L1,L2,L3,L4,L5,L6]
#leds as a list descending down the tree
LEDSDESC = [L0,L6,L5,L4,L2,L1,L3]
#gpio pin the game button is connected too
P1GAMEBUTTONPIN = 4
#gpio pin the 2 player game button is connected too
P2GAMEBUTTONPIN = 22
#gpio pin which will cause the game to stop if trigger
STOPGAMEBUTTONPIN = 17


class TreeRandom(threading.Thread):
    def __init__(self, xmasTree):
        #setup threading
        threading.Thread.__init__(self)
        #setup properties
        self.stopped = False
        self.running = False
        self.xmasTree = xmasTree
        
    def run(self):
        self.running = True
        while not self.stopped:
            ledsToLight = 0
            #loop through all the lights, randomly pick which ones to light
            for led in LEDS:
                if getrandbits(1) == 1:
                    ledsToLight = ledsToLight + led
            #turn the leds on
            self.xmasTree.leds_on(ledsToLight)
            #delay
            sleep(1)
        #when its stopped turn the leds off
        self.xmasTree.leds_on(0)
        self.running = False

    def stop(self):
        #stop the animation
        self.stopped = True
        #wait for it to stop running
        while self.running:
            sleep(0.01)

class TreeGame():
    def __init__(self, xmasTree, scoresFile):
        self.scoresFile = scoresFile
        self.scores = self._loadScores()
        #print self.scores

    def play(self):
        #turn on all leds
        xmasTree.leds_on(ALL)
        #wait a bit
        sleep(2)
        #get a random number, which will be how many leds will be lit before the green one
        steps = randint(7,14)
        for step in range(0,steps):
            #light a random red led
            ledToLight = LEDS[randint(1,6)]
            xmasTree.leds_on(ledToLight)
            #wait for a random time between 0.5 and 1 second
            timeToSleep = randint(5,10) / 10.0
            sleep(timeToSleep)
        #light the green led
        xmasTree.leds_on(L0)
        #get the time
        startTime = time()
        #wait for button to be released (if its pressed)
        while(GPIO.input(P1GAMEBUTTONPIN) == 1):
            sleep(0.001)
        #wait for the button to be pressed
        while(GPIO.input(P1GAMEBUTTONPIN) == 0):
            sleep(0.001)
        #get the time
        endTime = time()
        timeDiff = endTime - startTime
        #put the score in the score list and find the position
        # loop through all the scores
        for score in range(0,len(self.scores)):
            # is this time less than the current score?
            if timeDiff < self.scores[score]:
                #record the players position
                position = score
                self.scores.insert(score,timeDiff)
                break
        #save to the score file
        self._saveScores()
        #flash the position
        self._displayPosition(position)

    def _displayPosition(self,position):
        #if there position was less than 6, flash it on the tree
        # else flash all the lights
        if position <= 6:
            ledToLight = LEDSDESC[position]
        else:
            ledToLight = ALL
        #flash the position
        for count in range(15):
            xmasTree.leds_on(ledToLight)
            sleep(0.2)
            xmasTree.leds_on(0)
            sleep(0.2)

    # load the scores files
    def _loadScores(self):
        scores = []
        #does the file exist?  If so open it
        if isfile(self.scoresFile):
            with open(self.scoresFile, "r") as file:
                for score in file:
                    scores.append(float(score))
        else:
            #no file so put an initial score which is massive
            scores.append(999)

        return scores

    # save the scores file
    def _saveScores(self):
        with open(self.scoresFile, "w") as file:
            for score in self.scores:
                file.write(str(score)+"\n")

class TreeGame2Player():
    def __init__(self, xmasTree):
        self.xmasTree = xmasTree

    def play(self):
        #turn on all leds
        xmasTree.leds_on(ALL)
        #wait a bit
        sleep(2)
        #get a random number, which will be how many leds will be lit before the green one
        steps = randint(7,14)
        for step in range(0,steps):
            #light a random red led
            ledToLight = LEDS[randint(1,6)]
            xmasTree.leds_on(ledToLight)
            #wait for a random time between 0.5 and 1 second
            timeToSleep = randint(5,10) / 10.0
            sleep(timeToSleep)
        #setup event detection
        self.player1ButtonPressed = False
        self.player2ButtonPressed = False
        GPIO.add_event_detect(P1GAMEBUTTONPIN, GPIO.RISING, callback=self._playerButtonCallback, bouncetime=200)
        GPIO.add_event_detect(P2GAMEBUTTONPIN, GPIO.RISING, callback=self._playerButtonCallback, bouncetime=200)
        #light the green led
        xmasTree.leds_on(L0)
        #wait for a button to be pressed
        while not self.player1ButtonPressed and not self.player2ButtonPressed:
            sleep(0.001)
        #remove event detection
        GPIO.remove_event_detect(P1GAMEBUTTONPIN)
        GPIO.remove_event_detect(P2GAMEBUTTONPIN)
        #who won? display right (1P) or left (2P) led 
        if self.player1ButtonPressed: ledToLight = L3
        if self.player2ButtonPressed: ledToLight = L1
        self._displayWinner(ledToLight)
        
    def _displayWinner(self,ledToLight):
        #flash the winner
        for count in range(15):
            xmasTree.leds_on(ledToLight)
            sleep(0.2)
            xmasTree.leds_on(0)
            sleep(0.2)
        
    def _playerButtonCallback(self, pin):
        #make sure the callback hasnt been called already?
        if not self.player1ButtonPressed and not self.player1ButtonPressed:
            #see which player got there first
            if pin == P1GAMEBUTTONPIN: self.player1ButtonPressed = True
            elif pin == P2GAMEBUTTONPIN: self.player2ButtonPressed = True

#main program
if __name__ == "__main__":

    #setup GPIO
    GPIO.setmode(GPIO.BCM)

    #setup the 1P game button
    GPIO.setup(P1GAMEBUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #setup the 2P game button
    GPIO.setup(P2GAMEBUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #setup the stop game button
    GPIO.setup(STOPGAMEBUTTONPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #create threaded tree object
    xmasTree = XmasTree()
    #start the xmas tree
    xmasTree.start()
    #create tree game oject
    treeGame = TreeGame(xmasTree, "scores.txt")
    #create 2 player tree game object
    treeGame2Player = TreeGame2Player(xmasTree)

    try:
        stopGame = False
        #loop until the stop game pin is set
        while(not stopGame):
            #run the xmas tree random animation
            treeRandom = TreeRandom(xmasTree)
            treeRandom.start()
            
            #wait until a button is pressed to either start a new game or stop the game
            while(GPIO.input(P1GAMEBUTTONPIN) == 0 and GPIO.input(P2GAMEBUTTONPIN) == 0 and GPIO.input(STOPGAMEBUTTONPIN) == 0):
                sleep(0.01)
            
            #new 1 player game
            if GPIO.input(P1GAMEBUTTONPIN) == 1:                
                #stop the animation
                treeRandom.stop()
                #run the game
                treeGame.play()
                #game over, start the animation again
                sleep(1)

            #new 2 player game
            if GPIO.input(P2GAMEBUTTONPIN) == 1:                
                #stop the animation
                treeRandom.stop()
                #run the game
                treeGame2Player.play()
                #game over, start the animation again
                sleep(1)

            #stop game
            elif GPIO.input(STOPGAMEBUTTONPIN) == 1:
                stopGame = True
        
    finally:
        #stop tree random animation
        treeRandom.stop()
        #stop xmas tree
        xmasTree.stop()
        #cleanup gpio
        GPIO.cleanup()
