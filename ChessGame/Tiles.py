import pygame

class Tiles:
    def __init__(self, surface):
        self.surface = surface
        self.boards = {}
        self.initBoards()
        self.instructions = []
    
    def initBoards(self):
        origin = (12,18)
        deltaX = 54
        deltaY = 58
        for i in range (9):
            for j in range (10):
                new = ((origin[0] + (deltaX*i)),(origin[1] + int(deltaY*j)))
                self.boards[new] = None #None indicates tile not filled
    
    def setPiece(self, pos, piece):
        self.boards[pos] = piece
    
    def getPiece(self,pos):
        return self.boards[pos]
    
    def checkValidMove(self,pos):
        # General check for valid move
        if self.boards.get(pos) == None:
            return False
        return True
    
    def getTiles(self):
        return self.boards
    
    def setIns(self,pos):
        # apeend instruction object (green tile one)
        self.instructions.append(Instruction(self.surface,self.boards,pos))
    
    def drawIns(self):
        for i in self.instructions:
            i.draw()
    
    def refreshIns(self):
        self.instructions.clear()

    def getIns(self):
        return self.instructions
    
    def reset(self):
        #self.boards.clear()
        self.initBoards()
        self.refreshIns()
    
class Instruction:
    def __init__(self, surface, board, pos):
        self.surface = surface
        self.board = board
        self.pos = pos
        self.img = pygame.image.load("avail.png")
        self.rect = self.img.get_rect()
    
    def draw(self):
        self.surface.blit(self.img,self.pos)
    
    def getRect(self):
        return self.rect
    
    def checkCollide(self,mPos):
        if mPos[0] >= self.pos[0] and mPos[0] <= (self.pos[0]+45):
            if mPos[1] >= self.pos[1] and mPos[1] <= (self.pos[1]+45): 
                return True
        return False
    
    def setPos(self, pos):
        self.pos = pos
    
    def getPos(self):
        return self.pos


