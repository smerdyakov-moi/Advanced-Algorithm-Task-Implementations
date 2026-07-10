import time
import random
import matplotlib.pyplot as plt
import numpy as np

#Importing the data structures
import avl
import bst
import hashtable
import minheap

#Importing City class from anyone of these structures
from avl import City

#Random city generation to simulate the benchmarking process
def randomCitiesGen(n):
    cities = []
    ids = random.sample(range(1,1000000),n)
    for i in ids:
        x = random.uniform(-180,180)
        y = random.uniform(-90,90)
        popn = random.randint(5000,1000000)
        distance = random.uniform(1,400)
        cities.append(City(i, [x, y], popn, distance))
    return cities

#Defining the empirical testing with datasets of 100,1000, and 10000 data nodes
sizes = [100,1000,10000]

print(f"{'Structure':<12} | {'Size':<6} | {'Insert (s)':<12} | {'Search (s)':<12} | {'Delete (s)':<12}")
print("-" * 65)

bst_ins_times, bst_sea_times, bst_del_times = [], [], []
avl_ins_times, avl_sea_times, avl_del_times = [], [], []
heap_ins_times, heap_del_times = [], []
ht_ins_times, ht_sea_times, ht_del_times = [], [], []

for i in sizes:
    cities = randomCitiesGen(i)

    #Picking a random sample of 50 ids for search/delete operation performance
    sample_cities = random.sample(cities,50)
    sample_ids = [c.id for c in sample_cities] #Generates a list/array of random city IDs

    #A. BST Benchmarking
    
    #1. Insert
    bst_root = None
    start = time.perf_counter()
    for c in cities:
        bst_root = bst.insertNode(bst_root,c)
    bst_ins = time.perf_counter() - start #Calculates running time of insertion operation
    bst_ins_times.append(bst_ins)

    #2. Search
    start = time.perf_counter()
    for id in sample_ids:
        bst.search(bst_root,id)
    bst_sea = time.perf_counter() - start #Calculates running time of search operations
    bst_sea_times.append(bst_sea)

    #3. Delete
    start = time.perf_counter()
    for id in sample_ids:
        bst.deleteNode(bst_root,id)
    bst_del = time.perf_counter() - start #Calculates running time of delete operation
    bst_del_times.append(bst_del)

    print(f"{'BST':<12} | {i:<6} | {bst_ins:<12.6f} | {bst_sea:<12.6f} | {bst_del:<12.6f}")

    
    #B. AVL Benchmarking
    
    #1. Insert
    avl_root = None
    start = time.perf_counter()
    for c in cities:
        avl_root = avl.insertNode(avl_root,c)
    avl_ins = time.perf_counter() - start #Calculates running time of insertion operation
    avl_ins_times.append(avl_ins)

    #2. Search
    start = time.perf_counter()
    for id in sample_ids:
        avl.search(avl_root,id)
    avl_sea = time.perf_counter() - start #Calculates running time of search operations
    avl_sea_times.append(avl_sea)

    #3. Delete
    start = time.perf_counter()
    for id in sample_ids:
        avl.deleteNode(avl_root,id)
    avl_del = time.perf_counter() - start #Calculates running time of delete operation
    avl_del_times.append(avl_del)

    print(f"{'AVL':<12} | {i:<6} | {avl_ins:<12.6f} | {avl_sea:<12.6f} | {avl_del:<12.6f}")


    #C. Min Heap Benchmarking
    
    #1. Insert
    heap = minheap.minHeap()
    start = time.perf_counter()
    for c in cities:
        heap.insert(c)
    heap_ins = time.perf_counter() - start
    heap_ins_times.append(heap_ins)


    #2. Delete
    start = time.perf_counter()
    for _ in range(50):
        heap.delete()
    heap_del = time.perf_counter() - start
    heap_del_times.append(heap_del)

    #Min Heap doesn't have a dedicated search operation because they are built for rapid access to the abs min in the heap.
    print(f"{'Min-Heap':<12} | {i:<6} | {heap_ins:<12.6f} | {'N/A':<12} | {heap_del:<12.6f}")


    #D. Hash Table Benchmarking
    
    ht = hashtable.hashTable(i*2) # We do this so the hash table doesn't get crowded. This is called managing
                            #the load factor. Doubling the size of the table'll ensure plenty of open space for O(1)
                            #insert and search operations.
                    
    #1. Insert
    start = time.perf_counter()
    for c in cities:
        ht.insert(c)
    ht_ins = time.perf_counter() - start
    ht_ins_times.append(ht_ins)

    #2. Search
    start = time.perf_counter()
    for id in sample_ids:
        ht.search(id)   
    ht_sea = time.perf_counter() - start
    ht_sea_times.append(ht_sea)
    
    #3. Delete
    start = time.perf_counter()
    for id in sample_ids:
        ht.delete(id)
    ht_del = time.perf_counter() - start
    ht_del_times.append(ht_del)

    print(f"{'Hash Table':<12} | {i:<6} | {ht_ins:<12.6f} | {ht_sea:<12.6f} | {ht_del:<12.6f}")

