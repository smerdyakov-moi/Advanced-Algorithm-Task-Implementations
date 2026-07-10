import time
import random
import matplotlib.pyplot as plt
import numpy as np

import dijkstra
import prim
import bellmanford

#Importing nodes and graphs from one of the algorithmic implementations
from dijkstra import Node
from dijkstra import Graph # Adjacent list implementation

#Random city generation to simulate the benchmarking process
def randomGraphGen(v, edge_factor=4):
    g = Graph(v)
    for i in range(v - 1):
        weight = random.randint(1, 40)
        g.add_edge(i, i + 1, weight)
    
    total_edges = v * edge_factor
    edges_added = v - 1
    while edges_added < total_edges:
        src = random.randint(0, v - 1)
        dest = random.randint(0, v - 1)
        if src != dest:
            weight = random.randint(1, 40)
            g.add_edge(src, dest, weight)
            edges_added += 1
    return g

#Defining the empirical testing with datasets of 100,1000, and 10000 data nodes
sizes = [100, 1000, 10000]

print(f"{'Size':<6} | {'Dijkstra (s)':<15} | {'Prim (s)':<15} | {'Bellman (s)':<15}")
print("-" * 60)

dijkstra_times = []
prim_times = []
bellman_times = []

for i in sizes:
    g = randomGraphGen(i, edge_factor=4)
    
    #1. Dijkstra Benchmarking
    start = time.perf_counter()
    dijkstra.dijkstra(g, 0)
    t_dijkstra = time.perf_counter() - start
    dijkstra_times.append(t_dijkstra)
    
    #2. Prim Benchmarking
    start = time.perf_counter()
    prim.prim(g, 0)
    t_prim = time.perf_counter() - start
    prim_times.append(t_prim)
    
    #3. Bellman-Ford Benchmarking
    start = time.perf_counter()
    bellmanford.bellman_ford(g)
    t_bellman = time.perf_counter() - start
    bellman_times.append(t_bellman)
    
    print(f"{i:<6} | {t_dijkstra:<15.6f} | {t_prim:<15.6f} | {t_bellman:<15.6f}")

x_indices = np.arange(len(sizes))
bar_width = 0.25
labels = [str(s) for s in sizes]

fig, ax = plt.subplots(figsize=(9, 6))
ax.bar(x_indices - bar_width, dijkstra_times, bar_width, label='Dijkstra', color='#3498db')
ax.bar(x_indices, prim_times, bar_width, label='Prim', color='#2ecc71')
ax.bar(x_indices + bar_width, bellman_times, bar_width, label='Bellman-Ford', color='#e74c3c')

ax.set_xlabel('Dataset Size (N)')
ax.set_ylabel('Time (Seconds) - Log Scale')
ax.set_title('Graph Algorithms Performance Scaling')
ax.set_xticks(x_indices)
ax.set_xticklabels(labels)
ax.set_yscale('log')
ax.legend()
ax.grid(True, which="both", ls="--", alpha=0.3)

plt.tight_layout()
plt.savefig('graph_algorithm_scaling.png')
plt.show()