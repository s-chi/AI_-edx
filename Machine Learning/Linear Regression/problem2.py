import sys
import math

inputfile = sys.argv[1]
outputfile = sys.argv[2]

def mean(lista):
    
    summ = 0
    count = 0
    
    for i in lista:
        
        summ += i
        count += 1.
        
    return summ/count

def stdev(lista, media):
    
    sqrterr = [(x - media) ** 2 for x in lista]
    
    return math.sqrt(mean(sqrterr))


with open(inputfile,'r') as f:
    
    inlines = f.readlines()
    
inmatrix = []
line = [0,0,0]
labels = []

for inline in inlines:
    
    line[0] = 1.
    line[1],line[2],label = [float(x) for x in inline.split(",")]
    labels.append(label)
    inmatrix.append(list(line))

transposed = map(list, zip(*inmatrix))
xlist = transposed[1]
ylist = transposed[2]

xmean = mean(xlist)
xdev = stdev(xlist,xmean)
ymean = mean(ylist)
ydev = stdev(ylist,ymean)

for row in inmatrix:
    
    row[1] = (row[1] - xmean)/xdev
    row[2] = (row[2] - ymean)/ydev

alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]

with open(outputfile,'w') as f:
    
    pass

for alp in alpha:
    
    beta = [0.0,0.0,0.0]
    
    for itind in xrange(0,100): 
        
        for j in xrange(0,3): 
            
            derR = 0
            
            for i in xrange(len(inmatrix)): 
                
                effe = 0
                
                for k in xrange(len(beta)):
                    
                    effe += inmatrix[i][k]*beta[k] 
                    
                derR += (effe - labels[i])*inmatrix[i][j]
            
            derR = derR/len(inmatrix)
            
            beta[j] = beta[j] - alp * derR
            
    with open(outputfile,'a') as f:
        
        f.write("%s,%s,%s,%s,%s\n" % (alp,100,beta[0],beta[1],beta[2]))
        
alp = 1.2

beta = [0.0,0.0,0.0]

for itind in xrange(0,25): 
        
    for j in xrange(0,3): 
        
        derR = 0
        
        for i in xrange(len(inmatrix)): 
            
            effe = 0
            
            for k in xrange(len(beta)):
                
                effe += inmatrix[i][k]*beta[k] 
                
            derR += (effe - labels[i])*inmatrix[i][j]
        
        derR = derR/len(inmatrix)
        
        beta[j] = beta[j] - alp * derR
        
with open(outputfile,'a') as f:
    
    f.write("%s,%s,%s,%s,%s\n" % (alp,25,beta[0],beta[1],beta[2]))


        

