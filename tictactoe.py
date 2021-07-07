# -*- coding: utf-8 -*-
"""
Recriação do Jogo da Velha

@author: Prof. Daniel Cavalcanti Jeronymo

@Modificação e implementação: Pedro Baleroni
"""
maxCont = 0
player1chance = 0
player2chance = 0
drawCont = 0
cPlayer_ = 1
desligaJogo = 0

cX = -1
cY = -1

import pygame 
import sys
import os
import traceback
import random
import numpy as np
import copy

class GameConstants:
    #                  R    G    B
    ColorWhite     = (255, 255, 255)
    ColorBlack     = (  0,   0,   0)
    ColorRed       = (255,   0,   0)
    ColorGreen     = (  0, 255,   0)
    ColorBlue     = (  0, 0,   255)
    ColorDarkGreen = (  0, 155,   0)
    ColorDarkGray  = ( 40,  40,  40)
    BackgroundColor = ColorBlack
    
    screenScale = 1
    screenWidth = screenScale*600
    screenHeight = screenScale*600
    
    # grid size in units
    gridWidth = 3
    gridHeight = 3
    
    # grid size in pixels
    gridMarginSize = 5
    gridCellWidth = screenWidth//gridWidth - 2*gridMarginSize
    gridCellHeight = screenHeight//gridHeight - 2*gridMarginSize
    
    randomSeed = 0
    
    FPS = 30
    
    fontSize = 20

class Game:
    class GameState:
        # 0 empty, 1 X, 2 O
        grid = np.zeros((GameConstants.gridHeight, GameConstants.gridWidth))
        currentPlayer = 0
    
    def __init__(self, expectUserInputs=True):
        self.expectUserInputs = expectUserInputs
        
        # Game state list - stores a state for each time step (initial state)
        gs = Game.GameState()
        self.states = [gs]
        
        # Determines if simulation is active or not
        self.alive = True
        
        self.currentPlayer = 1
        
        # Journal of inputs by users (stack)
        self.eventJournal = []
    
    # Implements a game tick
    # Each call simulates a world step
    def update(self):  
        # If the game is done or there is no event, do nothing
        if not self.alive or not self.eventJournal:
            return
        
        # Get the current (last) game state
        gs = copy.copy(self.states[-1])
        
        # Switch player turn
        if gs.currentPlayer == 0:
            gs.currentPlayer = 1
        elif gs.currentPlayer == 1:
            gs.currentPlayer = 2
        elif gs.currentPlayer == 2:
            gs.currentPlayer = 1
            
        # Mark the cell clicked by this player if it's an empty cell
        x,y = self.eventJournal.pop()

        # Check if in bounds
        if x < 0 or y < 0 or x >= GameConstants.gridCellHeight or y >= GameConstants.gridCellWidth:
            return

        # Check if cell is empty
        if gs.grid[x][y] == 0:
            gs.grid[x][y] = gs.currentPlayer
        else: # invalid move
            return
        
        global gridTest

        gridTest = gs.grid

        
        
        
        # Check if end of game
        if winnerwinnerchickendinner(gridTest):
            pygame.quit()

        

        # Add the new modified state
        self.states += [gs]

#Agradecimento ao Arthur Ydalgo pela ajuda com o código abaixo, 
#   além de resolver um erro já existente, ajudou a prever um erro no handle game.

def winnerwinnerchickendinner(gridTest):
    for i in range(3): #linha
        w1 = set(gridTest[i, :])
        if len(w1) == 1 and min(w1) !=0:
            return w1.pop()
            
    for i in range(3):
        w1 = set(gridTest[:, i]) #coluna
        if len(w1) == 1 and min(w1) !=0:
            return w1.pop()

    w1= set(gridTest[j,j] for j in range(3)) #diagonal
    if len(w1) == 1 and min(w1) !=0:
        return w1.pop()

    w1= set(gridTest[-j-1,j] for j in range(3)) #contra-diagonal
    if len(w1) == 1 and min(w1) !=0:
        return w1.pop()

    contaCerta = 0 #chance de Dar Velha
    for testR in range(3):
        for testC in range(3):
            if gridTest[testC][testR] !=0:
                contaCerta += 1
    if contaCerta == 9:
        return 3

    return 0 #nenhum parametro de vitória



