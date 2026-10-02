import pygame as pg
#straightforward, just constants to use for the rest of the program
WIDTH=1024 
HEIGHT=768
TITLE = "Best Game Ever!!!"
TILESIZE = 32
FPS = 30

#colors
BGCOLOR = (80, 80, 80)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)