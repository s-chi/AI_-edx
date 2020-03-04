#!/usr/bin/python

import sys
import math
import resource
import time
start_time = time.time()

memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0

start = sys.argv[2].split(',')
n = int(math.sqrt(len(start)))

goal = list(start)
goal.sort()

fringe = [start]

max_search_depth = 0

startnum = int(''.join(start))
checkset = {startnum}

positions = [[0,0]]

def hcost( state, dim ) :
    cost = 0
    state = map(int, state)
    for i in range(1, dim**2):
        ind = state.index(i)
        cost += abs(ind % dim - i % dim) + abs(ind // dim - i // dim)
    return cost;


if sys.argv[1] == "bfs":
    
    while fringe:
        
        current = list(fringe[0])
        curpos = list(positions[0])
        del fringe[0]
        del positions[0]
        
        if current == goal:
            
            break
        
        else:
            
            ind = current.index('0')
            row = ind//n
            col = ind - n*row
            deeper = False
            if row > 0:
                temp = list(current)
                temp[ind] = temp[col + (row - 1)*n]
                temp[col + (row - 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4])
                    deeper = True
            if row < n-1:
                temp = list(current)
                temp[ind] = temp[col + (row + 1)*n]
                temp[col + (row + 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 1])
                    deeper = True
            if col > 0:
                temp = list(current)
                temp[ind] = temp[col - 1 + row*n]
                temp[col - 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 2])
                    deeper = True
            if col < n-1:
                temp = list(current)
                temp[ind] = temp[col + 1 + row*n]
                temp[col + 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 3])
                    deeper = True
            if deeper and curpos[0] + 1 > max_search_depth:
                max_search_depth = curpos[0] + 1
    
    
elif sys.argv[1] == "dfs":
    
    while fringe:
        
        current = fringe.pop()
        curpos = positions.pop()
        
        if current == goal:
            
            break
        
        else:
            
            ind = current.index('0')
            row = ind//n
            col = ind - n*row
            deeper = False
            if col < n-1:
                temp = list(current)
                temp[ind] = temp[col + 1 + row*n]
                temp[col + 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 3])
                    deeper = True
            if col > 0:
                temp = list(current)
                temp[ind] = temp[col - 1 + row*n]
                temp[col - 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 2])
                    deeper = True
            if row < n-1:
                temp = list(current)
                temp[ind] = temp[col + (row + 1)*n]
                temp[col + (row + 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 1])
                    deeper = True
            if row > 0:
                temp = list(current)
                temp[ind] = temp[col + (row - 1)*n]
                temp[col + (row - 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4])
                    deeper = True
            if deeper and curpos[0] + 1 > max_search_depth:
                max_search_depth = curpos[0] + 1
    
elif sys.argv[1] == "ast":
    
    fringecosts = [hcost(start, n)]
    fringeset = {startnum}
    
    while fringe:
        
        curcost = min(fringecosts)
        curind = fringecosts.index(curcost)
        current = list(fringe[curind])
        curpos = list(positions[curind])
        del fringecosts[curind]
        del fringe[curind]
        del positions[curind]
        tcurrent = int(''.join(current))
        fringeset.remove(tcurrent)
        
        if current == goal:
            
            break
        
        else:
            
            ind = current.index('0')
            row = ind//n
            col = ind - n*row
            deeper = False
            if row > 0:
                temp = list(current)
                temp[ind] = temp[col + (row - 1)*n]
                temp[col + (row - 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    fringeset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4])
                    fringecosts.append(curpos[0] + 1 + hcost(temp, n))
                    deeper = True
                elif ttemp in fringeset:
                    tempind = fringe.index(temp)
                    tempcost = curpos[0] + 1 + fringecosts[tempind] - positions[tempind][0]
                    if tempcost < fringecosts[tempind]:
                        fringecosts[tempind] = tempcost
                        positions[tempind][0] = curpos[0] + 1
                        positions[tempind][1] = curpos[1] * 4
                        deeper = True
                    
            if row < n-1:
                temp = list(current)
                temp[ind] = temp[col + (row + 1)*n]
                temp[col + (row + 1)*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    fringeset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 1])
                    fringecosts.append(curpos[0] + 1 + hcost(temp, n))
                    deeper = True
                elif ttemp in fringeset:
                    tempind = fringe.index(temp)
                    tempcost = curpos[0] + 1 + fringecosts[tempind] - positions[tempind][0]
                    if tempcost < fringecosts[tempind]:
                        fringecosts[tempind] = tempcost
                        positions[tempind][0] = curpos[0] + 1
                        positions[tempind][1] = curpos[1] * 4 + 1
                        deeper = True
                        
            if col > 0:
                temp = list(current)
                temp[ind] = temp[col - 1 + row*n]
                temp[col - 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    fringeset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 2])
                    fringecosts.append(curpos[0] + 1 + hcost(temp, n))
                    deeper = True
                elif ttemp in fringeset:
                    tempind = fringe.index(temp)
                    tempcost = curpos[0] + 1 + fringecosts[tempind] - positions[tempind][0]
                    if tempcost < fringecosts[tempind]:
                        fringecosts[tempind] = tempcost
                        positions[tempind][0] = curpos[0] + 1
                        positions[tempind][1] = curpos[1] * 4 + 2
                        deeper = True
                        
            if col < n-1:
                temp = list(current)
                temp[ind] = temp[col + 1 + row*n]
                temp[col + 1 + row*n] = '0'
                ttemp = int(''.join(temp))
                if ttemp not in checkset:
                    fringe.append(temp)
                    checkset.add(ttemp)
                    fringeset.add(ttemp)
                    positions.append([curpos[0] + 1, curpos[1] * 4 + 3])
                    fringecosts.append(curpos[0] + 1 + hcost(temp, n))
                    deeper = True
                elif ttemp in fringeset:
                    tempind = fringe.index(temp)
                    tempcost = curpos[0] + 1 + fringecosts[tempind] - positions[tempind][0]
                    if tempcost < fringecosts[tempind]:
                        fringecosts[tempind] = tempcost
                        positions[tempind][0] = curpos[0] + 1
                        positions[tempind][1] = curpos[1] * 4 + 3
                        deeper = True
                        
            if deeper and curpos[0] + 1 > max_search_depth:
                max_search_depth = curpos[0] + 1
    
depthind = curpos[0]
posind = curpos[1]
moves = []

while depthind > 0:
    
    locpos = posind % 4
    if   locpos == 0:
        moves.append('Up')
    elif locpos == 1:
        moves.append('Down')
    elif locpos == 2:
        moves.append('Left')
    elif locpos == 3:
        moves.append('Right')
        
    posind = posind // 4
    depthind -= 1
    
moves.reverse()

fo = open("output.txt", "w")

fo.write("path_to_goal: %s\n" % moves)
fo.write("cost_of_path: %s\n" % len(moves))
fo.write("nodes_expanded: %s\n" % (len(checkset) - len(fringe) - 1))
fo.write("search_depth: %s\n" % curpos[0])
fo.write("max_search_depth: %s\n" % max_search_depth)
fo.write("running_time: %.8f\n" % (time.time() - start_time))
fo.write("max_ram_usage: %.8f\n" % memory)

fo.close()
