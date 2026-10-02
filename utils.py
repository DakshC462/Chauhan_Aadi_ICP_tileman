import pygame as pg
from settings import *
from math import floor
 
class Map:#using text map, taking each element, and pasting it on screen
    def __init__(self,filename):
        self.data=[]
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth=len(self.data[0])
        self.tileheight=len(self.data)
        self.width=self.tilewidth * TILESIZE
        self.height=self.tileheight*TILESIZE
        print('map instantiated')

class Spritesheet:#access spritesheet for use in other parts of code
    def __init__(self, filename): #initializing the image into the game
        self.spritesheet = pg.image.load(filename).convert()
 
    def get_image(self, x, y, width, height):#retrieving image from file
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        new_image = pg.transform.scale(image,(width, height))
        image = new_image
        return image