import sys
import driver

def curboard(domains):
    
    listb = []
    
    for dom in domains:
        
        if len(dom) != 1:
            
            listb.append(0)
            
        else:
            
            listb.append(dom[0])
        
    return listb

def print_as_table(listb):
    
    for i in range(0,9):
        
        sys.stdout.write("|")
        
        for j in range(0,9):
            
            sys.stdout.write("%s|" % listb[9*i+j])
            
        sys.stdout.write("\n")
        
    sys.stdout.write("\n")
    
def nlist(i):
    
    ls = [0]*81
    ls[i] = '*'
    for j in neighbours(i):
        
        ls[j] = '*'
        
    return ls 


with open('sudokus_start.txt', 'r') as f:
    
    starts = f.read().splitlines()
    
with open('my_finish.txt', 'w') as f:
    
    pass

#print starts[0]
    
for board in starts:
    
    driver.main(board)
    
    with open('output.txt', 'r') as f:
        
        with open('my_finish.txt', 'a') as f2:
            
            f2.write(f.readline() + "\n")
    
    
