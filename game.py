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

# window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lost in Space-Time")
running=True
input=1
window=WINDOW
while running:
    if input==1:
        window,level=windows.start(window)
        input=2
    if input==2:
        level,window,result,input=windows.game(level,window)
    if input==4:
        window,input=windows.end(window,level,result)
    if input==3:
        running=False
pygame.quit()
sys.exit()
