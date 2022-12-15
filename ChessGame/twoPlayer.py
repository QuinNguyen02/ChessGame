import pygame, time, math
from chessPieces import *
from menu import *

class twoPlayer:
    def __init__(self,surface,menu):
        self.surface = surface
        self.time = pygame.time.Clock()
        self.closed_clicked = False
        self.continue_game = True
        # Timing bg
        self.timing = Timing(self.surface)
        # Other bg
        self.pause = Button(self.surface,'PAUSE',130,47,(510,230),30,'#7CC0EA',12)
        self.newGame = Button(self.surface,'NEW GAME',130,47,(510,290),26,'#D74B4B',12)
        self.menu = Button(self.surface,'MENU',130,47,(510,350),30,'#97DA8C',12)
        # surface
        self.bg = pygame.image.load("board2.png")
        self.bg = pygame.transform.scale(self.bg, (500,600))        
        # Pieces obj
        self.board = Tiles(self.surface)
        self.pieces = Pieces(self.surface, self.board)
        # State of the game
        self.choosing = False
        self.turn = 'red'
        self.chosenPiece = None
        
    def play(self):
    # whole game running process in order
        while not self.closed_clicked:
            self.handleEvents()
            self.draw()       
            if self.continue_game:
                self.update() 
                self.decideContinue()
            self.time.tick(60)     
    
    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.closed_clicked = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_game:
                    self.handleMouseDown(event)
                self.handleClickButton(event)

    def handleClickButton(self,event):
        # check if choose pause or new game 
        if self.pause.handleMouseDown(event.pos):
            if self.continue_game == True:
                self.continue_game = False
                self.pause.changeName("RESUME")
            else:
                self.continue_game = True
                self.pause.changeName("PAUSE")
        elif self.newGame.handleMouseDown(event.pos):
            self.resetGame() 
        elif self.menu.handleMouseDown(event.pos):
            self.returnMenu()
            
    def handleMouseDown(self,event):
        # 2 case: choose piece or choose position for that piece
        if not self.choosing: #not choosing yet 
            self.chosenPiece, self.choosing = self.pieces.checkMouseDown(event.pos,self.turn)
        else: #assign position
            # check if player change mind and choose another piece
            self.chosenPiece = self.pieces.checkChosenPiece(event.pos, self.chosenPiece)
            self.choosing = self.pieces.assignPos(event.pos, self.chosenPiece)
            # Change turn
            if not self.choosing and self.turn == 'red':
                self.turn = 'black'
            elif not self.choosing and self.turn == 'black':
                self.turn = 'red'            
    
    def draw(self):
        font = pygame.font.SysFont('Consolas', 30)
        self.surface.blit(self.bg, (0,0))
        # Draw timing board
        self.timing.draw()
        # Draw other
        self.pause.draw()
        self.newGame.draw()
        self.menu.draw()
        # Draw chess board
        self.pieces.draw()
        if self.choosing:
            self.board.drawIns()
        pygame.display.update()
    
    def update(self):
        self.continue_game = self.timing.update(self.turn)
    
    def decideContinue(self):
        win,winner = self.pieces.checkWin()
        if win:
            print('Winner is',winner)
            self.continue_game = False
    
    def resetGame(self):
        # In case player choose new game while pausing the current game
        self.continue_game = True 
        self.timing.reset()
        self.board.reset()
        self.pieces.reset()
        self.turn = 'red'
        
    def returnMenu(self):
        self.resetGame()
        self.closed_clicked = True
