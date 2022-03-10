#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      khang
#
# Created:     19-05-2017
# Copyright:   (c) khang 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#sprite classes for fighting game
import pygame as pg
from settings import *
import math
#Class for spritesheet so its convenient to load
class Spritesheet(object):
    def __init__(self,file_name):
        self.spritesheet = pg.image.load(file_name).convert()
    def get_image(self,x,y,width,height):
        image = pg.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.spritesheet, (0,0), (x,y,width,height))
        #Assuming WHITE as the transparent colour
        image.set_colorkey(WHITE)
        return image
#Player class
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game= game
        self.identity = "1"
        if self.identity == "1":
            if self.game.wraps_character1 == 1:
                self.load_images_wraps()
            elif self.game.rocky_character1 == 1:
                self.load_images_rocky()
            elif self.game.barber_character1 ==1:
                self.load_images_barber()
        #self.load_images_barber()
        self.image = self.standing_frames_r[0]
        self.pos_x = 350
        self.pos_y = 288
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 0
        self.health = 10
        self.dead = False
        self.walking = False
        self.current_frame = 0
        self.last_update= 0
        #Set jumping states
        self.canjump= True
        self.candoublejump = True
        self.cantriplejump = False
        #Only wraps can jump 3 times
        if self.game.wraps_character1 ==1 and self.identity == "1":
            self.cantriplejump = True
        self.onair = False
        self.wallslidingleft = False
        self.wallslidingright = False

        #Set facing direction
        self.direction = "R"


        self.rect= self.image.get_rect()
    #load images from sprite sheet
    def load_images_barber(self):
        #loading the idling frames
        self.standing_frames_r = [self.game.spritesheet.get_image(0, 0, 105, 93),
                                self.game.spritesheet.get_image(111, 0, 105, 93)]
        self.standing_frames_l = []
        #flip sprite to left
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame,True,False))
        self.walk_frames_r = [self.game.spritesheet.get_image(3, 198, 99, 93),
                              self.game.spritesheet.get_image(111, 201, 105, 90),
                              self.game.spritesheet.get_image(225, 198, 102, 93),
                              self.game.spritesheet.get_image(333, 201, 105, 90),
                              self.game.spritesheet.get_image(447, 198, 102, 93),
                              self.game.spritesheet.get_image(555, 201, 105, 90),
                              self.game.spritesheet.get_image(669, 198, 102, 93),
                              self.game.spritesheet.get_image(777, 201, 105, 90),]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
        self.jumping_frame = self.game.spritesheet.get_image(555,300,99,90)
        self.wallsliding_frame = self.game.spritesheet.get_image(333,297,105,93)
    def load_images_rocky(self):
        self.standing_frames_r = [self.game.spritesheet.get_image(0, 396, 102, 93),
                                self.game.spritesheet.get_image(111, 396, 102, 93)]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame,True,False))
        self.walk_frames_r = [self.game.spritesheet.get_image(3, 594, 96, 93),
                              self.game.spritesheet.get_image(111, 594, 99, 93),
                              self.game.spritesheet.get_image(225, 594, 99, 93),
                              self.game.spritesheet.get_image(333, 597, 100, 90),
                              self.game.spritesheet.get_image(447, 594, 99, 93),
                              self.game.spritesheet.get_image(555, 594, 99, 93),
                              self.game.spritesheet.get_image(669, 594, 99, 93),
                              self.game.spritesheet.get_image(777, 594, 99, 90),]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
        self.jumping_frame = self.game.spritesheet.get_image(555,693,102,93)
        self.wallsliding_frame = self.game.spritesheet.get_image(332, 693, 105, 93)
    def load_images_wraps(self):
        self.standing_frames_r = [self.game.spritesheet.get_image(0, 795, 105, 90),
                                self.game.spritesheet.get_image(111, 795, 105, 90)]
        self.standing_frames_l = []
        for frame in self.standing_frames_r:
            self.standing_frames_l.append(pg.transform.flip(frame,True,False))
        self.walk_frames_r = [self.game.spritesheet.get_image(0, 990, 102, 93),
                              self.game.spritesheet.get_image(111, 990, 102, 93),
                              self.game.spritesheet.get_image(225, 990, 102, 93),
                              self.game.spritesheet.get_image(333, 990, 102, 93),
                              self.game.spritesheet.get_image(447, 990, 102, 93),
                              self.game.spritesheet.get_image(555, 990, 102, 93),
                              self.game.spritesheet.get_image(669, 990, 102, 93),
                              self.game.spritesheet.get_image(777, 990, 102, 93),]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pg.transform.flip(frame,True,False))
        self.jumping_frame = self.game.spritesheet.get_image(555,1092,102,93)
        self.wallsliding_frame = self.game.spritesheet.get_image(335, 1089, 105, 93)


    def jump(self):
        #See if jump is available
        if self.canjump:
            self.canjump = False
            self.vel_y = JUMP_HEIGHT
        elif self.candoublejump:
            self.vel_y = JUMP_HEIGHT
            self.candoublejump = False
        elif self.cantriplejump:
            self.vel_y = JUMP_HEIGHT
            self.cantriplejump = False
    #stop moving all together
    def stop(self):
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y =0
    def update(self):
        self.animate()
        #setting death condition
        if self.health <= 0 or self.rect.bottom > 1200:
            self.dead = True
        #gravity
        self.acc_x = 0
        self.acc_y = PLAYER_GRAV
        if self.vel_y > 0:
            self.onair = True
        #Calculate direction

        keys = pg.key.get_pressed()
        #each character has different speed
        if keys[pg.K_a] and self.identity == "1":
            self.direction = "L"
            if self.game.barber_character1 == 1:
                self.acc_x = -PLAYER_ACC - 0.5
            if self.game.wraps_character1 == 1:
                self.acc_x = -PLAYER_ACC
            if self.game.rocky_character1 == 1:
                self.acc_x = -PLAYER_ACC + 0.5
            if self.wallslidingleft:
                self.acc_x = 0
        if keys[pg.K_d] and self.identity == "1":
            self.direction = "R"
            if self.game.barber_character1 == 1:
                self.acc_x = PLAYER_ACC + 0.5
            if self.game.wraps_character1 == 1:
                self.acc_x = PLAYER_ACC
            if self.game.rocky_character1 == 1:
                self.acc_x = PLAYER_ACC - 0.5
            if self.wallslidingright:
                self.acc_x = 0
        #apply friction
        if self.identity == "1":
            self.acc_x += self.vel_x * PLAYER_FRICTION
            #equations of motion
            self.vel_x += self.acc_x
            self.vel_y += self.acc_y
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
            self.pos_x += self.vel_x + 0.5*self.acc_x
            self.pos_y += self.vel_y + 0.5*self.acc_y
            #wrap around side of screen
        if self.pos_x > WIDTH:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = WIDTH
        self.rect.midbottom = (self.pos_x,self.pos_y)
        #if falling and player hits a platform, jump resets and player stands on it
        if self.vel_y > 0:
            hits = pg.sprite.spritecollide(self,self.game.platforms,False)
            if hits:
                if self.pos_y < hits[0].rect.bottom:
                    self.vel_y = 0
                    self.pos_y = hits[0].rect.top +1
                    self.onair = False
                    self.canjump = True
                    self.candoublejump = True
                    if self.game.wraps_character1 == 1 and self.identity == "1":
                        self.cantriplejump = True
        #setting list for when player collide with platforms from left and right
        solid_hits_right = pg.sprite.spritecollide(self,self.game.solid_platforms_right,False)
        solid_hits_left = pg.sprite.spritecollide(self,self.game.solid_platforms_left,False)
        #hit bottom
        if self.onair:
            solid_hits_bottom = pg.sprite.spritecollide(self,self.game.solid_platforms_bottom,False)
            if solid_hits_bottom:
                self.vel_y = 5
                self.rect.top = solid_hits_bottom[0].rect.bottom
        #hit left
        for block in solid_hits_left:
            if solid_hits_left and self.onair and self.direction == "L":
                if self.rect.y - block.rect.bottom < 0:
                    self.image = self.wallsliding_frame
                    self.vel_x = 0
                    self.acc_x =0
                    self.wallslidingleft = True
                    self.rect.left = block.rect.right
                    self.vel_y =1
        #hit right
        for block in solid_hits_right:
            if solid_hits_right and self.onair and self.direction == "R":
                if self.rect.y - block.rect.bottom < 0:
                    self.image = self.wallsliding_frame
                    self.image = pg.transform.flip(self.image, True, False)
                    self.vel_x = 0
                    self.acc_x =0
                    self.wallslidingright = True
                    self.rect.right = block.rect.left
                    self.vel_y =1
        #wallsliding
        if self.wallslidingleft == True:
            if keys[pg.K_d]:
                self.pos_x = self.rect.left +50
                self.wallslidingleft = False
                self.canjump = True
                self.candoublejump = True
        if self.wallslidingright == True:
            if keys[pg.K_a]:
                self.pos_x = self.rect.right -50
                self.wallslidingright = False
                self.canjump = True
                self.candoublejump = True

        if self.vel_y > 1:
            self.wallslidingleft = False
            self.wallslidingright = False
        if self.onair == False:
            self.wallslidingleft = False
            self.wallslidingright = False
            self.canjump = True

    def animate(self):
        #getting time
        now= pg.time.get_ticks()
        if self.vel_x != 0:
            self.walking = True
        else:
            self.walking = False
        #walk animation
        if self.onair:
            if self.direction == "R":
                self.image = self.jumping_frame
            if self.direction == "L":
                self.image =self.jumping_frame
                self.image = pg.transform.flip(self.image, True, False)

        if self.walking and not self.onair:
            #update every 100millisecond
            if now - self.last_update >  100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)% len(self.walk_frames_r)
                if self.vel_x > 0 :
                    self.direction = "R"
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.direction = "L"
                    self.image = self.walk_frames_l[self.current_frame]
        if not self.walking and not self.onair:
            if now - self.last_update> 170:
                if self.direction == "R":
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1)% len(self.standing_frames_r)
                    self.image = self.standing_frames_r[self.current_frame]
                elif self.direction == "L":
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1)% len(self.standing_frames_l)
                    self.image = self.standing_frames_l[self.current_frame]
        #using mask collision for pixel-perfect collision
        self.mask = pg.mask.from_surface(self.image)

