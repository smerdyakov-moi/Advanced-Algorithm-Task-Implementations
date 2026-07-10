#Simulated Annealing
import random
import math
from h1 import get_num_colors, calculate_imbalance


def objective_function(colors):
    # Minimiziing total colors primarily and color imbalance secondarilys
    return (get_num_colors(colors) * 100) + calculate_imbalance(colors)

def simulated_annealing(g, initial_colors, initial_temp=100.0, cooling_rate=0.95, iters_per_temp=50):
    current_colors = list(initial_colors)
    best_colors = list(initial_colors)
    
    current_energy = objective_function(current_colors)
    best_energy = current_energy
    
    temp = initial_temp
    
    while temp > 0.1:
        for _ in range(iters_per_temp):
            # Propose a neighbor state: change color of a random vertex
            u = random.randint(0, g.vertices - 1)
            old_color = current_colors[u]
            
            # Finding neighbor colors
            neighbor_colors = set()
            temp_node = g.graph[u]
            while temp_node:
                v = temp_node.vertex
                neighbor_colors.add(current_colors[v])
                temp_node = temp_node.next
            
            # New valid color
            max_c = max(current_colors)
            valid_alternatives = [c for c in range(max_c + 2) if c not in neighbor_colors and c != old_color]
            
            if not valid_alternatives:
                continue
                
            new_color = random.choice(valid_alternatives)
            
            # Apply proposed change
            current_colors[u] = new_color
            new_energy = objective_function(current_colors)
            
            # If condition to decide whether to accept the change or not
            if new_energy < current_energy:
                current_energy = new_energy
                if new_energy < best_energy:
                    best_energy = new_energy
                    best_colors = list(current_colors)
            else:
                delta = new_energy - current_energy
                acceptance_probability = math.exp(-delta / temp)
                if random.random() < acceptance_probability:
                    current_energy = new_energy
                else:
                    current_colors[u] = old_color
                    
        temp *= cooling_rate
        
    return best_colors