#Greedy Heuristic
import random
from collections import defaultdict

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

    def add_edge(self, source, destination, weight=0):
        if not self.allowed(source) or not self.allowed(destination):
            return

        # Since equitable graph coloring is undirected, we add edges in both directions
        node = Node(destination, weight)
        node.next = self.graph[source]
        self.graph[source] = node

        node = Node(source, weight)
        node.next = self.graph[destination]
        self.graph[destination] = node

#Random graph generation
def generate_random_graph(v, edge_prob=0.1):
    g = Graph(v)
    for i in range(v):
        for j in range(i + 1, v):
            if random.random() < edge_prob:
                g.add_edge(i, j)
    return g

def greedy_equitable(g):
    colors = [-1] * g.vertices
    color_counts = defaultdict(int)
    
    # Helper function for computing node degree via linked list traversal
    def get_degree(u):
        count = 0
        temp = g.graph[u]
        while temp:
            count += 1
            temp = temp.next
        return count

    # Sort vertices in descending order (reverse=True)
    vertices = sorted(range(g.vertices), key=get_degree, reverse=True)
    
    for u in vertices:
        # Traverse neighbors by walking down the custom linked list
        neighbor_colors = set()
        temp = g.graph[u]
        while temp:
            v = temp.vertex
            if colors[v] != -1:
                neighbor_colors.add(colors[v])
            temp = temp.next
        
        valid_colors = []
        if color_counts:
            max_c = max(color_counts.keys())
            for c in range(max_c + 1):
                if c not in neighbor_colors:
                    valid_colors.append(c)
        
        if not valid_colors:
            # Create a new color
            chosen_color = 0 if not color_counts else max(color_counts.keys()) + 1
        else:
            # Picking valid color with abs min current usage
            chosen_color = min(valid_colors, key=lambda c: color_counts[c])
            
        colors[u] = chosen_color
        color_counts[chosen_color] += 1
        
    return colors