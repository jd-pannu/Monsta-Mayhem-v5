#-------------------------------------------------------------------------------
# Name:        Main Menu
# Purpose:
#
# Author:      4601080
#
# Created:     16/05/2017
# Copyright:   (c) 4601080 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame as pg
import random
from settings import *
from sprites import *
from time import sleep
#variables for character select
wraps_character1 = 0
barber_character1 = 0
rocky_character1 = 0
wraps_character2 = 0
barber_character2 = 0
rocky_character2 = 0

class Game:
    def __init__(self):
        #initialize game window
        pg.init()
        pg.mixer.init()
        self.screen= pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.bg = pg.image.load("Background_Image.png").convert()
        self.title = pg.image.load("title.png").convert()
        self.title.set_colorkey(WHITE)
        self.wraps_character1 = 0
        self.barber_character1 = 0
        self.rocky_character1 = 0
        self.wraps_character2 = 0
        self.barber_character2 = 0
        self.rocky_character2 = 0
        self.end =False
        self.clock = pg.time.Clock()
        self.running= True
        self.playing = True
        self.load_data()
    def load_data(self):
        #load spritesheet
        self.spritesheet = Spritesheet("Spritesheet.png")

    def new(self):
        #start new game

        #List of all sprites
        self.all_sprites= pg.sprite.Group()
        #Spawn players
        self.player1= Player(self)
        self.player2 = Player2(self)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        #List of platforms
        #Standable platform
        self.platforms = pg.sprite.Group()
        self.platform_1 = Platform(self,120 - 120,508 - 50,self.spritesheet.get_image(26,1212,438,60))
        self.platform_2 = Platform(self,852 - 200,658- 350,self.spritesheet.get_image(26,1212,438,60))
        self.all_sprites.add(self.platform_1)
        self.all_sprites.add(self.platform_2)
        self.platforms.add(self.platform_1)
        self.platforms.add(self.platform_2)
        #Healthbar
        self.healthbar_p1 = Healthbar_p1(self)
        self.healthbar_p2 = Healthbar_p2(self)
        self.all_sprites.add(self.healthbar_p1)
        self.all_sprites.add(self.healthbar_p2)
        #Solid platform
        self.solid_platforms_left = pg.sprite.Group()
        self.solid_platforms_right = pg.sprite.Group()
        self.solid_platforms_bottom = pg.sprite.Group()
        #List of projectiles
        self.projectiles_list_player1 = pg.sprite.Group()
        self.projectiles_list_player2 = pg.sprite.Group()
        self.projectile_player1 = Projectile_player1(self)
        self.projectile_player2 = Projectile_player2(self)

        #Platforms position
        #Solid left
        self.solid_platform_l1 = solidPlatform(self,339- 120,550 - 50,self.spritesheet.get_image(252,1279,214,428))
        self.solid_platform_l2 = solidPlatform(self,1071 - 200,700 - 350,self.spritesheet.get_image(252,1279,214,428))
        self.all_sprites.add(self.solid_platform_l1)
        self.all_sprites.add(self.solid_platform_l2)
        self.solid_platforms_left.add(self.solid_platform_l1)
        self.solid_platforms_left.add(self.solid_platform_l2)

        #Solid right
        self.solid_platform_r1 = solidPlatform(self,125 - 120,550 - 50,self.spritesheet.get_image(20,1279,214,428))
        self.solid_platform_r2 = solidPlatform(self,857 - 200,700- 350,self.spritesheet.get_image(20,1279,214,428))
        self.all_sprites.add(self.solid_platform_r1)
        self.all_sprites.add(self.solid_platform_r2)
        self.solid_platforms_right.add(self.solid_platform_r1)
        self.solid_platforms_right.add(self.solid_platform_r2)



        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing and self.end == False:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - Update
        self.all_sprites.update()
        if self.player1.dead or self.player2.dead:
            self.end = True
            self.playing = False
            print(self.playing)
        #remove the projectile if it collides with objects
        for self.projectile_player1 in self.projectiles_list_player1:
            hits = pg.sprite.spritecollide(self.projectile_player1,self.platforms,False,pg.sprite.collide_mask)
            solid_platforms_bottom_hits = pg.sprite.spritecollide(self.projectile_player1,self.solid_platforms_bottom,False,pg.sprite.collide_mask)
            solid_platforms_left_hits = pg.sprite.spritecollide(self.projectile_player1,self.solid_platforms_left,False,pg.sprite.collide_mask)
            solid_platforms_right_hits = pg.sprite.spritecollide(self.projectile_player1,self.solid_platforms_right,False,pg.sprite.collide_mask)
            if hits or solid_platforms_bottom_hits or solid_platforms_left_hits or solid_platforms_right_hits:
                self.projectile_player1.canthrow = True
                self.projectiles_list_player1.remove(self.projectile_player1)
                self.all_sprites.remove(self.projectile_player1)
            if self.projectile_player1.canthrow == False and self.projectile_player1.rect.x > WIDTH -10:
                self.projectile_player1.canthrow = True
                self.projectiles_list_player1.remove(self.projectile_player1)
                self.all_sprites.remove(self.projectile_player1)

            if self.projectile_player1.canthrow == False and self.projectile_player1.rect.x < -10:
                self.projectile_player1.canthrow = True
                self.projectiles_list_player1.remove(self.projectile_player1)
                self.all_sprites.remove(self.projectile_player1)

        for self.projectile_player2 in self.projectiles_list_player2:
            hits = pg.sprite.spritecollide(self.projectile_player2,self.platforms,False,pg.sprite.collide_mask)
            solid_platforms_bottom_hits = pg.sprite.spritecollide(self.projectile_player2,self.solid_platforms_bottom,False,pg.sprite.collide_mask)
            solid_platforms_left_hits = pg.sprite.spritecollide(self.projectile_player2,self.solid_platforms_left,False,pg.sprite.collide_mask)
            solid_platforms_right_hits = pg.sprite.spritecollide(self.projectile_player2,self.solid_platforms_right,False,pg.sprite.collide_mask)
            if hits or solid_platforms_bottom_hits or solid_platforms_left_hits or solid_platforms_right_hits:
                self.projectile_player2.canthrow = True
                self.projectiles_list_player2.remove(self.projectile_player2)
                self.all_sprites.remove(self.projectile_player2)
            if self.projectile_player2.canthrow == False and self.projectile_player2.rect.x > WIDTH -10:
                self.projectile_player2.canthrow = True
                self.projectiles_list_player2.remove(self.projectile_player2)
                self.all_sprites.remove(self.projectile_player2)

            if self.projectile_player2.canthrow == False and self.projectile_player2.rect.x < -10:
                self.projectile_player2.canthrow = True
                self.projectiles_list_player2.remove(self.projectile_player2)
                self.all_sprites.remove(self.projectile_player2)
        #check to see if projectiles from player 1 has collided with player 2 and vice versa.
        player1_hit = pg.sprite.spritecollide(self.player1,self.projectiles_list_player2,False,pg.sprite.collide_mask)
        if player1_hit and self.projectile_player2.canthrow == False:
            projectile_hit_sound.play()
            self.projectile_player2.calc_collision()
            if self.wraps_character2 == 1:
                self.player1.health -=2
            elif self.barber_character2 ==1:
                self.player1.health -=1
            elif self.rocky_character2 ==1:
                self.player1.health -= 4
            if self.projectile_player2.collided_side == "L":
                self.player1.stop()
                self.player1.vel_x +=10
                if self.player1.onair:
                    self.player1.vel_x +=13
                if self.player1.walking:
                    self.player1.vel_x +=12
            elif self.projectile_player2.collided_side == "R":
                self.player1.stop()
                self.player1.vel_x -=10
                if self.player1.onair:
                    self.player1.vel_x -=13
                if self.player1.walking:
                    self.player1.vel_x +=12
            print(self.player1.health)
            self.projectile_player2.canthrow = True
            self.projectiles_list_player2.remove(self.projectile_player2)
            self.all_sprites.remove(self.projectile_player2)
        player2_hit = pg.sprite.spritecollide(self.player2,self.projectiles_list_player1,False,pg.sprite.collide_mask)
        if player2_hit  and self.projectile_player1.canthrow == False:
            projectile_hit_sound.play()
            self.projectile_player1.calc_collision()
            if self.wraps_character1 == 1:
                self.player2.health -=2
            elif self.barber_character1 ==1:
                self.player2.health -=1
            elif self.rocky_character1 ==1:
                self.player2.health -= 4
            if self.projectile_player1.collided_side == "L":
                self.player2.stop()
                self.player2.vel_x +=10
                if self.player2.onair:
                    self.player2.vel_x +=13
                if self.player2.walking:
                    self.player2.vel_x +=12
            elif self.projectile_player1.collided_side == "R":
                self.player2.stop()
                self.player2.vel_x -=10
                if self.player2.onair:
                    self.player2.vel_x -=13
                if self.player2.walking:
                    self.player2.vel_x +=12
            print(self.player2.health)
            self.projectile_player1.canthrow = True
            self.projectiles_list_player1.remove(self.projectile_player1)
            self.all_sprites.remove(self.projectile_player1)

    def events(self):
        # Game Loop - Events

        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.playing= False
                self.running = False
            if event.type == pg. KEYDOWN:
                if event.key == pg.K_w and self.player1.wallslidingleft == False and self.player1.wallslidingright == False:
                    self.player1.jump()
                    self.player1.onair = True
                if event.key == pg.K_UP and self.player2.wallslidingleft == False and self.player2.wallslidingright == False:
                    self.player2.jump()
                    self.player2.onair = True
                if self.projectile_player1.canthrow == True:
                    if event.key == pg.K_y :
                        print("y")
                        self.projectile_player1.update()
                        self.projectile_player1.rect.x = self.player1.pos_x +5
                        self.projectile_player1.rect.y = self.player1.pos_y - 50
                        self.all_sprites.add(self.projectile_player1)
                        self.projectiles_list_player1.add(self.projectile_player1)
                if self.projectile_player2.canthrow == True:
                    if event.key == pg.K_m:
                        print("m")
                        self.projectile_player2.update()
                        self.projectile_player2.rect.x = self.player2.pos_x +5
                        self.projectile_player2.rect.y = self.player2.pos_y - 50
                        self.all_sprites.add(self.projectile_player2)
                        self.projectiles_list_player2.add(self.projectile_player2)

    def gameover(self):
        mouse = pg.mouse.get_pos()
        x = mouse[0]
        y = mouse[1]
        if not self.running:
            return
        self.screen.blit(background_image, [0,0])

        #title font and display
        font = pg.font.SysFont('Agency FB', 160, True, False)
        text = font.render("Game Over", True, BLACK)
        self.screen.blit(text, [275, 90])
        font_win = pg.font.SysFont('Agency FB', 65, True, False)
        text_win_1 = font_win.render("Player 1 Wins", True, GREEN)
        text_win_2 = font_win.render("Player 2 Wins", True, GREEN)
        if self.player2.dead:
            self.screen.blit(text_win_1, [420, 300])
        elif self.player1.dead:
            self.screen.blit(text_win_2, [420, 300])

        if x >= 375 and x <= 775 and y >= 430 and y <= 495:
            self.screen.blit(button1_end_hover, [375,430])
        else:
            self.screen.blit(button1_end, [375,430])
        pg.display.flip()

    def draw(self):
        #Game Loop - draw
        self.screen.blit(self.bg,[0,0])
        self.all_sprites.draw(self.screen)
        #flip display
        pg.display.flip()


