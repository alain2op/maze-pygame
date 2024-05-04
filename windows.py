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
TIMER=180
ENERGY=360
LIGHTNING_BLUE=(0,191,255)
VISION_TILE_COUNT=3
#a function to remove part(rectangle) of an image and blit the remaining part of the image
def remove_and_blit(image, top_left, bottom_right):
    result_surface = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    result_surface.blit(image, (0, 0))
    remove_rect = pygame.Rect(top_left, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))
    pygame.draw.rect(result_surface, (0, 0, 0, 0), remove_rect)
    return result_surface

def update_highscores(score,level):
    file_name="highscores_"+str(level)+".txt"
    # Reading existing high scores
    with open(file_name) as file:
        high_scores = [int(line.strip()) for line in file.readlines()]
    # Adding the new score
    high_scores.append(score)   
    # Sorting the scores in descending order
    high_scores.sort(reverse=True)   
    # Taking top 5 scores
    top_scores = high_scores[:5]
    # Writing updated high scores to file
    with open(file_name, 'w') as file:
        for s in top_scores:
            file.write(str(s) + '\n')

# a buttn class that detects clicks and hovering and makes necessart changes
class Button:
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

def guide(window):

    guide = True
    manual1 = True
    manual2 = False
    button_font = pygame.font.Font("HARRYP__.TTF", 80)

    manual1_window=pygame.transform.scale(pygame.image.load("manual1.png"), (WIDTH, HEIGHT))
    manual2_window=pygame.transform.scale(pygame.image.load("manual2.png"), (WIDTH, HEIGHT))

    next_button = Button("Next",button_font,GOLD,BLACK,(100,800))
    close1_button = Button("Close",button_font,GOLD,BLACK,(1100,800))
    previous_button = Button("Previous",button_font,GOLD,BLACK,(100,800))
    close2_button = Button("Close",button_font,GOLD,BLACK,(1100,800))

    buttons = [next_button,close1_button,previous_button,close2_button]

    while guide:
        
        if manual1:
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
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        if next_button.is_hovered(mouse_pos):
                            manual1 = False
                            manual2 = True
                        elif close1_button.is_hovered(mouse_pos):
                            guide = False
                            manual2 = False
                            manual1 = False

            
            window.blit(manual1_window,(0,0))
            close1_button.draw(window)
            next_button.draw(window)

            pygame.display.flip()
        else:
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
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        if close2_button.is_hovered(mouse_pos):
                            guide = False
                            manual2 = False
                            manual1 = False
                        elif previous_button.is_hovered(mouse_pos):
                            manual1 = True
                            manual2 = False

            
            window.blit(manual2_window,(0,0))
            close2_button.draw(window)
            previous_button.draw(window)

            pygame.display.flip()



