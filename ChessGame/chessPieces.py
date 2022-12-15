import pygame, math
from Tiles import *

class Pieces:
    def __init__(self,surface,board):
        self.surface = surface
        self.board = board
        self.pieces = []
        self.deleted = []
        self.initPiece("red", [366,424,540])
        self.initPiece("black", [192,134,18])
        self.level = ["Chariot", "Horse", "Elephant", "Guard", "King", "Cannon", "Soldier"]
        self.updateBoard() 
        self.win = False
    
    def reset(self):
        self.pieces = []
        self.deleted = []
        self.initPiece("red", [366,424,540])
        self.initPiece("black", [192,134,18])
        self.updateBoard() 
        self.win = False
    
    def getPieces(self):
        return self.pieces
    def getDeleted(self):
        return self.deleted
    
    def initPiece(self, color, line):
        if color == "black":
            imgNames = ['B1.png','B2.png','B3.png','B4.png','B5.png','B6.png','B7.png']
        else:
            imgNames = ['R1.png','R2.png','R3.png','R4.png','R5.png','R6.png','R7.png']
            
        for i in range (12,445,54):
            new2 = None # Not all case have new2 but all has new1

            if i == 12 or i == 444:
                new1 = Chariot(self.surface, self.board, imgNames[0], (i,line[2]),color,10)
                new2 = Soldier(self.surface, self.board, imgNames[6], (i,line[0]),color,1)
            elif i == 66 or i == 390:    
                new1 = Horse(self.surface, self.board, imgNames[1], (i,line[2]),color, 4.5)
                new2 = Cannon(self.surface, self.board, imgNames[5], (i,line[1]),color, 5)
            elif i == 120 or i == 336:
                new1 = Elephant(self.surface, self.board, imgNames[2], (i,line[2]),color, 2.5)
                new2 = Soldier(self.surface, self.board, imgNames[6], (i,line[0]),color, 1)
            elif i == 174 or i == 282:
                new1 = Guard(self.surface, self.board, imgNames[3], (i,line[2]),color, 2)
            else:
                new1 = King(self.surface, self.board, imgNames[4], (i,line[2]),color, 100)
                new2 = Soldier(self.surface, self.board, imgNames[6], (i,line[0]),color, 1)
            
            lists = [new1,new2]
            if lists[1] == None:
                lists.pop(1)
            self.pieces.extend(lists)

    def updateBoard(self):
        for piece in self.pieces:
            self.board.getTiles()[piece.getPos()] = piece

    def draw(self):
        for piece in self.pieces:
            piece.draw()
    
    def checkMouseDown(self,mousePos,turn):
        # Function to get green move of chosen piece
        # Return chosen piece, boolean indicates whether a valid piece was chosen
        for piece in self.pieces:
            if piece.checkCollide(mousePos) and piece.getColor() == turn:
                piece.showValidMove(piece)
                return piece, True
        return None,False
    
    def checkChosenPiece(self,mousePos,chosenPiece):
        # Function to recheck if player want to change to move another piece
        # Return the latest chosen piece
        for piece in self.pieces:
            if piece.checkCollide(mousePos) and piece.getColor() == chosenPiece.getColor():
                self.board.refreshIns()
                piece.showValidMove(piece)
                return piece
        return chosenPiece
                
    def assignPos(self, mousePos, chosenPiece):
        # Function to assign chosenPiece to new position
        # It clear the avail move list and delete defeated piece if needed
        move = False
        for i in self.board.getIns():
            if i.checkCollide(mousePos): #if collide with avail move tile
                #Collide other piece
                if self.board.getTiles()[i.getPos()] != None:
                    self.deleted.append(self.board.getTiles()[i.getPos()])
                    #update list
                    self.pieces.remove(self.board.getTiles()[i.getPos()])
                #update board
                self.board.getTiles()[chosenPiece.getPos()] = None
                #update piece
                chosenPiece.setPos(i.getPos())
                #update board
                self.board.getTiles()[i.getPos()] = chosenPiece
                move = True
                   
        if move:
            self.board.refreshIns()
            return False
        return True
            
    def checkWin(self):
        for piece in self.deleted:
            if abs(piece.getScore()) == 100 :
                if piece.getColor() == 'black':
                    return True,'red'
                else:
                    return True,'black'
        return False,None


