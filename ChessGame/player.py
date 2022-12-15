''' This is the version can't run because recursive call stack depth of python is limited'''

from chessPieces import *
import random

class chessEngine:
    def __init__(self,surface,board,piece):
        self.surface = surface
        self.board = board
        self.pieceList = piece.getPieces() #list of 32 pieces
        self.deleted = piece.getDeleted() # list of deleted pieces
        self.availMove = {}
        #dictionary of avail move - key=piece, value= list of availMove
        self.score = 0 # latest score of the game
        self.total = 0 # score updated for each evaluated move
        
        self.chosenMove = None
        self.chosentPiece = None
        
        self.secondStage = []
    

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
    
    def evaluateMove(self):
        tree, smallest = self.checkFirstStage()
        #print('print tree')
        tree.inorder()      
        
        if type(smallest.getValue()) == list: #has more than 1 smallest move
            self.checkSecondStage(smallest,True)
        else:
            self.checkSecondStage(smallest,False) 

        # neu random dinh 1 dua khong di duoc thi se error

    def checkFirstStage(self):
        tree = BinarySearchTree()
        #for key,value in self.availMove.items():  
        for piece, moves in self.availMove.items():
            for move in moves: #move = instruction obj
                # Check if that move bump into an existence piece
                if self.board.getTiles()[move.getPos()] != None:
                    defeatedPiece = self.board.getTiles()[move.getPos()]
                    defeatedValue = defeatedPiece.getScore()
                else:
                    defeatedPiece = None
                    defeatedValue = 0
                score = self.total - defeatedValue
                # Key is the score of each move
                tree.put(score,Move(piece,defeatedPiece,piece.getPos(),move.getPos()))
        # Get tree node of the best move (given smallest score)
        smallest = tree._findSmallest(tree.getRoot())
        return tree,smallest
        
        
    def checkSecondStage(self,smallest,multiple):
        # Return Move obj of the best movement
        # smallest = leftmost TreeNode
        key = smallest.getKey()
        # Update score temporarily
        self.score = key
        values = smallest.getValue() #move obj
        
        resultList = []
        scoreList = []   
        
        if multiple:
            # Have similar case
            #print('hihi',len(values),values)
            for i in range (len(values)):
                #print(1,self.board.getTiles())
                self.update(values[i])
               
                redList = self.getRedList()
                self.getAvailMove(redList)     
                #print('RL',len(redList))
                #print('avil',self.availMove)                

                #print(2,self.board.getTiles())
                # change self.availMove for red
                newResult, newScore = self.evaluateSecondStage(key)
                resultList.append(newResult)
                scoreList.append(newScore)
                #print(resultList)
                #print(scoreList)
                self.redoUpdate(values[i])
                #print(3,self.board.getTiles())
            # Compare among those solutions
            leastAffected = min(scoreList) # find lowest score
            index = scoreList.index(leastAffected) # find position of the lowest
            self.secondStage.append(leastAffected)
            if resultList[index]: #True means worse
                # check the upper tree node
                self.checkUpperTree(smallest)
            else:
                #keep everything as it is
                self.update(values[index])
        else: #Only 1 smallest move
            self.update(values)
            newResult, worstScore = self.evaluateSecondStage(key)
            scoreList.append(worstScore)
            self.secondStage.append(worstScore)
            if worstScore != key: #2nd te hon 
                self.redoUpdate(values)
                self.checkUpperTree(smallest)
            else:
                self.update(values)
                
    
    def checkUpperTree(self,smallest):
        if smallest.getLeft() == None and smallest.getRight() == None:
            newNode = smallest.getParent()
        elif smallest.getRight() != None:
            newNode = smallest.getRight()  
        elif smallest.getLeft() != None:
            newNode = smallest.getLeft()
        
        #self.update(newNode.getValue())
        if type(newNode.getValue()) == list:
            self.checkSecondStage(newNode,True)
        else:
            self.checkSecondStage(newNode,False) 
    
    def evaluateSecondStage(self,key):
        #Second stage -- red moves
        worse = False
        #print('key is',key)
        recentScore = key
        for piece, moves in self.availMove.items():
            for move in moves: #move = instruction obj
                # Check if that move bump into an existence piece
                chosen = True
                if self.board.getTiles()[move.getPos()] != None:
                    defeatedPiece = self.board.getTiles()[move.getPos()]
                    defeatedValue = defeatedPiece.getScore()
                    #print('df pos',move.getPos())
                    #print('defeated',defeatedPiece,defeatedValue)
                    
                    moveObj = Move(piece,defeatedPiece,piece.getPos(),move.getPos())
                    if self.checkThirdStage(moveObj):
                        chosen = False
                    self.redoUpdate(moveObj) # redo 3rd stage
                else:
                    defeatedPiece = None
                    defeatedValue = 0
                score = recentScore - defeatedValue # Red represents positive
                if score > key and chosen: 
                    key = score # get the worse outcome might happen
                    worse = True
        return worse, key # ton that nang nhat la bn
        
    
    def checkThirdStage(self,moveObj):
        # 1:Update movement of red obj in second stage
        # 2:Get new BlackList
        # 3:Get new AvailMove dictionary
        # 2:Find if that piece can be defeated -> return True/else False
        self.update(moveObj)
        blackList = self.getBlackList()
        tempDict = self.getAvailMove(blackList,True)
        for piece, moves in tempDict.items():
            for move in moves:
                if move.getPos() == moveObj.getNewPos(): #2nd lead to defeat
                    return True
        return False
    
    def update(self,movement):
        #movement is Move obj
        #movement = smallest.getValue()
        chosenMove = movement.getNewPos()
        chosenPiece = movement.getChosenPiece()
        #update movement
        if self.board.getTiles()[chosenMove] != None:
            self.pieceList.remove(self.board.getTiles()[chosenMove]) 
            self.deleted.append(self.board.getTiles()[chosenMove])
        self.board.getTiles()[chosenPiece.getPos()] = None
        chosenPiece.setPos(chosenMove)
        self.board.getTiles()[chosenMove] = chosenPiece
        self.total = self.score
    
    def redoUpdate(self,movement):
        #movement is Move obj
        #movement = smallest.getValue()
        chosenMove = movement.getNewPos()
        chosenPiece = movement.getChosenPiece()
        defeatedPiece = movement.getDefeatedPiece()
        #update movement
        if defeatedPiece != None:
            self.pieceList.append(defeatedPiece) 
            self.deleted.remove(defeatedPiece)
            self.total = self.score + defeatedPiece.getScore()  
        self.board.getTiles()[chosenMove] = defeatedPiece
        chosenPiece.setPos(movement.getPrevPos())
        self.board.getTiles()[chosenPiece.getPos()] = chosenPiece
              
    
    def getRedList(self):
        redList = []
        for piece in self.pieceList:
            if piece.getColor() == 'red':
                redList.append(piece)  
        return redList

    def getBlackList(self):
        blackList = []
        for piece in self.pieceList:
            if piece.getColor() == 'black':
                blackList.append(piece)  
        return blackList 


class Move:
    def __init__(self,chosenPiece,dfPiece,oldPos,newPos):
        self.chosenPiece = chosenPiece
        self.defeatedPiece = dfPiece
        self.prevPos = oldPos
        self.newPos = newPos
        self.score = None
    
    # All getters
    def getChosenPiece(self):     
        return self.chosenPiece
    def getDefeatedPiece(self):     
        return self.defeatedPiece    
    def getPrevPos(self):       
        return self.prevPos
    def getNewPos(self):        
        return self.newPos
    def getScore(self):     
        return self.score
    
    # All setters
    def setScore(self,score):
        self.score = score
