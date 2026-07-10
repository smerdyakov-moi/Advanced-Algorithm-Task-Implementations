import time
import random

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

    #2. Search
    start = time.perf_counter()
    for id in sample_ids:
        bst.search(bst_root,id)
    bst_sea = time.perf_counter() - start #Calculates running time of search operations

    #3. Delete
    start = time.perf_counter()
    for id in sample_ids:
        bst.deleteNode(bst_root,id)
    bst_del = time.perf_counter() - start #Calculates running time of delete operation

    print(f"{'BST':<12} | {i:<6} | {bst_ins:<12.6f} | {bst_sea:<12.6f} | {bst_del:<12.6f}")

    
    #B. AVL Benchmarking
    
    #1. Insert
    avl_root = None
    start = time.perf_counter()
    for c in cities:
        avl_root = avl.insertNode(avl_root,c)
    avl_ins = time.perf_counter() - start #Calculates running time of insertion operation

    #2. Search
    start = time.perf_counter()
    for id in sample_ids:
        avl.search(avl_root,id)
    avl_sea = time.perf_counter() - start #Calculates running time of search operations

    #3. Delete
    start = time.perf_counter()
    for id in sample_ids:
        avl.deleteNode(avl_root,id)
    avl_del = time.perf_counter() - start #Calculates running time of delete operation

    print(f"{'AVL':<12} | {i:<6} | {avl_ins:<12.6f} | {avl_sea:<12.6f} | {avl_del:<12.6f}")


    