class Chariot:
    def __init__ (self, surface, board, img, pos, color, value):
        self.surface = surface
        self.board = board
        self.img = pygame.image.load(img)
        self.pos = pos
        self.state = True #indiciate whether still alive
        self.color = color
        self.rect = self.img.get_rect()
        if color == 'red':
            self.value = value
        else:
            self.value = -value 


    
    def getImage(self):
        return self.img
    
    def showValidMove(self,currentPiece):
        # Function to add valid green move tile to the list to show on board
        #constraint = cannot jump over other pieces
        # 2 directions: up and down
        self.checkMoveVertical(currentPiece)
        self.checkMoveHorizontal(currentPiece)
        #self.board.drawIns()
        
    def checkMoveVertical(self,currentPiece):
        closetPiece = [None,None]
        i = self.pos[1] + 58 
        while closetPiece[0] == None and i <= 540:
            if self.board.getTiles()[(self.pos[0],i)] == None:
                self.board.setIns((self.pos[0],i))
            else: 
                closetPiece[0] = self.board.getTiles()[(self.pos[0],i)]
                if currentPiece.getColor() != closetPiece[0].getColor():
                    self.board.setIns((self.pos[0],i))
            i += 58
        
        i = self.pos[1] - 58 
        while closetPiece[1] == None and i >= 18:
            if self.board.getTiles()[(self.pos[0],i)] == None:
                self.board.setIns((self.pos[0],i))
            else: 
                closetPiece[1] = self.board.getTiles()[(self.pos[0],i)]
                if currentPiece.getColor() != closetPiece[1].getColor():
                    self.board.setIns((self.pos[0],i))
            i -= 58
    
    def checkMoveHorizontal(self,currentPiece):
        closetPiece = [None,None]
        i = self.pos[0] + 54
        while closetPiece[0] == None and i <= 444:
            if self.board.getTiles()[(i, self.pos[1])] == None:
                self.board.setIns((i, self.pos[1]))
            else: 
                closetPiece[0] = self.board.getTiles()[(i, self.pos[1])]
                if currentPiece.getColor() != closetPiece[0].getColor():         
                    self.board.setIns((i, self.pos[1]))
            i += 54
        
        i = self.pos[0] - 54
        while closetPiece[1] == None and i >= 12:
            if self.board.getTiles()[(i, self.pos[1])] == None:
                self.board.setIns((i, self.pos[1]))
            else: 
                closetPiece[1] = self.board.getTiles()[(i, self.pos[1])]
                if currentPiece.getColor() != closetPiece[1].getColor():
                    self.board.setIns((i, self.pos[1]))
            i -= 54        

    def checkCollide(self,mPos):
        if mPos[0] >= self.pos[0] and mPos[0] <= (self.pos[0]+45):
            if mPos[1] >= self.pos[1] and mPos[1] <= (self.pos[1]+45): 
                return True
        return False
    
    def checkInRange(self, pos, minX, maxX, minY, maxY):
        if (pos[0] >= minX and pos[0] <= maxX and pos[1] >= minY and pos[1] <= maxY):
            return True
        else:
            return False
    
    def draw(self):
        self.surface.blit(self.img,self.pos)
    
    def getState(self):
        return self.state
    
    def setState(self,state):
        self.state = state
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos):
        self.pos = pos
    
    def getRect(self):
        return self.rect
    
    def getColor(self):
        return self.color

    def getScore(self):
        return self.value

