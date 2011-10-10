#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame, sys, os
sys.path.append('..')
import random, math
from pygame.locals import *
from onhocommon import board
os.environ['SDL_VIDEO_CENTERED'] = '1'

liczba_graczy = 8
player_list = []

liczba_zetonow = 3
zeton_list = []

rotate = pygame.transform.rotozoom
clock = pygame.time.Clock()

color_borgo = (24, 189, 238)
color_hegemonia = (254, 195, 0)
color_moloch = (218, 47, 0)
color_posterunek = (114, 186, 0)
color_doomsdaymachines = (127, 175, 186)
color_neodzungla = (164, 155, 50)
color_nowyjork = (183, 175, 223)
color_smart = (170, 98, 38)
color_vegas = (204, 204, 202)

color_list = [
(24, 189, 238),
(254, 195, 0),
(218, 47, 0),
(114, 186, 0),
(127, 175, 186),
(164, 155, 50),
(183, 175, 223),
(170, 98, 38),
(204, 204, 202)
]

sidepanel_size = (340, 800 / liczba_graczy)
panel_list = []

zeton_imgs = ['zet1.png', 'zet2.png', 'zet3.png']
zetonsprites = []
zetonslot1 = pygame.Rect((100, 650), (150, 150))
zetonslot2 = pygame.Rect((300, 650), (150, 150))
zetonslot3 = pygame.Rect((500, 650), (150, 150))

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

#classes for our game objects

class Cursor():
    def __init__(self):
        self.image, self.rect = load_image('kursor.png', -1)
        self.clicking = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos
        if self.clicking:
            self.rect.move_ip(5, 5)

    def click(self, target):
        self.clicking = 1
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.colliderect(target.rect)

    def unclick(self):
        self.clicking = 0

class Player():
    def __init__(self):
        pass

    def color_picker(self, color):
        self.color = color

    def rect_picker(self, rect):
        self.rect = rect

class Tiles():
    def __init__(self, img, slot):
        self.image, self.rect = load_image(img, -1)
        self.original = self.image
        self.rect.center = slot.center
        self.rot_var = 0
        self.mov_var = 0
        self.angle = 0

    def _spin(self):
        center = self.rect.center
        x = self.rect.center[0] - pygame.mouse.get_pos()[0]
        y = self.rect.center[1] - pygame.mouse.get_pos()[1]
        self.angle = int(180 * math.atan2(x, y) / math.pi)

        if self.angle < 0:
            self.tile_angle = 360 + self.angle
        else:
            self.tile_angle = self.angle

        self.image = rotate(self.original, self.angle, 1)
        self.rect = self.image.get_rect(center=center)

    def _moving(self):
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        if self.rot_var:
            self._spin()
        elif self.mov_var:
            self._moving()

#   def magnes(self, x, y):
#       a = self.rect.center[0]
#       b = self.rect.center[1]
#       print self.rect.center
#       if self.rect.center[0]<x:
#           print self.rect.center
#           a = a-1
#           self.rect.move_ip(a, b)
#       elif self.rect.center[0]>x:
#           print self.rect.center
#           a = a+1
#           self.rect.move_ip(a, b)


    def clicked(self, button):
        if button == 0:
            self.rot_var = 1
        elif button == 2:
            self.mov_var = 1

    def unclicked(self):
        if self.rot_var:
            self.rot_var = 0
        elif self.mov_var:
            self.mov_var = 0

def main():
    liczba_pom = 0
    help_rect = pygame.Rect((660, 0), (0, 0))

#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode ([1000, 800])
    pygame.display.set_caption('Open Neuroshina Hex Online')
    pygame.mouse.set_visible(0)

#Mouse init
    cursor = Cursor()

#Prepare Game Objects
    while liczba_pom < liczba_graczy:
        globals()['player%s' % liczba_pom] = Player()
        player_list.append('player%s' % liczba_pom)
        liczba_pom += 1
    liczba_pom = 0

    for i in player_list:
        globals()[i].rect_picker(pygame.Rect((660, 0), sidepanel_size))
        globals()[i].rect.top = help_rect.bottom
        help_rect = globals()[i].rect
        while True:
            try:
                rand = random.randint(0, liczba_graczy - 1)
                globals()[i].color_picker(color_list.pop(rand))
            except:
                continue
            else:
                break
            liczba_pom += 1
        liczba_pom = 0

    while liczba_pom < liczba_zetonow:
        globals()['zeton%s' % str(liczba_pom + 1)] = Tiles(zeton_imgs[liczba_pom], globals()['zetonslot%s' % str(liczba_pom + 1)])
        zeton_list.append('zeton%s' % str(liczba_pom + 1))
        liczba_pom += 1
    liczba_pom = 0


#Create Layout
    plansza_rect = pygame.Rect((0, 0), (660, 660))
    plansza_img = pygame.image.load(os.path.join('data', "plansza.png")).convert_alpha()
    plansza = board.Board(width=660, height=660)

    playerpanel_size = (660, 140)

    font_small = pygame.font.Font(None, 8)
    font_big = pygame.font.Font(None, 17)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    logo = pygame.image.load(os.path.join('data', "logo.png")).convert_alpha()
#Main Loop
    while 1:
        print clock.get_fps()
        clock.tick(60)
        for i in player_list:
            screen.fill(globals()[i].color, rect=globals()[i].rect, special_flags=0)

    #Handle Input Events
        for event in pygame.event.get():
            cursor.update()
            if 1 == 1:
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
                    print "srodkowy guzik"

                elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    for i in zeton_list:
                        if cursor.click(globals()[i]):
                            globals()[i].clicked(2)
                elif event.type is MOUSEBUTTONUP:
                    cursor.unclick()
                    for i in zeton_list:
                        globals()[i].unclicked()

            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                for i in zeton_list:
                    if cursor.click(globals()[i]):
                        globals()[i].clicked(0)



            elif event.type == QUIT:
                return
        for z in zeton_list:
            globals()[z].update()

#Draw Everything

        screen.blit(plansza_img, (plansza_rect))
        for z in zeton_list:
            screen.blit(globals()[z].image, (globals()[z].rect))

        for srodek in plansza.hex_centres():
            pygame.draw.lines(screen, (0, 0, 0), True, plansza.hex_draw(srodek), 6)
            pygame.draw.lines(screen, (200, 200, 200), True, plansza.hex_draw(srodek), 2)

        screen.blit(globals()[z].image, (globals()[z].rect))
        screen.blit(cursor.image, (cursor.rect))
        pygame.display.flip()

#Game Over
