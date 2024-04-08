import numpy as np
import pygame
import random
import math
def tile_checker(maze):
    rows, cols = maze.shape

    for i in range(rows - 1):
        for j in range(cols - 1):
            if maze[i, j] == 0 and maze[i, j+1] == 0 and maze[i+1, j] == 0 and maze[i+1, j+1] == 0:
                return False
    
    return True
#after each iteration, the probability to move towards end point increases of the path using this fn
def probs_change(probs,inc,size):
    for i in range(4):
        if i in inc:
            probs[i]+=0.02*8/(size+1)
            if probs[i]>0.5:
                probs[i]=0.5
        else:
            probs[i]-=0.02*8/(size+1)
            if probs[i]<0:
                probs[i]=0
    return probs
#if the path reaches edge, it can only have 3 choices
def edge_choice(probs, move, moves):
    move=np.array(move)
    index = next((i for i, arr in enumerate(moves) if np.array_equal(arr, move)), None)
    fmoves=list(moves)
    fprobs=probs[:]
    fmoves.pop(index)
    fprobs.pop(index)
    return random.choices(fmoves, fprobs)[0]

def path_generator(size,start,end):
    maze=np.ones((size,size))
    dirs=np.array([(end[0]-start[0])/abs(end[0]-start[0]),(end[1]-start[1])/abs(end[1]-start[1])])
    moves=(np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0]))
    probs=[]
    inc=[]
    for i in range(4):
        if np.any(moves[i]==dirs):
            probs.append(0.1)
            inc.append(i)
        else :
            probs.append(0.4)
    probs_init=probs
    tile=start
    maze[int(tile[0]),int(tile[1])]=0
    while(np.all(tile==end)==False):
        if((tile[0]/(size-1)==0 or (tile[0]/(size-1)==1)) and (tile[1]/(size-1)==0 or tile[1]/(size-1)==1)):
            maze=np.ones((size,size))
            probs=probs_init
            tile=start
            maze[int(tile[0]),int(tile[1])]=0
        else:
            while True:
                if(tile[0]/(size-1)==0):
                    move=np.array([-1,0])
                    choice=edge_choice(probs,move,moves)
                elif(tile[0]/(size-1)==1):
                    move=np.array([1,0])
                    choice=edge_choice(probs,move,moves)
                elif(tile[1]/(size-1)==0):
                    move=np.array([0,-1])
                    choice=edge_choice(probs,move,moves)
                elif(tile[1]/(size-1)==1):
                    move=np.array([0,1])
                    choice=edge_choice(probs,move,moves)
                else:
                    choice=random.choices(list(moves),probs)[0]
                tile[0]+=choice[0]
                tile[1]+=choice[1]
                maze[int(tile[0]),int(tile[1])]=0
                if(tile_checker(maze)):
                    probs=probs_change(probs,inc,size)
                    break
                else:
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
    for i in range(0):
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
            maze[int(tile[0]),int(tile[1])]=0
            if tile_checker(maze):
                break
            else:
                maze[int(tile[0]),int(tile[1])]=1
                tile-=moves[move]
                poss_moves.remove(move)
    return maze

pygame.init()
tile_size = 50
maze = maze_generator(5)
window_width = maze.shape[1] * tile_size
window_height = maze.shape[0] * tile_size
window = pygame.display.set_mode((window_width, window_height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(WHITE)
    for y in range(maze.shape[0]):
        for x in range(maze.shape[1]):
            if maze[y, x] == 1:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(window, color, (x * tile_size, y * tile_size, tile_size, tile_size))
    pygame.display.update()
pygame.quit()
