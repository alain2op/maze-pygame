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
ENERGY=400
LIGHTNING_BLUE=(0,191,255)
VISION_TILE_COUNT=3
#a function to remove part(rectangle) of an image and blit the remaining part of the image
def remove_and_blit(image, top_left, bottom_right):
    result_surface = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    result_surface.blit(image, (0, 0))
    remove_rect = pygame.Rect(top_left, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))
    pygame.draw.rect(result_surface, (0, 0, 0, 0), remove_rect)
    return result_surface

# a buttn class that detects clicks and hovering and makes necessart changes
class button:
    def __init__(self, text, font, text_color, border_color, position):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.border_color = border_color
        self.position = position
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.rect = self.rendered_text.get_rect()
        self.rect.topleft = position
        self.hovered = False

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
# a sprite class that takes in a sprite sheets and divides it into individual frames and stores it in an array
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

    #loading and storing required images,fonts,variables for the start_window
    start_image = pygame.transform.scale(pygame.image.load("start.jpeg"), (WIDTH, HEIGHT))
    title_font = pygame.font.Font("HARRYP__.TTF", 180)
    button_font = pygame.font.Font("HARRYP__.TTF", 80)
    exit_font=pygame.font.Font("HARRYP__.TTF", 120)
    labyrinth = button("labyrinth", button_font, GOLD, BLACK, (100, 600))
    wormhole = button("wormhole", button_font, GOLD, BLACK, (500, 600))
    singularity = button("singularity", button_font, GOLD, BLACK, (900, 600))
    exit_button=button("Exit",exit_font,GOLD,BLACK,(530,720))
    title = "Lost in Space-Time"
    title_positions = [(300, 200), (550, 200), (800, 400)]#position of each word of the title for the animation done

#logic for game opening animation, where each word appears after a delay
    window.blit(start_image, (0, 0))
    words = title.split()
    pygame.display.flip()
    time.sleep(0.5) 
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
        # each of the 4 buttons is being drawn
        buttons=[labyrinth,wormhole,singularity,exit_button]
        for button in buttons:
            button.draw(window)

        #event handling for  hovering over the buttons and click on the buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        button.set_hovered(True)
                    else:
                        button.set_hovered(False)                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if labyrinth.is_hovered(mouse_pos):
                        return 2,window,1
                    elif wormhole.is_hovered(mouse_pos):
                        return 2,window,2
                    elif singularity.is_hovered(mouse_pos):
                        return 2,window,3
                    elif exit_button.is_hovered(mouse_pos):
                        return 0,window,0
        #updating displays for hovering effect
        pygame.display.flip()
    pygame.quit()
    sys.exit() 


def game(level,window):

    # a loading window since maze-generation takes a bit of time
    loading=pygame.transform.scale(pygame.image.load("loading.jpeg"),(WIDTH,HEIGHT))
    window.blit(loading,(0,0))
    pygame.display.flip()

    #adjusting parameters for the levels
    if level==1:
        size=27
        floors=1
    elif level==2:
        size=11
        floors=3
    elif level==3:
        size=9
        floors=5
    
    #setting display parameters
    vision_tile_count=VISION_TILE_COUNT
    tile_size=HEIGHT//(2*vision_tile_count+1)

    # a proxy window generated for movement animations, (9*9) tile size image is generated for 7*7 image which is displayed
    proxy_window = pygame.Surface((tile_size * (2 * vision_tile_count + 3), tile_size * (2 * vision_tile_count + 3)))

    #maze is generated
    centre = np.array([(floors-1)/2,(size - 1)/2, (size - 1)/2])
    generated_maze, generated_path,end_point = maze.maze_generator(size,floors)

    #creating the instance of the character
    player1 = player_file.player( centre, generated_maze,ENERGY)

    #player sprite movement animations and orientations loaded and stored
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

    #a set of variables created to handle time slipping(teleported to an instance in the past)    
    tile_tracker=[]#tracks the positions at each second
    teleport_times=[]#stores the timestamps when to teleport
    teleport_pushback_times=[]#stores how long back to teleport
    for i in range(20):
        teleport_times.append(random.randint(30000,50000))#teleports a random time between 30-50s
        teleport_pushback_times.append(random.randint(15000,25000))# teleports back 15-25s
    teleport_index=0#to go through the arrays
    last_tracker_time=pygame.time.get_ticks()#to track tiles every second
    last_teleport_time=pygame.time.get_ticks()#to track teleportation

