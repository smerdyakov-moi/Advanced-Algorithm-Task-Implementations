class City:
    def __init__(self,id,coord,popn,distance): 
        self.id = id
        self.coord = coord
        self.popn = popn
        self.distance = distance


class hashTable:
    def __init__(self,size):
        self.size = size
        self.table = [None for i in range(size)]
    
    def insert(self,city):
        index = city.id % self.size
        start = index #saving the entry point
        tombstone = None # Tombstone refers to a deleted entry/city. We assume it to be none at the beginning of any given operation

        while self.table[index] != None:
            if self.table[index] == "DELETED":
                if tombstone == None:
                    tombstone = index

            elif self.table[index].id == city.id: #Update operation not really necessary
                self.table[index] = city
                return
            
            index = (index+1)%self.size #circular wrapping to prevent infinite loop
            if (index==start):
                break 
    
        if tombstone != None:
            self.table[tombstone] = city
        else:
            self.table[index] = city
    

    def search(self, id):
        index = id % self.capacity
        start_index = index
        
        while self.table[index] is not None:
            if self.table[index] != "DELETED" and self.table[index].id == id:
                return self.table[index]
            index = (index + 1) % self.capacity
            if index == start_index:
                return None
        return None
        
    def delete(self, id):
        index = id % self.capacity
        start_index = index
        
        while self.table[index] is not None:
            if self.table[index] != "DELETED" and self.table[index].id == id:
                city = self.table[index]
                self.table[index] = "DELETED"
                return city
            index = (index + 1) % self.capacity
            if index == start_index:
                return None
        return None