#animation classes for each sprite
class Wraps_Animation(pg.sprite.Sprite):
    def __init__(self,x,y):

        super().__init__()

        self.image = pg.image.load("Wraps_Credits.png").convert()

        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changespeed(self, x, y):

        self.change_x += x
        self.change_y += y

    def update(self):

        #animating the sprites on credits
        if self.rect.y == 380:
            self.change_y = 1
        if self.rect.y == 435:
            self.change_y = -1
        self.rect.y += self.change_y


class Rocky_Animation(pg.sprite.Sprite):
    def __init__(self,x,y):

        super().__init__()

        self.image = pg.image.load("Rocky_Credits.png").convert()

        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changespeed(self, x, y):

        self.change_x += x
        self.change_y += y

    def update(self):
        #animating the sprites on credits
        if self.rect.y == 380:
            self.change_y = 1
        if self.rect.y == 435:
            self.change_y = -1
        self.rect.y += self.change_y


class Barber_Animation(pg.sprite.Sprite):
    def __init__(self,x,y):

        super().__init__()

        self.image = pg.image.load("Barber_Credits.png").convert()

        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changespeed(self, x, y):

        self.change_x += x
        self.change_y += y

    def update(self):
        #animating the sprites on credits
        if self.rect.y == 380:
            self.change_y = 1
        if self.rect.y == 435:
            self.change_y = -1
        self.rect.y += self.change_y


