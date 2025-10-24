
def func4(sp, stat, n): 
    best_index=-1
    best_seats=10
    for i in range(len(sp)):
        current_seats=sp[i]
        current_status=stat[i]
        if(current_status=="0"):
            current_seats=abs(current_seats-n)
            if(best_index==-1 or current_seats<best_seats):
                best_index=i
                best_seats=current_seats                    
    return best_index
    
func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5 
func4([1, 0, 5, 1, 3], "10100", 4) # print 4 
func4([4, 6, 5, 8], "1000", 4) # print 2
print(func4([3, 1, 5, 4, 3, 2], "101000", 2))
print(func4([1, 0, 5, 1, 3], "10100", 4))
print(func4([4, 6, 5, 8], "1000", 4))