class Horse(Chariot):
    def showValidMove(self,currentPiece):
        changes = [(2,1),(1,2),(-2,1),(1,-2)]
        for change in changes:
            self.checkValidMove(currentPiece,change)
    
    def checkValidMove(self, currentPiece, change):
        if change[0] >= 0 and change[1] >= 0:
            deltaX = 54
            deltaY = 58
        else:
            deltaX = -54
            deltaY = -58
        
        if change[0] == 2 or change[0] == -2:
            newPosX = self.pos[0] + deltaX
            if newPosX >= 12 and newPosX <= 444:
                if self.board.getTiles()[(newPosX, self.pos[1])] == None:
                    self.checkLTile(currentPiece,(newPosX,self.pos[1]),'x',deltaX)
        else:
            newPosY = self.pos[1] + deltaY
            if newPosY >= 18 and newPosY <= 540:
                if self.board.getTiles()[(self.pos[0], newPosY)] == None:
                    self.checkLTile(currentPiece,(self.pos[0], newPosY),'y',deltaY)
    
    def checkLTile(self,currentPiece,newPos,direction,change):
        if direction == 'x': #horizontally
            L1 = (newPos[0] + change, newPos[1] + 58)
            L2 = (newPos[0] + change, newPos[1] - 58)
        else:
            L1 = (newPos[0] + 54, newPos[1] + change)
            L2 = (newPos[0] - 54, newPos[1] + change)            
        
        color = currentPiece.getColor()
        if (L1[0] >= 12 and L1[0] <= 444 and L1[1] >= 18 and L1[1] <= 540):
            self.getLPos(color,L1)
        if (L2[0] >= 12 and L2[0] <= 444 and L2[1] >= 18 and L2[1] <= 540):
            self.getLPos(color,L2)
    
    def getLPos(self,color,pos):
        if self.board.getTiles()[pos] == None:
                self.board.setIns(pos)
        else:
            if color != self.board.getTiles()[pos].getColor():
                self.board.setIns(pos)  
                     
class Elephant(Chariot):
    def showValidMove(self,currentPiece):
        changes = [(1,1),(1,-1),(-1,1),(-1,-1)]
        for change in changes:
            self.checkValidMove(currentPiece,change)
    
    def checkValidMove(self,currentPiece,change):
        checkPos = (self.pos[0] + 54*change[0], self.pos[1] + 58*change[1])
        if self.checkInRange(checkPos,12,444,18,540):
            if self.board.getTiles()[checkPos] == None:
                self.checkElephantMove(change,currentPiece.getColor())
    
    def checkElephantMove(self,change,color):
        change = (change[0]*2,change[1]*2)
        pos = (self.pos[0] + 54*change[0], self.pos[1] + 58*change[1])
        if self.checkInRange(pos,12,444,18,540) and self.checkBorder(pos,color):
            if self.board.getTiles()[pos] == None:
                    self.board.setIns(pos)
            else:
                if color != self.board.getTiles()[pos].getColor():
                    self.board.setIns(pos)          
                    
    def checkBorder(self,pos,color):
        if color == 'black'and pos[1] > 250:
            return False
        elif color == 'red' and pos[1] < 308:
            return False
        else:
            return True
        
class Guard(Elephant):
    def showValidMove(self,currentPiece):
        Elephant.showValidMove(self,currentPiece)
    
    def checkValidMove(self,currentPiece,change):
        allowed = False
        checkPos = (self.pos[0] + 54*change[0], self.pos[1] + 58*change[1])
        color = currentPiece.getColor() 
        
        if color == 'black' and self.checkInRange(checkPos,174,282,18,134):
                allowed = True
        elif color == 'red' and self.checkInRange(checkPos,174,282,424,540):
                allowed = True
        
        if allowed == True and self.board.getTiles()[checkPos] == None :
            self.board.setIns(checkPos)
        elif allowed == True:
            if color != self.board.getTiles()[checkPos].getColor():
                self.board.setIns(checkPos)           
           
class King(Guard):
    def showValidMove(self,currentPiece):
        changes = [(1,0),(0,1),(-1,0),(0,-1)]
        for change in changes:
            self.checkValidMove(currentPiece,change)

