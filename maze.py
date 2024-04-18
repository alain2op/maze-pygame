#This is the file that generates random mazes
import numpy as np
import pygame
import random
import math
ITERATIONS=10000
PROBABILITY=0.01

#read this after reading path_generator function
#this function checks if any loops are getting created when the path is being generated and returns a bool
def translator(choice):
    moves=[np.array([0,1,0]),np.array([1,0,0]),np.array([0,-1,0]),np.array([-1,0,0]),np.array([0,0,1]),np.array([0,0,-1])]
    if np.array_equal(choice,moves[0]):
        #down
        return "D" 
    if np.array_equal(choice,moves[1]):
        #climb up
        return "C"
    if np.array_equal(choice,moves[2]):
        #up
        return "U"
    if np.array_equal(choice,moves[3]):
        #fall down
        return "F"
    if np.array_equal(choice,moves[4]):
        #right
        return "R"
    if np.array_equal(choice,moves[5]):
        #left
        return "L"
def tile_checker(maze,tile):
    check=True
    floor,col,row=int(tile[0]),int(tile[1]),int(tile[2])
    neighbors=[]
    floors,cols,rows = maze.shape
    if col < cols - 1:
        neighbors.append(maze[floor, col + 1,row])
    if col > 0:
        neighbors.append(maze[floor, col - 1,row])
    if floor > 0:
        neighbors.append(maze[floor - 1, col,row])
    if floor < floors - 1:
        neighbors.append(maze[floor + 1, col,row])
    if row < rows - 1:
        neighbors.append(maze[floor, col,row+1])
    if row > 0:
        neighbors.append(maze[floor, col,row-1])
    zeros=neighbors.count(0)
    if zeros>1:
        check=False
    return check
#read this after reading path_generator function
#after each iteration, the probability to move towards end point increases of the path using this function.
#the probabilities can be adjusted to increase or decrease the correct path length
def probs_change(probs,inc,moves):
    #inc is an array that basically shows the 2 directions that is from start to end.
    #for example if start=(5,5) and end is (10,0), then inc contains indices of (1,0) and (0,-1)
    for i in range(6):
        if i in inc:
            if moves[i][1]==0 and moves[i][2]==0:
                probs[i]+=0.005
                if probs[i]>0.18:
                    probs[i]=0.12
            else:
                probs[i]+=0.01
                if probs[i]>0.33:
                    probs[i]=0.30               
        else:
            if moves[i][1]==0 and moves[i][2]==0:
                probs[i]-=0.005
                if probs[i]<0:
                    probs[i]=0.03
            else:
                probs[i]-=0.01
                if probs[i]<0:
                    probs[i]=0.12
    return probs
