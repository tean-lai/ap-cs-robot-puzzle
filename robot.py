'''
Created on Oct 1, 2018

@author: quest
'''
from graphics import *
from random import *
from math import *

def setup():
    global dimX, dimY, grid, win, direction, squareSize
    
    dimX = 7 #x dimension of the grid
    dimY = 4 #y dimension of the grid
    tempList = [] #used to create the grid
    grid = []
    squareSize = 50
    
    win = GraphWin('Robot', dimX * squareSize, dimY * squareSize + 48)
    win.setBackground('white')
    
    for i in range(dimX):
        tempList.append(0)
    for i in range(dimY):
        grid.append(tempList[:])
             
    message = Text(Point(dimX * squareSize / 2, dimY * squareSize + 24), "Hit 'w' to go forward, 'a' to turn left, \n'd' to turn right, and 'escape' to exit the program")
    message.draw(win)
    
    grid[randint(0, dimY - 1)][randint(0, dimX - 1)] = 1
    direction = randint(0, 3) * pi / 2 #the direction is stored as an angle in radians

def drawGridSquares():
    for x in range(dimX):
        for y in range(dimY):
            square = Polygon(Point(x * squareSize, y * squareSize),
                             Point((x + 1) * squareSize, y * squareSize),
                             Point((x + 1) * squareSize, (y + 1) * squareSize),
                             Point(x * squareSize, (y + 1) * squareSize))
            square.setFill('light blue')
            square.draw(win)
            
    points = []
    r = squareSize / 2 #radius of triangle
    drawX = squareSize * (robotX + 1 / 2)
    drawY = squareSize * (robotY + 1 / 2)
    
    for i in range(3): #draws the robot
        points.append(Point(drawX + r * cos(direction + i * 2 * pi / 3), drawY - r * sin(direction + i * 2 * pi / 3)))
    tri = Polygon(points)
    tri.setFill('gray')
    tri.setOutline('gray')
    tri.draw(win)

def getCoord():
    for i in range(len(grid)):
            if sum(grid[i]) == 1:
                return i, grid[i].index(1)

def canMove():
    try:
        testing = grid[robotY - int(sin(direction))][robotX + int(cos(direction))]
        if ((robotY - int(sin(direction)) < 0) or (robotX + int(cos(direction)) < 0)):
            return False
        else:
            return True
    except:
        return False

def moveForward():
    if canMove():
        grid[robotY], grid[robotY - int(sin(direction))] = grid[robotY - int(sin(direction))], grid[robotY]
        grid[robotY][robotX], grid[robotY][robotX + int(cos(direction))] = grid[robotY][robotX + int(cos(direction))], grid[robotY][robotX]

def rotateLeft():
    global direction
    direction = direction + pi / 2

def rotateRight():
    global direction
    direction = direction - pi / 2

def main():
    global robotX, robotY, direction
    setup()
    while True:
        
        
        robotY, robotX = getCoord()
        drawGridSquares()
        
        key = win.getKey()
                    
        if key == 'Escape': #if user presses the escape key, the program exits
            win.close()
            return
        elif key == 'w':
            moveForward()
        elif key == 'a':
            rotateLeft()
        elif key == 'd':
            rotateRight()
        
        

main()