import sys

def neighbours(i):
    
    rowind = i // 9
    colind = i % 9
    sqrowind = rowind // 3
    sqcolind = colind // 3
    neighs = []
    
    for j in range(0,9):
        
        newind = 9 * rowind + j
        
        if newind != i:#compare with elements in same row
            
            neighs.append(newind)
            
        newind = 9 * j + colind
        
        if newind != i:#compare with elements in same column
            
            neighs.append(newind)
            
    for j in range(0,3):#compare with elements in same subsquare
        
        newrowind = sqrowind * 3 + j
        
        if newrowind != rowind:
            
            for k in range(0,3):
                
                newcolind = sqcolind * 3 + k
                
                if newcolind != colind:
                    
                    newind = 9 * newrowind + newcolind
                    neighs.append(newind)
                    
    return neighs


def revised(domains, curarc):
    
    rev = False
    
    for x in domains[curarc[0]]:
        
        xcompat = False
        
        for y in domains[curarc[1]]:
            
            if y != x:
                
                xcompat = True
                break
        
        if not xcompat:
            
            domains[curarc[0]].remove(x)
            rev = True
            
    return rev


def ac3(domains):
    
    
    arcs = []
    
    for i in range(0,81):#populate arcs
        
        for j in neighbours(i):
            
            arcs.append((i,j))
                        
    while arcs:
    
        curarc = arcs[0]
        del arcs[0]
        
        if revised(domains, curarc):
            
            if domains[curarc[0]]:
                
                for j in neighbours(curarc[0]):
                    
                    if j != curarc[1]:
                        
                       arcs.append((j,curarc[0]))                 
                
            else:
                
                return False
            
    return True

def bts(domains):
    
    mindomlen = 10
    
    for i in range(0,81):
        
        domlen = len(domains[i])
        
        if domlen > 1:
            
            if domlen < mindomlen:
                
                mindomlen = domlen
                mindomi = i
                
        elif domlen == 0:
            
            return False
        
        elif domlen == 1:
            
            for z in neighbours(i):
                
                if domains[i][0] in domains[z]:
                    
                    domains[z].remove(domains[i][0])
        
    if mindomlen == 10:
        
        return domains
    
    else:
        
        for x in domains[mindomi]:
            
            newdomains = [y[:] for y in domains]
            newdomains[mindomi] = [x]
            
            for z in neighbours(mindomi):
                
                if x in newdomains[z]:
                    
                    newdomains[z].remove(x)
                    
            res = bts(newdomains)
            
            if res:
                
                return res
            
        return False

def solved(domains):
    
    for dom in domains:
        
        if len(dom) != 1:
            
            return False
        
    return True


def main(arg):
                
    board = list(arg)
    board = map(int, board)

    domains = []

    for elem in board:#populate domains
            
        if elem != 0:
            
            domains.append([elem])
            
        else:
            
            domains.append(range(1,10))
            
    for i in range(0,81):
        
        if len(domains[i]) == 1:
            
            for j in neighbours(i):
                
                if domains[i][0] in domains[j]:
                    
                    domains[j].remove(domains[i][0])
            
    domsac3 = [x[:] for x in domains]

    consistent = ac3(domsac3)

    if not consistent:
        
        print "Not consistent"
        #return False
        
    if solved(domsac3):
        
        with open('output.txt','w') as f:
            
            f.write(''.join(str(x) for dom in domsac3 for x in dom) + " AC3")
            
    else:
        
        final = bts(domains)
        
        if final:
            
            with open('output.txt','w') as f:
                
                f.write(''.join(str(x) for dom in final for x in dom) + " BTS")
                
        else:
            
            print "No solution found"
            #return False

    
if __name__ == "__main__":
    main(sys.argv[1])
    




