import sys
import pandas
import matplotlib.pyplot as plt

inputfile = sys.argv[1]
outputfile = sys.argv[2]

inp = pandas.read_csv(inputfile, names=['x','y','label'])


def effe(ex, ws):
    
    summ = ws[2] + ws[0] * ex[0] + ws[1] * ex[1]
    
    if summ > 0:
        
        return 1
    
    else:
        
        return -1


xpoints = [0,15]
ws = [0,0,0]

outlist = []

plt.ion()
fig, ax = plt.subplots()


while True:
    
    wsold = list(ws)

    for ind, row in inp.iterrows():
        
        if row[2] * effe(row, ws) <= 0:
            
            ws[0] += row[2] * row[0]
            ws[1] += row[2] * row[1]
            ws[2] += row[2]
            ypoints = [-(ws[2]+ws[0]*xx)/float(ws[1]) for xx in xpoints]
            ax.clear()
            s = ax.scatter(inp.x, inp.y, c=inp.label, cmap='bwr')
            plt.plot(xpoints,ypoints)            
            plt.draw()
            plt.pause(0.2)
            
    outlist.append(list(ws))
    if wsold == ws:
        
        break
    
outdf = pandas.DataFrame(outlist)
outdf.to_csv(outputfile, index=False, header=False)
            
        
        
    
    
    
    
    
        
