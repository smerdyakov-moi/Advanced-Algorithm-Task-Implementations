import threading
import time

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
        self.graph[source] = node

class minHeap:
    def __init__(self):
        self.heap = []
    
    def swap(self, index, parent):
        temp = self.heap[index]
        self.heap[index] = self.heap[parent]
        self.heap[parent] = temp
    
    def insert(self, value):
        self.heap.append(value)
        self.sift_up(len(self.heap)-1)

    def sift_up(self, index):
        parent = int((index-1)/2)
        while(index > 0 and self.heap[index][0] < self.heap[parent][0]):
            self.swap(index, parent)
            index = parent
            parent = int((index-1)/2)

    def delete(self):
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.sift_down(0)
        return min_val
    
    def sift_down(self, index):
        left = 2*index+1
        right = 2*index+2
        min_idx = index
        size = len(self.heap)

        if(left < size and self.heap[left][0] < self.heap[min_idx][0]):
            min_idx = left
        if(right < size and self.heap[right][0] < self.heap[min_idx][0]):
            min_idx = right
        
        if (min_idx != index):
            self.swap(min_idx, index)
            self.sift_down(min_idx)

def workerThread(graph, heap, distances, heap_cv, dist_lock):
    global active_count #defines how many threads are running

    while True:
        with heap_cv: #only continues when mutex lock is set to false for priority queue changes
            while not heap.heap and active_count > 0: #make  a thread wait if some other thread is actively in the middle
                    #of traversing other neighbors, this prevents false exits
                heap_cv.wait()
            
            if not heap.heap and active_count == 0: #validates actual completion
                break

            wt, curr = heap.delete()
            active_count += 1 #tracking how many threads working
            
        #after it exits out of the with  heap_cv, it immediately resolves the lock
        temp = graph.graph[curr]
        while temp:
            vertex = temp.vertex
            weight = temp.weight
            
            with dist_lock: #acquires a mutex lock to prevent race condition where threads might overwrite
                #exact same slots in distances array
                if wt + weight < distances[vertex]:
                    distances[vertex] = wt + weight
                    with heap_cv:
                        heap.insert((wt + weight, vertex))
                        heap_cv.notify_all()
            temp = temp.next
            
        with heap_cv:
            active_count -= 1
            if not heap.heap and active_count == 0:
                heap_cv.notify_all() # resolves threads stuck at heap_cv.wait(), telling them to continue as queu   e
                    #has been updated

# Base concurrent Dijkstra
def concurrent_dijkstra(graph, source, numThreads):
    global active_count 
    active_count = 0

    distances = [float('inf')] * graph.vertices
    distances[source] = 0

    heap = minHeap()
    heap.insert((0, source))

    heap_lock = threading.Lock() #mutex lock to guarantee priority queue structure
    heap_cv = threading.Condition(heap_lock) #  gives access to heap_lock for   wait() and notify_all()
    dist_lock = threading.Lock() #mutex lock for distances array``

    threads = []
    
    #Simple thread creation and thread termination s
    for _ in range(numThreads):
        t = threading.Thread(
            target=workerThread, 
            args=(graph, heap, distances, heap_cv, dist_lock)
        )
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()

    return distances

if __name__ == "__main__":
    g = Graph(7)
    g.add_edge(0, 1, 6)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 5)
    g.add_edge(1, 4, 2)
    g.add_edge(2, 1, 1)
    g.add_edge(2, 4, 4)
    g.add_edge(3, 5, 2)
    g.add_edge(4, 3, 1)
    g.add_edge(4, 5, 7)
    g.add_edge(5, 6, 3)

    result = concurrent_dijkstra(g, 0, 4)
    print("Concurrent Shortest Paths from Source 0: ", result)