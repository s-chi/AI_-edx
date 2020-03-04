from BaseAI import BaseAI
import time

rn1_4 = range(1,4)
rn12 = range(12)
rn4_16 = range(4,16)
rn15 = range(15)
rn1_16 = range(1,16)
rn16 = range(16)
rn4 = range(4)
rn3_m1_m1 = range(3,-1,-1)
rn3 = range(3)

freew = 4337
monow = 462
merw = 11523

class PlayerAI(BaseAI):

    def getMove(self, grid):
        
        startime = time.clock()
        maxdepth = 4
        boardv = tuple([item for sublist in grid.map for item in sublist])
        
        while time.clock() - startime < 0.2:
        
            hashtable_max = {}
            hashtable_min = {}
            maxdepth += 1
            resfin = maximize(boardv,  - float("inf"),  float("inf"), maxdepth, startime, hashtable_max, hashtable_min)
            
            if resfin == None:
                
                break
            
            movefin = resfin[0]
        
        return movefin


def maximize(boardv, alpha, beta, maxdepth, startime, hashtable_max, hashtable_min):
    
    if time.clock() - startime < 0.2:
        
        bohash = hash(boardv)
        
                        
        if hashtable_max.has_key(bohash):
            
            return hashtable_max[bohash]
    
        if maxdepth > 0:
            
            moves = getAvMovs(boardv)
        
            if moves:
            
                maxUtil = - float("inf")
                maxMove = None
            
                for i in moves:
                
                    res = minimize(mov(boardv,i), alpha, beta, maxdepth - 1, startime, hashtable_max, hashtable_min)
                    
                    if res == None:
                        
                        return None
                
                    if res > maxUtil:
                    
                        maxUtil = res
                        maxMove = i
                    
                        if maxUtil >= beta:
                    
                            break
                
                        if maxUtil > alpha:
                    
                            alpha = maxUtil
                    
                
                hashtable_max[bohash] = (maxMove, maxUtil)
                return (maxMove, maxUtil)
            
            else:
            
                rutil = eval_util(boardv)
                hashtable_max[bohash] = (None, rutil)                
                return (None, rutil)
            
        else:
            
            rutil = eval_util(boardv)
            hashtable_max[bohash] = (None, rutil)
            return (None, rutil)
        
    else:
        
        return None
        
def minimize(boardv, alpha, beta, maxdepth, startime, hashtable_max, hashtable_min):
    
    if time.clock() - startime < 0.2: 
        
        bohash = hash(boardv)
                        
        if hashtable_min.has_key(bohash):
            
            return hashtable_min[bohash]
        
        if maxdepth > 0:
            
            freecells = getAvCels(boardv)
            
            moves = [(x,y) for x in freecells for y in (2,4)]
            
            minUtil = float("inf")
        
            for i in moves:
            
                res = maximize(insTil(boardv,i[0],i[1]), alpha, beta, maxdepth - 1, startime, hashtable_max, hashtable_min)
                
                if res == None:
                
                    return None
            
                if res[1] < minUtil:
                
                    minUtil = res[1]
                
                    if minUtil <= alpha:
                
                        break
            
                    if minUtil < beta:
                    
                        beta = minUtil
                    
            hashtable_min[bohash] = minUtil
            return minUtil
            
        else:
            
            rutil = eval_util(boardv)
            hashtable_min[bohash] = rutil
            return rutil
    
    else:
        
        return None
    
def eval_util(boardv):
    
    mono = [0]*3
    monot = ((0,-1,-2,-3,1,0,-1,-2,2,1,0,-1,3,2,1,0),
             (3,2,1,0,2,1,0,-1,1,0,-1,-2,0,-1,-2,-3),
             (-3,-2,-1,0,-2,-1,0,1,-1,0,1,2,0,1,2,3))
    mer = 0
    free = 0
    
    for i in rn16:
        
        
        if (boardv[i] == 0):
            
            free += 1
        
        for j in rn3:
            
            mono[j] += boardv[i] * monot[j][i]
        
    
    
    for i in rn1_4:
        
        i4 = 4 * i
        im1 = i - 1
        i4m4 = i4 - 4
        
        if boardv[i4] == boardv[i4m4] and boardv[i4] != 0:
            
            mer += 1
            
        if boardv[i] == boardv[im1] and boardv[i] != 0:
            
            mer += 1;
        
        for j in rn1_4:
            
            ind = i4 + j;
            indm1 = ind - 1;
            indm4 = ind - 4;
            
            
            if boardv[ind] != 0:
            
                if boardv[ind] == boardv[indm4]:
        
                    mer += 1;
                
                if boardv[ind] == boardv[indm1]:
                
                    mer += 1;
    
    
    return  max(boardv) + freew * free + merw * mer + monow * max(mono)

