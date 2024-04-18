import os
import pygame
import numpy as np
class player:
    def __init__(self,colour,centre,maze):
        self.colour=colour
        self.tile=centre
        self.orientation=3
        self.images=[]
        self.maze=maze
        self.floor=int((self.maze.shape[0]-1)/2)
        image_names = ["top.jpeg", "left.jpeg", "bottom.jpeg", "right.jpeg"]
        folder_path = os.path.join(os.getcwd(), colour)
        for name in image_names:
            file_path=os.path.join(folder_path,name)
            self.images.append(pygame.image.load(file_path).convert_alpha())
def rotate(player,command):
    #commands can be 0,1,2,3 for see up,see left,see down,see right respectively
    player.orientation=command
def move(player,command):
    #commands can be 0,1,2,3,4 for stay,move up,move left,move down and move right respectively
    moves=[np.array([0,0,0]),np.array([0,1,0]),np.array([-1,0,0]),np.array([0,-1,0]),np.array([1,0,0]),np.array([0,0,1]),np.array([0,0,-1])]
    possible=True
    check_move=moves[command]+player.tile
    #checking if tile out of bounds
    for i in range(check_move.shape[0]):
        if check_move[i] < 0 or check_move[i] >= player.maze.shape[i]:
            possible=False
    #checking if tile is 1
    if possible and player.maze[int(check_move[0]),int(check_move[1]),int(check_move[2])]==1:
        possible=False
    #update tile(Move)
    if possible:
        if command==2:
            player.floor-=1
        if command==4:
            player.floor+=1
        player.tile=np.copy(check_move)