def character_select_display():

    #background display
    screen.blit(background_image, [0,0])

    #title font and display
    font = pg.font.SysFont('Agency FB', 60, True, False)
    text = font.render("Character Select", True, BLACK)
    screen.blit(text, [415, 20])

    #display all content in character select

    #hover for character select
    if x > 85 and x < 85+275 and y > 125 and y < 125+350:
        screen.blit(Wraps_character_hover, [85, 125])
    else:
        screen.blit(Wraps_character, [85, 125])

    if x > 465 and x < 465+275 and y > 125 and y < 125+350:
        screen.blit(Barber_character_hover, [465, 125])
    else:
        screen.blit(Barber_character, [465, 125])

    if x > 840 and x < 840+275 and y > 125 and y < 125+350:
        screen.blit(Rocky_character_hover, [840, 125])
    else:
        screen.blit(Rocky_character, [840, 125])

    #different texts
    font_select = pg.font.SysFont('Agency FB', 37, True, False)
    text_select1_wraps = font_select.render("Player 1 has selected: Wraps ", True, GREEN)
    text_select2_wraps = font_select.render("Player 2 has selected: Wraps ", True, GREEN)
    text_select1_barber = font_select.render("Player 1 has selected: Barber ", True, GREEN)
    text_select2_barber = font_select.render("Player 2 has selected: Barber ", True, GREEN)
    text_select1_rocky = font_select.render("Player 1 has selected: Rocky ", True, GREEN)
    text_select2_rocky = font_select.render("Player 2 has selected: Rocky ", True, GREEN)


    #display for character select with the choices of character the player has made
    if wraps_character1 == 1:
        screen.blit(text_select1_wraps, [150, 575])
    else:
        if wraps_character1 == 1:
            screen.blit(text_select1_wraps, [150, 575])

    if barber_character1 == 1:
        screen.blit(text_select1_barber, [150, 575])
    else:
        if barber_character1 == 1:
            screen.blit(text_select1_barber, [150, 575])

    if rocky_character1 == 1:
        screen.blit(text_select1_rocky, [150, 575])
    else:
        if rocky_character1 == 1:
            screen.blit(text_select1_rocky, [150, 575])


    #same but for second player
    if wraps_character2 == 1:
        screen.blit(text_select2_wraps, [675, 575])
    else:
        if wraps_character2 == 1:
            screen.blit(text_select2_wraps, [675, 575])

    if barber_character2 == 1:
        screen.blit(text_select2_barber, [675, 575])
    else:
        if barber_character2 == 1:
            screen.blit(text_select2_barber, [675, 575])

    if rocky_character2 == 1:
        screen.blit(text_select2_rocky, [675, 575])
    else:
        if rocky_character2 == 1:
            screen.blit(text_select2_rocky, [675, 575])

    if wraps_character2 != 0 or barber_character2 != 0 or rocky_character2 != 0:
        if x > 390 and x < 390+400 and y > 515 and y < 515+65:
            screen.blit(button1_start_hover, [390, 515])
        else:
            screen.blit(button1_start, [390, 515])

    #if statement for hover of the back button
    if x > 2 and x <= 99 and y >= 561 and y < 561+63:
        screen.blit(button_back_hover, [-1,561])
    else:
        screen.blit(button_back, [-1,561])

    #font and display for the back button
    font_back = pg.font.SysFont('Agency FB', 30, True, False)
    text_back = font_back.render("Back", True, BLACK)
    screen.blit(text_back, [24, 575])


