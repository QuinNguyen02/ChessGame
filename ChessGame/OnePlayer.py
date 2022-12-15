import pygame, time, math
from chessPieces import *
from player import *
from ChessEngine import *
from menu import Timing, Button

class onePlayer:
    def __init__(self,surface):
        # surface
        self.surface = surface
        self.time = pygame.time.Clock()
        self.closed_clicked = False
        self.continue_game = True
        '''
        # Timing bg
        self.timing = Timing(self.surface)
        # Other bg
        self.pause = Button(self.surface,'PAUSE',130,47,(510,250),30,'#7CC0EA')
        self.newGame = Button(self.surface,'NEW GAME',130,47,(510,310),26,'#D74B4B')        
        '''
        # bg obj
        self.bg = pygame.image.load("board2.png")
        self.bg = pygame.transform.scale(self.bg, (500,600))
        # Pieces obj
        self.board = Tiles(self.surface)
        self.pieces = Pieces(self.surface, self.board)
        self.posit = []
        # State of the game
        self.choosing = False
        self.turn = 'red'
        self.chosenPiece = None
        # computer AI
        self.computer = chessEngine(self.surface,self.board,self.pieces)
        # wining frame
        self.text = None
        self.winingBoard = Button(self.surface,self.text,300,150,(100,250),30,'#7CC0EA',50)

    def play(self):
    # whole game running process in order
        while not self.closed_clicked:
            self.handleEvents()
            self.draw()
            self.update()
            if self.continue_game:
                self.decideContinue()
            self.time.tick(60)   
        #print(self.posit) 
    
    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            #print(len(self.pieces.getPieces()))
            if event.type == pygame.QUIT:
                self.closed_clicked = True
            elif event.type == pygame.MOUSEBUTTONDOWN and self.turn == 'red' and self.continue_game:
                self.handleMouseDown(event)  
            elif self.turn == 'black' and self.continue_game:
                blackList = self.getBlackPieces()
                self.computer.getAvailMove(blackList)
                self.computer.evaluateMove()
                self.turn = 'red' 
         

    def getBlackPieces(self):
        blackList = []
        for piece in self.pieces.getPieces():
            if piece.getColor() == 'black':
                blackList.append(piece)  
        return blackList
    
    def handleMouseDown(self,event):
        '''if self.pause.handleMouseDown(event.pos):
            self.continue_game = False
        elif self.newGame.handleMouseDown(event.pos):
            self.resetGame()'''          
        # 2 case: choose piece or choose position for that piece
        #self.posit.append(pygame.mouse.get_pos())
        if not self.choosing: #not choosing yet 
            self.chosenPiece, self.choosing = self.pieces.checkMouseDown(event.pos,self.turn)
        else: #assign position
            # check if player change mind and choose another piece
            self.chosenPiece = self.pieces.checkChosenPiece(event.pos, self.chosenPiece)
            self.choosing = self.pieces.assignPos(event.pos, self.chosenPiece)
            if not self.choosing:
                self.turn = 'black'
    
    def draw(self):
        self.surface.blit(self.bg, (0,0))
        self.pieces.draw()
        #self.timing.draw()
        #self.pause.draw()
        #self.newGame.draw()
        if self.choosing and self.turn == 'red':
            self.board.drawIns()
        if not self.continue_game:
            self.winingBoard.changeName(self.text)
            self.winingBoard.draw()
        pygame.display.update()
    
    def update(self):
        #self.continue_game = self.timing.update(self.turn)
        pass

    def decideContinue(self):
        win,winner = self.pieces.checkWin()
        if win:
            self.continue_game = False
            if winner == 'black':
                self.text = 'YOU LOSE -_-'
                #print('winner is black')
            else:
                self.text = 'YOU WIN ^_^'

    def resetGame(self):
        self.timing.reset()
        self.board.reset()
        self.pieces.reset()
        self.turn = 'red'
