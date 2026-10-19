import pygame as pg
from settings import *
from pygame.sprite import Sprite#sprite attributes
from utils import *

from os import path

vec = pg.math.Vector2

def collide_hit_rect(one, two):#object that was getting collided with
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):#collision physics
    # check for x collision
    if dir == 'x':
        # checking to see if we've collided with hitrects from left or right
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're to the left of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                # reposition the player (sprite) to the left side of the wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                # reposition the player (sprite) to the right side of the wall
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        # checking to see if we've collided with hitrects from top or bottom
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're above the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                # reposition the player (sprite) to the top of the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            #checks if we are below the wall
            if hits[0].rect.centery < sprite.hit_rect.centery:
                #reposition to bottom of wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 
            sprite.vel.y = 0#reset velocity after collision
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):#player class initialized, init runs once
        self.groups = game.all_sprites#sprite group
        Sprite.__init__(self, self.groups)#initialized sprite
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))#importing spritesheet for the directory from main
        self.load_images()#loading images from sprite_sheet file
        #player dimensions, image, and color
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        #player base speed
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        #frames for animation
        self.last_update = 0
        self.current_frame = 0
        self.dir = "none"
        self.coins = 0
    
    def get_keys(self):
        # reset v to 0
        # listen for event specific to keys pressed
        # change velocity based on which key is pressed
        self.vel = vec(0,0)
        self.dir = "none"
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:#if left arrow or a, move left
            self.vel.x = -PLAYER_SPEED
            #self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:#if right arrow or d, move right
            self.dir = "right"
            self.vel.x = PLAYER_SPEED
            #self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:#up on up arrow key or w key
            self.vel.y = -PLAYER_SPEED#y axis is inverted, going up means you have to minus player speed
            #self.vy = -PLAYER_SPEED#y axis is inverted, going up means you have to minus player speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:#down on down arrow key or s key
            self.vel.y = PLAYER_SPEED
            #self.vy = PLAYER_SPEED
        #check to see if player is moving diagonally
        if self.vel.x != 0 and self.vel.y != 0:
            #self.vel.normalize() didnt work well
            self.vel *= 0.7071
        #x != 0 and self.vy != 0:
        #   self.vx *= 0.7071
        #   self.vy *= 0.7071
    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.dir == "right":
            pass
    def load_images(self):#loading images from spritesheet. Each image is one tilesize apart, and their dimensions are one tilesize long, allowing us to go through sprite sheet and access full image
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
        self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
    def update(self):
        self.get_keys()#keys for movement
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            self.coins += 1
        self.animate()#loop through character states
        self.rect.center = self.pos#position of sprite is center instead of top left corner
        self.pos += self.vel * self.game.dt#movement
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')#x collisions - left or right
        self.hit_rect.centery = self.pos.y#colliding with center, not corners
        collide_with_walls(self, self.game.all_walls, 'y')#y collisions - up or down
        self.rect.center = self.hit_rect.center#colliding with center, not corners
        
class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        pg.draw.circle(self.image, (YELLOW), (16, 16), 16)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("wall initialized")
        print(self.rect.x)
        print(self.rect.y)
    def update(self):
        pass

class Wall(Sprite):#another sprite that is a green wall, comments and format copied from player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image=pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x=self.x
        self.rect.y=self.y
        print("wall initialized")

class Mob(Sprite):#another sprite that is a green wall, comments and format copied from player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.vx, self.vy = 500,0
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

        self.dir = "none"
        self.last_update = 0
        self.current_frame = 0
        self.hit_rect = MOB_HIT_RECT
        print("mob initialized")
        print(self.rect.x)
        print(self.rect.y)

    def load_images(self):
            self.idle_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                                ]
            self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                                ]    
    def animate(self):
            # use the time element to get now
            now = pg.time.get_ticks()
            if self.dir == "none":
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    bottom = self.rect.bottom
                    self.image = self.idle_frames[self.current_frame]
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
            elif self.dir == "right":
                pass
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0
    
    def update(self):#moving left to right, boucing off of end, going down, and moving right to left
        self.animate()
        self.chase(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center