def credit_display():

    #background display
    screen.blit(background_image, [0,0])

    #title font and display
    font = pg.font.SysFont('Agency FB', 60, True, False)
    text = font.render("Credits", True, BLACK)
    screen.blit(text, [515, 20])

    #display all content in credit

    screen.blit(Jaideep_name, [8, 347])

    screen.blit(Khang_name, [410, 347])

    screen.blit(Mwila_name, [790, 347])

    screen.blit(Credit_box, [48, 100])


    #if statement for hover of the back button
    if x > 2 and x <= 99 and y >= 561 and y < 561+63:
        screen.blit(button_back_hover, [-1,561])
    else:
        screen.blit(button_back, [-1,561])

    #font and display for the back button
    font_back = pg.font.SysFont('Agency FB', 30, True, False)
    text_back = font_back.render("Back", True, BLACK)
    screen.blit(text_back, [24, 575])

    #all sprites being animated on the screen
    all_sprites_list.update()
    all_sprites_list.draw(screen)



def instruction_display():

    #background display
    screen.blit(background_image, [0,0])

    #title font and display
    font = pg.font.SysFont('Agency FB', 60, True, False)
    text = font.render("Controls", True, BLACK)
    screen.blit(text, [500, 20])

    #display all content in instructions

    screen.blit(Instruction_box, [48, 95])

    #if statement for hover of the back button
    if x > 2 and x <= 99 and y >= 561 and y < 561+63:
        screen.blit(button_back_hover, [-1,561])
    else:
        screen.blit(button_back, [-1,561])

    #font and display for the back button
    font_back = pg.font.SysFont('Agency FB', 30, True, False)
    text_back = font_back.render("Back", True, BLACK)
    screen.blit(text_back, [24, 575])
