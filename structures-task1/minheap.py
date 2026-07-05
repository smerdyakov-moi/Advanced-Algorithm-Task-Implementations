class City:
    def __init__(self,id,coord,popn,distance): 
        self.id = id
        self.coord = coord
        self.popn = popn
        self.distance = distance

class minHeap:
    def __init__(self):
        self.heap = []
        
    def swap(self,index,parent):
        temp = self.heap[index]
        self.heap[index] = self.heap[parent]
        self.heap[parent] = temp
    
    def insert(self,city):
        self.heap.append(city)
        self.sift_up(len(self.heap)-1)
    
    def sift_up(self,index):
        parent  = int((index-1)/2)
        while(index>0 and self.heap[index].distance<self.heap[parent].distance):
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

        if(left<size and self.heap[left].distance< self.heap[min].distance):
            min = left
        if(right<size and self.heap[right].distance < self.heap[min].distance):
            min = right
        
        if min!=index:
            self.swap(index,min)
            self.sift_down(min)

    def heap_sort(self):
        original = list(self.heap)
        sorted = []
        while (self.heap):
            deleted = self.delete()
            sorted.append(deleted)
        self.heap = original
        return sorted
