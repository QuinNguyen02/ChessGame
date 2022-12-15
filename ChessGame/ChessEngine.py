from chessPieces import *
from BinarySearchTree import *
# key = score, value = piece obj moving
import random

class chessEngine:
    def __init__(self,surface,board,piece):
        self.surface = surface
        self.board = board
        self.pieceList = piece.getPieces()
        self.deleted = piece.getDeleted()
        self.availMove = {}
        #dictionary of avail move - key=piece, value= list of availMove
        self.score = 0
        self.total = 0
        self.defeatedPiece = None
        self.chosenMove = None
        self.chosenPiece = None
        self.kingPos = None #Keep track of black King
        
    def getKingPos(self):
        blackList = self.getColorList('black')
        for piece in blackList:
            if abs(piece.getScore()) == 100:
                self.kingPos = piece.getPos()        
    
    def getAvailMove(self,pieceList,demo = None):
        # Get available move of each piece in the given list
        if demo == True:
            tempDict = {}
            for piece in pieceList:
                piece.showValidMove(piece)
                tempDict[piece] = self.board.getIns().copy()
                self.board.refreshIns()
            return tempDict
        else:
            self.availMove.clear()
            for piece in pieceList:              
                piece.showValidMove(piece)
                self.availMove[piece] = self.board.getIns().copy()
                self.board.refreshIns() 
    
        self.total, self.score = self.calculateTotalScore(self.pieceList)
    
    def evaluateMove(self):
        self.getKingPos()
        # Reset each time its move
        updateNeed = True
        self.chosenPiece = None
        # Check if any black pieces are being in danger
        inDanger, tempBoard, rivals = self.checkBlackInDanger()
        if inDanger != None:
            demoScore = self.total - inDanger.getScore()
            #print(demoScore,'demoS')
            preventRival = False
        # Find all available moves of each piece and evaluate to find best move
        chosen = False  
        for piece, moves in self.availMove.items():
            for move in moves: #move = instruction obj
                # valid indicates new move worth more points in return
                valid = True
                # Check if that move bump into an existence piece
                if self.board.getTiles()[move.getPos()] != None:
                    defeatedPiece = self.board.getTiles()[move.getPos()]
                    defeatedValue = defeatedPiece.getScore()               
                else:
                    defeatedPiece = None
                    defeatedValue = 0
                
                score = self.total - defeatedValue
                
                if score < self.score:
                    # Check if that move leads to that piece being defeated next turn
                    prevPos = piece.getPos()
                    defeated, pointLoss = self.checkSecondStage(piece,move.getPos())
                    # Eliminate all move that lead to the Kind being defeated
                    if pointLoss == -100:
                        self.availMove[piece].remove(move)
                        valid = False
                    elif defeated:
                        self.availMove[piece].remove(move)
                        # check whether red loses more or black loses more
                        # if red still loses more -> still consider this move
                        if abs(pointLoss) > abs(defeatedValue): 
                            valid = False
                    self.redoUpdate(defeatedPiece,prevPos,move.getPos(),piece)
                            
                    if valid:   
                        self.score = score
                        self.chosenMove = move.getPos()
                        self.chosenPiece = piece
                        self.defeatedPiece = defeatedPiece
                        chosen = True
        
        # This is when we already found the best solution
        if inDanger != None and chosen:
            # check if rival is defeated or inDanger already moves
            if (self.defeatedPiece) in rivals or (self.chosenPiece is inDanger):
                preventRival = True        
                # what if many larger -> choose smallest ?
                # what if all equal to self.score -> randomly choosing
        
        # If has inDanger, has to help not randomly choosing
        if inDanger != None:     
            #print(demoScore,self.score,preventRival)
            if demoScore > self.score and not preventRival: #worst case if not help
                if self.rescueInDanger(inDanger, tempBoard, demoScore, rivals):
                    #true means already update
                    updateNeed = False
        
        # If none solution has been chosen
        #if self.chosenPiece == None:
        if not chosen and updateNeed:
            # Sorted in order of value of all pieces in descending order
            blackList = self.getColorList('black')
            blackList = sorted(blackList, key=lambda piece: piece.getScore(),reverse = False)
            # Prioritize moving pieces with high value except from the King
            if (len(blackList) > 7):
                newList = blackList[1:7]
            else:
                newList = blackList
            self.chosenPiece = random.choice(newList)        
            
            while len(list(self.availMove[self.chosenPiece])) == 0:
                newList.remove(self.chosenPiece)
                self.chosenPiece = random.choice(newList)    
            self.chosenMove = random.choice(list(self.availMove[self.chosenPiece])).getPos()   

        #update movement
        if updateNeed:
            self.update(self.chosenPiece,self.chosenMove)

    def rescueInDanger(self,inDanger, tempBoard, demoScore, rivals):
        # Try to find new position for inDanger to run away
        run = False
        blackList = self.getColorList('black')
        # find way to move inDanger
        inDanger.showValidMove(inDanger)
        validMoves = self.board.getIns().copy()
        self.board.refreshIns()
        prevPos = inDanger.getPos()
        # Check possible move without being defeated
        for move in validMoves:
            dfPiece = self.board.getTiles().get(move.getPos())
            result,score = self.checkSecondStage(inDanger,move.getPos())
            # To check if next move is not defeated -> choose
            if not result:
                self.score = demoScore
                self.chosenMove = move.getPos()
                self.chosenPiece = inDanger    
                run = True
            self.redoUpdate(dfPiece,prevPos,move.getPos(),inDanger)

        if not run: 
            #try to prevent if inDanger is the king
            if inDanger.getScore() == -100:
                if self.checkKingSafety(inDanger,rivals):
                    return True
                else:
                    return False
            else:
                return False
        else:
            # If can run, update by that new move
            self.update(self.chosenPiece,self.chosenMove)
            return True
                # Try to move other piece into to sacrifice instead 
                
    def checkKingSafety(self,inDanger,rival):
        # Return True if find and move a piece to protect the King
        for piece, moves in self.availMove.items():
            for move in moves: #move = instruction obj
                valid = True
                prevPos = piece.getPos()
                self.update(piece,move.getPos())
                rival[0].showValidMove(rival[0])
                rivalAvailMove = self.board.getIns().copy()
                self.board.refreshIns()                
                for movement in rivalAvailMove:
                    if movement.getPos() == inDanger.getPos():
                        valid = False
                        break
                if not valid:
                    self.redoUpdate(None,prevPos,move.getPos(),piece)
                else:
                    return True
        return False
    
    def checkBlackInDanger(self):
        # tempBoard store chess game
        #Key is position, value is all pieces that can move into that position
        redList = self.getColorList('red')
        blackList = self.getColorList('black')
        tempBoard = Tiles(self.surface).getTiles()
        for piece in redList:
            piece.showValidMove(piece)
            availMoves = self.board.getIns().copy()
            for move in availMoves:
                if tempBoard[move.getPos()] == None:
                    tempBoard[move.getPos()] = [piece]
                else:
                    
                    tempBoard[move.getPos()].append(piece) 
            self.board.refreshIns()
                   
        #Check if the pos of pieces in red list exist in tempBoard dictionary
        inDanger = None
        for piece in blackList: 
            if tempBoard.get(piece.getPos()) != None:
                if inDanger == None:
                    inDanger = piece
                else:
                    if abs(inDanger.getScore()) < abs(piece.getScore()):
                        inDanger = piece
                        
        if inDanger != None:
            rivals = tempBoard[inDanger.getPos()]
            # We just want to know if that piece is protected, so which piece doesnt matter
            prevPos = rivals[0].getPos()
            self.update(rivals[0],inDanger.getPos())
            # Return piece with highest value that are in danger
            # Check if inDanger is protected by another piece, inDanger's value < rival's value
            # Return true if it is protected -> dont need to rescue
            if not self.checkSafe(blackList,inDanger,rivals,prevPos):            
                return inDanger, tempBoard, rivals
        return None, None, None
    
    def checkSafe(self,blackList,inDanger,rivals,prevPos):
        #Get a temporary dic of avail move of each piece
        #Key is position, value is all pieces that can move into that position
        #Return True if another black piece can defeat the rival
        tempBoard = Tiles(self.surface).getTiles()
        for piece in blackList:
            piece.showValidMove(piece)
            availMoves = self.board.getIns().copy()
            for move in availMoves:
                if tempBoard[move.getPos()] == None:
                    tempBoard[move.getPos()] = [piece]
                else:
                    tempBoard[move.getPos()].append(piece) 
            self.board.refreshIns()         
        self.redoUpdate(inDanger,prevPos,inDanger.getPos(),rivals[0])
        
        redValuable = False
        score1 = abs(inDanger.getScore())
        for piece in rivals:
            if piece.getScore() >= score1:
                redValuable = True
            
        # Check if black piece can eat back and red attacker is more valuable than black eaten
        if tempBoard.get(inDanger.getPos()) != None and redValuable == True:
            return True
        else:
            return False
    
    def checkSecondStage(self,chosenPiece,newPos):
        # Function to check whether that move lead to the defeat of the king or itself
        # new pos is the position that black piece plan to move into
        # check if that move lead to the King being defeated
        kingDefeated = False
        pieceDefeated = False
        # check if that move lead to that piece being defeated
        self.update(chosenPiece,newPos)
        redList = self.getColorList('red')
        tempDict = self.getAvailMove(redList,True)
        # Check each possible move of the red piece responding to the demo move of black piece
        for piece, moves in tempDict.items():
            for move in moves:
                if move.getPos() == self.kingPos: 
                    kingDefeated  = True
                elif move.getPos() == newPos: #2nd lead to defeat
                    pieceDefeated = True
        
        if kingDefeated:
            return True,-100
        elif pieceDefeated:
            # if being defeated, black lose this amount of points
            #print('df',chosenPiece,chosenPiece.getScore())
            return True, chosenPiece.getScore() 
        else:
            return False, 0            
        
    def update(self,chosenPiece,chosenMove):
        #chosenMove is new move
        if self.board.getTiles()[chosenMove] != None:
            self.pieceList.remove(self.board.getTiles()[chosenMove]) 
            self.deleted.append(self.board.getTiles()[chosenMove])
        self.board.getTiles()[chosenPiece.getPos()] = None
        chosenPiece.setPos(chosenMove)
        self.board.getTiles()[chosenMove] = chosenPiece         
        #self.total = self.score  
        
    def redoUpdate(self,defeatedPiece,prevPos,currentPos,chosenPiece):
        if defeatedPiece != None:
            self.pieceList.append(defeatedPiece) 
            self.deleted.remove(defeatedPiece)
            #self.total = self.score + defeatedPiece.getScore()  
        self.board.getTiles()[currentPos] = defeatedPiece
        chosenPiece.setPos(prevPos)
        self.board.getTiles()[chosenPiece.getPos()] = chosenPiece                

    def getColorList(self,color):
        colorList = []
        for piece in self.pieceList:
            if piece.getColor() == color:
                colorList.append(piece)  
        return colorList  

    def calculateTotalScore(self,pieceList):
        total = 0
        for piece in pieceList:
            total += piece.getScore()
        return total,total