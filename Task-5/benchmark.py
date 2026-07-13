import threading
import time
import random
import matplotlib.pyplot as plt
import numpy as np

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

def sequential_dijkstra(graph, source):
    distances = [float('inf')] * graph.vertices
    distances[source] = 0
    heap = minHeap()
    heap.insert((0, source))
    while heap.heap:
        wt, curr = heap.delete()
        temp = graph.graph[curr]
        while temp:
            vertex = temp.vertex
            weight = temp.weight
            if wt + weight < distances[vertex]:
                distances[vertex] = wt + weight
                heap.insert((wt + weight, vertex))
            temp = temp.next
    return distances

def workerThread(graph, heap, distances, heap_cv, dist_lock):
    global active_count
    while True:
        with heap_cv:
            while not heap.heap and active_count > 0:
                heap_cv.wait()
            if not heap.heap and active_count == 0:
                break
            wt, curr = heap.delete()
            active_count += 1
        temp = graph.graph[curr]
        while temp:
            vertex = temp.vertex
            weight = temp.weight
            with dist_lock:
                if wt + weight < distances[vertex]:
                    distances[vertex] = wt + weight
                    with heap_cv:
                        heap.insert((wt + weight, vertex))
                        heap_cv.notify_all()
            temp = temp.next
        with heap_cv:
            active_count -= 1
            if not heap.heap and active_count == 0:
                heap_cv.notify_all()

def concurrent_dijkstra(graph, source, numThreads):
    global active_count 
    active_count = 0
    distances = [float('inf')] * graph.vertices
    distances[source] = 0
    heap = minHeap()
    heap.insert((0, source))
    heap_lock = threading.Lock() 
    heap_cv = threading.Condition(heap_lock) 
    dist_lock = threading.Lock() 
    threads = []
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

def generate_large_graph(v, p):
    g = Graph(v)
    for i in range(v):
        for j in range(v):
            if i != j and random.random() < p:
                g.add_edge(i, j, random.randint(1, 10))
    return g

if __name__ == "__main__":
    print("Generating network graph...")
    g = generate_large_graph(500, 0.10)
    
    start = time.perf_counter()
    seq_res = sequential_dijkstra(g, 0)
    t_seq = time.perf_counter() - start
    print(f"Sequential Execution Time: {t_seq:.6f} seconds\n")
    
    thread_counts = [1, 2, 4, 8]
    runtimes = []
    speedups = []
    
    print(f"{'Threads':<10} | {'Runtime (s)':<15} | {'Speedup Factor':<15}")
    print("-" * 46)
    
    for tc in thread_counts:
        start = time.perf_counter()
        con_res = concurrent_dijkstra(g, 0, tc)
        t_con = time.perf_counter() - start
        
        speedup = t_seq / t_con
        runtimes.append(t_con)
        speedups.append(speedup)
        
        print(f"{tc:<10} | {t_con:<15.6f} | {speedup:<15.4f}x")
        
    plt.figure(figsize=(8, 5))
    plt.plot(thread_counts, speedups, marker='o', linestyle='-', color='#e74c3c', linewidth=2, label='Observed Speedup')
    plt.plot(thread_counts, thread_counts, linestyle='--', color='#7f8c8d', label='Ideal Linear Scaling (Theoretical)')
    plt.xlabel('Thread Count (Background Processing Workers)')
    plt.ylabel('Speedup Factor (T_seq / T_concurrent)')
    plt.title('Task 3: Concurrency Framework Scalability Analysis')
    plt.xticks(thread_counts)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('speedup_vs_threads.png')
    plt.show()