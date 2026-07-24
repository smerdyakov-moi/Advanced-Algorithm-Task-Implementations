def assign_mice_to_holes(mice, holes):
    if len(mice) != len(holes):
        return -1
        
    mice.sort()
    holes.sort()
    max_time = 0
    
    for i in range(len(mice)):
        max_time = max(max_time, abs(mice[i] - holes[i]))
        
    return max_time

mice = [4, -4, 2]
holes = [4, 0, 5]

print(assign_mice_to_holes(mice, holes))