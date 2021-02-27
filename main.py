import pygame
import sys
import os
import time

from pygame.locals import *

from vector import *
from sprite import *
from player import *
from level import *
from block import *
from obstacle import *

########## SETUP ##########
## constants ##
WIDTH = 1024
HEIGHT = 768
SCALE = 64
TARGET_UPDATE_INTERVAL = 1 / 30
RENDER_DISTANCE_HORIZONTAL = 9
RENDER_DISTANCE_VERTICAL = 7

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ake: The Pathfinder")

########## INPUT ##########

input_dict = {
    "UP": False,
    "LEFT": False,
    "RIGHT": False,
    "ENTER": False
    }


########## GAME DATA ##########
level = Level()
level_data = level.get_data()

playing = [False]

play_time_final = [0.0]
play_time_start = [time.time()]

########## LOAD ASSETS ##########
# load images
background_sprite = Sprite("sprites/background.png")

chest_sprite = Sprite("sprites/chest.png")


dirt_sprite_list = [Sprite("sprites/dirt.png"),                     # 0
                    Sprite("sprites/dirt_top.png"),                 # 1
                    Sprite("sprites/dirt_right.png"),               # 2
                    Sprite("sprites/dirt_bottom.png"),              # 3
                    Sprite("sprites/dirt_left.png"),                # 4
                    Sprite("sprites/dirt_corner_top_left.png"),     # 5
                    Sprite("sprites/dirt_corner_top_right.png"),    # 6
                    Sprite("sprites/dirt_corner_bottom_left.png"),  # 7
                    Sprite("sprites/dirt_corner_bottom_right.png"), # 8
                    Sprite("sprites/dirt_edge_top_left.png"),       # 9
                    Sprite("sprites/dirt_edge_top_right.png"),      # a
                    Sprite("sprites/dirt_edge_bottom_left.png"),    # b
                    Sprite("sprites/dirt_edge_bottom_right.png"),   # c
                    Sprite("sprites/dirt_whole.png")                # d
                    ]

lava_sprite_sheet_list = [Sprite_sheet("sprites/lava.png", Vector(64, 64), 3, 25),
                          Sprite_sheet("sprites/lava.png", Vector(64, 64), 3, 25),
                          Sprite_sheet("sprites/lava.png", Vector(64, 64), 3, 25)
                          ]
lava_sprite_sheet_list[1].set_current_index(1)
lava_sprite_sheet_list[2].set_current_index(2)
spike_sprite_sheet_list = [Sprite_sheet("sprites/spike_bottom.png", Vector(64, 64), 1, 1),
                           Sprite_sheet("sprites/spike_left.png", Vector(64, 64), 1, 1),
                           Sprite_sheet("sprites/spike_right.png", Vector(64, 64), 1, 1)
                           ]

player_sprite_sheet_dict = {
    "IDLE": Sprite_sheet("sprites/player_idle.png", Vector(30, 54), 1, 1),
    "WALKING RIGHT": Sprite_sheet("sprites/player_walking_right.png", Vector(29, 56), 8, 2),
    "WALKING LEFT": Sprite_sheet("sprites/player_walking_left.png", Vector(29, 56), 8, 2),
    "JUMPING FRONT": Sprite_sheet("sprites/player_jumping_front.png", Vector(32, 55), 1, 1),
    "JUMPING RIGHT": Sprite_sheet("sprites/player_jumping_right.png", Vector(30, 54), 1, 1),
    "JUMPING LEFT": Sprite_sheet("sprites/player_jumping_left.png", Vector(30, 54), 1, 1)
    }

font_16 = pygame.font.Font("Kanit-Medium.ttf", 16)
font_32 = pygame.font.Font("Kanit-Medium.ttf", 32)
font_48 = pygame.font.Font("Kanit-Medium.ttf", 48)

# instantiate elements
background = Block(background_sprite, Vector(), Vector(WIDTH * 2, HEIGHT * 2), "")

player = [Player(player_sprite_sheet_dict, Vector(3.25 * SCALE, 3 * SCALE), Vector(33, 48))]

