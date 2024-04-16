import numpy as np
import pygame
import random
import math
def tile_checker(maze,tile):
    rows, cols = maze.shape
    check=True
    # for i in range(rows - 1):
    #     for j in range(cols - 1):
    #         if maze[i, j] == 0 and maze[i, j+1] == 0 and maze[i+1, j] == 0 and maze[i+1, j+1] == 0:
    #             check=False
    row,col=int(tile[0]),int(tile[1])
    neighbors=[]
    rows, cols = maze.shape
    if col < cols - 1:
        neighbors.append(maze[row, col + 1])
    if col > 0:
        neighbors.append(maze[row, col - 1])
    if row > 0:
        neighbors.append(maze[row - 1, col])
    if row < rows - 1:
        neighbors.append(maze[row + 1, col])
    zeros=neighbors.count(0)
    if zeros>1:
        check=False
    return check
#after each iteration, the probability to move towards end point increases of the path using this fn
def probs_change(probs,inc,size):
    for i in range(4):
        if i in inc:
            probs[i]+=0.02*8/(size+1)
            if probs[i]>0.5:
                probs[i]=0.4
        else:
            probs[i]-=0.02*8/(size+1)
            if probs[i]<0:
                probs[i]=0.1
    return probs
def path_generator(size,start,end):
    path_tiles=[]
    maze=np.ones((size,size))
    dirs=np.array([(end[0]-start[0])/abs(end[0]-start[0]),(end[1]-start[1])/abs(end[1]-start[1])])
    moves=[np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0])]
    probs=[]
    inc=[]
    count=0
    for i in range(4):
        if np.any(moves[i]==dirs):
            probs.append(0.1)
            inc.append(i)
        else :
            probs.append(0.4)
    probs_init=probs[:]
    tile=start[:]
    maze[int(tile[0]),int(tile[1])]=0
    while(tile[0]!=end[0] or tile[1]!=end[1]):
        x_edge=(tile[0]==0) or (tile[0]==size-1)
        y_edge=(tile[1]==0) or (tile[1]==size-1)
        if(x_edge and y_edge):
            maze=np.ones((size,size))
            probs=probs_init[:]
            tile=start[:]
            maze[int(tile[0]),int(tile[1])]=0
        else:
            cmoves=moves[:]
            cprobs=probs[:]
            while True:
                if(len(cmoves)==0):
                    maze=np.ones((size,size))
                    probs=probs_init[:]
                    tile=start[:]
                    maze[int(tile[0]),int(tile[1])]=0
                    break
                    # x,y=int(tile[0]),int(tile[1])
                    # maze[x,y]=1
                    # if maze[x-1,y]==0:
                    #     tile=maze[x-1,y]
                    #     break
                    # if maze[x+1,y]==0:
                    #     tile=maze[x+1,y]
                    #     break
                    # if maze[x,y-1]==0:
                    #     tile=maze[x,y-1]
                    #     break
                    # if maze[x,y+1]==0:
                    #     tile=maze[x,y+1]
                    #     break
                if(tile[0]/(size-1)==0):
                    move=np.array([-1,0])
                    index = next((i for i, arr in enumerate(cmoves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        cmoves.pop(index)
                        cprobs.pop(index)
                        i=0
                        for cmove in cmoves:
                            ntile=tile+cmove
                            if maze[int(ntile[0]),int(ntile[1])]==0:
                                cmoves.pop(i)
                                cprobs.pop(i)
                            i=i+1
                    choice=random.choices(cmoves,cprobs)[0]
                elif(tile[0]/(size-1)==1):
                    move=np.array([1,0])
                    index = next((i for i, arr in enumerate(cmoves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        cmoves.pop(index)
                        cprobs.pop(index)
                        i=0
                        for cmove in cmoves:
                            ntile=tile+cmove
                            if maze[int(ntile[0]),int(ntile[1])]==0:
                                cmoves.pop(i)
                                cprobs.pop(i)
                            i=i+1
                    choice=random.choices(cmoves,cprobs)[0]
                elif(tile[1]/(size-1)==0):
                    move=np.array([0,-1])
                    index = next((i for i, arr in enumerate(cmoves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        cmoves.pop(index)
                        cprobs.pop(index)
                        i=0
                        for cmove in cmoves:
                            ntile=tile+cmove
                            if maze[int(ntile[0]),int(ntile[1])]==0:
                                cmoves.pop(i)
                                cprobs.pop(i)
                            i=i+1
                    choice=random.choices(cmoves,cprobs)[0]
                elif(tile[1]/(size-1)==1):
                    move=np.array([0,1])
                    index = next((i for i, arr in enumerate(cmoves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        cmoves.pop(index)
                        cprobs.pop(index)
                        i=0
                        for cmove in cmoves:
                            ntile=tile+cmove
                            if maze[int(ntile[0]),int(ntile[1])]==0:
                                cmoves.pop(i)
                                cprobs.pop(i)
                            i=i+1
                    choice=random.choices(cmoves,cprobs)[0]
                else:
                    i=0
                    for cmove in cmoves:
                        ntile=tile+cmove
                        if maze[int(ntile[0]),int(ntile[1])]==0:
                            cmoves.pop(i)
                            cprobs.pop(i)
                        i=i+1
                    choice=random.choices(cmoves,cprobs)[0]
                tile[0]+=choice[0]
                tile[1]+=choice[1]
                already=False
                if(maze[int(tile[0]),int(tile[1])]==0):
                    already=True
                maze[int(tile[0]),int(tile[1])]=0
                index = next((i for i, arr in enumerate(cmoves) if np.array_equal(arr, choice)), -1)
                if index!=-1:
                    cmoves.pop(index)
                    cprobs.pop(index)
                if(tile_checker(maze,tile)):
                    probs=probs_change(probs,inc,size)
                    print(maze,'\n')
                    print(count)
                    count+=1
                    break
                else:
                    if(not already):
                        maze[int(tile[0]),int(tile[1])]=1
                    tile[0]-=choice[0]
                    tile[1]-=choice[1]
    return maze
def maze_generator(level):
    size=5+2*level
    start=np.array([(size-1)/2,(size-1)/2])
    vertex=random.randint(0,3)
    moves=(np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0]))
    end=np.array([0,0])
    if vertex==0:
        end=np.array([0,0])
    elif vertex==1:
        end=np.array([size-1,0])
    elif vertex==2:
        end=np.array([size-1,size-1])
    else:
        end=np.array([0,size-1])
    maze=path_generator(size,start,end)
    path=np.copy(maze)
    for i in range(10000):
        zeros=np.where(maze==0)
        poss_moves=[]
        rand_zero=random.randint(0,zeros[0].size-1)
        tile=np.array([zeros[0][rand_zero],zeros[1][rand_zero]])
        if((tile[0]/(size-1)==0 or tile[0]/(size-1)==1) and (tile[1]/(size-1)==0 or tile[1]/(size-1)==1)):
            continue
        elif(tile[0]/(size-1)==0):
            poss_moves=[0,1,2]
        elif(tile[0]/(size-1)==1):
            poss_moves=[0,2,3]
        elif(tile[1]/(size-1)==1):
            poss_moves=[1,2,3]
        elif(tile[1]/(size-1)==0):
            poss_moves=[0,1,3]
        else:
            poss_moves=[0,1,2,3]
        while(len(poss_moves)>0):
            move=random.choice(poss_moves)
            tile+=moves[move]
            already=False
            if maze[int(tile[0]),int(tile[1])]==0:
                already=True
            maze[int(tile[0]),int(tile[1])]=0
            if tile_checker(maze,tile):
                break
            else:
                if not already:
                    maze[int(tile[0]),int(tile[1])]=1
                tile-=moves[move]
                poss_moves.remove(move)
    endx,endy=int(end[0]),int(end[1])
    cendx,cendy=int(not(endx/(size-1)))*(size-1),int(not(endy/(size-1)))*(size-1)
    maze[endx,cendy]=1
    maze[cendx,cendy]=1
    maze[cendx,endy]=1
    return maze,path

pygame.init()
tile_size = 50
level=7
centre=np.array([2+level,2+level])
maze,path = maze_generator(level)
window_width = maze.shape[1] * tile_size
window_height = maze.shape[0] * tile_size
window = pygame.display.set_mode((window_width, window_height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(200,255,200)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(WHITE)
    for y in range(maze.shape[0]):
        for x in range(maze.shape[1]):
            if path[y, x] == 0:
                color = GREEN
            elif maze[y,x]==0:
                color = WHITE
            else:
                color=BLACK
            pygame.draw.rect(window, color, (x * tile_size, y * tile_size, tile_size, tile_size))
    pygame.draw.rect(window,BLUE, (centre[0] * tile_size, centre[1]* tile_size, tile_size, tile_size))
    pygame.display.update()
pygame.quit()