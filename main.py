'''
Anton Vannesjö Grupp 3
KTH

#168 minröjning

Beskrivning:
- En ny version på gamla MsRöj.
- Sparar spelardatan på en fil.
- Visar toplista.

Struktur:
1. Visar meny för att spela eller visa toplista
2. Vid nytt spel skapas en instans av klassen Player och Game
3. Användaren får välja storlek på plan och svårhetsnivå
4. En spelplan skapas och minor slumpas ut
5. Spelloopen består av att användaren får välja var denna vill röja en mina.
    Om en ruta med en mina väljs avslutas spelet och alla rutor visas.
    Användaren kan flagga positioner.
    Trycker användaren på en tom ruta öppnas alla andra tomma rutor som angränsar.
    Rutor med minor bredvid markeras med hur många minor som angränsar denna.
6. Tiden sparas till en fil och topplistan visas.
'''


# ORIGO TOP LEFT


import time
import random


# convert from sec to [min][sec]
def secToMin(sec):
    return [int(sec) // 60, int(sec%60)]


# ENABLE DEBUG True/False
DEBUG = False

# enable cheat (show mines) [bool]
CHEAT = False

# toplist file name
filenameTopList = "toplist.dat"

# save game file name
filenameSaveGame = "savegame.dat"

# define fixed board size [x: int][y: int]
size = [[7, 7],     # easy[0]
        [12, 15],   # medium [1]
        [15, 25]]   # hard [2]

# define fixed % of mines in decimal format [float]
difficulty =    [0.15,   #easy[0]
                0.25,    #medium [1]
                0.35]    #hard [2]


class Player:   # def player data (str, str)
    def __init__(self, name, age):
        self.__name = name  # [str]
        self.__age = age    # [str]

    # return instant variables
    def name(self):
        return self.__name

    def age(self):
        return self.__age

class Game:     # main game class
    # set size and difficulty
    def __init__(self, boardSize, difficulty):
        self.__size = boardSize  # list w/ two elements y and x size
        self.__percMines = difficulty

        # declare constants
        self.__EMPTY = False
        self.__ISMINE = True
        self.__HIDDEN = False
        self.__SHOWN = True
        self.__NOFLAG = False
        self.__FLAG = True

        # make empty game board
        self.__board = []   # [y][x][n] n=0: bool mine, n=1: bool show/hide,
                            # n=2: bool flagged, n=3: int mines around
        # end game if true
        self.__endGame = False

        # True if Victory
        self.__victory = False

        # game time
        self.__timeStart = 0
        self.__timeElapsed = 0

        # number of mines
        self.__mineCount = 0

        # number of flags
        self.__flagCount = 0

        # number of showned positions
        self.__shownCount = 0

        if DEBUG:
            self.__counter = 0

    # get elapsed time
    def getElapsedTime(self):
        return self.__timeElapsed

    # get number of mines
    def getMineCount(self):
        return self.__mineCount

    # get number of flags
    def getFlagCount(self):
        return self.__flagCount

    # get number of shown position
    def getShownCount(self):
        return self.__shownCount

    # get bool Victory
    def getVictory(self):
        return  self.__victory


    def makeGame(self):

        # generate array in three dimensions
        # board[y_cord][x_cord][status]

        # assign status: [EMPTY, HIDDEN, NOFLAG, 0]:
        for y in range(self.__size[0]):     # loop through size of x
            self.__board.append([])

            for x in range(self.__size[1]): # loop through size of y
                self.__board[y].append([])

                for z in range(4):          # loop through size of options per coordinate
                    self.__board[y][x].append([])

                # assign mines randomly
                if random.random() < self.__percMines:
                    self.__board[y][x][0] = True
                    self.__mineCount += 1
                else:
                    self.__board[y][x][0] = False
                self.__board[y][x][1] = self.__HIDDEN
                self.__board[y][x][2] = self.__NOFLAG
                self.__board[y][x][3] = 0   # 0 mines arround

        return

    # check for mines or mark nr of mines around
    def checkPosition(self, y, x):
        # check the given position and positions around for mines

        if DEBUG:
            self.__counter += 1
            print("131: iteration: ", self.__counter)
            print("132: Position: X: ", chr(ord('A')+x), " Y: ", y+1)
            self.printGame()

        # if already shown, return
        if self.__board[y][x][1] == self.__SHOWN:
            if DEBUG:
                print("138: Already shown!")
            return

        # mark position as shown
        self.__board[y][x][1] = self.__SHOWN
        self.__shownCount += 1

        # and remove flag
        if self.__board[y][x][2]:
            self.__board[y][x][2] = self.__NOFLAG
            self.__flagCount -= 1

        # if mine, return
        if self.__board[y][x][0] == self.__ISMINE:
            if DEBUG:
                print("137: ISMINE")
            return

        # check all directions and increase mineCount if mine found
        for i_y in range(-1, 2, 1):       # check -1, 0 +1 around y
            for i_x in range(-1, 2, 1):   # check -1, 0 +1 around x
                if DEBUG:
                    print("151: Check around for mines. x: ", i_x, ' y: ', i_y)
                # skipp if i_y, i_x == 0 or outside boarders
                if i_y == 0 and i_x == 0 or (y+i_y) < 0 or (x+i_x) < 0 or\
                        (y+i_y) > self.__size[0]-1 or (x+i_x) > self.__size[1]-1:
                    if DEBUG:
                        print("154: skipp y= 0, x= 0 or outside range, continue")
                    continue
                if self.__board[y+i_y][x+i_x][0] == self.__ISMINE:
                    if DEBUG:
                        print("158: MINE FOUND! increased counter.")
                    self.__board[y][x][3] += 1  # if mine, increase counter
                    if DEBUG:
                        print("Mines around: ", self.__board[y][x][3])

        # if bombs around, mark as shown and return
        if self.__board[y][x][3] > 0:
            if DEBUG:
                print("164: Bombs around, return")
            self.__board[y][x][1] = self.__SHOWN
            return

        # if no bombs around, repeat function for every position around
        else:
            for i_y in range(-1, 2, 1):       # check -1, 0 +1 around y
                for i_x in range(-1, 2, 1):     # check -1, 0 +1 around x
                    # skipp if i_y, i_x == 0 or outside boarders
                    if i_y == 0 and i_x == 0 or (y+i_y) < 0 or (x+i_x) < 0 or\
                            (y+i_y) > self.__size[0]-1 or (x+i_x) > self.__size[1]-1:
                        if DEBUG:
                            print("182: skipp y= 0, x= 0 or outside range, continue")
                        continue

                    if DEBUG:
                        print("186: next to check: ", end='')
                        # print or input
                        print(' x= '+chr(ord('A')+x+i_x)+' y= '+str(y+i_y+1))
                        print()
                        print()
                    self.checkPosition(y+i_y, x+i_x)
        return

    def printGame(self):
        # print game board, where it is shown

        # print space before labels for x-axis
        print("{:<5}".format(""), end='')

        # print labels for x-axis
        for x in range(len(self.__board[0])):
            print("{:<2}".format(chr(ord('A') + x)), end=' ')
        print()

        # print the rest of the board
        for y in range(len(self.__board)):
            # print labels for y-axis
            print("{:<2}".format(str(y + 1)), end=chr(124) + '  ')

            # loop through all positions and print symbols
            for x in range(len(self.__board[y])):
                if self.__board[y][x][1] == self.__SHOWN or (self.__board[y][x][0] and CHEAT):
                    # if no mine
                    if not self.__board[y][x][0]:
                        # show nr of mines around
                        if self.__board[y][x][3]:
                            print("{:<2}".format(self.__board[y][x][3]), end=' ')

                        else:
                            # print ' ' as no mine
                            print("{:<2}".format(' '), end=' ')

                    # if mine
                    elif self.__board[y][x][0] == self.__ISMINE:
                        print("{:<2}".format('M'), end=' ')

                else:
                    # print notshown * or flag f
                    print("{:<2}".format('f' if self.__board[y][x][2] else '*'), end=' ')
            print()

        # number of mines remaining:
        print("\nNumber of mines remaining: ", self.__mineCount - self.__flagCount)

        # time elapsed:
        temp = int(time.time() - self.__timeStart)
        print("Time elapsed: ", secToMin(temp)[0], " min ", secToMin(temp)[1], "sec")

        return

    def gameLoop(self):
        # global CHEAT
        global CHEAT

        # set system time at game start
        self.__timeStart = time.time()

        while not self.__endGame:
            if DEBUG:
                self.__counter = 0

            while True:
                self.printGame()

                # TODO: option to save game
                print("\n1 - Check for mine")
                print("2 - Place or remove flag")
                print("E - Exit game")
                menuChoice = input("Choose: ")

                if menuChoice == '1':   #check for mine
                    while True:
                        # ask user to input X coordinate (letters)
                        userX = input(("\nEnter X position (A - " + chr(ord('A')+len(self.__board[0])-1) + "): ")).lower()

                        # check for correct letter
                        if userX.isalpha() and len(userX) == 1 and ord('a') <= ord(userX) and\
                                ord(chr(ord('a') + len(self.__board[0])-1)) >= ord(userX):
                            userX = ord(userX.lower()) - ord('a')   # convert to coordinate
                            break

                        else:
                            print("Wrong input!\n")

                    while True:
                        # ask user to input Y coordinate (figures)
                        userY = input("Enter Y position (1 - " + str(len(self.__board)) + "): ")
                        print()

                        # check for correct figure
                        if userY.isdigit():
                            if int(userY) >= 1 and int(userY) <= len(self.__board):
                                userY = int(userY) - 1  # convert to coordinate
                                break

                        print("Wrong input!")

                    # if mine: game over
                    if self.__board[userY][userX][0] == self.__ISMINE:
                        self.__endGame = True
                        # save game session elapsed time
                        self.__timeElapsed = time.time() - self.__timeStart
                        print("\n\n***** GAME OVER! *****\n")

                        # set all positions to shown
                        for y in range(self.__size[0]):  # loop through size of y
                            for x in range(self.__size[1]):  # loop through size of x
                                self.__board[y][x][1] = self.__SHOWN

                        self.printGame()
                        print("\n\n***** GAME OVER! *****\n")
                        break

                    else:
                        # check if shown and look for mines around
                        if not self.__board[userY][userX][1]:
                            self.checkPosition(userY, userX)
                        else:
                            print("***** CAUTION: already opened *****")

                        if self.__size[0]*self.__size[1] - self.__mineCount <= self.__shownCount:
                            # save game session elapsed time
                            self.__timeElapsed = time.time() - self.__timeStart
                            print("\n\n***** Victory! *****\n")
                            # set Victory flag
                            self.__victory = True
                            self.printGame()
                            print("\n\n***** Victory! *****\n")

                            return

                    break

                elif menuChoice == '2': # place or remove flag

                    while True:
                        # ask user to input X coordinate (letters)
                        userX = input(("\nEnter X position (A - " + chr(ord('A')+len(self.__board[0])-1) + "): ")).lower()

                        # check for correct letter
                        if (userX.isalpha() and len(userX) == 1 and ord('a') <= ord(userX) and
                                ord(chr(ord('a') + len(self.__board[0])-1)) >= ord(userX)):
                            userX = ord(userX.lower())-ord('a')
                            break

                        else:
                            print("Wrong input!\n")

                    while True:
                        # ask user to input Y coordinate (figures)
                        userY = input("Enter Y position (1 - " + str(len(self.__board)) + "): ")
                        print()

                        # check for correct input
                        if userY.isdigit():
                            if int(userY) >= 1 and int(userY) <= len(self.__board): # is within range
                                userY = int(userY) - 1
                                break

                        print("Wrong input!\n")

                    # if location already shown disregard input
                    if not self.__board[userY][userX][1]:
                        # invert flag status and increase/decrease flag count
                        if not self.__board[userY][userX][2]:
                            self.__board[userY][userX][2] = self.__FLAG
                            self.__flagCount += 1
                        else:
                            self.__board[userY][userX][2] = self.__NOFLAG
                            self.__flagCount -= 1
                    else:
                        print("***** CAUTION: can not flag position *****")
                    break

                elif menuChoice == 'e' or menuChoice == 'E':

                    print("\n\n")
                    self.__endGame = True
                    # save game session elapsed time
                    self.__timeElapsed = time.time() - self.__timeStart
                    break

                elif menuChoice == '§':  # enable CHEAT
                    if CHEAT:
                        CHEAT = False
                        print("***** CHEAT DISABLED *****\n")
                    else:
                        CHEAT = True
                        print("***** CHEAT ENABLED *****\n")
                    continue

                else:
                    print("\nWrong value, enter 1, 2 or E/e")

        return


def newGame():

    # create new game

    # enter player name
    while True:
        name = input("\nEnter your name: ")
        if len(name) <= 20 and len(name) >= 3:
            break
        else:
            print("Name to short or long, min 3 and max 20 characters")

    # enter player age
    while True:
        age = input("Enter your age: ")
        if age.isdigit():
            if int(age) < 999 and int(age) >= 0:
                break
            else:
                print("To large value")
        else:
            print("Wrong value, enter a figure.")
            continue

    player = Player(name, age)

    while True:
        print("\nChoose one of the following game sizes (width x height):")
        print("1. Small:    ", size[0][0], 'x', size[0][1])
        print("2. Medium:   ", size[1][0], 'x', size[1][1])
        print("3. Big:      ", size[2][0], 'x', size[2][1])

        menuChoice = input("Choose an option: ")

        if menuChoice == '1':
            gameSize = size[0]
            break
        elif menuChoice == '2':
            gameSize = size[1]
            break
        elif menuChoice == '3':
            gameSize = size[2]     # [y, x]
            break
        elif menuChoice == 'e' or menuChoice == 'E':
            print("\n\n")
            return
        else:
            print("\nWrong value, enter an option 1-3")

    while True:
        print("\n1. Easy:    ", int(difficulty[0]*100), "% mines")
        print("2. Medium:  ", int(difficulty[1]*100), "% mines")
        print("3. Hard:    ", int(difficulty[2]*100), "% mines")

        menuChoice = input("Choose difficulty: ")

        if menuChoice == '1':
            gameDiffic = difficulty[0]
            break
        elif menuChoice == '2':
            gameDiffic = difficulty[1]
            break
        elif menuChoice == '3':
            gameDiffic = difficulty[2]
            break
        elif menuChoice == 'e' or menuChoice == 'E':
            print("\n")
            return
        else:
            print("\nWrong value, enter an option 1-3")

    print('\n')

    game = Game(gameSize, gameDiffic)   # create new instance of class Game
    game.makeGame()             # make new game board
    game.gameLoop()             # run game loop

    # open file to append and save stats if victory
    if game.getVictory():
        with open(filenameTopList, 'a', encoding='utf-8') as fileTopList:
            # append player data and game data to file. ';' separated file. Create file if it doesn't exist.
            # name;age;sizeX;sizeY;difficulty[%];time[seconds]
            fileTopList.write(player.name() + ';' + player.age() + ';' + str(gameSize[0]) + ';' +
                              str(gameSize[1]) + ';' + str(gameDiffic) + ';' + str(int(game.getElapsedTime())) + '\n')
        print("\n***** Results saved! *****\n\n")


def topList():

    while True:
        print("\nChoose Toplist for one of the following game sizes (width x height):")
        print("1. Small:    ", size[0][0], 'x', size[0][1])
        print("2. Medium:   ", size[1][0], 'x', size[1][1])
        print("3. Big:      ", size[2][0], 'x', size[2][1])

        menuChoice = input("Choose an option: ")

        if menuChoice == '1':
            topListSize = size[0]
            break
        elif menuChoice == '2':
            topListSize = size[1]
            break
        elif menuChoice == '3':
            topListSize = size[2]     # [x, y]
            break
        elif menuChoice == 'e' or menuChoice == 'E':
            print("\n\n")
            return
        else:
            print("\nWrong value, enter an option 1-3")

    while True:
        print("\n1. Easy:    ", int(difficulty[0]*100), "% mines")
        print("2. Medium:  ", int(difficulty[1]*100), "% mines")
        print("3. Hard:    ", int(difficulty[2]*100), "% mines")

        menuChoice = input("Choose difficulty: ")

        if menuChoice == '1':
            topListDiffic = difficulty[0]
            break
        elif menuChoice == '2':
            topListDiffic = difficulty[1]
            break
        elif menuChoice == '3':
            topListDiffic = difficulty[2]
            break
        elif menuChoice == 'e' or menuChoice == 'E':
            print("\n")
            return
        else:
            print("\nWrong value, enter an option 1-3")

    try:
        # open toplist file, if it exist
        fileTopList = open(filenameTopList, 'r', encoding='utf-8')

        # split into lines
        lines = fileTopList.readlines()

        # close file
        fileTopList.close()

        # in every line remove '\n' and split on ';'
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip('\n').split(';')

        # sort list on board sizeX, sizeY, %mines and time
        lines.sort(key=lambda x: (int(x[2]), int(x[3]), float(x[4]), int(x[5])))

        counter = 0  # counter for top 10
        print('')  # \n

        # Print labels: '#', Name, Age, Time
        print("{:<3}{:<20}{:<10}{:<10}".format("#", "Name", "Age", "Time"))

        for j in range(len(lines)):     # loop through all lines in file
            if DEBUG:
                print(int(lines[j][2]), ' ', topListSize[0])
                print(int(lines[j][3]), ' ', topListSize[1])
                print(float(lines[j][4]), ' ', topListDiffic)
                print(int(lines[j][2]) == topListSize[0])
                print(int(lines[j][3]) == topListSize[1])
                print(float(lines[j][4]) == topListDiffic)

            # if (sizeX & sizeY & diff) == selected
            if (int(lines[j][2]) == topListSize[0] and int(lines[j][3]) == topListSize[1] and
                    float(lines[j][4]) == topListDiffic):
                counter += 1

                # print '#' Name, Age, Time
                print("{:<3}{:<20}{:<10}{:<15}".format(str(counter) + '.', lines[j][0], lines[j][1],
                                                     str(secToMin(int(lines[j][5]))[0]) +
                                                     " min " + str(secToMin(int(lines[j][5]))[1]) + " sec"))
            #only show top ten
            if j > 10:
                break

        if counter == 0:
            print("***** No Entries! *****")

        print("\n\n\n")


    except FileNotFoundError:
        print("***** No top list exist *****\n\n")
        return

def menu():
    # Start of program

    # define that CHEAT is global
    global CHEAT

    # Game menu
    while True:
        # TODO: load game
        print("Welcome to mine sweeper!")
        print("1. New game")
        print("2. Show top list")
        print("E. Exit")

        menuChoice = input("Choose an option: ")

        if menuChoice == '1':
            newGame()  # to init Game class
        elif menuChoice == '2':
            topList()
        elif menuChoice == 'e' or menuChoice == 'E':
            print("\nThanks for playing!")
            return
        elif menuChoice == 'c' or menuChoice == 'C':
            print("Made by Anton Vannesjö, KTH\n\n")
            continue
        elif menuChoice == '§': # enable CHEAT
            if CHEAT:
                CHEAT = False
                print("***** CHEAT DISABLED *****\n")
            else:
                CHEAT = True
                print("***** CHEAT ENABLED *****\n")
            continue
        else:
            print("wrong option\n\n")
            continue


menu()
#run game menu