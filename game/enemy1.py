#Sean Nishi
#Lunk Game
#class for the player
#12/22/2022

import pygame
from settings import *
import random
import time

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/enemy1/enemy1animation1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        #modify model rect to be a slightly less tall hitbox. Will use this for movement
        self.hitbox = self.rect.inflate(0, -26)
        self.direction = pygame.math.Vector2()
        self.speed = 0.5
        random.seed(time.time())#TODO: seed with time

        self.obstacle_sprites = obstacle_sprites
        self.timer = 100

    def move(self, speed):
        self.timer +=1
        #update direction every 100 ticks. Still moves every tick
        if self.timer >= 10:
            #update/randomize direction
            #get random number
            seed = random.randint(1, 1000)
            #if odd turn left else right
            if seed %2:
                self.direction.x = -1
            else:
                self.direction.x = 1
            #if %3 false turn up else down
            if seed % 3:
                self.direction.y = -1
            else:
                self.direction.y = 1
            self.timer = 0

        #prevent diagonal moving from increasing speed
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        #update
        self.hitbox.x += self.direction.x * speed
        self.collision_check('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision_check('vertical')
        self.rect.center = self.hitbox.center

    def collision_check(self, direction):
        #horizontal collision detection
        if direction == 'horizontal':
            #look at all obstacle sprites
            for sprite in self.obstacle_sprites:
                #check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    #check direction of collision
                    if self.direction.x > 0:#moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:#moving left
                        self.hitbox.left = sprite.hitbox.right
            
        #vertical collision detection  
        if direction == 'vertical':
            #look at all sprites
            for sprite in self.obstacle_sprites:
                #check if rects collide
                if sprite.hitbox.colliderect(self.hitbox):
                    #check direction of collision
                    if self.direction.y < 0:#moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:#moving down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.move(self.speed)