class Cannon(Chariot):
    def showValidMove(self,currentPiece):
        Chariot.showValidMove(self,currentPiece)
    
    def checkMoveVertical(self,currentPiece):
        closetPiece = [None,None]
        i = self.pos[1] + 58 
        count = [0,0]
        while closetPiece[0] == None and i <= 540:
            if self.board.getTiles()[(self.pos[0],i)] == None:
                if count[0] == 0:
                    self.board.setIns((self.pos[0],i))
            else: 
                if count[0] == 1:
                    closetPiece[0] = self.board.getTiles()[(self.pos[0],i)]
                    if currentPiece.getColor() != closetPiece[0].getColor():
                        self.board.setIns((self.pos[0],i))
                else:
                    count[0] = 1
            i += 58
        
        i = self.pos[1] - 58 
        while closetPiece[1] == None and i >= 18:
            if self.board.getTiles()[(self.pos[0],i)] == None:
                if count[1] == 0:
                    self.board.setIns((self.pos[0],i))
            else: 
                if count[1] == 1:
                    closetPiece[1] = self.board.getTiles()[(self.pos[0],i)]
                    if currentPiece.getColor() != closetPiece[1].getColor():
                        self.board.setIns((self.pos[0],i))
                count[1] = 1
            i -= 58
    
    def checkMoveHorizontal(self,currentPiece):
        closetPiece = [None,None]
        count = [0,0]
        i = self.pos[0] + 54
        while closetPiece[0] == None and i <= 444:
            if self.board.getTiles()[(i, self.pos[1])] == None:
                if count[0] == 0:
                    self.board.setIns((i, self.pos[1]))
            else:
                if count[0] == 1:
                    closetPiece[0] = self.board.getTiles()[(i, self.pos[1])]
                    if currentPiece.getColor() != closetPiece[0].getColor():         
                        self.board.setIns((i, self.pos[1]))
                count[0] = 1
            i += 54
        
        i = self.pos[0] - 54
        while closetPiece[1] == None and i >= 12:
            if self.board.getTiles()[(i, self.pos[1])] == None:
                if count[1] == 0:
                    self.board.setIns((i, self.pos[1]))
            else:
                if count[1] == 1:
                    closetPiece[1] = self.board.getTiles()[(i, self.pos[1])]
                    if currentPiece.getColor() != closetPiece[1].getColor():
                        self.board.setIns((i, self.pos[1]))
                count[1] = 1
            i -= 54        
        

class Soldier(Chariot): #Chot
    def showValidMove(self,currentPiece):
        color = currentPiece.getColor()
        self.checkValidMove(currentPiece, color)

    def checkValidMove(self,currentPiece,color):
        if color == 'black':
            deltaY = 58
        else:
            deltaY = -58
        
        if currentPiece.getPos()[1] >= 308 and color == 'black':
            self.checkTilesHor(color)
            self.value = -2
        elif currentPiece.getPos()[1] <= 250 and color == 'red':
            self.checkTilesHor(color)
            self.value = 2
        self.checkTilesVert(deltaY,color)
            
    
    def checkTilesHor(self, color):
        pos = self.pos
        start = pos[0]-54
        end = pos[0]+55
        if pos[0] == 12: #piece at the left end
            start = pos[0]+54
        if pos[0] == 444:#piece at the right end
            end = pos[0]
            
        for i in range (start, end, 108):
            if self.board.getTiles()[(i,pos[1])] == None:
                self.board.setIns((i,pos[1]))
            else:
                if color != self.board.getTiles()[(i,pos[1])].getColor():
                    self.board.setIns((i,pos[1]))
    
    def checkTilesVert(self, deltaY, color):   
        # Function to allow piece move deltaY tiles forward
        if self.pos[1] != 18 and self.pos[1] != 540:
            if self.board.getTiles()[(self.pos[0], self.pos[1]+deltaY)] == None:
                self.board.setIns((self.pos[0],self.pos[1]+deltaY))
            else:
                if color != self.board.getTiles()[(self.pos[0], self.pos[1]+deltaY)].getColor():
                    self.board.setIns((self.pos[0],self.pos[1]+deltaY))  


#Check chot(soldier) di ngang ngay goc trai va phai
# chot ben trai khong di ngang phai dc luc qua cau