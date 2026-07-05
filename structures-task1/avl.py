class City:
    def __init__(self,id,coord,popn,distance): 
        self.id = id
        self.coord = coord
        self.popn = popn
        self.distance = distance
        
class Node:
    def __init__(self,city: City):
        self.city = city
        self.left = None
        self.right = None

def height(root): #Useful for calculating the balance factor and rebalancing the tree
    if (root == None): return -1
    lheight = height(root.left)
    rheight = height(root.right)
    return max(lheight,rheight)+1      

def getBalance(ptr): #helper function  for calculating BF of each node
     if(ptr): return height(ptr.left) - height(ptr.right)
     return 0

#Rotations helper functions for performing necessary left/right rotations
def rightRotate (ptr):
     print('Rotating on:' ,ptr.city.id)
     x = ptr.left
     temp = x.right
     x.right = ptr
     ptr.left = temp
     return x

def leftRotate (ptr):
     print ('Rotating on:', ptr.city.id)
     x = ptr.right
     temp = x.left
     x.left = ptr
     ptr.right = temp
     return x

def insertNode(ptr,city):
    if (ptr == None): return Node(city)
     
    if (ptr.city.id>city.id): ptr.left = insertNode(ptr.left,city)
    elif(ptr.city.id<city.id): ptr.right = insertNode(ptr.right,city)

    balance = getBalance(ptr)

    if (balance >1 and getBalance(ptr.left) >= 0): #LL
         return rightRotate(ptr)
    
    if (balance <-1 and getBalance(ptr.right) <= 0): #RR
          return leftRotate(ptr)
    
    if (balance >1 and getBalance(ptr.left) < 0): #LR
         ptr.left = leftRotate(ptr.left)
         return rightRotate(ptr)
    
    if (balance <-1 and getBalance(ptr.right) > 0 ): #RL
         ptr.right = rightRotate (ptr.right)
         return leftRotate(ptr)

    return ptr

def getPredecessor(ptr):
    ptr = ptr.left
    while(ptr != None and ptr.right != None):
        ptr = ptr.right
    
    return ptr

def deleteNode(root, id):
    if(root == None): return root
    if(root.city.id > id):  
        root.left = deleteNode(root.left, id)
    elif(root.city.id < id): 
        root.right = deleteNode(root.right, id)
    else:
        if(root.left == None):
            return root.right
        elif(root.right == None):
            return root.left
        else:
            predecessor = getPredecessor(root) 
            root.city = predecessor.city 
            root.left = deleteNode(root.left, predecessor.city.id)

    balance = getBalance(root)

    if (balance > 1 and getBalance(root.left) >= 0): 
        return rightRotate(root)
    
    if (balance < -1 and getBalance(root.right) <= 0): 
        return leftRotate(root)
    
    if (balance > 1 and getBalance(root.left) < 0): 
        root.left = leftRotate(root.left)
        return rightRotate(root)
    
    if (balance < -1 and getBalance(root.right) > 0): 
        root.right = rightRotate(root.right)
        return leftRotate(root)
        
    return root

def search(root,id):
    if(root == None or root.city.id == id): return root
    if(root.city.id<id): return search(root.right,id)
    if(root.city.id>id): return search (root.left,id)