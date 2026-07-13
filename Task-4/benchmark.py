import time
import matplotlib.pyplot as plt
import numpy as np

from h1 import generate_random_graph, greedy_equitable, get_num_colors, calculate_imbalance
from h2 import simulated_annealing

sizes = [50, 200, 500] 

print(f"{'Size (V)':<10} | {'Greedy Colors':<15} | {'Greedy Imbalance':<18} | {'SA Colors':<10} | {'SA Imbalance':<15} | {'Greedy (s)':<12} | {'SA (s)':<10}")
print("-" * 105)

greedy_times = []
sa_times = []
greedy_imbalances = []
sa_imbalances = []

for v in sizes:
    g = generate_random_graph(v, edge_prob=0.15)
    
    start = time.perf_counter()
    greedy_sol = greedy_equitable(g)
    t_greedy = time.perf_counter() - start
    
    g_cols = get_num_colors(greedy_sol)
    g_imb = calculate_imbalance(greedy_sol)
    
    greedy_times.append(t_greedy)
    greedy_imbalances.append(g_imb)
    
    start = time.perf_counter()
    sa_sol = simulated_annealing(g, greedy_sol, initial_temp=100.0, cooling_rate=0.85, iters_per_temp=100)
    t_sa = time.perf_counter() - start
    
    sa_cols = get_num_colors(sa_sol)
    sa_imb = calculate_imbalance(sa_sol)
    
    sa_times.append(t_sa)
    sa_imbalances.append(sa_imb)
    
    print(f"{v:<10} | {g_cols:<15} | {g_imb:<18} | {sa_cols:<10} | {sa_imb:<15} | {t_greedy:<12.6f} | {t_sa:<10.6f}")

x_indices = np.arange(len(sizes))
bar_width = 0.35
labels = [str(s) for s in sizes]

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#3498db'
color2 = '#e74c3c'

bars1 = ax1.bar(x_indices - bar_width/2, greedy_imbalances, bar_width, label='Greedy Imbalance', color=color1, alpha=0.7)
bars2 = ax1.bar(x_indices + bar_width/2, sa_imbalances, bar_width, label='Simulated Annealing Imbalance', color=color2, alpha=0.7)

ax1.set_xlabel('Graph Size (Vertices)')
ax1.set_ylabel('Imbalance (Max Class Size - Min Class Size)', color='#2c3e50')
ax1.set_title('Trade-off: Solution Quality vs Runtime in Equitable Graph Colouring')
ax1.set_xticks(x_indices)
ax1.set_xticklabels(labels)
ax1.tick_params(axis='y', labelcolor='#2c3e50')

ax2 = ax1.twinx()
color3 = '#2980b9'
color4 = '#c0392b'
ax2.plot(x_indices, greedy_times, color=color3, marker='o', linestyle='dashed', linewidth=2, label='Greedy Runtime (s)')
ax2.plot(x_indices, sa_times, color=color4, marker='s', linestyle='dashed', linewidth=2, label='SA Runtime (s)')
ax2.set_ylabel('Execution Time (Seconds) - Log Scale', color='#2c3e50')
ax2.tick_params(axis='y', labelcolor='#2c3e50')
ax2.set_yscale('log')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

plt.tight_layout()
plt.savefig('equitable_colouring_scaling.png')
plt.show()