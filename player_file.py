import os
import pygame
import numpy as np
class player:
    def __init__(self,centre,maze,energy):
        self.tile=centre
        self.orientation=3
        self.maze=maze
        self.floor=int((self.maze.shape[0]-1)/2)
        self.max_energy=energy
        self.energy=energy
        self.checkpoint=centre
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
        if command!=0:
            player.energy-=1
            player.energy=min(player.energy,player.max_energy)