def test():
    print("Working")

def main_menu():

    #background display
    screen.blit(background_image, [0,0])

    screen.blit(title, [67,25])

    #if statement for hover of each button in main menu:
    # play game
    if x >= 390 and x <= 790 and y >= 200 and y <= 265:
        screen.blit(button1_hover, [390,200])
    else:
        screen.blit(button1, [390,200])
    #instructions
    if x >= 390 and x <= 790 and y >= 315 and y <= 380:
        screen.blit(button1_hover, [390,315])
    else:
        screen.blit(button1, [390,315])
    #credits
    if x >= 390 and x <= 790 and y >= 430 and y <= 495:
        screen.blit(button1_hover, [390,430])
    else:
        screen.blit(button1, [390,430])


    #font and display of the words in main menu
    font = pg.font.SysFont('Agency FB', 35, True, False)

    #text for the main menu and for the buttons
    text = font.render("Play Game", True, font_color)
    text2 = font.render("Instructions", True, font_color)
    text3 = font.render("Credits", True, font_color)

    screen.blit(text, [530, 135+75])
    screen.blit(text2, [520, 260+66])
    screen.blit(text3, [540, 395+45])
#variables for screen change
instruction = 0
credit = 0
play_game = 0
start = 0

pg.init()

#screen size
size = (1200, 626)
screen = pg.display.set_mode(size)


