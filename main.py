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

Output:Graphics - things are drawn, sound, haptics

GAME: CS:GO

GOAL: Kill everyone on the other team, terrorist team needs to plant bomb on good team, defuse the bomb

RULES: 
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
        self.high_score = 0
        self.score = 0

    def load_data(self,map):#loads image and audio folders into program
        self.game_dir=path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt")
        self.img_dir = path.join(self.game_dir, 'images')#sets up image directory
        # sound handling
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "pickup.wav"))
        self.map = Map(path.join(self.game_dir,map))

        try:
            with open(self.game_save_file, 'x', encoding="utf-8") as file:
                file.write("hello world!")
            print("file created successfully!")

        except FileExistsError:
            print("File already exists")

        with open(self.game_save_file, 'r') as file:
            try:
                self.high_score = int(file.read())
            except:
                # self.high_score = 0
                print("high score not read...")

    def new(self):#adding the sprite to the screen
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        #self.player = Player(self, WIDTH/2, HEIGHT/2)
        #self.cactus = Wall(self, 2, 0)
        #self.enemy = Mob(self, 5, 0)

        for row, tiles in enumerate(self.map.data):#pulling out mobs and walls from text map and putting onto screen
            for col, tile, in enumerate(tiles):
                if tile=='1':#wall from map
                    Wall(self,col,row)
                if tile=="M":#mob from map
                    Mob(self,col, row)
                if tile == 'C':#coin from map
                    Coin(self, col, row)
        for row, tiles in enumerate(self.map.data):#pulling out player from text map and putting onto screen
            for col, tile, in enumerate(tiles):
                if tile=='P':
                    self.player = Player(self, col, row)
        pg.mixer.music.load(path.join(self.snd_dir, "Juhani Junkala_Stage 1.ogg"))
        pg.mixer.music.play(loops=-1)

    def run(self):#running the events/doing the drawing onto the screen
        self.playing = True
        while self.playing:#running game with ticks
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def events(self):#starting and maintaining the screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.score > self.high_score:
                    with open(path.join(self.game_dir, self.game_save_file), 'w') as f:
                        f.write(str(self.score))
                if self.playing:
                    self.playing = False
                self.running=False

    def draw_text(self, text, size, color, x, y):#text on screen settings with location and font
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def update(self):#updating sprite location when it receives an input
        self.all_sprites.update()

    def draw(self):
        # this order matters: the first things are on the bottom because they are the first to be drawn
        # the last lines in this method are drawn on top or last
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Frames per second:{1/self.dt}", 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins:{self.player.coins}", 24, WHITE, WIDTH/2, HEIGHT/7)
        self.draw_text(f"Score:{self.score}", 24, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text(f"High Score:{self.high_score}", 24, WHITE, WIDTH/2, HEIGHT/12)
        pg.display.flip()

if __name__ == "__main__":
    g = Game()#calling Game class

while g.running:#running both methods
    g.new()
    g.run()