def leader(window):

    leader = True

    button_font = pygame.font.Font("HARRYP__.TTF", 80)

    leaderboard_window=pygame.transform.scale(pygame.image.load("leaderboard.png"), (WIDTH, HEIGHT))

    close_button = Button("Close",button_font,GOLD,BLACK,(600,820))

    labyrinth = button_font.render("Labyrinth",True,GOLD)
    wormhole = button_font.render("Wormhole",True,GOLD)
    singularity = button_font.render("Singularity",True,GOLD)

    laby_rect = labyrinth.get_rect(center = (230,100))
    worm_rect = wormhole.get_rect(center = (650,100))
    sing_rect = singularity.get_rect(center = (1070,100))

    scores1 = []
    with open("highscores_1.txt",'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = int(lines[i])
            scores1.append(lines[i])

    scores2 = []
    with open("highscores_2.txt",'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = int(lines[i])
            scores2.append(lines[i])

    scores3 = []
    with open("highscores_3.txt",'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            lines[i] = int(lines[i])
            scores3.append(lines[i])

    surf1 = []
    rect1 = []
    for i in range(len(scores1)):
        surf1.append(button_font.render("{}. {}".format(i+1,scores1[i]),True,LIGHTNING_BLUE))
        rect1.append(surf1[i].get_rect(center = (230,220+i*140)))

    surf2 = []
    rect2 = []
    for i in range(len(scores2)):
        surf2.append(button_font.render("{}. {}".format(i+1,scores2[i]),True,LIGHTNING_BLUE))
        rect2.append(surf2[i].get_rect(center = (650,220+i*140)))

    surf3 = []
    rect3 = []
    for i in range(len(scores3)):
        surf3.append(button_font.render("{}. {}".format(i+1,scores3[i]),True,LIGHTNING_BLUE))
        rect3.append(surf3[i].get_rect(center = (1070,220+i*140)))


    while leader:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if close_button.is_hovered(mouse_pos):
                    close_button.set_hovered(True)
                else:
                    close_button.set_hovered(False)                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if close_button.is_hovered(mouse_pos):
                        leader = False
            
            window.blit(leaderboard_window,(0,0))
            window.blit(labyrinth,laby_rect)
            window.blit(wormhole,worm_rect)
            window.blit(singularity,sing_rect)

            for i in range(len(scores1)):
                window.blit(surf1[i],rect1[i])
            for i in range(len(scores2)):
                window.blit(surf2[i],rect2[i])
            for i in range(len(scores3)):
                window.blit(surf3[i],rect3[i])

            close_button.draw(window)

            pygame.display.flip()
                    

def start(window):

    #loading and storing required images,fonts,variables for the start_window
    start_image = pygame.transform.scale(pygame.image.load("start.jpeg"), (WIDTH, HEIGHT))
    title_font = pygame.font.Font("HARRYP__.TTF", 180)
    button_font = pygame.font.Font("HARRYP__.TTF", 80)
    small_button_font=pygame.font.Font("HARRYP__.TTF", 60)
    exit_font=pygame.font.Font("HARRYP__.TTF", 120)
    labyrinth = Button("labyrinth", button_font, GOLD, BLACK, (100, 600))
    wormhole = Button("wormhole", button_font, GOLD, BLACK, (500, 600))
    singularity = Button("singularity", button_font, GOLD, BLACK, (900, 600))
    exit_button=Button("Exit",exit_font,GOLD,BLACK,(600,700))
    manual=Button("A guide through space-time",small_button_font,GOLD,BLACK,(50,840))
    leaderboard=Button("Hall of Fame",small_button_font,GOLD,BLACK,(950,840))
    title = "Lost in Space-Time"
    title_positions = [(300, 200), (550, 200), (800, 400)]#position of each word of the title for the animation done

    # manual1_open,manual2_open,leaderboard_open=False


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
        window.blit(start_image, (0, 0))

        for word_no in range(len(words)):
            text_surface = title_font.render(words[word_no], True, GOLD)
            text_rect = text_surface.get_rect()
            text_rect.center = title_positions[word_no]
            window.blit(text_surface, text_rect)

        # each of the 4 buttons is being drawn
        buttons=[labyrinth,wormhole,singularity,exit_button,leaderboard,manual]
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
                    elif manual.is_hovered(mouse_pos):
                        guide(window)
                    elif leaderboard.is_hovered(mouse_pos):
                        leader(window)

                    
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
    #logic for generating time potions
    potion_tiles=[]
    if level==1:
        zeros=np.where(generated_maze==0)
        number_of_zeros=len(zeros[0])
        index=random.randint(0,number_of_zeros-1)
        potion_tile=np.array([zeros[0][index],zeros[1][index],zeros[2][index]])
        potion_tiles.append(potion_tile)
        for i in range(2):
            found=False
            while not found:
                found=True
                index=random.randint(0,number_of_zeros-1)
                potion_tile=np.array([zeros[0][index],zeros[1][index],zeros[2][index]])
                for potion_tile_1 in potion_tiles:
                    if (abs(potion_tile[1]-potion_tile_1[1])+abs(potion_tile[2]-potion_tile_1[2])<20):
                        found=False
                if found:
                    potion_tiles.append(potion_tile)
    if level==2:
        zeros=np.where(generated_maze==0)
        number_of_zeros=len(zeros[0])
        for i in range(3):
            found = False
            while not found:
                index=random.randint(0,number_of_zeros-1)
                if zeros[0][index]==i:
                    found=True
                    potion_tiles.append(np.array([zeros[0][index],zeros[1][index],zeros[2][index]]))
    if level==3:
        zeros=np.where(generated_maze==0)
        number_of_zeros=len(zeros[0])
        for i in range(0,5,2):
            found = False
            while not found:
                index=random.randint(0,number_of_zeros-1)
                if zeros[0][index]==i:
                    found=True
                    potion_tiles.append(np.array([zeros[0][index],zeros[1][index],zeros[2][index]]))
    potion_tiles_init=potion_tiles[:]

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

    time_portal_open=[]
    time_portal_close=[]
    space_portal_open=[]
    space_portal_close=[]
    for index in range(7):
        open_time_filename="portal_green/tile0"+str(index+8)+".png"
        close_time_filename="portal_green/tile0"+str(index+15)+".png"
        time_portal_open.append(pygame.transform.scale(pygame.image.load(open_time_filename),(tile_size,tile_size)))
        time_portal_close.append(pygame.transform.scale(pygame.image.load(close_time_filename),(tile_size,tile_size)))
        open_space_filename="portal_purple/tile0"+str(index+8)+".png"
        close_space_filename="portal_purple/tile0"+str(index+15)+".png"
        space_portal_open.append(pygame.transform.scale(pygame.image.load(open_space_filename),(tile_size,tile_size)))
        space_portal_close.append(pygame.transform.scale(pygame.image.load(close_space_filename),(tile_size,tile_size)))
    #a set of variables created to handle time slipping(teleported to an instance in the past)    
    tile_tracker=[]#tracks the positions at each second
    teleport_times=[]#stores the timestamps when to teleport
    teleport_pushback_times=[]#stores how long back to teleport
    for i in range(20):
        teleport_times.append(random.randint(30000,40000))#teleports a random time between 50-60s
        teleport_pushback_times.append(random.randint(15000,20000))# teleports back 15-25s
    teleport_index=0#to go through the arrays
    last_tracker_time=pygame.time.get_ticks()#to track tiles every second
    last_teleport_time=pygame.time.get_ticks()#to track teleportation
    teleporting=False
    teleporting1=False

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
    wormhole=pygame.transform.scale(pygame.image.load("wormhole.png"),(tile_size,tile_size))
    energy_image=pygame.transform.scale(pygame.image.load("energy.png"),(200,30))
    potion_image=pygame.transform.scale(pygame.image.load("potion.png"),(tile_size//2,tile_size//2))
    checkpoint_images=[]
    for index in range(5):
        file_name="checkpoint/tile00"+str(index)+".png"
        checkpoint_images.append(pygame.transform.scale(pygame.image.load(file_name),(tile_size//2,tile_size//2)))

#storing required font sizes
    game_font_1 = pygame.font.Font("HARRYP__.TTF", 60)
    game_font_2 = pygame.font.Font("HARRYP__.TTF", 80)
    game_font_3=pygame.font.Font("HARRYP__.TTF",40)   
    game_font_4=pygame.font.Font("HARRYP__.TTF",100)  

#storing and drawing the 3 buttons
    home=Button("Home",game_font_4,GOLD,BLACK,(1050,720))
    exit=Button("Exit",game_font_4,GOLD,BLACK,(1050,840))
    restart=Button("Restart",game_font_4,GOLD,BLACK,(1050,600))
    restart.draw(window)
    home.draw(window)
    exit.draw(window)

#storing and drawing the labels of the 3 parameters that change as the game progresses
    floor_text = Button("Spatial Zone : ", game_font_1, GOLD, BLACK, (970, 80))
    timer_text_1=Button("Temporal Breakdown Timer :",game_font_3,GOLD,BLACK,(955,180))
    energy_text=Button("Chrono-Morphic Energy : ",game_font_3,GOLD,BLACK,(975,350))   
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
    last_use_teleport=last_set_teleport=pygame.time.get_ticks()
#main loop
    while game_running:
        previous_tile=player1.tile
        current_time = pygame.time.get_ticks()

        #player wins if he reached the endpoint
        if player1.tile[0]==end_point[0] and player1.tile[1]==end_point[1] and player1.tile[2]==end_point[2]:
            time.sleep(1)
            score=300*timer//TIMER+(300*player1.energy//ENERGY)+500
            return 3,window,[1,int(score)],level #1 is for winning and 0 if lost
        
        #player loses if timer or energy becomes 0
        if (timer<=0) or (player1.energy<=0):
            score=300*timer//TIMER+300*player1.energy//ENERGY
            return 3,window,[0,int(score)],level
        
        #consumption of potion
        potion_found=False
        potion_index=100
        for j in range(len(potion_tiles)):
            if potion_tiles[j][0] == player1.tile[0] and potion_tiles[j][1] == player1.tile[1] and potion_tiles[j][2] == player1.tile[2]:
                potion_found=True
                potion_index=j
                player1.energy += ENERGY / 10
        if potion_found:
            potion_tiles.pop(potion_index)

        #tile tracking for time slipping
        if current_time-last_tracker_time>=1000:
            timer-=(current_time-last_tracker_time)//1000
            tile_tracker.append(player1.tile)
            last_tracker_time=current_time
        
        #logic for time_slipping
        if current_time-last_teleport_time>=teleport_times[teleport_index%20]:
            teleporting=True
            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(time_portal_open[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(time_portal_close[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            
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
                        potion_tiles=potion_tiles_init[:]

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
            elif pygame.K_z in pressed_keys and pygame.time.get_ticks()-last_set_teleport>5000:
                player1.checkpoint=player1.tile
                player1.energy-=ENERGY/20
                last_set_teleport=pygame.time.get_ticks()
                for j in range(5):
                    window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                    window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                    window.blit(checkpoint_images[j], ((vision_tile_count+1/4) * tile_size, (vision_tile_count+1/4) * tile_size))
                    #updating timer,energy and floors
                    floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                    timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                    pygame.display.flip()
                    time.sleep(0.1)
            elif pygame.K_x in pressed_keys and pygame.time.get_ticks()-last_use_teleport>5000:
                player1.energy-=ENERGY/20
                last_use_teleport=pygame.time.get_ticks()
                teleporting1=True
                for j in range(7):
                    window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                    window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
                    window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                    window.blit(space_portal_open[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                    #updating timer,energy and floors
                    floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                    timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                    pygame.display.flip()
                    time.sleep(0.1)
                for j in range(7):
                    window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                    window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                    window.blit(space_portal_close[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                    #updating timer,energy and floors
                    floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                    timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                    pygame.display.flip()
                    time.sleep(0.1)
                player1.tile=player1.checkpoint
                player1.floor=int(player1.tile[0])
            if walk_code in range(1,5):
                moved=True
                time.sleep(0.04)
            player_file.move(player1, movement_direction)
            last_movement_time = current_time 

        #logic for animation of movement
        if moved and not(player1.tile[0]==previous_tile[0] and player1.tile[1]==previous_tile[1] and player1.tile[2]==previous_tile[2]):
            for j in range(9):
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                    if player1.floor==player1.checkpoint[0] and x+player1.tile[2]==player1.checkpoint[2] and y+player1.tile[1]==player1.checkpoint[1]:
                        img=checkpoint_images[4]
                        proxy_window.blit(img, ((x+vision_tile_count+1+1/4) * tile_size, (y+vision_tile_count+1+1/4) * tile_size))
                    for j in range(len(potion_tiles)):
                        if player1.floor==potion_tiles[j][0] and x+player1.tile[2]==potion_tiles[j][2] and y+player1.tile[1]==potion_tiles[j][1]:
                            img=potion_image
                            proxy_window.blit(img, ((x+vision_tile_count+1+1/4) * tile_size, (y+vision_tile_count+1+1/4) * tile_size))
                    if player1.floor==end_point[0] and x+player1.tile[2]==end_point[2] and y+player1.tile[1]==end_point[1]:
                        img=wormhole
                        proxy_window.blit(img, ((x+vision_tile_count+1) * tile_size, (y+vision_tile_count+1) * tile_size))                    

        if teleporting:

            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(time_portal_open[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(time_portal_close[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            teleporting=False
        
        if teleporting1:
            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(space_portal_open[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            for j in range(7):
                window.blit(proxy_window,(0,0),(tile_size,tile_size,(2*vision_tile_count+1)*tile_size,(2*vision_tile_count+1)*tile_size))
                window.blit(faces[player1.orientation],((vision_tile_count)*tile_size,(vision_tile_count)*tile_size))
                window.blit(space_images_background[space_frame_index],(945,0),(0,0,355,945))
                window.blit(space_portal_close[j], ((vision_tile_count - 1) * tile_size, vision_tile_count * tile_size))
                #updating timer,energy and floors
                floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
                timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
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
                pygame.display.flip()
                time.sleep(0.1)
            teleporting1=False
    
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
        floor_number_text=Button(str(player1.floor),game_font_2,LIGHTNING_BLUE,BLACK,(1240,70))
        timer_text=Button(str(timer),game_font_2,LIGHTNING_BLUE,BLACK,(1080,240))
        timer_text.draw(window)
        floor_number_text.draw(window)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        runs+=1
    pygame.quit()
    sys.exit()





def end(window,level,result):
    #handling cases for winning and losing and doing similarly as the start window

    if result[0]==1:
        end_image = pygame.transform.scale(pygame.image.load("end_won.jpeg"), (WIDTH, HEIGHT))
        title_font = pygame.font.Font("HARRYP__.TTF", 140)
        button_font = pygame.font.Font("HARRYP__.TTF", 80)
        title = "You are free"
        title_positions = [(350, 250), (600, 250), (850, 250)]
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

    elif result[0]==0:
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

    #updating highscores
    current_score = result[1]  
    update_highscores(current_score,level)

    home = Button("Home", button_font, GOLD, BLACK, (150, 800))
    play_again = Button("Play Again", button_font, GOLD, BLACK, (500, 800))
    exit = Button("Exit", button_font, GOLD, BLACK, (950, 800))
    score_text=Button("Score : ",title_font,GOLD,BLACK,(350,500))
    score=Button(str(result[1]),title_font,LIGHTNING_BLUE,BLACK,(700,500))
    buttons=[home,play_again,exit]
    start_running = True
    while start_running:
        
        for button in buttons:
            button.draw(window)
        score_text.draw(window)
        score.draw(window)

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
                    if home.is_hovered(mouse_pos):
                        return 1,window
                    elif play_again.is_hovered(mouse_pos):
                        return 2,window
                    elif exit.is_hovered(mouse_pos):
                        return 0,window
                    
        pygame.display.flip()
    pygame.quit()
    sys.exit() 