#sprite animation group
all_sprites_list = pg.sprite.Group()

#creating the sprite for credit
Wraps_sprite = Wraps_Animation(125, 435)
all_sprites_list.add(Wraps_sprite)

Rocky_sprite = Rocky_Animation(535, 435)
all_sprites_list.add(Rocky_sprite)

Barber_sprite = Barber_Animation(910, 435)
all_sprites_list.add(Barber_sprite)




#music import
pg.mixer.music.load("menu_music.ogg")
game_music = pg.mixer.Sound("game_music.ogg")
screen_select = pg.mixer.Sound("select_screen.wav")
projectile_hit_sound = pg.mixer.Sound("projectile_hit.wav")


#background image
background_image = pg.image.load("Background.png").convert()

#button image
button1 = pg.image.load("Button1.png").convert()
button1.set_colorkey(WHITE)

#button's hover display image
button1_hover = pg.image.load("Button2.png").convert()
button1_hover.set_colorkey(WHITE)

#back button display
button_back = pg.image.load("BackButton1.png").convert()
button_back.set_colorkey(WHITE)

#back button hover display
button_back_hover = pg.image.load("BackButton2.png").convert()
button_back_hover.set_colorkey(WHITE)

button1_end = pg.image.load("Button1_end.png").convert()
button1_end.set_colorkey(WHITE)

button1_end_hover = pg.image.load("Button2_end.png").convert()
button1_end_hover.set_colorkey(WHITE)

#title display
title = pg.image.load("title.png").convert()
title.set_colorkey(WHITE)

#credit sprite 1
credit_sprite_display1 = pg.image.load("Barber_Credits.png").convert()
credit_sprite_display1.set_colorkey(WHITE)

#credit sprite 2
credit_sprite_display2 = pg.image.load("Rocky_Credits.png").convert()
credit_sprite_display2.set_colorkey(WHITE)

#credit sprite 3
credit_sprite_display3 = pg.image.load("Wraps_Credits.png").convert()
credit_sprite_display3.set_colorkey(WHITE)

#Khang name image
Khang_name = pg.image.load("Khang_name.png").convert()
Khang_name.set_colorkey(BLACK)

#Jaideep name image
Jaideep_name = pg.image.load("Jaideep_name.png").convert()
Jaideep_name.set_colorkey(BLACK)

#Mwila name image
Mwila_name = pg.image.load("Mwila_name.png").convert()
Mwila_name.set_colorkey(BLACK)

#Credit info box
Credit_box = pg.image.load("Credit_Info_update2.png").convert()
Credit_box.set_colorkey(WHITE)

#instruction info box
Instruction_box = pg.image.load("Instruction_Info.png").convert()
Instruction_box.set_colorkey(WHITE)

#all character select images
Barber_character = pg.image.load("Barber Char_Select.png").convert()
Barber_character.set_colorkey(WHITE)

Barber_character_hover = pg.image.load("Barber Char_Select_2.png").convert()
Barber_character_hover.set_colorkey(WHITE)

Rocky_character = pg.image.load("Rocky Char_Select.png").convert()
Rocky_character.set_colorkey(WHITE)

Rocky_character_hover = pg.image.load("Rocky Char_Select_2.png").convert()
Rocky_character_hover.set_colorkey(WHITE)

Wraps_character = pg.image.load("Wraps Char_Select.png").convert()
Wraps_character.set_colorkey(WHITE)

Wraps_character_hover = pg.image.load("Wraps Char_Select_2.png").convert()
Wraps_character_hover.set_colorkey(WHITE)

#start button and hover
button1_start = pg.image.load("Button1_start.png").convert()
button1_start.set_colorkey(WHITE)

button1_start_hover = pg.image.load("Button2_start.png").convert()
button1_start_hover.set_colorkey(WHITE)

#caption image
pg.display.set_caption("Monsta Mayhem")
pg.display.set_icon(pg.image.load("Barber_Credits.png"))

done = False


clock = pg.time.Clock()

