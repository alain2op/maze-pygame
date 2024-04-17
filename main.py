import pygame
import random
import maze
import numpy as np
import player_file
SIZE=5
TILE_SIZE=100
MOVEMENT_DELAY = 100  # in milliseconds


pygame.init()
tile_size = TILE_SIZE
size = SIZE
centre = np.array([(size - 1)/2, (size - 1)/2,(size-1)/2])
generated_maze, generated_path = maze.maze_generator(size)
window_width = generated_maze.shape[2] * tile_size
window_height = generated_maze.shape[1] * tile_size
window = pygame.display.set_mode((window_width, window_height))
BLACK = (0, 0, 0)
WHITE=(255,255,255)
GREEN=(200,255,200)
BLUE=(0,0,255)
lava = pygame.transform.scale(pygame.image.load("lava.jpeg"), (tile_size, tile_size))
cloud= pygame.transform.scale(pygame.image.load("cloud.jpeg"), (tile_size, tile_size))
# land=pygame.transform.scale(pygame.image.load(""),(tile_size,tile_size))
running = True
player1 = player_file.player("green", centre, generated_maze)
pressed_keys = {}
# Constants for movement sensitivity
last_movement_time = pygame.time.get_ticks()
floor=int((size-1)/2)
maze_file=open("maze.txt","w")
maze_file.write("-----path-----------")
maze_file.write(str(generated_path))
maze_file.write("-------maze---------")
maze_file.write(str(generated_maze))
maze_file.close()
while running:
    current_time = pygame.time.get_ticks()
    time_since_last_movement = current_time - last_movement_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pressed_keys[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                del pressed_keys[event.key]
    # Check if enough time has passed since last movement
    if time_since_last_movement >= MOVEMENT_DELAY:
        movement_direction = 0
        if pygame.K_UP in pressed_keys:
            movement_direction = 3
        elif pygame.K_LEFT in pressed_keys:
            movement_direction = 6
        elif pygame.K_DOWN in pressed_keys:
            movement_direction = 1
        elif pygame.K_RIGHT in pressed_keys:
            movement_direction = 5
        elif pygame.K_LSHIFT in pressed_keys:
            movement_direction=4
        elif pygame.K_LCTRL in pressed_keys:
            movement_direction=2
        player_file.move(player1, movement_direction)
        last_movement_time = current_time  # Update last movement time

    orientation = player1.orientation
    if pygame.K_w in pressed_keys:
        orientation = 1
    elif pygame.K_a in pressed_keys:
        orientation = 2
    elif pygame.K_s in pressed_keys:
        orientation = 3
    elif pygame.K_d in pressed_keys:
        orientation = 4
    player_file.rotate(player1, orientation)

    window.fill(WHITE)
    for y in range(generated_maze.shape[0]):
        for x in range(generated_maze.shape[1]):
            if generated_path[player1.floor,y,x]==0:
                color=GREEN
            elif generated_maze[player1.floor,y,x]==0:
                color=WHITE
            else:
                color = BLACK
            pygame.draw.rect(window, color, (x * tile_size, y * tile_size, tile_size, tile_size))
    z,y,x = player1.tile[0], player1.tile[1],player1.tile[2]
    image = player1.images[player1.orientation - 1]
    image=pygame.image.load("ball.jpeg")
    window.blit(pygame.transform.scale(image, (tile_size, tile_size)), (x * tile_size, y * tile_size))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