#this function generates only one path from start to end.
#the algorithm uses probabilities to generate moves for the path
def path_generator(size,start,end,floors):
    #initiliazes maze to all ones
    maze=np.ones((floors,size,size))
    dirs=np.array([(end[0]-start[0])/abs(end[0]-start[0]),(end[1]-start[1])/abs(end[1]-start[1]),(end[2]-start[2])/abs(end[2]-start[2])])
    moves=[np.array([0,1,0]),np.array([1,0,0]),np.array([0,-1,0]),np.array([-1,0,0]),np.array([0,0,1]),np.array([0,0,-1])]
    probs=[]
    inc=[]
    #inc array stores one horizontal move and one vertical move to move closer to the end from start
    #for example if start=(5,5) and end is (10,0), then inc contains indices of (1,0) and (0,-1)
    #initialising probabilities for each move and the inc array
    for i in range(6):
        if np.any(moves[i]==dirs):
            if moves[i][1]==0 and moves[i][2]==0:
                probs.append(0.05)
            else:
                probs.append(0.11)
            inc.append(i)
        else :
            if moves[i][1]==0 and moves[i][2]==0:
                probs.append(0.16)
            else:
                probs.append(0.28)
    #storing the initial probabilities for future references
    probs_init=probs[:]
    tile=start[:]
    maze[int(tile[0]),int(tile[1]),int(tile[2])]=0
    #the algorithm designed simply uses a probablisitic approach from start to end.
    #the path starts from centre and moves while checking it doesnt form any loops in the maze
    # if the path enters the wrong corner(not end) or if the path doesnt have any move without forming loops,then the algorithm starts again
    solution=open("path.txt","w")
    while(tile[0]!=end[0] or tile[1]!=end[1] or tile[2]!=end[2]):
        #whiel loop runs until a move is found
        x_edge=(tile[0]==0) or (tile[0]==size-1)
        y_edge=(tile[1]==0) or (tile[1]==size-1)
        z_edge=(tile[2]==0) or (tile[2]==size-1)
        if(x_edge and y_edge and z_edge):
            #checks if the path reached wrong corner(that is not the end)
            maze=np.ones((floors,size,size))
            probs=probs_init[:]
            tile=np.array([(floors-1)/2,(size-1)/2,(size-1)/2])
            maze[int(tile[0]),int(tile[1]),int(tile[2])]=0
            solution=open("path.txt","w")
        else:
            #creating current moves and probs, to remove moves that are not possible
            possible_moves=moves[:]
            possible_probs=probs[:]
            while True:
                if(len(possible_moves)==0):
                    #if there is no move without forming a loop, algorithm resets
                    maze=np.ones((floors,size,size))
                    probs=probs_init[:]
                    tile=np.array([(floors-1)/2,(size-1)/2,(size-1)/2])
                    maze[int(tile[0]),int(tile[1]),int(tile[2])]=0
                    solution=open("path.txt","w")
                    break
                #begin{handles edge tile cases}
                if(tile[0]/(floors-1)==0):
                    move=np.array([-1,0,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                if(tile[0]/(floors-1)==1):
                    move=np.array([1,0,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                if(tile[1]/(size-1)==0):
                    move=np.array([0,-1,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                if(tile[1]/(size-1)==1):
                    move=np.array([0,1,0])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                if(tile[2]/(size-1)==1):
                    move=np.array([0,0,1])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                if(tile[2]/(size-1)==0):
                    move=np.array([0,0,-1])
                    index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, move)), -1)
                    if index!=-1:
                        possible_moves.pop(index)
                        possible_probs.pop(index)
                    #end{handled edge tile cases}                
                    #when not on a edge tile
                    #basically checks to not move back in the path
                i=0
                for current_move in possible_moves:
                    new_tile=tile+current_move
                    if maze[int(new_tile[0]),int(new_tile[1]),int(new_tile[2])]==0:
                        possible_moves.pop(i)
                        possible_probs.pop(i)
                    i=i+1
                choice=random.choices(possible_moves,possible_probs)[0]
                tile[0]+=choice[0]
                tile[1]+=choice[1]
                tile[2]+=choice[2]
                #already is a variable to check if the tile is already open(0) and doesn't close it(1) if the path fails
                already=False
                if(maze[int(tile[0]),int(tile[1]),int(tile[2])]==0):
                     already=True
                maze[int(tile[0]),int(tile[1]),int(tile[2])]=0
                index = next((i for i, arr in enumerate(possible_moves) if np.array_equal(arr, choice)), -1)
                #removes the current move choice from possible moves for the next iteration
                if index!=-1:
                    possible_moves.pop(index)
                    possible_probs.pop(index)
                #loop ends if finally tile_checker is true
                if(tile_checker(maze,tile)):
                    probs=probs_change(probs,inc,moves)
                    print(probs)
                    solution.write(translator(choice))
                    solution.write("\n")
                    break
                else:
                    #else we move back to the original tile and iterate other moves
                    if(not already):
                        maze[int(tile[0]),int(tile[1]),int(tile[2])]=1
                    tile[0]-=choice[0]
                    tile[1]-=choice[1]
                    tile[2]-=choice[2]
    print("\n------------end---------------\n")
    solution.close()
    return maze
def maze_generator(size,floors):
    #this generates the remaining maze after the path is generated
    #randomly one of the tile is chosen and generates one more 0 tile neighbouring to it randomly without forming loops
    #this is iterated a lot of times, to create the maze :)
    #rest basically works like path_generator
    start=np.array([(floors-1)/2,(size-1)/2,(size-1)/2])
    vertex=random.randint(0,7)
    moves=(np.array([0,1,0]),np.array([1,0,0]),np.array([0,-1,0]),np.array([-1,0,0]),np.array([0,0,1]),np.array([0,0,-1]))
    #randomly generating end as one of the corners, so people can't know beforehand,not even me :( 
    end=np.array([0,0,0])
    if vertex==0:
        end=np.array([0,0,0])
    elif vertex==1:
        end=np.array([floors-1,0,0])
    elif vertex==2:
        end=np.array([floors-1,size-1,0])
    elif vertex==3:
        end=np.array([0,size-1,0])
    elif vertex==4:
        end=np.array([0,0,size-1])
    elif vertex==5:
        end=np.array([floors-1,0,size-1])
    elif vertex==6:
        end=np.array([floors-1,size-1,size-1])
    elif vertex==7:
        end=np.array([0,size-1,size-1])
    maze=path_generator(size,start,end,floors)
    path=np.copy(maze)
    for i in range(ITERATIONS):
        zeros=np.where(maze==0)
        poss_moves=[0,0,0,1,2,2,2,3,4,4,4,5,5,5]
        rand_zero=random.randint(0,zeros[0].size-1)
        tile=np.array([zeros[0][rand_zero],zeros[1][rand_zero],zeros[2][rand_zero]])
        if((tile[2]/(size-1)==0 or tile[2]/(size-1)==1) and (tile[1]/(size-1)==0 or tile[1]/(size-1)==1) and (tile[0]/(floors-1)==0 or tile[0]/(floors-1)==1)):
            continue
        if(tile[0]/(floors-1)==0):
            while 3 in poss_moves:
                poss_moves.remove(3)
        if(tile[0]/(floors-1)==1):
            while 1 in poss_moves:
                poss_moves.remove(1)
        if(tile[1]/(size-1)==1):
            while 0 in poss_moves:
                poss_moves.remove(0)
        if(tile[1]/(size-1)==0):
            while 2 in poss_moves:
                poss_moves.remove(2)
        if(tile[2]/(size-1)==0):
            while 5 in poss_moves:
                poss_moves.remove(5)
        if (tile[2]/(size-1)==1):
            while 4 in poss_moves:
                poss_moves.remove(4)
        while(len(poss_moves)>0):
            move=random.choice(poss_moves)
            tile+=moves[move]
            already=False
            if maze[int(tile[0]),int(tile[1]),int(tile[2])]==0:
                already=True
            maze[int(tile[0]),int(tile[1]),int(tile[2])]=0
            if tile_checker(maze,tile):
                break
            else:
                if not already:
                    maze[int(tile[0]),int(tile[1]),int(tile[2])]=1
                tile-=moves[move]
                poss_moves.remove(move)
    #finally setting the other corners to 1 so that only 1 end is point is left
    endx,endy,endz=int(end[0]),int(end[1]),int(end[2])
    complementary_endx,complementary_endy,complementary_endz=int(not(endx/(floors-1)))*(floors-1),int(not(endy/(size-1)))*(size-1),int(not(endz/(size-1)))*(size-1)
    maze[endx,complementary_endy,endz]=1
    maze[complementary_endx,complementary_endy,endz]=1
    maze[complementary_endx,endy,endz]=1
    maze[endx,complementary_endy,complementary_endz]=1
    maze[complementary_endx,complementary_endy,complementary_endz]=1
    maze[complementary_endx,endy,complementary_endz]=1
    maze[endx,endy,complementary_endz]=1
    return maze,path
