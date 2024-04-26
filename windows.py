import pygame
import numpy as np
import os 
import time
import maze
import player_file
import random
import sys

WIDTH=1300
HEIGHT=945
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
GOLD=(255,215,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
MOVEMENT_DELAY = 150  # in milliseconds
BLACK = (0, 0, 0)
GREEN=(200,255,200)
BLUE=(0,0,255)


class button:
    def __init__(self, text, font, text_color, border_color, position,size):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_color = border_color
        self.position = position
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.rect = self.rendered_text.get_rect()
        self.rect.topleft = position
        self.hovered = False
        self.size=size

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, self.rect,-1)
        surface.blit(self.rendered_text, self.rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def set_hovered(self, hovered):
        if hovered:
            self.rendered_text = self.font.render(self.text, True, (150, 110, 0)) 
        else:
            self.rendered_text = self.font.render(self.text, True, self.text_color)


def start(window):
    start_image = pygame.transform.scale(pygame.image.load("start.jpeg"), (WIDTH, HEIGHT))
    title_font = pygame.font.Font("HARRYP__.TTF", 180)
    button_font = pygame.font.Font("HARRYP__.TTF", 80)
    title = "Lost in Space-Time"
    title_positions = [(300, 200), (550, 200), (800, 400)]
    WINDOW.blit(start_image, (0, 0))
    words = title.split()
    pygame.display.update()
    time.sleep(0.5)
    
    labyrinth = button("labyrinth", button_font, GOLD, BLACK, (100, 800), (300, 100))
    wormhole = button("wormhole", button_font, GOLD, BLACK, (500, 800), (300, 100))
    singularity = button("singularity", button_font, GOLD, BLACK, (900, 800), (300, 100))
    
    for word_no in range(len(words)):
        text_surface = title_font.render(words[word_no], True, GOLD)
        text_rect = text_surface.get_rect()
        text_rect.center = title_positions[word_no]
        WINDOW.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(0.5)
    pygame.display.update()
    
    start_running = True
    while start_running:
        labyrinth.draw(WINDOW)
        wormhole.draw(WINDOW)
        singularity.draw(WINDOW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if labyrinth.is_hovered(mouse_pos):
                    labyrinth.set_hovered(True)
                else:
                    labyrinth.set_hovered(False)
                    
                if wormhole.is_hovered(mouse_pos):
                    wormhole.set_hovered(True)
                else:
                    wormhole.set_hovered(False)
                    
                if singularity.is_hovered(mouse_pos):
                    singularity.set_hovered(True)
                else:
                    singularity.set_hovered(False)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if labyrinth.is_hovered(mouse_pos):
                        return WINDOW,1
                    elif wormhole.is_hovered(mouse_pos):
                        return WINDOW,2
                    elif singularity.is_hovered(mouse_pos):
                        return WINDOW,3
        pygame.display.update()
    pygame.quit()
    sys.exit() 


def game(level,window):
    result=0
    if level==1:
        size=15
        floors=1
    elif level==2:
        size=9
        floors=3
    elif level==3:
        size=7
        floors=5
    tile_size=945//size
    centre = np.array([(floors-1)/2,(size - 1)/2, (size - 1)/2])
    generated_maze, generated_path,end_point = maze.maze_generator(size,floors)
    player1 = player_file.player("green", centre, generated_maze)

    pressed_keys = {}
    last_movement_time = pygame.time.get_ticks()
    game_running=True
    tile_tracker=[]
    teleport_times=[]
    teleport_pushback_times=[]
    for i in range(20):
        teleport_times.append(random.randint(50000,70000))
        teleport_pushback_times.append(random.randint(15000,25000))
    teleport_index=0
    last_tracker_time=pygame.time.get_ticks()
    last_teleport_time=pygame.time.get_ticks()

    white_blue_images=[]
    white_images=[]
    blue_images=[]
    space_images=[]
    for index in range(12):
        white_blue_images.append(pygame.image.load("white_blue/white_blue_"+str(index+1)+".jpg"))
        white_images.append(pygame.image.load("white/white_"+str(index+1)+".jpg"))
        blue_images.append(pygame.image.load("blue/blue_"+str(index+1)+".jpg"))
        space_images.append(pygame.image.load("space/space_"+str(index+1)+".jpg"))
    tile_image=pygame.image.load("tile.jpg")

    timer=420
    energy=100000
    i=0
    spiral_frame_index=0
    space_frame_index=0
    while game_running:

        current_time = pygame.time.get_ticks()
        if current_time-last_tracker_time>=1000:
            tile_tracker.append(player1.tile)
            last_tracker_time=current_time
            timer-=1
        
        if current_time-last_teleport_time>=teleport_times[teleport_index%20]:
            for dim in range(3):
                time_to_teleport=len(tile_tracker)-1-teleport_pushback_times[teleport_index%20]//1000
                player1.tile[dim]=tile_tracker[time_to_teleport][dim]
                last_teleport_time=current_time
            player1.floor=int(player1.tile[0])
            teleport_index+=1
        
        time_since_last_movement = current_time - last_movement_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                pressed_keys[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in pressed_keys:
                    del pressed_keys[event.key]

        if player1.tile[0]==end_point[0] and player1.tile[1]==end_point[1] and player1.tile[2]==end_point[2]:
            time.sleep(1)
            result=1
            return level,window,result

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
            last_movement_time = current_time 

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
        window.fill((0,200,200))
        for y in range(generated_maze.shape[1]):
            for x in range(generated_maze.shape[2]):
                if generated_maze[player1.floor,y,x]==0 and player1.floor>0 and player1.floor<floors-1 and generated_maze[player1.floor-1,y,x]==0 and generated_maze[player1.floor+1,y,x]==0 :
                    img=white_blue_images[spiral_frame_index]
                elif generated_maze[player1.floor,y,x]==0 and player1.floor>0 and generated_maze[player1.floor-1,y,x]==0:
                    img=white_images[spiral_frame_index]
                elif generated_maze[player1.floor,y,x]==0 and player1.floor<floors-1 and generated_maze[player1.floor+1,y,x]==0:
                    img=blue_images[spiral_frame_index]
                elif generated_maze[player1.floor,y,x]==0:
                    img=tile_image
                elif generated_maze[player1.floor,y,x]==1:
                    img=space_images[space_frame_index%12]
                window.blit(pygame.transform.scale(img, (tile_size, tile_size)), (x * tile_size, y * tile_size))
        if (player1.floor==end_point[0]):
            trophy=pygame.image.load("trophy.jpeg")
            window.blit(pygame.transform.scale(trophy, (tile_size, tile_size)), (end_point[2] * tile_size, end_point[1]* tile_size))
        spiral_frame_index=(spiral_frame_index+1)%12
        if(i%7==0):
            space_frame_index+=1
        z,y,x = player1.tile[0], player1.tile[1],player1.tile[2]
        image = player1.images[player1.orientation - 1]
        RED = (255, 0, 0)
        pygame.draw.circle(window, RED + (128,), ((x+0.5)*tile_size,(y+0.5)*tile_size), tile_size*2//10)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        i+=1
    pygame.quit()
    sys.exit()


def end(window,level,result):
    if result==1:
        end_image = pygame.transform.scale(pygame.image.load("end.jpeg"), (WIDTH, HEIGHT))
        title_font = pygame.font.Font("HARRYP__.TTF", 180)
        button_font = pygame.font.Font("HARRYP__.TTF", 80)
        title = "You are free"
        title_positions = [(350, 200), (600, 200), (850, 200)]
        window.blit(end_image, (0, 0))
        words = title.split()
        pygame.display.update()
        time.sleep(0.5)
        
        home = button("Home", button_font, GOLD, BLACK, (150, 800), (300, 100))
        play_again = button("Play Again", button_font, GOLD, BLACK, (500, 800), (300, 100))
        exit = button("Exit", button_font, GOLD, BLACK, (950, 800), (300, 100))
        
        for word_no in range(len(words)):
            text_surface = title_font.render(words[word_no], True, GOLD)
            text_rect = text_surface.get_rect()
            text_rect.center = title_positions[word_no]
            window.blit(text_surface, text_rect)
            pygame.display.update()
            time.sleep(0.5)
        pygame.display.update()
        
        start_running = True
        while start_running:
            home.draw(WINDOW)
            play_again.draw(WINDOW)
            exit.draw(WINDOW)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if home.is_hovered(mouse_pos):
                        home.set_hovered(True)
                    else:
                        home.set_hovered(False)
                        
                    if play_again.is_hovered(mouse_pos):
                        play_again.set_hovered(True)
                    else:
                        play_again.set_hovered(False)
                        
                    if exit.is_hovered(mouse_pos):
                        exit.set_hovered(True)
                    else:
                        exit.set_hovered(False)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if home.is_hovered(mouse_pos):
                            return WINDOW,1
                        elif play_again.is_hovered(mouse_pos):
                            return WINDOW,2
                        elif exit.is_hovered(mouse_pos):
                            return WINDOW,3
            pygame.display.update()
        pygame.quit()
        sys.exit() 


