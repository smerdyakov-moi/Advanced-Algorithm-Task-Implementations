import threading
import  time

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
