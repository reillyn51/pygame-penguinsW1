#Feel free to use parts of the code below in your final project!

#The code below is for generating map5 as seen in the Maps folder in the Final Project Scaffold. You can edit it to your own liking!

import pygame, sys, os
from pygame.locals import *
import time
import mixer

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Final Project Scaffold')

tile_size = (20, 20)

BACKGROUND = pygame.image.load('background.png').convert_alpha()
# BACKGROUND.blit(BACKGROUND, (900, 500))
BACKGROUND = pygame.transform.scale(BACKGROUND, (800, 600))

turret = pygame.image.load(
  "Game_Assets/Miscellaneous/turret.png").convert_alpha()
turret = pygame.transform.scale(turret, (40, 40))

turret_rect = pygame.Rect(0, 0, 40, 40)
# snowball (good to go)
snowball = pygame.image.load('Snow.png').convert_alpha()
snowball = pygame.transform.scale(snowball, (20, 20))

# stars (good to go)
star = pygame.image.load('Game_Assets/Miscellaneous/star.png').convert_alpha()
star = pygame.transform.scale(star, tile_size)
# power ups (if time)

fence = pygame.image.load('Game_Assets/Map_Tiles/fence.png').convert_alpha()
fence = pygame.transform.scale(fence, tile_size)  # (fence, (16,16))

PLAYER = pygame.image.load('Skipper.png').convert_alpha()
PLAYER = pygame.transform.scale(PLAYER, (30, 30))

PLAYER_rect = pygame.Rect(180, 575, 30, 30)
snowball_rect = pygame.Rect(PLAYER_rect.x, PLAYER_rect.y, 5, 5)
snowball_rect = screen.blit(snowball, (PLAYER_rect.x, PLAYER_rect.y))

finish = pygame.image.load('finish.png').convert_alpha()
finish = pygame.transform.scale(finish, (50, 50))
start = pygame.image.load('Checkertile.png').convert_alpha()
start = pygame.transform.scale(start, (50, 50))


def load_map(path):
  '''Function to load the map file and split it into list.

    Inputs:
    path: the folder where the map is stored

    Outputs:
    game_map: the map on the screen
    
    '''
  f = open(path + '.txt', 'r')
  data = f.read()
  f.close
  data = data.split('\n')
  game_map = []
  for row in data:
    game_map.append(list(row))
  return game_map


def collision_test(rect, tiles):
  '''
    Function to test if one rect collides with another.

    Inputs:
    rect: an objects rectangle that is going to be checked for collision
    tiles: a set of images used to make the map that is being checked for collison

    Outputs:
    hit_list: a list of tiles an object collides with
    
    '''

  hit_list = []
  for tile in tiles:
    if rect.colliderect(tile):
      hit_list.append(tile)
  return hit_list


# movement function (up, down, left, right)
def move(rect, movement, tiles):
  '''
    Function that allows characters to falling thorugh the ground.

    Inputs:
    rect: the rectangle of the player
    movement: a list of movements for the player
    tiles: a set of images used to make the map that is being checked for collison

    Outputs:
    rect: the rect of the player
    collision_types: what the player rect collides with
    
    '''
  collision_types = {
    'top': False,
    'bottom': False,
    'right': False,
    'left': False
  }
  rect.x += movement[0]
  hit_list = collision_test(rect, tiles)
  for tile in hit_list:
    if movement[0] > 0:
      rect.right = tile.left
      collision_types['right'] = True
    elif movement[0] < 0:
      rect.left = tile.right
      collision_types['left'] = True
  rect.y += movement[1]
  hit_list = collision_test(rect, tiles)
  for tile in hit_list:
    if movement[1] > 0:
      rect.bottom = tile.top
      collision_types['bottom'] = True
    elif movement[1] < 0:
      rect.top = tile.bottom
      collision_types['top'] = True

  return rect, collision_types


star_collision = []
#Loads map file
game_map = [load_map('Maps/map1'),
            load_map('Maps/map2')
            ]  #Opens the map as listed in maps.txt in the Maps folder.

PLAYER_right = False
PLAYER_left = False
PLAYER_up = False
PLAYER_down = False
HIDDEN_STAR_x = []
HIDDEN_STAR_y = []
snowball_frequency_counter = 0
snowball_rects = []
snowball_rect_list = []
collided_stars = []
hit_by_snowball_counter = 0
global level
level = 0

# background song:
from pygame import mixer

mixer.init()
pygame.mixer.music.load('Song.mp3')
pygame.mixer.music.play(-1, 0.0)

