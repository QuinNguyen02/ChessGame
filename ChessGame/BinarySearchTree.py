class TreeNode:
    def __init__(self,key,value,left=None,right=None,parent=None):
        self.value = value
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
    
    def setValue(self,value): self.value = [value]
    def setKey(self,key): self.key = key
    def setParent(self,node): self.parent = node
    def setLeft(self,node): self.left = node
    def setRight(self,node): self.right = node
    
    def getValue(self): return self.value
    def getKey(self): return self.key
    def getParent(self): return self.parent
    def getRight(self): return self.right
    def getLeft(self): return self.left

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def getSize(self): return self.size
    def getRoot(self): return self.root
    
    def get(self,key):
        return self._get(key,self.root)
    def _get(self,key,current):
        if not current:
            return None
        elif current.getKey() == key:
            return current.getValue() 
        elif key < current.getKey():
            return self._get(key,current.getLeft())
        else:
            return self._get(key,current.getRight())
        
    def put(self,key,value):
        if not self.root:
            self.root = TreeNode(key,value)
            self.size += 1
        else:
            self._add(key,value,self.root)
    def _add(self,key,value,current):
        if key < current.getKey():
            if not current.getLeft(): # Left does not exist
                current.setLeft(TreeNode(key,value,parent=current))
                self.size += 1
            else:
                self._add(key,value,current.getLeft())
        elif key == current.getKey():
            if type(current.getValue()) != list:
                current.setValue(current.getValue()) #Change 1st val to list
            current.getValue().append(value)# Update value
        else:
            if not current.getRight(): # Right does not exist
                current.setRight(TreeNode(key,value,parent=current))
                self.size += 1
            else:
                self._add(key,value,current.getRight())
                

    def delete(self,key):
        if self.size > 1:
            nodeToRemove = self._locate(key,self.root)
            if nodeToRemove: #There is node with that key
                self._remove(nodeToRemove)
                self.size -= 1
            else:
                raise KeyError('Error, key not in the tree')
        elif self.size == 1 and self.root.getKey() == key:
            self.root = None
            self.size -= 1
        else: # Have one Node and it is not in the key/empty tree
            raise KeyError('Error, key not in the tree')
    
    def _locate(self,key,current):
        if not current: # Node is empty
            return None
        elif key  == current.getKey():
            return current
        elif key < current.getKey():
            return self._locate(key,current.getLeft())
        else:
            return self._locate(key,current.getRight())        
    
    def _remove(self,currentNode):
        parentNode = currentNode.getParent()
        leftNode = currentNode.getLeft()
        rightNode = currentNode.getRight()
        
        #first case: no child
        if leftNode == None and rightNode == None:
            if currentNode == parentNode.getLeft():
                parentNode.setLeft(None)
            else:
                parentNode.setRight(None)
        #second case: 1 child in left
        elif leftNode == None and rightNode:
            if parentNode == None: # The node to delete is the root
                self.root = rightNode
            elif currentNode == parentNode.getLeft():
                parentNode.setLeft(rightNode)
            else: 
                parentNode.setRight(rightNode)
            rightNode.setParent(parentNode)
        # Have one child in left
        elif leftNode and rightNode == None:
            if parentNode == None: # The node to delete is the root
                self.root = leftNode
            elif currentNode == parentNode.getLeft():
                parentNode.setLeft(leftNode)
            else: 
                parentNode.setRight(leftNode)
            leftNode.setParent(parentNode)   
        #third case: have two children
        else:
            swap = self._findSmallest(currentNode.getRight())
            currentNode.setKey(swap.getKey())
            currentNode.setValue(swap.getValue())
            self._remove(swap)
        
    def _findSmallest(self,currentNode):
        if currentNode.getLeft():
            return self._findSmallest(currentNode.getLeft())
        else:
            return currentNode
    
    def _findLargest(self,currentNode):
        if currentNode.getRight():
            return self._findLargest(currentNode.getRight())
        else:
            return currentNode
    
    def inorder(self):
        self._inorder(self.root)
    
    def _inorder(self,node):
        if node:
            self._inorder(node.getLeft())
            print(node.getKey(), node.getValue())
            self._inorder(node.getRight())


