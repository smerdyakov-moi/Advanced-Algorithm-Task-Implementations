class Node:
    def __init__(self, data, weight=0):
        self.vertex = data
        self.weight = weight
        self.next = None

class Graph:
    def __init__(self, size):
        self.vertices = size
        self.graph = [None] * self.vertices

    def allowed(self, src):
        if src < 0 or src >= self.vertices:
            return False
        return True

    def add_edge(self, source, destination, weight):
        if not self.allowed(source) or not self.allowed(destination):
            print("Index out of range")
            return

        node = Node(destination, weight)
        node.next = self.graph[source]
        self.graph[source] = node #indirected

def bellman_ford(graph):
    distances  = [float('inf')]*graph.vertices
    distances[0] = 0 #always taking source as 0 

    #Outer loop runs V-1 times
    for i in range(graph.vertices-1):
        for u in  range(graph.vertices):#traversing through all the edges in the adj list
            curr = graph.graph[u]
            while(curr!=None):
                v=curr.vertex
                weight=curr.weight
                #edge relaxation
                if (distances[u]!=float('inf') and distances[u]+weight<distances[v]):
                    distances[v] = weight + distances[u]
                curr=curr.next

    #Check for negative weight cycle
    for u in  range(graph.vertices):#traversing through all the edges in the adj list
            curr = graph.graph[u]
            while(curr!=None):
                v=curr.vertex
                weight=curr.weight
                #edge relaxation
                if (distances[u]!=float('inf')and distances[u]+weight<distances[v]):
                   print('Graph  contains a negative edge weighht cycle')
                   return None
                curr=curr.next
    
    return distances



#Taking example of a directed graph
g = Graph(6)
g.add_edge(0,1,10)
g.add_edge(0,5,8)
g.add_edge(5,4,1)
g.add_edge(4,3,-1)
g.add_edge(3,2,-2)
g.add_edge(2,1,1)
g.add_edge(1,3,2)
g.add_edge(4,1,-4)

print(bellman_ford(g))