class Player2(Player):
    def __init__(self,game):
        super().__init__(game)
        self.identity = "2"
        if self.identity == "2":
            if self.game.wraps_character2 == 1:
                self.load_images_wraps()
            elif self.game.rocky_character2 == 1:
                self.load_images_rocky()
            elif self.game.barber_character2 ==1:
                self.load_images_barber()
        #set a different spawn position for player 2
        self.pos_x = 1060
        self.pos_y = 288
        if self.game.wraps_character2 ==1 and self.identity == "2":
            self.cantriplejump = True

        self.direction = "L"
    def load_images_rocky(self):
        super().load_images_rocky()
    def load_images_barber(self):
        super().load_images_barber()
    def load_images_wraps(self):
        super().load_images_wraps()
    def jump(self):
        super().jump()
    def stop(self):
        super().stop()
    def update(self):
        super().update()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.identity == "2":
            self.direction = "L"
            if self.game.barber_character2 == 1:
                self.acc_x = -PLAYER_ACC - 0.5
            if self.game.wraps_character2 == 1:
                self.acc_x = -PLAYER_ACC
            if self.game.rocky_character2 == 1:
                self.acc_x = -PLAYER_ACC + 0.5
            if self.wallslidingleft:
                self.acc_x = 0
        if keys[pg.K_RIGHT] and self.identity == "2":
            self.direction = "R"
            if self.game.barber_character2 == 1:
                self.acc_x = PLAYER_ACC + 0.5
            if self.game.wraps_character2 == 1:
                self.acc_x = PLAYER_ACC
            if self.game.rocky_character2 == 1:
                self.acc_x = PLAYER_ACC - 0.5
            if self.wallslidingright:
                self.acc_x = 0
        if self.identity == "2":
            self.acc_x += self.vel_x * PLAYER_FRICTION
            #equations of motion
            self.vel_x += self.acc_x
            self.vel_y += self.acc_y
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
            self.pos_x += self.vel_x + 0.5*self.acc_x
            self.pos_y += self.vel_y + 0.5*self.acc_y
        if self.vel_y > 0:
            hits = pg.sprite.spritecollide(self,self.game.platforms,False)
            if hits:
                if self.pos_y < hits[0].rect.bottom:
                    self.vel_y = 0
                    self.pos_y = hits[0].rect.top + 1
                    self.onair = False
                    self.canjump = True
                    self.candoublejump = True
                    if self.game.wraps_character2 == 1 and self.identity == "2":
                        self.cantriplejump = True
        if self.wallslidingleft == True:
            if keys[pg.K_RIGHT]:
                self.pos_x = self.rect.left +50
                self.wallslidingleft = False
                self.canjump = True
                self.candoublejump = True
        if self.wallslidingright == True:
            if keys[pg.K_LEFT]:
                self.pos_x = self.rect.right -50
                self.wallslidingright = False
                self.canjump = True
                self.candoublejump = True
    def animate(self):
        super().animate()

