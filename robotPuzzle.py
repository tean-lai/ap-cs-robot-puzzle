'''
Created on Oct 4, 2018

@author: tean_lai
'''
from graphics import *
from random import randint
from math import sin, cos, radians

def main():
    print('Welcome to the Robot Puzzle!')
    print('What level? (random is default)')
    levelType = input('Available levels ["1", "2"]: ') #2 is from Legend of Zelda Twilight Princess
    if levelType == '2':
        levelType = 'levelTwo.txt'
    elif levelType == '1':
        levelType = 'levelOne.txt'
    else:
        levelType = 'random'
    
    setup(levelType)

    while True:
        key = win.getKey()

        if key == 'w':
            moveFoward()
        elif key == 'a':
            turnLeft()
        elif key == 'd':
            turnRight()
        elif key == 'Escape':
            win.close()
            input('awwwwww why not finish it?')
            return
        updateRobot()

        winCondition = 2
        for i in range(2):
            if abs(grid[winSpots[i][1]][winSpots[i][0]]) == 1:
                winCondition -= 1

        if not(winCondition):
            win.getKey()
            win.close()
            print('good job on winning!')
            input()
            return
def setup(levelType):
    global winX, winY, grid, win, squareSize
    
    grid = [] #0 = air, 1 = robot, -1 = robot2, 2 = block, 3 = win conditions

    generateLevel(levelType)
    
    squareSize = 60
    winX = dimX * squareSize
    winY = dimY * squareSize
    
    win = GraphWin('Robot Puzzle', winX, winY)
    
    rules()
    
    drawGridSquares()

    updateRobot()
def rules(): #displays the rules for the program
    rules = Text(Point(winX / 2, winY / 2),  '''
 Press 'w' to move forward
 'a' to turn left
 'd' to turn right
 'escape' to quit the game
    

 ...press any key to continue...''')
    rules.draw(win)
    
    win.getKey()
    
    rules.setText('''
 The point of this game is to
 get the two robots to land on the
 green squares, the robot will only
 move if there is a blue square in 
 front of them
        
 ...press any key to continue...''')
    
    win.getKey()
    
    rules.setText('''
 The dark gray robot will be controlled
 by you, the light gray robot will
 mirror the other
 Good Luck
        

 ...press any key to continue...''')
    
    win.getKey()
def generateLevel(mode):
    global direction, dimX, dimY, winSpots, grid
    
    if mode == 'random': #generates a level from random
        dimX = randint(5, 9)
        dimY = randint(5, 9)
        
        tempList = [] #used to create the grid

        for i in range(dimX):
            tempList.append(0)
        for i in range(dimY):
            grid.append(tempList[:])
        
        direction = randint(0, 3) * 90
        
        for i in range(-1, 2, 2):
            while True:
                x, y = randint(0, dimX - 1), randint(0, dimY - 1)
                if grid[y][x] == 0:
                    grid[y][x] = i
                    break
        
        for i in range(randint(2, 4)):
            while True:
                x, y = randint(0, dimX - 1), randint(0, dimY - 1)
                if grid[y][x] == 0:
                    grid[y][x] = 2
                    break

        winSpots = [] #will hold two coordinates that are the win conditions

        for i in range(2):
            while True:
                x, y = randint(0, dimX - 1), randint(0, dimY - 1)
                if grid[y][x] == 0:
                    grid[y][x] = 3
                    winSpots.append([x, y])
                    break

    else: #generates the level from a text file
        level = open(mode, 'r')

        dimX = int(level.readline())
        dimY = int(level.readline())

        direction = int(level.readline())

        winSpots = [level.readline().split(), level.readline().split()] #will hold two coordinates that are the win conditions
        for i in range(2):
            for j in range(2):
                winSpots[i][j] = int(winSpots[i][j])

        for i in range(6):
            line = level.readline()
            grid.append(line.split())

        for y in range(dimY):
            for x in range(dimX):
                grid[y][x] = int(grid[y][x])


        level.close()
def drawGridSquares():
    for x in range(dimX):
        for y in range(dimY):
            square = Polygon(Point(x * squareSize, y * squareSize),
                             Point((x + 1) * squareSize, y * squareSize),
                             Point((x + 1) * squareSize, (y + 1) * squareSize),
                             Point(x * squareSize, (y + 1) * squareSize))
            if grid[y][x] == 2:
                square.setFill('black')
            elif grid[y][x] == 3:
                square.setFill('light green')
            else:
                square.setFill('light blue')
            square.draw(win)
def updateRobot():
    global robot1, robot2

    try:
        robot1.undraw()
        robot2.undraw()
    except:
        pass

    points1, points2 = [], []
    x1, y1 = getCoord('robot1')
    x2, y2 = getCoord('robot2')
    r = squareSize / 2
    drawX1, drawX2 = squareSize * (x1 + 1 / 2), squareSize * (x2 + 1 / 2)
    drawY1, drawY2 = squareSize * (y1 + 1 / 2), squareSize * (y2 + 1 / 2)
    
    for i in range(3): #draws the robots
        points1.append(Point(drawX1 + r * cos(radians(direction + i * 120)), drawY1 - r * sin(radians(direction + i * 120))))
        points2.append(Point(drawX2 + r * cos(radians(direction + i * 120 + 180)), drawY2 - r * sin(radians(direction + i * 120 + 180))))
    robot1, robot2 = Polygon(points1), Polygon(points2)
    robot1.setFill('gray')
    robot1.setOutline('black')
    robot1.draw(win)
    robot2.setFill('light gray')
    robot2.setOutline('black')
    robot2.draw(win)
def getCoord(robot):
    index = 1

    if robot == 'robot2':
        index -= 2

    for j in range(dimY):
        for i in range(dimX):
            if grid[j][i] == index:
                return i, j
def turnLeft():
    global direction
    direction += 90
def turnRight():
    global direction
    direction -= 90
def moveFoward():

    if canMove('robot1'):
        x, y = getCoord('robot1')
        tryX = x + int(cos(radians(direction)))
        tryY = y - int(sin(radians(direction)))

        grid[y][x], grid[tryY][tryX] = grid[tryY][tryX], grid[y][x]


    if canMove('robot2'):
        x, y = getCoord('robot2')
        tryX = x - int(cos(radians(direction)))
        tryY = y + int(sin(radians(direction)))

        grid[y][x], grid[tryY][tryX] = grid[tryY][tryX], grid[y][x]
def canMove(robot):
    index = 1

    if robot == 'robot2':
        index -= 2

    x, y = getCoord(robot)

    try:
        tryX = x + int(index * cos(radians(direction)))
        tryY = y - int(index * sin(radians(direction)))

        testing = grid[tryY][tryX]

        if (tryY < 0) or (tryX < 0):
            return False
        elif grid[tryY][tryX] == 2 or grid[tryY][tryX] == -1 * index:
            return False


        else:
            return True
    except:
        return False

main()