def getAvMovs(boardv):
    
    moves = []
    
    for i in rn12:
        if boardv[i]==0:
            if boardv[i+4]!=0:
                moves.append(0)
                if i // 4 > 0:
                    if boardv[i-4]!=0:
                        moves.append(1)
                        if i % 4 < 3:
                            if boardv[i+1]!=0:
                                moves.append(2)
                                if i % 4 > 0:
                                    if boardv[i-1]!=0:
                                        moves.append(3)            
                break
        elif boardv[i] == boardv[i + 4]:
            moves.append(0)
            moves.append(1)
            break
        
    if 1 not in moves:
        for i in rn4_16:
            if boardv[i]==0 and boardv[i-4]!=0:
                moves.append(1)
                if i % 4 < 3:
                    if boardv[i+1]!=0:
                        moves.append(2)
                        if i % 4 > 0:
                            if boardv[i-1]!=0:
                                moves.append(3)
                break
                
    if 2 not in moves:
        for i in rn15:
            if boardv[i]==0:
                if i % 4 < 3:
                    if boardv[i+1]!=0:
                        moves.append(2)
                        if i % 4 > 0:
                            if boardv[i-1]!=0:
                                moves.append(3)
                        break
            elif i % 4 < 3:
                if boardv[i] == boardv[i + 1]:
                    moves.append(2)
                    moves.append(3)
                    break
                
    if 3 not in moves:
        for i in rn1_16:
            if boardv[i]==0:
                if i % 4 > 0:
                    if boardv[i-1]!=0:
                        moves.append(3)
                        break  
    return moves

def getAvCels(boardv):
    
    cels = []
    
    for i in rn16:
        if boardv[i] == 0:
            cels.append(i)
    
    return cels

def insTil(boardv, cel, val):
    
    newboardv = boardv[:cel] + (val,) + boardv[cel + 1:]
    
    return newboardv

def mov(boardv, dr):
    
    boardl = [0] * 16
    
    
    if dr == 0:
        
        for coli in rn4:
            index = coli
            for rowi in rn4:
                bind = 4 * rowi + coli
                if boardl[index] == 0:
                    boardl[index] = boardv[bind]
                elif boardl[index] == boardv[bind]:
                    boardl[index] *= 2
                    index += 4
                else:
                    index += 4
                    boardl[index] = boardv[bind]                
        
    elif dr == 1:
        
        for coli in rn4:
            index = 12 + coli
            for rowi in rn3_m1_m1:
                bind = 4 * rowi + coli
                if boardl[index] == 0:
                    boardl[index] = boardv[bind]
                elif boardl[index] == boardv[bind]:
                    boardl[index] *= 2
                    index -= 4
                else:
                    index -= 4
                    boardl[index] = boardv[bind]
        
        
    elif dr == 2:
        
        for rowi in rn4:
            index = 4 * rowi
            for coli in rn4:
                bind = 4 * rowi + coli
                if boardl[index] == 0:
                    boardl[index] = boardv[bind]
                elif boardl[index] == boardv[bind]:
                    boardl[index] *= 2
                    index += 1
                else:
                    index += 1
                    boardl[index] = boardv[bind]
        
    elif dr ==3:
        
        for rowi in rn4:
            index = 4*rowi + 3
            for coli in rn3_m1_m1:
                bind = 4 * rowi + coli
                if boardl[index] == 0:
                    boardl[index] = boardv[bind]
                elif boardl[index] == boardv[bind]:
                    boardl[index] *= 2
                    index -= 1
                else:
                    index -= 1
                    boardl[index] = boardv[bind]
                    
                    
    return tuple(boardl)



        
        
        
        
        
        
        
