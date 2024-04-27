import pygame
import numpy as np
import os 
import time

import pygame.display
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
TIMER=300
ENERGY=800
LIGHTNING_BLUE=(0,191,255)

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

class sprites:
    def __init__(self, file_path, num_frames, frame_width, frame_height):
        self.sprite_sheet = pygame.image.load(file_path)
        self.num_frames = num_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self.extract_frames()

    def extract_frames(self):
        frames = []
        for i in range(self.num_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            scaled_frame=pygame.transform.scale(frame,(135,135))
            frames.append(scaled_frame)
        return frames


def start(window):
    global title_font,button_font
    start_image = pygame.transform.scale(pygame.image.load("start.jpeg"), (WIDTH, HEIGHT))
    title_font = pygame.font.Font("HARRYP__.TTF", 180)
    button_font = pygame.font.Font("HARRYP__.TTF", 80)
    title = "Lost in Space-Time"
    title_positions = [(300, 200), (550, 200), (800, 400)]
    WINDOW.blit(start_image, (0, 0))
    words = title.split()
    pygame.display.flip()
    time.sleep(0.5)
    
    labyrinth = button("labyrinth", button_font, GOLD, BLACK, (100, 800), (300, 100))
    wormhole = button("wormhole", button_font, GOLD, BLACK, (500, 800), (300, 100))
    singularity = button("singularity", button_font, GOLD, BLACK, (900, 800), (300, 100))
    
    for word_no in range(len(words)):
        text_surface = title_font.render(words[word_no], True, GOLD)
        text_rect = text_surface.get_rect()
        text_rect.center = title_positions[word_no]
        WINDOW.blit(text_surface, text_rect)
        pygame.display.flip()
        time.sleep(0.5)
    pygame.display.flip()
    
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
        pygame.display.flip()
    pygame.quit()
    sys.exit() 


def game(level,window):

    result=0
    if level==1:
        size=27
        floors=1
    elif level==2:
        size=11
        floors=3
    elif level==3:
        size=9
        floors=5

    global movement_direction
    vision_tile_count=3
    tile_size=945//(2*vision_tile_count+1)
    centre = np.array([(floors-1)/2,(size - 1)/2, (size - 1)/2])
    generated_maze, generated_path,end_point = maze.maze_generator(size,floors)
    player1 = player_file.player("green", centre, generated_maze)

    walk_up=sprites("movement/up.png",9,575//9+1,60)
    walk_down=sprites("movement/down.png",9,575//9+1,60)
    walk_right=sprites("movement/right.png",9,575//9+1,60)
    walk_left=sprites("movement/left.png",9,575//9+1,60)

    walks=[walk_up.frames,walk_left.frames,walk_down.frames,walk_right.frames]
    face_up=walk_up.frames[0]
    face_down=walk_down.frames[0]
    face_right=walk_right.frames[0]
    face_left=walk_left.frames[0]
    faces=[face_up,face_left,face_down,face_right]

    pressed_keys = {}
    last_movement_time = pygame.time.get_ticks()
    game_running=True
    tile_tracker=[]
    teleport_times=[]
    teleport_pushback_times=[]
    for i in range(20):
        teleport_times.append(random.randint(20000,30000))
        teleport_pushback_times.append(random.randint(10000,15000))
    teleport_index=0
    last_tracker_time=pygame.time.get_ticks()
    last_teleport_time=pygame.time.get_ticks()

    white_blue_images=[]
    white_images=[]
    blue_images=[]
    space_images_background=[]
    for index in range(12):
        white_blue_images.append(pygame.transform.scale(pygame.image.load("white_blue/white_blue_"+str(index+1)+".jpg"),(tile_size,tile_size)))
        white_images.append(pygame.transform.scale(pygame.image.load("white/white_"+str(index+1)+".jpg"),(tile_size,tile_size)))
        blue_images.append(pygame.transform.scale(pygame.image.load("blue/blue_"+str(index+1)+".jpg"),(tile_size,tile_size)))
    for index in range(40):
        space_images_background.append(pygame.transform.scale(pygame.image.load("space/space_"+str(index)+".gif"),(WIDTH,HEIGHT)))
    tile_image=pygame.transform.scale(pygame.image.load("tile.jpg"),(tile_size,tile_size))
    trophy=pygame.transform.scale(pygame.image.load("trophy.jpeg"),(tile_size,tile_size))

    timer=420
    energy=10000
    i=0
    spiral_frame_index=0
    space_frame_index=0
    space_frame_time_stamp=pygame.time.get_ticks()
    game_font_1 = pygame.font.Font("HARRYP__.TTF", 60)
    game_font_2 = pygame.font.Font("HARRYP__.TTF", 80)
    game_font_3=pygame.font.Font("HARRYP__.TTF",40)   
    game_font_4=pygame.font.Font("HARRYP__.TTF",100)  
    floor_text = button("Spatial Zone : ", game_font_1, GOLD, BLACK, (970, 80), (300, 100))
    timer_text_1=button("Temporal Breakdown Timer :",game_font_3,GOLD,BLACK,(955,180),(300,100))
    timer_text_1.draw(window)
    floor_text.draw(window)
    home=button("Home",game_font_4,GOLD,BLACK,(1050,720),(300,100))
    exit=button("Exit",game_font_4,GOLD,BLACK,(1050,840),(300,100))
    home.draw(window)
    exit.draw(window)
    restart=button("Restart",game_font_4,GOLD,BLACK,(1050,600),(300,100))
    restart.draw(window)
    pygame.display.flip()
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
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                home.set_hovered(home.is_hovered(mouse_pos))
                exit.set_hovered(exit.is_hovered(mouse_pos))
                restart.set_hovered(restart.is_hovered(mouse_pos))
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if exit.is_hovered(mouse_pos):
                        return level,window,1,3
                    elif home.is_hovered(mouse_pos):
                        return level,window,1,1
                    elif restart.is_hovered(mouse_pos):
                        player1=player_file.player("green",centre,generated_maze)
                        timer=TIMER
                        energy=ENERGY

        if player1.tile[0]==end_point[0] and player1.tile[1]==end_point[1] and player1.tile[2]==end_point[2]:
            time.sleep(1)
            result=1
            return level,window,result
        
        moved=False
        walk_move=[0,0,0] 
        walk_code=0         
        if time_since_last_movement >= MOVEMENT_DELAY:
            movement_direction = 0
            if pygame.K_UP in pressed_keys:
                movement_direction = 3
                walk_move=[0,-1,0]
                walk_code=1
                player1.orientation=0
            elif pygame.K_LEFT in pressed_keys:
                movement_direction = 6
                walk_move=[-1,0,0]
                walk_code=2
                player1.orientation=1
            elif pygame.K_DOWN in pressed_keys:
                movement_direction = 1
                walk_move=[0,1,0]
                walk_code=3
                player1.orientation=2
            elif pygame.K_RIGHT in pressed_keys:
                movement_direction = 5
                walk_move=[0,0,1]
                walk_code=4
                player1.orientation=3
            elif pygame.K_LSHIFT in pressed_keys:
                movement_direction=4
            elif pygame.K_LCTRL in pressed_keys:
                movement_direction=2
            if walk_code in range(1,5):
                moved=True
                time.sleep(0.04)
                for i in range(5):
                    window.blit(tile_image,(vision_tile_count*tile_size,vision_tile_count*tile_size))
                    window.blit(walks[walk_code-1][i],(vision_tile_count*tile_size,vision_tile_count*tile_size))
                    timer_text_1.draw(window)
                    floor_text.draw(window)
                    home.draw(window)
                    exit.draw(window)
                    restart.draw(window)
                    floor_number_text=button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70),(300,100))
                    timer_text=button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240),(300,100))
                    timer_text.draw(window)
                    floor_number_text.draw(window)
                    pygame.display.flip()
                    time.sleep(0.04)
            player_file.move(player1, movement_direction)
            last_movement_time = current_time 

        if pygame.K_w in pressed_keys:
            player1.orientation = 0
        elif pygame.K_a in pressed_keys:
            player1.orientation = 1
        elif pygame.K_s in pressed_keys:
            player1.orientation = 2
        elif pygame.K_d in pressed_keys:
            player1.orientation = 3

        
        window.blit(space_images_background[space_frame_index%40],(0,0))
        img=space_images_background[space_frame_index%40]
        for y in range(-vision_tile_count,vision_tile_count+1):
            for x in range(-vision_tile_count,vision_tile_count+1):
                if player1.tile[2]+x>=0 and player1.tile[2]+x<size and player1.tile[1]+y>=0 and player1.tile[1]+y<size:
                    if generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor>0 and player1.floor<floors-1 and generated_maze[player1.floor-1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and generated_maze[player1.floor+1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 :
                        img=white_blue_images[(spiral_frame_index+x+y)%12]
                        window.blit(img, ((x+vision_tile_count) * tile_size, (y+vision_tile_count) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor>0 and generated_maze[player1.floor-1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=white_images[(spiral_frame_index+x+y)%12]
                        window.blit(img, ((x+vision_tile_count) * tile_size, (y+vision_tile_count) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor<floors-1 and generated_maze[player1.floor+1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=blue_images[(spiral_frame_index+x+y)%12]
                        window.blit(img, ((x+vision_tile_count) * tile_size, (y+vision_tile_count) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=tile_image
                        window.blit(img, ((x+vision_tile_count) * tile_size, (y+vision_tile_count) * tile_size))
                    if player1.floor==end_point[0] and x+player1.tile[2]==end_point[2] and y+player1.tile[1]==end_point[1]:
                        img=trophy
                        window.blit(img, ((x+vision_tile_count) * tile_size, (y+vision_tile_count) * tile_size))
        spiral_frame_index=(spiral_frame_index+1)%12
        if pygame.time.get_ticks()-space_frame_time_stamp>=40 :
            space_frame_index=(space_frame_index+1)%40
            space_frame_time_stamp=pygame.time.get_ticks()
        z,y,x = player1.tile[0], player1.tile[1],player1.tile[2]
        image = player1.images[player1.orientation - 1]
        
        # floor_text = button_font.render("Spatial Zones",True,GOLD)
        # pygame.draw.rect(WINDOW, BLACK, self.rect,-1)
        # window.blit(floor_text, floor_text.get_rect()

        if moved:
            for l in range(4):
                window.blit(tile_image,(vision_tile_count*tile_size,vision_tile_count*tile_size))
                window.blit(walks[walk_code-1][l+5],(vision_tile_count*tile_size,vision_tile_count*tile_size))
                timer_text_1.draw(window)
                floor_text.draw(window)
                home.draw(window)
                exit.draw(window)
                restart.draw(window)
                floor_number_text=button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70),(300,100))
                timer_text=button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240),(300,100))
                timer_text.draw(window)
                floor_number_text.draw(window)
                pygame.display.flip()
                time.sleep(0.04)
        window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
        timer_text_1.draw(window)
        floor_text.draw(window)
        home.draw(window)
        exit.draw(window)
        restart.draw(window)
        floor_number_text=button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70),(300,100))
        timer_text=button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240),(300,100))
        timer_text.draw(window)
        floor_number_text.draw(window)
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
        pygame.display.flip()
        time.sleep(0.5)
        
        home = button("Home", button_font, GOLD, BLACK, (150, 800), (300, 100))
        play_again = button("Play Again", button_font, GOLD, BLACK, (500, 800), (300, 100))
        exit = button("Exit", button_font, GOLD, BLACK, (950, 800), (300, 100))
        
        for word_no in range(len(words)):
            text_surface = title_font.render(words[word_no], True, GOLD)
            text_rect = text_surface.get_rect()
            text_rect.center = title_positions[word_no]
            window.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.5)
        pygame.display.flip()
        
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
            pygame.display.flip()
        pygame.quit()
        sys.exit() 


