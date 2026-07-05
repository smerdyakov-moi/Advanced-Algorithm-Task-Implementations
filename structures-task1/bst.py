#1. Defining the city's class
class City:
    def __init__(self,id,coord,popn): 
        self.id = id
        self.coord = coord
        self.popn = popn

#Coordinates are stored in [x,y] linear array whereas id and popn are just integers


#2. Implementation of BST
class Node:
    def __init__(self,city: City):
        self.city = city
        self.left = None
        self.right = None


def insertNode(ptr,city): #passing the city object to the node for Node.city to store it for  future referencing
    if(ptr == None): return Node(city)
    
    if(city.id<ptr.city.id): ptr.left = insertNode(ptr.left,city)
    elif(city.id>ptr.city.id): ptr.right = insertNode(ptr.right,city)
    
    return ptr

def getPredecessor(ptr):
    ptr = ptr.left
    while(ptr != None and ptr.right != None):
        ptr = ptr.right
    
    return ptr

def deleteNode(root,id):
    if(root == None): return root
    if(root.city.id>id):  root.left = deleteNode(root.left,id)
    if(root.city.id<id): root.right = deleteNode(root.right,id)
    else:
        if(root.left == None):
            return root.right
        elif(root.right == None):
            return root.left
        else:
            predecessor = getPredecessor(root) 
            root.city = predecessor.city #one-way swapping the value i.e. storing the predecessor in the TBD node
            root.left = deleteNode(root.left,predecessor.city.id) #since the TBD node is storing the predecessor value, we remove
            #the predecessor node
        
    return root

root = None