class Projectile_player1(pg.sprite.Sprite):
    #size 51x39
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game= game
        self.identity = "1"
        self.load_images()
        self.image = self.game.spritesheet.get_image(333, 33, 51, 50)
        self.rect= self.image.get_rect()
        self.pos_x = 0
        self.pos_y= 0
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 0
        self.collided_side = ""
        self.canthrow = True
        self.direction = "R"
        self.spinning = False
        self.current_frame = 0
        self.last_update= 0
    def load_images(self):
        if self.game.barber_character1 == 1 and self.identity == "1":
            self.spinning_frames = [self.game.spritesheet.get_image(249, 27, 51, 39),
                                self.game.spritesheet.get_image(366, 21, 39, 51),
                                self.game.spritesheet.get_image(471, 27, 51, 39),
                                self.game.spritesheet.get_image(588, 21, 39, 51)]
        if self.game.rocky_character1 == 1 and self.identity == "1":
            self.spinning_frames = [self.game.spritesheet.get_image(255, 426, 39, 33),
                                self.game.spritesheet.get_image(369, 423, 33, 39),
                                self.game.spritesheet.get_image(477, 426, 39, 33),
                                self.game.spritesheet.get_image(591, 423, 33, 39)]
        if self.game.wraps_character1 == 1 and self.identity == "1":
            self.spinning_frames = [self.game.spritesheet.get_image(231, 819, 63, 42),
                                self.game.spritesheet.get_image(363, 795, 42, 63),
                                self.game.spritesheet.get_image(477, 816, 63, 42),
                                self.game.spritesheet.get_image(588, 819, 42, 63)]
    def update(self):
        self.animate()
        self.acc_x = 0
        self.acc_y = PROJECTILE_GRAV
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or self.game.player1.vel_x <0:
            self.direction = "L"
        if keys[pg.K_d] or self.game.player1.vel_x >0:
            self.direction = "R"
        if self.canthrow == True:
            if self.direction == "R":
                if keys[pg.K_y]:
                    if self.game.wraps_character1 ==1:
                        self.vel_x =10
                        self.vel_y = -10
                        self.canthrow = False
                    elif self.game.rocky_character1 ==1:
                        self.vel_x =12
                        self.vel_y = -8
                        self.canthrow = False
                    elif self.game.barber_character1 ==1:
                        self.vel_x =17
                        self.vel_y = -10
                        self.canthrow = False
            if self.direction == "L":
                if keys[pg.K_y]:
                    if self.game.wraps_character1 ==1:
                        self.vel_x =-10
                        self.vel_y = -10
                        self.canthrow = False
                    elif self.game.rocky_character1 ==1:
                        self.vel_x =-12
                        self.vel_y = -8
                        self.canthrow = False
                    elif self.game.barber_character1 ==1:
                        self.vel_x =-17
                        self.vel_y = -10
                        self.canthrow = False
        self.vel_x += self.acc_x
        self.vel_y += self.acc_y
        self.rect.x += self.vel_x + 0.5*self.acc_x
        self.rect.y += self.vel_y + 0.5*self.acc_y
        #can only throw again if the projectile has hit platform
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits and self.canthrow == False:
            self.canthrow = True
    def calc_collision(self):
        #see if the players are hit from right side or left side
        if self.rect.x < self.game.player2.rect.centerx:
            self.collided_side = "L"
        if self.rect.x > self.game.player2.rect.centerx:
            self.collided_side ="R"
    def animate(self):
        now= pg.time.get_ticks()
        if self.canthrow == False:
            if now - self.last_update >  80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)% len(self.spinning_frames)
                self.image = self.spinning_frames[self.current_frame]

        self.mask = pg.mask.from_surface(self.image)