#storing frames and images of the background and tile animations and other required images
    white_blue_images=[]
    white_images=[]
    blue_images=[]
    space_images_background=[]
    for index in range(12):
        white_blue_images.append(pygame.transform.scale(pygame.image.load("white_blue/white_blue_"+str(index+1)+".jpg"),(tile_size,tile_size)))
        white_images.append(pygame.transform.scale(pygame.image.load("white/white_"+str(index+1)+".jpg"),(tile_size,tile_size)))
        blue_images.append(pygame.transform.scale(pygame.image.load("blue/blue_"+str(index+1)+".jpg"),(tile_size,tile_size)))
    for index in range(40):
        space_images_background.append(pygame.transform.scale(pygame.image.load("space/space_"+str(index)+".gif"),(WIDTH+tile_size*2,HEIGHT+tile_size*2)))
    tile_image=pygame.transform.scale(pygame.image.load("tile.jpg"),(tile_size,tile_size))
    trophy=pygame.transform.scale(pygame.image.load("trophy.jpeg"),(tile_size,tile_size))
    energy_image=pygame.transform.scale(pygame.image.load("energy.png"),(200,30))

    

#storing required font sizes
    game_font_1 = pygame.font.Font("HARRYP__.TTF", 60)
    game_font_2 = pygame.font.Font("HARRYP__.TTF", 80)
    game_font_3=pygame.font.Font("HARRYP__.TTF",40)   
    game_font_4=pygame.font.Font("HARRYP__.TTF",100)  

#storing and drawing the 3 buttons
    home=button("Home",game_font_4,GOLD,BLACK,(1050,720))
    exit=button("Exit",game_font_4,GOLD,BLACK,(1050,840))
    restart=button("Restart",game_font_4,GOLD,BLACK,(1050,600))
    restart.draw(window)
    home.draw(window)
    exit.draw(window)

#storing and drawing the labels of the 3 parameters that change as the game progresses
    floor_text = button("Spatial Zone : ", game_font_1, GOLD, BLACK, (970, 80))
    timer_text_1=button("Temporal Breakdown Timer :",game_font_3,GOLD,BLACK,(955,180))
    energy_text=button("Chrono-Morphic Energy : ",game_font_3,GOLD,BLACK,(975,350))   
    timer_text_1.draw(window)
    floor_text.draw(window)
    energy_text.draw(window)

#updating the display
    pygame.display.flip()


#setting parameters that change in the game
    pressed_keys = {}#tracks all the keys that are pressed
    last_movement_time = pygame.time.get_ticks()#updates movement time to add sensitivity to the movement
    game_running=True#runs the loop
    timer=TIMER
    runs=0#counts the runs of while loop
    #variables to animate spiral and space background
    spiral_frame_index=0
    space_frame_index=0
    space_frame_time_stamp=pygame.time.get_ticks()