def probability(gridTest, cPlayer):
    winnerChance = winnerwinnerchickendinner(gridTest) #if some win, end of recursive function
    if winnerChance != 0:
        if winnerChance == 1: # probability red one win
            global player1chance
            player1chance += 1
        elif winnerChance == 2: # chance to blue get the cup
            global player2chance
            player2chance += 1
        elif winnerChance == 3: # every guys upstairs sucks
            global drawCont
            drawCont += 1
        return

    if cPlayer == 1: #new player to play
        cPlayer = 2
    elif cPlayer == 2:
        cPlayer = 1

    # try every next game step possible

    for row in range(len(gridTest)):
        for collum in range(len(gridTest[row])):
            if(gridTest[row][collum] == 0): #only empty spaces
                newGrid = copy.deepcopy(gridTest)
                newGrid[row][collum] = cPlayer
                probability(newGrid, cPlayer)
    

       

def drawGrid(screen, game):
    rects = []

    rects = [screen.fill(GameConstants.BackgroundColor)]
    
    # Get the current game state
    gs = game.states[-1]
    grid = gs.grid
 
    # Draw the grid
    for row in range(GameConstants.gridHeight):
        for column in range(GameConstants.gridWidth):
            color = GameConstants.ColorWhite
            
            if grid[row][column] == 1:
                color = GameConstants.ColorRed
            elif grid[row][column] == 2:
                color = GameConstants.ColorBlue
            
            m = GameConstants.gridMarginSize
            w = GameConstants.gridCellWidth
            h = GameConstants.gridCellHeight
            rects += [pygame.draw.rect(screen, color, [(2*m+w) * column + m, (2*m+h) * row + m, w, h])]    
    
    return rects


def draw(screen, font, game):
    rects = []
            
    rects += drawGrid(screen, game)

    return rects


def initialize():
    random.seed(GameConstants.randomSeed)
    pygame.init()
    game = Game()
    font = pygame.font.SysFont('Courier', GameConstants.fontSize)
    fpsClock = pygame.time.Clock()

    # Create display surface
    screen = pygame.display.set_mode((GameConstants.screenWidth, GameConstants.screenHeight), pygame.DOUBLEBUF)
    screen.fill(GameConstants.BackgroundColor)
        
    return screen, font, game, fpsClock


def handleEvents(game):
    #gs = game.states[-1]
    
    for event in pygame.event.get():
       
        global maxCont          # all plays
        global drawCont         # draw plays
        global cX
        global cY
       
        pos = pygame.mouse.get_pos()
        global cPlayer_ 
        global player1chance    # player red wins
        global player2chance    # player blue wins
        global drawCont         # draw cont
        if((cX != pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth))or(cY != pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight))):            
            cX = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            cY = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
            gs = game.states[-1]
            grid = copy.deepcopy(gs.grid)#copia a grid do jogo atual
            player1chance=0
            player2chance=0
            drawCont = 0
            if(grid[cY][cX]==0 and cY!=-1 and cX!=-1):#confere se a posição sendo verificada é válida
                jogador = copy.copy(cPlayer_)                
                grid[cY][cX] = jogador #atribui o jogador atual ao teste, considerando o quadrado que está em cima
                probability(grid,jogador) #chama a função recursiva
                
                maxCont = (player2chance + player1chance + drawCont)
                #calcula a chance e mostra de acordo com o atual jogador
                if(cPlayer_==1):                    
                    print("Chance do Vermelho ganhar: {:.2f}%".format(100*player1chance/maxCont))
                    print("Chance de empatar: {:.2f} %".format(100*drawCont/maxCont))
                else:
                    print("Chance do Azul ganhar: {:.2f}%".format(100*player2chance/maxCont))
                    print("Chance de empatar: {:.2f} %".format(100*drawCont/maxCont))

    
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            col = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            row = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
            #print('clicked cell: {}, {}'.format(cellX, cellY))
            if cPlayer_ == 1:
                cPlayer_ = 2
            elif cPlayer_ == 2:
                cPlayer_ = 1
            # send player action to game
            game.eventJournal.append((row, col))
            
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

            
def mainGamePlayer():
    try:
        # Initialize pygame and etc.
        screen, font, game, fpsClock = initialize()
              
        # Main game loop
        while game.alive:
            # Handle events
            handleEvents(game)
                    
            # Update world
            game.update()
            
            # Draw this world frame
            rects = draw(screen, font, game)     
            pygame.display.update(rects)
            
            # Delay for required FPS
            fpsClock.tick(GameConstants.FPS)
            
        # close up shop
        pygame.quit()
    except SystemExit:
        pass
    except Exception as e:
        #print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        pygame.quit()
        #raise Exception from e
    
    
if __name__ == "__main__":
    # Set the working directory (where we expect to find files) to the same
    # directory this .py file is in. You can leave this out of your own
    # code, but it is needed to easily run the examples using "python -m"
    mainGamePlayer()