#playing music through the menu
pg.mixer.music.play(-1)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
    #if the intruction button is clicked on the menu set instruction variable to 1
    # 1 displays and 0 hides
    if event.type == pg.MOUSEBUTTONDOWN and x >= check and x <= 790 and y >= 315 and y <= 380:
            screen_select.play()
            sleep(0.3)
            instruction = 1
    #back button which is shown every where but the main menu
    #function of the back button is to set all variables to 0 and that will display the menu
    if event.type == pg.MOUSEBUTTONDOWN and x > check4 and x <= 99 and y >= 561 and y < 561+63:
        screen_select.play()
        sleep(0.3)
        instruction = 0
        credit = 0
        play_game = 0
        wraps_character1 = 0
        barber_character1 = 0
        rocky_character1 = 0
        wraps_character2 = 0
        barber_character2 = 0
        rocky_character2 = 0
        start = 0

    #the credit variable turn 1 when that button is clicked in the menu
    if event.type == pg.MOUSEBUTTONDOWN and x >= check2 and x <= 790 and y >= 430 and y <= 495:
        screen_select.play()
        sleep(0.3)
        credit = 1

    #setting the play game variable to one when the play game is clicked which will take you to character select screen
    if event.type == pg.MOUSEBUTTONDOWN and x >= check3 and x <= 790 and y >= 200 and y <= 265:
        screen_select.play()
        sleep(0.3)
        play_game = 1

    #all these button presses are involved in character select and are used to select characters same idea with swtting variables to 1 or 0
    #but this time for selecting a character not to change screens
    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_wraps_1 and x < 85+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        wraps_character1 = 1
        rocky_character1 = 0
        barber_character1 = 0

    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_barber_1 and x < 465+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        barber_character1 = 1
        rocky_character1 = 0
        wraps_character1 = 0

    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_rocky_1 and x < 840+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        rocky_character1 = 1
        barber_character1 = 0
        wraps_character1 = 0

    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_wraps_2 and x < 85+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        wraps_character2 = 1
        rocky_character2 = 0
        barber_character2 = 0

    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_barber_2 and x < 465+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        barber_character2 = 1
        rocky_character2 = 0
        wraps_character2 = 0

    if event.type == pg.MOUSEBUTTONDOWN and x > check_character_rocky_2 and x < 840+275 and y > 125 and y < 125+350:
        screen_select.play()
        sleep(0.3)
        rocky_character2 = 1
        barber_character2 = 0
        wraps_character2 = 0

    #this button is used for returning to the menu when the game end it sets all variables to 0
    if event.type == pg.MOUSEBUTTONDOWN and x >= check_back_menu and x <= 775 and y >= 430 and y <= 495:
        #playing music
        screen_select.play()
        #delay so music is played for screen change
        sleep(0.3)
        instruction = 0
        credit = 0
        play_game = 0
        wraps_character1 = 0
        barber_character1 = 0
        rocky_character1 = 0
        wraps_character2 = 0
        barber_character2 = 0
        rocky_character2 = 0
        start = 0
        pg.mixer.music.play(-1)
        game_music.stop()

    #this code is for the start button and it will be used to start the game
    #if statement is for the button and it will only activiate when the characters are selected
    #if the variables for any select for second character equals 1 the button will appear and activate
    if wraps_character2 != 0 or barber_character2 != 0 or rocky_character2 != 0:
        if event.type == pg.MOUSEBUTTONDOWN and x > check_game_start and x < 390+400 and y > 515 and y < 515+65:
            screen_select.play()
            sleep(0.3)
            start = 1
            pg.mixer.music.stop()
            game_music.play(-1)

    #mouse location variables
    mouse = pg.mouse.get_pos()
    x = mouse[0]
    y = mouse[1]

    #checks are used to stop buttons from functioning when they are not needed
    if start == 1:
        check_back_menu = 375
        check4 = 2400
    else:
        check_back_menu = 2400
        check4 = 2

    #if all varibales are 0 then menu is in display so the checks activate the menu buttons but disable the rest
    #by putting the other buttons out of range so they aren't clicked
    if credit == 0 and instruction == 0 and play_game == 0:
        check = 390
        check3 = 390
        check4 = 2400
    else:
        check = 2400
        check3 = 2400
        check4 = 2

    if instruction == 0 and play_game == 0 and credit == 0:
        check2 = 390
        check3 = 390
        check4 = 2400
    else:
        check2 = 2400
        check3 = 2400
        check4 = 2

    if play_game == 0 and instruction == 0 and credit == 0:
        check = 390
        check2 = 390
        check4 = 2400
    else:
        check = 2400
        check2 = 2400
        check4 = 2

    #checks for the characters select in which the player 1 selects first then player 2
    #to acheive this the check for player 1 are on put then turned off when they make a choice
    #the chekc is rested when the player goes back so they can pick againg if they waant to
    if play_game == 1 and instruction == 0 and credit == 0:
        check_character_wraps_1 = 85
        check_character_barber_1 = 465
        check_character_rocky_1 = 840
        check_character_wraps_2 = 2400
        check_character_barber_2 = 2400
        check_character_rocky_2 = 2400
        if wraps_character1 != 0 or barber_character1 != 0 or rocky_character1 != 0:
            check_character_wraps_1 = 2400
            check_character_barber_1 = 2400
            check_character_rocky_1 = 2400
            check_character_wraps_2 = 85
            check_character_barber_2 = 465
            check_character_rocky_2 = 840
            if wraps_character2 != 0 or barber_character2 != 0 or rocky_character2 != 0:
                check_character_wraps_1 = 2400
                check_character_barber_1 = 2400
                check_character_rocky_1 = 2400
                check_character_wraps_2 = 2400
                check_character_barber_2 = 2400
                check_character_rocky_2 = 2400
                check_game_start = 390
    else:
        check_character_wraps_1 = 2400
        check_character_barber_1 = 2400
        check_character_rocky_1 = 2400
        check_character_wraps_2 = 2400
        check_character_barber_2 = 2400
        check_character_rocky_2 = 2400
        check_back_menu = 2400
        check_game_start = 2400

    #if statements to display certain screens when the variable is 1 and it changes to 1 from button clicks
    if instruction == 1:
        #displaying intructions
        instruction_display()
    else:
        #otherwise the menu
        main_menu()
        if instruction == 1:
            instruction_display()

    if credit == 1:
        #displaying credits
        credit_display()
    else:
        if credit == 1:
            credit_display()

    if play_game == 1:
        #character select display
        character_select_display()
    else:
        if play_game == 1:
            character_select_display()

    pg.display.flip()
    #once the characters are selected putting the correct sprites in the game to use for gameplay
    if start ==1:
        g = Game()
        g.barber_character1 = barber_character1
        g.barber_character2 = barber_character2
        g.rocky_character1 = rocky_character1
        g.rocky_character2 = rocky_character2
        g.wraps_character1 = wraps_character1
        g.wraps_character2 = wraps_character2
        while g.running:
            if g.playing:
                g.new()
            if not g.running:
                done = True
            if g.end:
                g.gameover()
                for event in pg.event.get():
                    mouse = pg.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]
                    #check for closing window
                    if event.type == pg.QUIT:
                        if g.playing:
                            g.playing= False
                        g.running= False
                        done = True
                    if event.type == pg.MOUSEBUTTONDOWN and x >= 375 and x <= 775 and y >= 430 and y <= 495:
                        print("Yes")
                        if g.playing:
                            g.playing= False
                        g.running= False
                        instruction = 0
                        credit = 0
                        play_game = 0
                        wraps_character1 = 0
                        barber_character1 = 0
                        rocky_character1 = 0
                        wraps_character2 = 0
                        barber_character2 = 0
                        rocky_character2 = 0
                        start = 0

    clock.tick(60)

pg.quit()