#main loop
    while game_running:
        previous_tile=player1.tile
        current_time = pygame.time.get_ticks()

        #player wins if he reached the endpoint
        if player1.tile[0]==end_point[0] and player1.tile[1]==end_point[1] and player1.tile[2]==end_point[2]:
            time.sleep(1)
            return 3,window,1,level #1 is for winning and 0 if lost
        
        #player loses if timer or energy becomes 0
        if (timer<=0) or (player1.energy<=0):
            return 3,window,0,level

        #tile tracking for time slipping
        if current_time-last_tracker_time>=1000:
            tile_tracker.append(player1.tile)
            last_tracker_time=current_time
            timer-=1
        
        #logic for time_slipping
        if current_time-last_teleport_time>=teleport_times[teleport_index%20]:
            for dim in range(3):
                time_to_teleport=len(tile_tracker)-1-teleport_pushback_times[teleport_index%20]//1000
                player1.tile[dim]=tile_tracker[time_to_teleport][dim]
                last_teleport_time=current_time
            player1.floor=int(player1.tile[0])
            teleport_index=(teleport_index+1)%20
        
        
        time_since_last_movement = current_time - last_movement_time
        for event in pygame.event.get():
            #storing clicked keys to give continuous movement on pressing
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                pressed_keys[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in pressed_keys:
                    del pressed_keys[event.key]
            #hovering animation for buttons on the right of the window
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                home.set_hovered(home.is_hovered(mouse_pos))
                exit.set_hovered(exit.is_hovered(mouse_pos))
                restart.set_hovered(restart.is_hovered(mouse_pos))  
            #event handling for button clicks on the right                 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if exit.is_hovered(mouse_pos):
                        return 0,window,0,level
                    elif home.is_hovered(mouse_pos):
                        return 1,window,0,level
                    elif restart.is_hovered(mouse_pos):
                        last_teleport_time=current_time
                        player1=player_file.player(centre,generated_maze,ENERGY)
                        timer=TIMER

        #conditions for movement and storing walk and orientation variables for animation and posture, there is a movement delay of 150ms for handling the sensitivity, though it doesn't make sense due to the delays of animation,but kept just in case  
        moved=False
        walk_moves=[[0,0],[0,-1],[-1,0],[0,1],[1,0]]
        walk_move=walk_moves[0]
        walk_code=0   
        #movement directions are calibrated      
        if time_since_last_movement >= MOVEMENT_DELAY:
            movement_direction = 0
            if pygame.K_UP in pressed_keys:
                movement_direction = 3
                walk_move=walk_moves[1]
                walk_code=1
                player1.orientation=0
            elif pygame.K_LEFT in pressed_keys:
                movement_direction = 6
                walk_move=walk_moves[2]
                walk_code=2
                player1.orientation=1
            elif pygame.K_DOWN in pressed_keys:
                movement_direction = 1
                walk_move=walk_moves[3]
                walk_code=3
                player1.orientation=2
            elif pygame.K_RIGHT in pressed_keys:
                movement_direction = 5
                walk_move=walk_moves[4]
                walk_code=4
                player1.orientation=3
            elif pygame.K_LSHIFT in pressed_keys:#for moving up
                movement_direction=4
            elif pygame.K_LCTRL in pressed_keys:#for moving down
                movement_direction=2
            if walk_code in range(1,5):
                moved=True
                time.sleep(0.04)
            player_file.move(player1, movement_direction)
            last_movement_time = current_time 

        #logic for animation of movement
        if moved and not(player1.tile[0]==previous_tile[0] and player1.tile[1]==previous_tile[1] and player1.tile[2]==previous_tile[2]):
            for j in range(9):
                #updating timer,energy and floors
                floor_number_text=button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
                energy_level=remove_and_blit(energy_image,(6+188*player1.energy//ENERGY,6),(194,24))
                #drawing other buttons and text
                timer_text_1.draw(window)
                floor_text.draw(window)
                home.draw(window)
                exit.draw(window)
                restart.draw(window)
                timer_text.draw(window)
                floor_number_text.draw(window)
                energy_text.draw(window)  
                window.blit(energy_level,(1050,420))
                #blitting proxy window for smooth animation and blitting the sprite animation over it
                window.blit(proxy_window,(0,0),(tile_size*(1+j*walk_move[0]/9),tile_size*(1+j*walk_move[1]/9),(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(walks[walk_code-1][j],(tile_size*vision_tile_count,tile_size*vision_tile_count))
                pygame.display.flip()
                time.sleep(0.04)

        #updating the proxy_window
        proxy_window.blit(space_images_background[space_frame_index%40],(0,0))
        img=space_images_background[space_frame_index%40]
        for y in range(-vision_tile_count-1,vision_tile_count+2):
            for x in range(-vision_tile_count-1,vision_tile_count+2):
                if player1.tile[2]+x>=0 and player1.tile[2]+x<size and player1.tile[1]+y>=0 and player1.tile[1]+y<size:
                    if generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor>0 and player1.floor<floors-1 and generated_maze[player1.floor-1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and generated_maze[player1.floor+1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 :
                        img=white_blue_images[(spiral_frame_index+x+y)%12]
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor>0 and generated_maze[player1.floor-1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=white_images[(spiral_frame_index+x+y)%12]
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0 and player1.floor<floors-1 and generated_maze[player1.floor+1,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=blue_images[(spiral_frame_index+x+y)%12]
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))
                    elif generated_maze[player1.floor,int(player1.tile[1]+y),int(player1.tile[2]+x)]==0:
                        img=tile_image
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))
                    if player1.floor==end_point[0] and x+player1.tile[2]==end_point[2] and y+player1.tile[1]==end_point[1]:
                        img=trophy
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))

        #drawing the game window from proxy window and orientation and other parameters over it
        window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
        window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
        window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
        #logic for updating animatons of spiral and space
        spiral_frame_index=(spiral_frame_index+1)%12
        if pygame.time.get_ticks()-space_frame_time_stamp>=40 :
            space_frame_index=(space_frame_index+1)%40
            space_frame_time_stamp=pygame.time.get_ticks()
        #drawing other parameters and buttons and updating
        timer_text_1.draw(window)
        floor_text.draw(window)
        home.draw(window)
        exit.draw(window)
        energy_text.draw(window)
        energy_level=remove_and_blit(energy_image,(6+188*player1.energy//ENERGY,6),(194,24))
        window.blit(energy_level,(1050,420))
        restart.draw(window)
        floor_number_text=button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
        timer_text=button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
        timer_text.draw(window)
        floor_number_text.draw(window)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        runs+=1
    pygame.quit()
    sys.exit()


def end(window,level,result):
    #handling cases for winning and losing and doing similarly as the start window
    if result==1:
        end_image = pygame.transform.scale(pygame.image.load("end_won.jpeg"), (WIDTH, HEIGHT))
        title_font = pygame.font.Font("HARRYP__.TTF", 180)
        button_font = pygame.font.Font("HARRYP__.TTF", 80)
        title = "You are free"
        title_positions = [(350, 200), (600, 200), (850, 200)]
        window.blit(end_image, (0, 0))
        words = title.split()
        pygame.display.flip()
        time.sleep(0.5)
            
        for word_no in range(len(words)):
            text_surface = title_font.render(words[word_no], True, GOLD)
            text_rect = text_surface.get_rect()
            text_rect.center = title_positions[word_no]
            window.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.5)
        pygame.display.flip()
    elif result==0:
        end_image = pygame.transform.scale(pygame.image.load("end_lost.jpeg"), (WIDTH, HEIGHT))
        title_font = pygame.font.Font("HARRYP__.TTF", 140)
        button_font = pygame.font.Font("HARRYP__.TTF", 80)
        title = "You are trapped at the end of Space-Time"
        title_positions = [(100, 150), (260, 150), (500, 150),(700,150),(400,350),(550,350),(700,350),(1020,350)]
        window.blit(end_image, (0, 0))
        words = title.split()
        pygame.display.flip()
        time.sleep(0.5)
            
        for word_no in range(len(words)):
            text_surface = title_font.render(words[word_no], True, GOLD)
            text_rect = text_surface.get_rect()
            text_rect.center = title_positions[word_no]
            window.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.5)
        pygame.display.flip()

    home = button("Home", button_font, GOLD, BLACK, (150, 800))
    play_again = button("Play Again", button_font, GOLD, BLACK, (500, 800))
    exit = button("Exit", button_font, GOLD, BLACK, (950, 800))
    buttons=[home,play_again,exit]
    start_running = True
    while start_running:
        
        for button in buttons:
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        button.set_hovered(True)
                    else:
                        button.set_hoved(False)
                    
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