x_indices = np.arange(len(sizes))
bar_width = 0.2
labels = [str(s) for s in sizes]

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(x_indices - 1.5 * bar_width, bst_ins_times, bar_width, label='BST', color='#3498db')
ax1.bar(x_indices - 0.5 * bar_width, heap_ins_times, bar_width, label='Min-Heap', color='#2ecc71')
ax1.bar(x_indices + 0.5 * bar_width, ht_ins_times, bar_width, label='Hash Table', color='#f1c40f')
ax1.bar(x_indices + 1.5 * bar_width, avl_ins_times, bar_width, label='AVL', color='#e74c3c')
ax1.set_xlabel('Dataset Size (N)')
ax1.set_ylabel('Time (Seconds) - Log Scale')
ax1.set_title('Insertion Performance Scaling')
ax1.set_xticks(x_indices)
ax1.set_xticklabels(labels)
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, which="both", ls="--", alpha=0.3)
plt.tight_layout()
plt.savefig('chart_insertion.png')

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(x_indices - 1.0 * bar_width, bst_sea_times, bar_width, label='BST', color='#3498db')
ax2.bar(x_indices + 0.0 * bar_width, ht_sea_times, bar_width, label='Hash Table', color='#f1c40f')
ax2.bar(x_indices + 1.0 * bar_width, avl_sea_times, bar_width, label='AVL', color='#e74c3c')
ax2.set_xlabel('Dataset Size (N)')
ax2.set_ylabel('Time (Seconds)')
ax2.set_title('Search Performance Scaling (Batch of 50)')
ax2.set_xticks(x_indices)
ax2.set_xticklabels(labels)
ax2.legend()
ax2.grid(True, ls="--", alpha=0.3)
plt.tight_layout()
plt.savefig('chart_search.png')

fig3, ax3 = plt.subplots(figsize=(8, 5))
ax3.bar(x_indices - 1.5 * bar_width, bst_del_times, bar_width, label='BST', color='#3498db')
ax3.bar(x_indices - 0.5 * bar_width, heap_del_times, bar_width, label='Min-Heap (Extract-Min)', color='#2ecc71')
ax3.bar(x_indices + 0.5 * bar_width, ht_del_times, bar_width, label='Hash Table', color='#f1c40f')
ax3.bar(x_indices + 1.5 * bar_width, avl_del_times, bar_width, label='AVL', color='#e74c3c')
ax3.set_xlabel('Dataset Size (N)')
ax3.set_ylabel('Time (Seconds) - Log Scale')
ax3.set_title('Deletion Performance Scaling (Batch of 50)')
ax3.set_xticks(x_indices)
ax3.set_xticklabels(labels)
ax3.set_yscale('log')
ax3.legend()
ax3.grid(True, which="both", ls="--", alpha=0.3)
plt.tight_layout()
plt.savefig('chart_deletion.png')

plt.show()