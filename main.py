import pygame
from pygame.locals import *

pygame.init()

# setting up the screen
screen = pygame.display.set_mode((500, 500))
# frame rate of the game
clock = pygame.time.Clock()
# establish name of the game
pygame.display.set_caption("Tic Tac Toe")

# size of the screen
screenWidth = screen.get_width()
screenHeight = screen.get_height()
print(screenWidth, screenHeight)

# number of squares
# can be adjusted to have tic tac toe of any number instead of just three
squareNumber = 3

# basic square width and height
squareWidthDistance = screenWidth // squareNumber
squareHeightDistance = screenHeight // squareNumber
print(squareWidthDistance, squareHeightDistance)
# colour of the square
squareColour = pygame.Color(100, 100, 100)
# width of the square
squareWidth = 3
# state of the square: Empty, X, or O
squareState = "E"
# dictionary of squares
squareDict = {}

# range of the width of the squares
rangeWidth = range(0, screenWidth - squareWidthDistance, squareWidthDistance)
rangeHeight = range(0, screenHeight - squareHeightDistance, squareHeightDistance)

# filling the board
for width in rangeWidth:
    for height in rangeHeight:
        squareRect = pygame.Rect((width, height), (squareWidthDistance, squareHeightDistance))
        squareDict[(width, height)] = [squareRect, squareColour, squareWidth, squareState]

# find 3 in a row
def rowOf3(squarePos, squareState):
    x, y = squarePos
    checkState = lambda x, y: squareDict[(x, y)][-1] == squareState if (x,y) in squareDict.keys() else False

    # check the horizontal, vertical, and diaganonals 
    # if there is a complete row of 3 or any square number - 1
    horiD = sum([1 for state in rangeWidth if checkState(x - state, y)])
    horiU = sum([1 for state in rangeWidth if checkState(x + state, y)])
    vertiD = sum([1 for state in rangeHeight if checkState(x, y - state)])
    vertiU = sum([1 for state in rangeHeight if checkState(x, y + state)])
    diagDR = sum([1 for state1, state2 in zip(rangeWidth, rangeHeight) if checkState(x + state1, y - state2)])
    diagDL = sum([1 for state1, state2 in zip(rangeWidth, rangeHeight) if checkState(x - state1, y - state2)])
    diagUR = sum([1 for state1, state2 in zip(rangeWidth, rangeHeight) if checkState(x + state1, y + state2)])
    diagUL = sum([1 for state1, state2 in zip(rangeWidth, rangeHeight) if checkState(x - state1, y + state2)])

    positions = [horiD, horiU, horiD + horiU, 
                vertiD, vertiU, vertiD + vertiU, 
                diagDR, diagDL, diagDR + diagUR, 
                diagUR, diagUL, diagDL + diagUL]
    # print(positions)

    return squareNumber - 1 in positions

# for playing the game
play = True
# deciding whether it's an x or an o
move = 0
# no letting any more placements after the game is over
over = False
while play:
    # fitting the board to play in a nice grey
    screen.fill((23, 23, 23))
    clock.tick(10)
    
    for event in pygame.event.get():
        if (event.type == QUIT):
            play = False
        elif (event.type == MOUSEBUTTONDOWN):
            # checking each square and putting an x or an o
            # an x will be a more red while o is blue with a touch of green
            for square in squareDict:
                mouseX, mouseY = pygame.mouse.get_pos()
                squareRect, squareColour, _, squareState = squareDict[square]
                if (squareRect.collidepoint(mouseX, mouseY) and squareState == "E" and not over):
                    # x's go first and o's go second
                    if (move % 2 == 0):
                        squareState = "X"
                        squareColour = pygame.Color(100, 0, 0)
                    else:
                        squareState = "O"
                        squareColour = pygame.Color(0, 25, 100)
                    
                    # checking if the game is over
                    if (rowOf3(square, squareState)):
                        print("Game Over!", squareState, "won the game!!!")
                        over = True
                    else:
                        print("Not yet")
                        # print([squareDict[x][-1] for x in squareDict])
                    # incrementing the move
                    move += 1
                    # updating the square only if it was actually changed
                    squareDict[square] = [squareRect, squareColour, _, squareState]

    # drawing the board
    for square in squareDict:
        squareRect, squareColour, squareWidth, squareState = squareDict[square]
        if squareState in ["X", "O"]:
            pygame.draw.rect(screen, squareColour, squareRect)
        else:
            pygame.draw.rect(screen, squareColour, squareRect, squareWidth)

    # updating the pygame screen
    pygame.display.flip()
    