map_list = []
for row in range(0, len(level_data)):
    map_list.append([])
    for column in range(0, len(level_data[0])):
        if level_data[row][column] == "0":
            map_list[row].append(Block(dirt_sprite_list[0],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "1":
            map_list[row].append(Block(dirt_sprite_list[1],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "2":
            map_list[row].append(Block(dirt_sprite_list[2],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "3":
            map_list[row].append(Block(dirt_sprite_list[3],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "4":
            map_list[row].append(Block(dirt_sprite_list[4],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "5":
            map_list[row].append(Block(dirt_sprite_list[5],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "6":
            map_list[row].append(Block(dirt_sprite_list[6],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "7":
            map_list[row].append(Block(dirt_sprite_list[7],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "8":
            map_list[row].append(Block(dirt_sprite_list[8],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "9":
            map_list[row].append(Block(dirt_sprite_list[9],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "a":
            map_list[row].append(Block(dirt_sprite_list[10],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "b":
            map_list[row].append(Block(dirt_sprite_list[11],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "c":
            map_list[row].append(Block(dirt_sprite_list[12],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "d":
            map_list[row].append(Block(dirt_sprite_list[13],
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "COLLIDE"))
        elif level_data[row][column] == "L":
            map_list[row].append(Obstacle(lava_sprite_sheet_list[0],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE,
                                                      row * SCALE + SCALE * 0.1,
                                                      SCALE,
                                                      SCALE * 0.9),
                                          "GAME OVER"))
        elif level_data[row][column] == "<":
            map_list[row].append(Obstacle(lava_sprite_sheet_list[1],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE,
                                                      row * SCALE + SCALE * 0.1,
                                                      SCALE,
                                                      SCALE * 0.9),
                                          "GAME OVER"))
        elif level_data[row][column] == ">":
            map_list[row].append(Obstacle(lava_sprite_sheet_list[2],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE,
                                                      row * SCALE + SCALE * 0.1,
                                                      SCALE,
                                                      SCALE * 0.9),
                                          "GAME OVER"))
        elif level_data[row][column] == "S":
            map_list[row].append(Obstacle(spike_sprite_sheet_list[0],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE,
                                                      row * SCALE + SCALE * 0.7,
                                                      SCALE,
                                                      SCALE * 0.3),
                                          "GAME OVER"))
        elif level_data[row][column] == "[":
            map_list[row].append(Obstacle(spike_sprite_sheet_list[1],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE,
                                                      row * SCALE,
                                                      SCALE * 0.3,
                                                      SCALE),
                                          "GAME OVER"))
        elif level_data[row][column] == "]":
            map_list[row].append(Obstacle(spike_sprite_sheet_list[2],
                                          Vector(column * SCALE, row * SCALE),
                                          Vector(SCALE, SCALE),
                                          pygame.Rect(column * SCALE + SCALE * 0.7,
                                                      row * SCALE,
                                                      SCALE * 0.3,
                                                      SCALE),
                                          "GAME OVER"))
        elif level_data[row][column] == "C":
            map_list[row].append(Block(chest_sprite,
                                       Vector(column * SCALE, row * SCALE),
                                       Vector(SCALE, SCALE),
                                       "WIN"))
        else:
            map_list[row].append(0)
            
########## FUNCTIONS ##########
def update(player, playing, play_time_start):
    if playing[0]:
        if not(player[0].get_dead()) and not(player[0].get_won()):
            player[0].update(input_dict)
            player[0].collide(map_list)
    else:
        player[0].set_velocity(Vector())
        if input_dict["ENTER"]:
            player[0] = Player(player_sprite_sheet_dict, Vector(3.25 * SCALE, 3 * SCALE), Vector(33, 48))
            player[0].set_velocity(Vector())
            play_time_start[0] = time.time()
            playing[0] = True


def render():
    surface.fill(WHITE)
    background.render(surface,
                      Vector((player[0].get_position().get_x() - WIDTH/2) / 5 + 120,
                             (player[0].get_position().get_y() - HEIGHT/2) / 5 + 70))
    
    # render game objects
    for row in range(0, len(map_list)):
        for column in range(0, len(map_list[0])):
            if row >= player[0].get_position().get_y()/SCALE - RENDER_DISTANCE_VERTICAL and row <= player[0].get_position().get_y()/SCALE + RENDER_DISTANCE_VERTICAL and column >= player[0].get_position().get_x()/SCALE - RENDER_DISTANCE_HORIZONTAL and column <= player[0].get_position().get_x()/SCALE + RENDER_DISTANCE_HORIZONTAL:
                if map_list[row][column] != 0:
                    map_list[row][column].render(surface,
                                                 Vector(player[0].get_position().get_x() - WIDTH/2,
                                                 player[0].get_position().get_y() - HEIGHT/2))

    player[0].render(surface, Vector(player[0].get_position().get_x() - WIDTH/2,
                                  player[0].get_position().get_y() - HEIGHT/2))

def render_user_interface(playing, play_time_final):
    play_time = 0.0
    if playing[0] and not(player[0].get_dead()) and not(player[0].get_won()):
        play_time = get_play_time()
        play_time_obj = font_32.render("TIME: " + str(play_time), True, WHITE)
        play_time_rect = play_time_obj.get_rect()
        play_time_rect.topleft = (20, 10)
        surface.blit(play_time_obj, play_time_rect)
    elif playing[0] and player[0].get_dead():
        play_time = get_play_time()
        
        playing[0] = False
        play_time_obj = font_32.render("TIME: " + str(play_time), True, WHITE)
        play_time_rect = play_time_obj.get_rect()
        play_time_rect.topleft = (20, 10)
        surface.blit(play_time_obj, play_time_rect)
    elif playing[0] and player[0].get_won():
        play_time = get_play_time()
        play_time_final[0] = play_time
        
        playing[0] = False
        play_time_obj = font_32.render("TIME: " + str(play_time), True, WHITE)
        play_time_rect = play_time_obj.get_rect()
        play_time_rect.topleft = (20, 10)
        surface.blit(play_time_obj, play_time_rect)
    elif player[0].get_dead():
        game_over_obj = font_32.render("GAME OVER!", True, WHITE)
        game_over_rect = game_over_obj.get_rect()
        game_over_rect.center = (WIDTH/2, HEIGHT/2 - 50)
        surface.blit(game_over_obj, game_over_rect)

        play_again_obj = font_16.render("PRESS ENTER TO PLAY AGAIN.", True, WHITE)
        play_again_rect = play_again_obj.get_rect()
        play_again_rect.center = (WIDTH/2, HEIGHT/2 - 20)
        surface.blit(play_again_obj, play_again_rect)
    elif player[0].get_won():
        play_time = get_play_time()

        game_over_obj = font_32.render("YOU WON!", True, WHITE)
        game_over_rect = game_over_obj.get_rect()
        game_over_rect.center = (WIDTH/2, HEIGHT/2 - 117)
        surface.blit(game_over_obj, game_over_rect)

        play_again_obj = font_16.render("YOUR TIME IS:", True, WHITE)
        play_again_rect = play_again_obj.get_rect()
        play_again_rect.center = (WIDTH/2, HEIGHT/2 - 87)
        surface.blit(play_again_obj, play_again_rect)

        game_over_obj = font_48.render(str(play_time_final[0]), True, WHITE)
        game_over_rect = game_over_obj.get_rect()
        game_over_rect.center = (WIDTH/2, HEIGHT/2 - 60)
        surface.blit(game_over_obj, game_over_rect)

        play_again_obj = font_16.render("PRESS ENTER TO PLAY AGAIN.", True, WHITE)
        play_again_rect = play_again_obj.get_rect()
        play_again_rect.center = (WIDTH/2, HEIGHT/2 - 20)
        surface.blit(play_again_obj, play_again_rect)
    else:
        play_again_obj = font_32.render("PRESS ENTER TO PLAY.", True, WHITE)
        play_again_rect = play_again_obj.get_rect()
        play_again_rect.center = (WIDTH/2, HEIGHT/2 - 20)
        surface.blit(play_again_obj, play_again_rect)

def get_play_time():
    play_time_current = time.time()
    play_time = play_time_current - play_time_start[0]
    play_time *= 10
    play_time //= 1
    play_time /= 10
    return play_time
        
        
        
    

########## GAME LOOP ##########
running = True
time_delta = 0;
time_last = time.time()

update_delta = 0
update_count = 0

while running:
    time_current = time.time()
    time_delta += time_current - time_last
    update_delta += time_current - time_last
    time_last = time_current
    while time_delta > TARGET_UPDATE_INTERVAL:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                    input_dict["UP"] = True
                if event.key == K_a or event.key == K_LEFT:
                    input_dict["LEFT"] = True
                if event.key == K_d or event.key == K_RIGHT:
                    input_dict["RIGHT"] = True
                if event.key == K_RETURN:
                    input_dict["ENTER"] = True
            if event.type == pygame.KEYUP:
                if event.key == K_w or event.key == K_UP or event.key == K_SPACE:
                    input_dict["UP"] = False
                if event.key == K_a or event.key == K_LEFT:
                    input_dict["LEFT"] = False
                if event.key == K_d or event.key == K_RIGHT:
                    input_dict["RIGHT"] = False
                if event.key == K_RETURN:
                    input_dict["ENTER"] = False
        update(player, playing, play_time_start)
        render()
        render_user_interface(playing, play_time_final)
            
        pygame.display.update()
        
        update_count += 1
        time_delta -= TARGET_UPDATE_INTERVAL
        
    while update_delta > 1:
        update_ups = update_count
        update_count = 0
        print("UPS:", update_ups)
        update_delta -= 1

pygame.quit()
sys.exit()