class Projectile_player2(pg.sprite.Sprite):
    #size 51x39 or 39
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game= game
        self.identity = "2"
        self.load_images()
        self.image = self.spinning_frames[0]
        self.rect= self.image.get_rect()
        self.pos_x = 0
        self.pos_y= 0
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 0
        self.collided_side =""
        self.canthrow = True
        self.direction = "L"
        self.spinning = False
        self.current_frame = 0
        self.last_update= 0
    def load_images(self):
        if self.game.barber_character2 == 1 and self.identity == "2":
            self.spinning_frames = [self.game.spritesheet.get_image(249, 27, 51, 39),
                                self.game.spritesheet.get_image(366, 21, 39, 51),
                                self.game.spritesheet.get_image(471, 27, 51, 39),
                                self.game.spritesheet.get_image(588, 21, 39, 51)]
        if self.game.rocky_character2 == 1 and self.identity == "2":
            self.spinning_frames = [self.game.spritesheet.get_image(255, 426, 39, 33),
                                self.game.spritesheet.get_image(369, 423, 33, 39),
                                self.game.spritesheet.get_image(477, 426, 39, 33),
                                self.game.spritesheet.get_image(591, 423, 33, 39)]
        if self.game.wraps_character2 == 1 and self.identity == "2":
            self.spinning_frames = [self.game.spritesheet.get_image(231, 819, 63, 42),
                                self.game.spritesheet.get_image(363, 795, 42, 63),
                                self.game.spritesheet.get_image(477, 816, 63, 42),
                                self.game.spritesheet.get_image(588, 819, 42, 63)]
    def update(self):
        self.animate()
        self.acc_x = 0
        self.acc_y = PROJECTILE_GRAV
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or self.game.player2.vel_x <0:
            self.direction = "L"
        if keys[pg.K_RIGHT] or self.game.player2.vel_x >0:
            self.direction = "R"
        if self.canthrow == True:
            if self.direction == "R":
                if keys[pg.K_m]:
                    if self.game.wraps_character2 ==1:
                        self.vel_x =10
                        self.vel_y = -10
                        self.canthrow = False
                    elif self.game.rocky_character2 ==1:
                        self.vel_x =12
                        self.vel_y = -8
                        self.canthrow = False
                    elif self.game.barber_character2 ==1:
                        self.vel_x =17
                        self.vel_y = -10
                        self.canthrow = False
            if self.direction == "L":
                if keys[pg.K_m]:
                    if self.game.wraps_character2 ==1:
                        self.vel_x =-10
                        self.vel_y = -10
                        self.canthrow = False
                    elif self.game.rocky_character2 ==1:
                        self.vel_x =-12
                        self.vel_y = -8
                        self.canthrow = False
                    elif self.game.barber_character2 ==1:
                        self.vel_x =-17
                        self.vel_y = -10
                        self.canthrow = False
        self.vel_x += self.acc_x
        self.vel_y += self.acc_y
        self.rect.x += self.vel_x + 0.5*self.acc_x
        self.rect.y += self.vel_y + 0.5*self.acc_y
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits and self.canthrow == False:
            self.canthrow = True
    def calc_collision(self):
        if self.rect.x < self.game.player1.rect.centerx:
            self.collided_side = "L"
        if self.rect.x > self.game.player1.rect.centerx:
            self.collided_side ="R"

    def animate(self):
        now= pg.time.get_ticks()
        if self.canthrow == False:
            if now - self.last_update >  80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)% len(self.spinning_frames)
                self.image = self.spinning_frames[self.current_frame]

        self.mask = pg.mask.from_surface(self.image)