run = True
while run:
  tile_rects = []
  star_rects = []
  finish_line_rects = []
  popped_snowballs = []
  turret_number = 0
  hit_by_snowball = False

  screen.blit(BACKGROUND, (0, 0))
  y = 0
  for row in game_map[level]:
    x = 0
    for tile in row:
      if tile == '1':
        screen.blit(fence, (x * tile_size[0], y * tile_size[1]))

        tile_rects.append(
          pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0],
                      tile_size[1]))
      elif tile == '2':

        rect = pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0],
                           tile_size[1])

        if rect not in collided_stars:
          star_rects.append(rect)

      elif tile == '3':
        screen.blit(turret, (x * tile_size[0], y * tile_size[1]))
        turret_number += 1
        snowball_rect_list.append(x * tile_size[0] + 12)
        snowball_rect_list.append(y * tile_size[1] + 45)
        tile_rects.append(
          pygame.Rect(x * tile_size[0], y * tile_size[1], turret_rect[2],
                      turret_rect[3]))

      elif tile == '4':
        screen.blit(
          finish,
          (x * tile_size[0], y * tile_size[1]))  # fix this line a little
        finish_line_rects.append(
          pygame.Rect(x * tile_size[0], y * tile_size[0], tile_size[1],
                      tile_size[1]))

      elif tile == '5':
        screen.blit(
          start,
          (x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))

        pass
      x += 1
    y += 1

  # star collisions

  num_stars_collected = 0

  star_hit_list = collision_test(PLAYER_rect, star_rects)
  if star_hit_list == []:

    for s in star_rects:

      screen.blit(star, (s.x, s.y))

  elif star_hit_list != []:

    for collided_star in star_hit_list:

      collided_stars.append(collided_star)

  PLAYER_movement = [0, 0]
  if PLAYER_right:
    PLAYER_movement[0] += 2
  if PLAYER_left:
    PLAYER_movement[0] -= 2
  if PLAYER_up:
    PLAYER_movement[1] -= 2
  if PLAYER_down:
    PLAYER_movement[1] += 2

  PLAYER_rect, PLAYER_collisions = move(PLAYER_rect, PLAYER_movement,
                                        tile_rects)

  snowball_movement = 0
  # turret snowball firing
  if snowball_frequency_counter == 100:
    snowball_frequency_counter = 0
    for x in range(0, turret_number * 2 - 1, 2):
      screen.blit(snowball, (snowball_rect_list[x], snowball_rect_list[x + 1]))
      snowball_rects.append(
        pygame.Rect(snowball_rect_list[x], snowball_rect_list[x + 1], 20, 20))

  else:
    snowball_frequency_counter += 1
    snowball_movement += 2

  for x in range(0, len(snowball_rects)):
    snowball_rects[x].y += 2

    if snowball_rects[x].y > 600:
      if x in popped_snowballs == False:
        popped_snowballs.append(x)
    for tile in tile_rects:
      if snowball_rects[x].colliderect(tile):
        if x in popped_snowballs == False:
          popped_snowballs.append(x)
    screen.blit(snowball, (snowball_rects[x].x, snowball_rects[x].y))
    if PLAYER_rect.colliderect(snowball_rects[x]):
      # run = False
      '''BLACK = (0, 0, 0)
      font = pygame.font.SysFont(None, 50)
      imgage = font.render('You lose!', True, BLACK)
      screen.fill((255, 100, 100))
      screen.blit(imgage, (50, 50))
      pygame.time.wait(5000)'''
      snowball_rect_list = []
      collided_stars = []
      PLAYER_rect = pygame.Rect(180, 575, 30, 30)
      hit_by_snowball = True
      # run = False

  if hit_by_snowball:
    hit_by_snowball_counter += 1

  for snowball in popped_snowballs:
    snowball_rects.pop(snowball)

  screen.blit(PLAYER, (PLAYER_rect.x, PLAYER_rect.y))
  BLACK = (0, 0, 0)
  font_game_info = pygame.font.SysFont(None, 20)
  image_num_stars = font_game_info.render(
    f'Stars Collected: {len(collided_stars)}', True, BLACK)
  level_text = font_game_info.render(f'Level: {level + 1}', True, BLACK)
  hit_counter = font_game_info.render(
    f'Hit by snowball: {hit_by_snowball_counter} Times', True, BLACK)
  screen.blit(image_num_stars, (160, 0))
  screen.blit(level_text, (100, 0))
  screen.blit(hit_counter, (280, 0))

  hit_list_finish_line = collision_test(PLAYER_rect, finish_line_rects)
  if hit_list_finish_line != []:
    if level == 0:
      level += 1
      snowball_rect_list = []
      collided_stars = []
      PLAYER_rect = pygame.Rect(180, 575, 30, 30)

    # replicate this condition in case the rectangle needs to be changed
    # if level == 1:
    #     level += 1
    #     snowball_rect_list = []
    #     PLAYER_rect = pygame.Rect(180, 575, 30, 30)

    else:
      font = pygame.font.SysFont(None, 50)
      BLACK = (0, 0, 0)
      imgage = font.render('Congrats! You beat the game!', True, BLACK)
      screen.fill((0, 255, 0))
      screen.blit(imgage, (50, 50))
      # run = False
  #Defines which keys move the characters
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.VIDEORESIZE:
      WINDOW = pygame.display.set_mode(event.size)

    if event.type == KEYDOWN:
      if event.key == K_RIGHT:
        PLAYER_right = True
      if event.key == K_LEFT:
        PLAYER_left = True
      if event.key == K_UP:
        PLAYER_up = True
      if event.key == K_DOWN:
        PLAYER_down = True
    if event.type == KEYUP:
      if event.key == K_RIGHT:
        PLAYER_right = False
      if event.key == K_LEFT:
        PLAYER_left = False
      if event.key == K_UP:
        PLAYER_up = False
      if event.key == K_DOWN:
        PLAYER_down = False

    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  snowball_rect_list = []
  pygame.display.update()
  clock.tick(60)

#end screen
#def gameOverScreen():

# font = pygame.font.SysFont(None, 24)
# img = font.render('hello', True, BLUE)
# screen.blit(img, (20, 20))
