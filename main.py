#This file was created by: Daksh Chauhan
#Code inspired by game dev Chris Bradfield who was inspired by Notch

import pygame as pg
from sprites import *
from settings import *
from utils import *

'''
Data types: boolean, JSON, strongs

Input(events): keyboard, mouse, right click, voice, 
power button, eye tracking, camera, gyroscoping, electrostatic,
location, volume button, microphone

Process: cursor position, position of the player, score, enemy position, 
velocity, aim in FPS, 

Output:Graphics - things are drawn, sound, haptics, 
'''

class Game:#something that contains objects, organized
    def __init__(self):#a method within class to add attributes to the class game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("Game initialized...")
        pg.display.set_caption(TITLE)
        self.running=True#game running in the background(pause, home screen)
        self.playing=True#actual game being played
        self.clock = pg.time.Clock()

    def load_data(self,map):
        self.game_dir=path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')#sets up image directory
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.map = Map(path.join(self.game_dir,map))

    def new(self):#adding the sprite to the screen
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        #self.player = Player(self, WIDTH/2, HEIGHT/2)
        #self.cactus = Wall(self, 2, 0)
        #self.enemy = Mob(self, 5, 0)

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='1':
                    Wall(self,col,row)
                if tile=="M":
                    pass
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile=='P':
                    Player(self,col,row)

    def run(self):#running the events/doing the drawing onto the screen
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def events(self):#starting and maintaining the screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running=False

    def update(self):#updating sprite location when it receives an input
        self.all_sprites.update()

    def draw(self):#draw the screen and the sprites on the screen
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()#calling Game class

while g.running:#running both methods
    g.new()
    g.run()