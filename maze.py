#This is the file that generates random mazes
import numpy as np
import pygame
import random
import math
#read this after reading path_generator function
#this function checks if any loops are getting created when the path is being generated and returns a bool
def tile_checker(maze,tile):
    check=True
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
#read this after reading path_generator function
#after each iteration, the probability to move towards end point increases of the path using this function.
#the probabilities can be adjusted to increase or decrease the correct path length
def probs_change(probs,inc,size):
    #inc is an array that basically shows the 2 directions that is from start to end.
    #for example if start=(5,5) and end is (10,0), then inc contains indices of (1,0) and (0,-1)
    for i in range(4):
        if i in inc:
            probs[i]+=0.02*(8/(size+1))**2
            if probs[i]>0.5:
                probs[i]=0.35
        else:
            probs[i]-=0.02*(8/(size+1))**2
            if probs[i]<0:
                probs[i]=0.15
    return probs
#this function generates only one path from start to end.
#the algorithm uses probabilities to generate moves for the path
def path_generator(size,start,end):
    #initiliazes maze to all ones
    maze=np.ones((size,size))
    dirs=np.array([(end[0]-start[0])/abs(end[0]-start[0]),(end[1]-start[1])/abs(end[1]-start[1])])
    moves=[np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0])]
    probs=[]
    inc=[]
    #inc array stores one horizontal move and one vertical move to move closer to the end from start
    #for example if start=(5,5) and end is (10,0), then inc contains indices of (1,0) and (0,-1)
    #initialising probabilities for each move and the inc array
    for i in range(4):
        if np.any(moves[i]==dirs):
            probs.append(0.1)
            inc.append(i)
        else :
            probs.append(0.4)
    #storing the initial probabilities for future references
    probs_init=probs[:]
    tile=start[:]
    maze[int(tile[0]),int(tile[1])]=0
    #the algorithm designed simply uses a probablisitic approach from start to end.
    #the path starts from centre and moves while checking it doesnt form any loops in the maze
    # if the path enters the wrong corner(not end) or if the path doesnt have any move without forming loops,then the algorithm starts again
    while(tile[0]!=end[0] or tile[1]!=end[1]):
        #whiel loop runs until a move is found
        x_edge=(tile[0]==0) or (tile[0]==size-1)
        y_edge=(tile[1]==0) or (tile[1]==size-1)
        if(x_edge and y_edge):
            #checks if the path reached wrong corner(that is not the end)
            maze=np.ones((size,size))
            probs=probs_init[:]
            tile=np.array([(size-1)/2,(size-1)/2])
            maze[int(tile[0]),int(tile[1])]=0
        else:
            #creating current moves and probs, to remove moves that are not possible
            possible_moves=moves[:]
            possible_probs=probs[:]
            while True:
                if(len(possible_moves)==0):
                    #if there is no move without forming a loop, algorithm resets
                    maze=np.ones((size,size))
                    probs=probs_init[:] 
                    tile=np.array([(size-1)/2,(size-1)/2])
                    maze[int(tile[0]),int(tile[1])]=0
                    break
                #begin{handles edge tile cases}
                if(tile[0]/(size-1)==0):
                    move=np.array([-1,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                        i=0
                        #checks to not move back in the path
                        for current_move in possible_moves:
                            new_tile=tile+current_move
                            if maze[int(new_tile[0]),int(new_tile[1])]==0:
                                possible_moves.pop(i)
                                possible_probs.pop(i)
                            i=i+1
                    choice=random.choices(possible_moves,possible_probs)[0]
                elif(tile[0]/(size-1)==1):
                    move=np.array([1,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                        i=0
                        #checks to not move back in the path  
                        for current_move in possible_moves:
                            new_tile=tile+current_move
                            if maze[int(new_tile[0]),int(new_tile[1])]==0:
                                possible_moves.pop(i)
                                possible_probs.pop(i)
                            i=i+1
                    choice=random.choices(possible_moves,possible_probs)[0]
                elif(tile[1]/(size-1)==0):
                    move=np.array([0,-1])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                        i=0
                        #checks to not move back in the path
                        for current_move in possible_moves:
                            new_tile=tile+current_move
                            if maze[int(new_tile[0]),int(new_tile[1])]==0:
                                possible_moves.pop(i)
                                possible_probs.pop(i)
                            i=i+1
                    choice=random.choices(possible_moves,possible_probs)[0]
                elif(tile[1]/(size-1)==1):
                    move=np.array([0,1])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                        i=0
                        #checks to not move back in the path
                        for current_move in possible_moves:
                            new_tile=tile+current_move
                            if maze[int(new_tile[0]),int(new_tile[1])]==0:
                                possible_moves.pop(i)
                                possible_probs.pop(i)
                            i=i+1
                    choice=random.choices(possible_moves,possible_probs)[0]
                    #end{handled edge tile cases}                
                else:
                    #when not on a edge tile
                    i=0
                    #basically checks to not move back in the path
                    for current_move in possible_moves:
                        new_tile=tile+current_move
                        if maze[int(new_tile[0]),int(new_tile[1])]==0:
                            possible_moves.pop(i)
                            possible_probs.pop(i)
                        i=i+1
                    choice=random.choices(possible_moves,possible_probs)[0]
                tile[0]+=choice[0]
                tile[1]+=choice[1]
                #already is a variable to check if the tile is already open(0) and doesn't close it(1) if the path fails
                already=False
                if(maze[int(tile[0]),int(tile[1])]==0):
                     already=True
                maze[int(tile[0]),int(tile[1])]=0
                index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, choice)), -1)
                #removes the current move choice from possible moves for the next iteration
                if index!=-1:
                    possible_moves.pop(index)
                    possible_probs.pop(index)
                #loop ends if finally tile_checker is true
                if(tile_checker(maze,tile)):
                    probs=probs_change(probs,inc,size)
                    break
                else:
                    #else we move back to the original tile and iterate other moves
                    if(not already):
                        maze[int(tile[0]),int(tile[1])]=1
                    tile[0]-=choice[0]
                    tile[1]-=choice[1]
    return maze
def maze_generator(size):
    #this generates the remaining maze after the path is generated
    #randomly one of the tile is chosen and generates one more 0 tile neighbouring to it randomly without forming loops
    #this is iterated a lot of times, to create the maze :)
    #rest basically works like path_generator
    start=np.array([(size-1)/2,(size-1)/2])
    vertex=random.randint(0,3)
    moves=(np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0]))
    #randomly generating end as one of the corners, so people can't know beforehand,not even me :( 
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
    #finally setting the other corners to 1 so that only 1 end is point is left
    endx,endy=int(end[0]),int(end[1])
    complementary_endx,complementary_endy=int(not(endx/(size-1)))*(size-1),int(not(endy/(size-1)))*(size-1)
    maze[endx,complementary_endy]=1
    maze[complementary_endx,complementary_endy]=1
    maze[complementary_endx,endy]=1
    return maze,path