#healthbar
class Healthbar_p1(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game= game
        self.load_images()
        self.image = self.current_frame[0]
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.identity = 1
    def load_images(self):
        self.current_frame = [self.game.spritesheet.get_image(566, 1203, 337, 65),
                              self.game.spritesheet.get_image(566, 1271, 337, 65),
                              self.game.spritesheet.get_image(566, 1339, 337, 65),
                              self.game.spritesheet.get_image(566, 1407, 337, 65),
                              self.game.spritesheet.get_image(566, 1475, 337, 65),
                              self.game.spritesheet.get_image(566, 1543, 337, 65),
                              self.game.spritesheet.get_image(566, 1611, 337, 65),
                              self.game.spritesheet.get_image(566, 1679, 337, 65),
                              self.game.spritesheet.get_image(566, 1747, 337, 65),
                              self.game.spritesheet.get_image(566, 1815, 337, 65),
                              self.game.spritesheet.get_image(566, 1883, 337, 65)]
    def update(self):
        if self.game.player1.health > 0 and self.identity == 1:
            self.image = self.current_frame [10 - self.game.player1.health]
        if self.game.player1.health <= 0 and self.identity == 1:
            self.image = self.current_frame [10]


class Healthbar_p2(Healthbar_p1):
    def __init__(self,game):
        super().__init__(game)
        self.rect.x = WIDTH - 347
        self.identity = 2
    def load_images(self):
        super().load_images()
    def update(self):
        if self.game.player2.health > 0 and self.identity == 2:
            self.image = self.current_frame [10 - self.game.player2.health]
        if self.game.player2.health <= 0 and self.identity == 2:
            self.image = self.current_frame [10]


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.game= game
        self.image= image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
class solidPlatform(pg.sprite.Sprite):
    def __init__(self, game, x, y,image):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)




