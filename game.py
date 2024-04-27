import pygame
import random
import maze
import numpy as np
import player_file
import windows
import time
import sys
WIDTH=1300
HEIGHT=945
pygame.init()
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))

#
pygame.display.set_caption("Lost in Space-Time")
running=True
input=1
window=WINDOW
while running:
    if input==1:
        input,window,level=windows.start(window)
    if input==2:
        input,window,result,level=windows.game(level,window)
    if input==3:
        input,window=windows.end(window,level,result)
    if input==0:
        running=False
pygame.quit()
sys.exit()
