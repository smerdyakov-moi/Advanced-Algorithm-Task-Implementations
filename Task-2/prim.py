class Node:
    def __init__(self, data, weight=0):
        self.vertex = data
        self.weight = weight
        self.next = None


class graph:
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
        self.graph[source] = node


class minHeap:
    def __init__(self):
        self.heap = []

    def swap(self,index,parent):
        temp = self.heap[index]
        self.heap[index] = self.heap[parent]
        self.heap[parent] = temp
    
    def insert(self,value):
        self.heap.append(value)
        self.sift_up(len(self.heap)-1)
    
    def sift_up(self,index):
        parent  = int((index-1)/2)
        while(index>0 and self.heap[index][0] < self.heap[parent][0]):
            self.swap(index,parent)
            index = parent
            parent = int ((index-1)/2)
    
    def delete(self):
        if not self.heap:
            return None
        
        if len(self.heap) == 1 :
            return self.heap.pop()
        
        min = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.sift_down(0)
        return min

    def sift_down(self,index):
        left = 2*index+1
        right = 2*index+2
        min = index
        size = len(self.heap)

        if(left<size and self.heap[left][0]< self.heap[min][0]):
            min = left
        if(right<size and self.heap[right] [0]< self.heap[min][0]):
            min = right
        
        if min!=index:
            self.swap(index,min)
            self.sift_down(min)



def prim(graph,start):
    visited = [False] * graph.vertices #helps the algo keep track of visited nodes so we don't run into cycles
    mst_edges = [] #will store tuple of edges chosen in format: [parent,curr,weight]
    cost = 0

    heap = minHeap()
    heap.insert((0,start,-1)) # [weight,curr,parent] , we are prioritizing the weight here at index 0

    while heap.heap:
        weight,curr,parent = heap.delete()
        
        if visited[curr]:
            continue
        
        visited[curr] = True
        cost+=weight

        if (parent!=-1):
            mst_edges.append((parent,curr,weight))
        
        temp = graph.graph[curr]
    
        while temp:
            neighbor = temp.vertex
            edge_weight = temp.weight

            if not visited[neighbor]:
                heap.insert((edge_weight,neighbor,curr))
            temp = temp.next
        
    print("Total MST Cost: ", cost)
    print("Edges in MST: ")
    for u,v,w in mst_edges:
        print(f"{u} - {v} (Weight: {w})")


g = graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

prim(g, 0)