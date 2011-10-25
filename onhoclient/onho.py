#!/usr/bin/python
#-*- coding: utf-8 -*-

import pygame, sys, os
import random, math
sys.path.append('..')
from pygame.locals import *
from onhocommon import board
    
os.environ['SDL_VIDEO_CENTERED'] = '1'
SHOW_FPS = False

#settings
liczba_graczy = 5
player_list = []

liczba_zetonow = 3
zeton_list = []

chat_rect = pygame.Rect((0, 300), (625, 20))
chat_rect2 = pygame.Rect((0, 300), (625, 20))
chat_list = []
chat_buff = []

rotate = pygame.transform.rotozoom
rot_speed = 60
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

if liczba_graczy >= 5:
    sidepanel_size = (375, 700 / liczba_graczy)
else:
    sidepanel_size = (375, 750 / liczba_graczy / 2)
panel_list = []

#Pygame init
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode ([1000, 700])
pygame.display.set_caption('Open Neuroshina Hex Online')

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
    
def type():
    pass
    
def show():
    for t in chat_list:
        screen.blit(t.rendertext, t.rect)
        t.timeleft -= 0.1
        if t.timeleft <= 0:
            chat_list.remove(t)
            for tt in chat_list:
                tt.rect.bottom = tt.rect.bottom + 20
#music
pygame.mixer.music.load(os.path.join('data', "muz2.ogg"))
#pygame.mixer.music.play(-1, 0.0)

#fonts
fontsmall = pygame.font.SysFont('verdana', 12, bold=True, italic=False)
fontchat = pygame.font.SysFont('verdana', 14, bold=True, italic=False)
fontmed = pygame.font.SysFont('verdana', 16, bold=True, italic=False)
fontbig = pygame.font.SysFont('verdana', 28, bold=True, italic=False)

#Apanel
aplayer_name = ""
aplayer_color = (0,0,0)
aplayer_playername = fontmed.render("nazwa gracza", True, (255,255,255))
aplayer_playername_rect = aplayer_playername.get_rect()
#aplayer_playername = fontsmall.render(player1.name, True, (player1.color))

aplayer_timeleft = fontbig.render("1:30", True, (255,255,255))
aplayer_timeleft_rect = aplayer_timeleft.get_rect()

aplayer_panel_rect = pygame.Rect((0, 590), (625, 110))

aplayer_panel_ava, aplayer_panel_avarect = load_image("avatar.png", -1)
aplayer_panel_clk, aplayer_panel_clkrect = load_image("clock.png", -1)


aplayer_panel_res_n, aplayer_panel_resrect_n = load_image("reset_n.png", -1)
aplayer_panel_end_n, aplayer_panel_endrect_n = load_image("end_n.png", -1)

aplayer_panel_res_h, aplayer_panel_resrect_h = load_image("reset_h.png", -1)
aplayer_panel_end_h, aplayer_panel_endrect_h = load_image("end_h.png", -1)

aplayer_panel_res_d, aplayer_panel_resrect_d = load_image("reset_d.png", -1)
aplayer_panel_end_d, aplayer_panel_endrect_d = load_image("end_d.png", -1)

aplayer_panel_res, aplayer_panel_resrect = aplayer_panel_res_d, aplayer_panel_resrect_n
aplayer_panel_end, aplayer_panel_endrect = aplayer_panel_end_d, aplayer_panel_endrect_n

aplayer_panel_leftrect = pygame.Rect((0, 590), (230, 110))
aplayer_panel_avarect.left = aplayer_panel_leftrect.left + 7
aplayer_panel_avarect.bottom = aplayer_panel_leftrect.bottom - 7
aplayer_panel_timerect = pygame.Rect((87,503),(128,80))

aplayer_playername_rect.top = aplayer_panel_leftrect.top
aplayer_playername_rect.centerx = aplayer_panel_leftrect.centerx

aplayer_timeleft_rect.top = aplayer_playername_rect.bottom
aplayer_timeleft_rect.centerx = aplayer_panel_timerect.centerx + 20

aplayer_panel_clkrect.left = aplayer_panel_avarect.right + 4
aplayer_panel_clkrect.top = aplayer_panel_avarect.top
aplayer_panel_endrect.right = aplayer_panel_leftrect.right - 4
aplayer_panel_endrect.bottom = aplayer_panel_leftrect.bottom - 7
aplayer_panel_resrect.right = aplayer_panel_endrect.left - 4
aplayer_panel_resrect.bottom = aplayer_panel_leftrect.bottom - 7

aplayer_panel_rightrect = pygame.Rect((aplayer_panel_leftrect.right, 590), (aplayer_panel_rect[2] - aplayer_panel_leftrect[2] , 110))

#Tiles
zeton_imgs = ['zet1.png', 'zet2.png', 'zet3.png']
zetonsprites = []

zetonslot3 = pygame.Rect((0, 0), (10, 10))
zetonslot2 = pygame.Rect((0, 0), (10, 10))
zetonslot1 = pygame.Rect((0, 0), (10, 10))

zetonslot2.centerx = aplayer_panel_rightrect.centerx
zetonslot3.left = zetonslot2.right + 110
zetonslot1.right = zetonslot2.left - 110

zetonslot3.bottom = aplayer_panel_rightrect.bottom - 50
zetonslot2.bottom = aplayer_panel_rightrect.bottom - 50
zetonslot1.bottom = aplayer_panel_rightrect.bottom - 50

zetonslot1_occupy = True
zetonslot2_occupy = True
zetonslot3_occupy = True


#Board
plansza_rect = pygame.Rect((0, 0), (625, 590))
plansza_img = pygame.image.load(os.path.join('data', "plansza.png")).convert_alpha()

plansza = board.Board(width=555, height=520)
plansza.update()
plansza_surface = pygame.Surface((555, 520), SRCALPHA).convert_alpha()

grid_offset = (50, 10)

chat_rect.bottomleft = plansza_rect.bottomleft
chat_rect2.bottomleft = plansza_rect.bottomleft
#grid_offset = (0, 0)

def check_slots():
    global zetonslot1_occupy, zetonslot2_occupy, zetonslot3_occupy
    for o in zeton_list:
        if (zetonslot1.collidepoint(globals()[o].rect.center)):
            zetonslot1_occupy = True
            break
        else :
            zetonslot1_occupy = False
    for o in zeton_list:
        if (zetonslot2.collidepoint(globals()[o].rect.center)):
            zetonslot2_occupy = True
            break
        else :
            zetonslot2_occupy = False
    for o in zeton_list:
        if (zetonslot3.collidepoint(globals()[o].rect.center)):
            zetonslot3_occupy = True
            break
        else :
            zetonslot3_occupy = False
    return zetonslot1_occupy, zetonslot2_occupy, zetonslot3_occupy
        
        
#classes for our game objects
class Chat():
    def __init__(self, sender, text):
        self.text = text
        self.rendertext = fontchat.render(str(sender) + text, True, (player0.color))
        self.sender = sender
        self.rect = self.rendertext.get_rect()
        self.rect.bottom = chat_rect.bottom - 20 - len(chat_list)*20
        self.timeleft = 30.0
        chat_list.append(self)
        
class Cursor():
    def __init__(self):
        self.image, self.rect = load_image('kursor.png', -1)
        self.clicking = 0

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos

        if aplayer_panel_resrect.collidepoint(pos):
           globals()["aplayer_panel_res"] =  globals()["aplayer_panel_res_h"]
        else:
           globals()["aplayer_panel_res"] =  globals()["aplayer_panel_res_n"]
        if aplayer_panel_endrect.collidepoint(pos):
           globals()["aplayer_panel_end"] =  globals()["aplayer_panel_end_h"]
        else:
           globals()["aplayer_panel_end"] =  globals()["aplayer_panel_end_n"]
         

    def click(self, target):
        self.clicking = 1
        hitbox = self.rect
        try:
            return target.rect.collidepoint(pygame.mouse.get_pos())
            print "zeton"
        except:
            return target.collidepoint(pygame.mouse.get_pos())
        
    def unclick(self):
        self.clicking = 0
        aplayer_panel_resrect.bottom = aplayer_panel_rect.bottom - 7
        aplayer_panel_endrect.bottom = aplayer_panel_rect.bottom - 7
        aplayer_panel_endrect.right = aplayer_panel_leftrect.right - 4
        aplayer_panel_resrect.right = aplayer_panel_endrect.left - 4


class Player():
    def __init__(self, name):
        self.name = fontsmall.render(name, True, (0, 0, 0))
        self.namerect = self.name.get_rect()
        self.leftrect = pygame.Rect((0, 0),(50, sidepanel_size[1]))
        self.ava, self.avarect = load_image("ava.png", -1)
        self.revers, self.reversrect = load_image("revers.png", -1)
        self.hpleft = 20
        self.hp = fontbig.render(str(self.hpleft), True, (255, 255, 255))
        self.hprect = self.hp.get_rect()
        self.rank = 100
        self.rightrect = pygame.Rect((0, 0),(80, sidepanel_size[1]))
        self.tilesleft = 35
        self.tiles = fontmed.render(str(self.tilesleft)+"/35", True, (255, 255, 255))
        self.tilesrect = self.tiles.get_rect()

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

        self.angle = self.tile_angle
        self.image = rotate(self.original, self.angle, 1)
        self.rect = self.image.get_rect(center=center)

    def _moving(self):
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        if self.rot_var:
            self._spin()
        elif self.mov_var:
            self._moving()

    def _rot(self, znak):
        center = self.rect.center
        clock.tick(rot_speed)
        self.angle += znak
        self.image = rotate(self.original, self.angle, 1)
        self.rect = self.image.get_rect(center=center)
        screen.blit(plansza_img, (plansza_rect))
        screen.blit(plansza_surface, (grid_offset))
        screen.blit(self.image, (self.rect))
        pygame.draw.line(screen, (70, 70, 70), (player1.rect.left -1 ,0), (aplayer_panel_rect.right - 1, 700), 1)
        for z in zeton_list:
            screen.blit(globals()[z].image, (globals()[z].rect))
        pygame.display.flip()

    def rotomagnes(self):
        if self.angle > 30 and self.angle < 60:
            while self.angle < 60:
                self._rot(1)
        elif self.angle > 60 and self.angle <= 90:
            while self.angle > 60:
                self._rot(-1)

        elif self.angle > 90 and self.angle < 120:
            while self.angle < 120:
                self._rot(1)
        elif self.angle > 120 and self.angle <= 150:
            while self.angle > 120:
                self._rot(-1)

        elif self.angle > 150 and self.angle < 180:
            while self.angle < 180:
                self._rot(1)
        elif self.angle > 180 and self.angle <= 210:
            while self.angle > 180:
                self._rot(-1)

        elif self.angle > 210 and self.angle < 240:
            while self.angle < 240:
                self._rot(1)
        elif self.angle > 240 and self.angle <= 270:
            while self.angle > 240:
                self._rot(-1)

        elif self.angle > 270 and self.angle < 300:
            while self.angle < 300:
                self._rot(1)
        elif self.angle > 300 and self.angle <= 330:
            while self.angle > 300:
                self._rot(-1)

        elif self.angle > 330 and self.angle < 360:
            while self.angle < 360:
                self._rot(1)
        elif self.angle > 0 and self.angle <= 30:
            while self.angle > 0:
                self._rot(-1)


    def clicked(self, button):
        if button == 0:
            self.rot_var = 1
        elif button == 2:
            self.mov_var = 1

    def unclicked(self):
        if self.rot_var:
            self.rot_var = 0
            self.rotomagnes()
        elif self.mov_var:
            self.mov_var = 0

def main():
    chat = False
    chat_lock = False
    chat_buff = []
    chat_buff2 = []
    chat_text = ""
    chat_text2 = ""
    
    liczba_pom = 0
    help_rect = pygame.Rect((660, 0), (0, 0))

#Mouse init
    cursor = Cursor()

#Prepare Game Objects
    while liczba_pom < liczba_graczy:
        globals()['player%s' % liczba_pom] = Player("Plajer %s" % str(liczba_pom + 1))
        player_list.append('player%s' % liczba_pom)
        liczba_pom += 1
    liczba_pom = 0

    for i in player_list:
        globals()[i].rect_picker(pygame.Rect((625, 0), sidepanel_size))
        globals()[i].rect.top = help_rect.bottom + 1
        help_rect = globals()[i].rect
        globals()[i].namerect.centerx = globals()[i].rect.centerx - (globals()[i].rightrect[2]/2) + globals()[i].namerect[2]/2
        globals()[i].namerect.top = globals()[i].rect.top + 5
        globals()[i].leftrect.topleft = globals()[i].rect.topleft
        globals()[i].avarect.topleft = globals()[i].rect.topleft
        globals()[i].avarect.left = globals()[i].avarect.left + 5
        globals()[i].avarect.top = globals()[i].avarect.top + 5
        globals()[i].hprect.bottomleft = globals()[i].rect.bottomleft
        globals()[i].hprect.centerx = globals()[i].leftrect.centerx
        globals()[i].rightrect.topright = globals()[i].rect.topright
        globals()[i].tilesrect.bottomleft = globals()[i].rightrect.bottomleft
        globals()[i].tilesrect.bottom = globals()[i].rightrect.bottom - 5
        globals()[i].tilesrect.centerx = globals()[i].rightrect.centerx
        globals()[i].reversrect.midbottom = globals()[i].tilesrect.midtop
        globals()[i].reversrect.top = globals()[i].reversrect.top + 5
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

    for srodek in plansza.hex_centres:
        pygame.draw.polygon(plansza_surface, (0, 0, 0), plansza.hex_draw(srodek), 7)
        pygame.draw.polygon(plansza_surface, (150, 150, 150), plansza.hex_draw(srodek), 3)
        pygame.draw.polygon(plansza_surface, (255, 255, 255), plansza.hex_draw(srodek), 1)


#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Main Loop
    while 1:
        clock.tick(60)

#Test stuff
        if SHOW_FPS == 1:
            print clock.get_fps()

#Drawing GRID
        screen.blit(plansza_img, (plansza_rect))
        screen.blit(plansza_surface, ((grid_offset)))
        
#Drawing APANEL
        screen.fill((0,0,0), rect=aplayer_panel_leftrect)
        screen.fill((player0.color), rect=aplayer_panel_rightrect)
#        screen.fill((aplayer_color), rect=aplayer_panel_rect)
        pygame.draw.line(screen, (70, 70, 70), (aplayer_panel_rect.topleft), (aplayer_panel_rect.topright), 1)
        screen.blit(aplayer_panel_ava, (aplayer_panel_avarect))
        screen.blit(aplayer_playername, aplayer_playername_rect)
        screen.blit(aplayer_timeleft, aplayer_timeleft_rect)
        screen.blit(aplayer_panel_clk, (aplayer_panel_clkrect))
        screen.blit(aplayer_panel_res, (aplayer_panel_resrect))
        screen.blit(aplayer_panel_end, (aplayer_panel_endrect))
        pygame.draw.line(screen, (70, 70, 70), (player1.rect.left -1 ,0), (aplayer_panel_rect.right - 1, 700), 1)
        
#Drawing tiles
        for z in zeton_list:
            screen.blit(globals()[z].image, (globals()[z].rect))

#Drawing player panels
        for i in player_list:
            pygame.draw.line(screen, (70, 70, 70), (globals()[i].rect.bottomleft), (globals()[i].rect.bottomright), 4)
            screen.fill(globals()[i].color, rect=globals()[i].rect)
            screen.fill((0, 0, 0),rect=globals()[i].leftrect)
            screen.blit(globals()[i].name, globals()[i].namerect)
            screen.blit(globals()[i].ava, globals()[i].avarect)
            screen.blit(globals()[i].hp, globals()[i].hprect)
            screen.fill((0, 0, 0),rect=globals()[i].rightrect)
            screen.blit(globals()[i].tiles, globals()[i].tilesrect)
            screen.blit(globals()[i].revers, globals()[i].reversrect)
            if chat == True:
                screen.fill((0, 0, 0),rect=chat_rect)
                screen.blit(fontsmall.render(chat_text, True, (255, 255, 255)), chat_rect)
                screen.blit(fontsmall.render(chat_text2, True, (255, 255, 255)), chat_rect2)

            
        show()
        screen.blit(cursor.image, (cursor.rect))

#Handle Input Events
        for event in pygame.event.get():
            pygame.key.set_repeat(10000, 10000)
            cursor.update()
            if 1 == 1:
                
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
                    print "srodkowy guzik"

                elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    for i in zeton_list:
                        if cursor.click(globals()[i]):
                            globals()[i].clicked(2)
                            break
                    if cursor.click(aplayer_panel_resrect):
                        print "reset"
                        aplayer_panel_resrect.move_ip(3,3)
                        pass
                    elif cursor.click(aplayer_panel_endrect):
                        print "koniec tury"
                        aplayer_panel_endrect.move_ip(3,3)
                        pass
                            
                            
                elif event.type is MOUSEBUTTONUP:
                    cursor.unclick()
                    for i in zeton_list:
                        if globals()[i].mov_var:
                            help1 = pygame.mouse.get_pos()[0] - grid_offset[0]
                            help2 = pygame.mouse.get_pos()[1] - grid_offset[1]
                            czy_nad_hexem, index_pola, srodek_pola = plansza.position_on_hex((help1, help2))
                            if czy_nad_hexem:
                                globals()[i].rect.center = srodek_pola + grid_offset
                            else:
                                check_slots()
                                if zetonslot1_occupy == False:
                                    globals()[i].rect.center = zetonslot1.center
                                elif zetonslot2_occupy == False:
                                    globals()[i].rect.center = zetonslot2.center
                                elif zetonslot3_occupy == False:
                                    globals()[i].rect.center = zetonslot3.center
                        globals()[i].unclicked()

            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                for i in zeton_list:
                    if cursor.click(globals()[i]):
                        globals()[i].clicked(0)
                        break
  
            if chat == True:
                chat_lock = True
                if len(chat_text)<58:
                    chat_rect.height = 20
                    chat_rect.bottomleft = plansza_rect.bottomleft                
                    if event.type == KEYDOWN and event.key != K_BACKSPACE and event.key != K_RETURN and event.key != K_TAB:
                        chat_buff.append(event.unicode)
                        chat_text = ''.join(chat_buff)   
                    elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                        try:
                            chat_buff.pop()
                        except:
                            pass
                            
                        chat_text = ''.join(chat_buff)         
                            
                elif len(chat_text)==58 and len(chat_text2)<60:
                    chat_rect.height = 40
                    chat_rect.bottomleft = plansza_rect.bottomleft
                    if event.type == KEYDOWN and event.key != K_BACKSPACE and event.key != K_RETURN and event.key != K_TAB:
                        chat_buff2.append(event.unicode)
                        chat_text2 = ''.join(chat_buff2)   
                    elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                        try:
                            chat_buff2.pop()
                        except:
                            chat_buff.pop()
                            
                        chat_text = ''.join(chat_buff)
                        chat_text2 = ''.join(chat_buff2)  


                          
            if chat == False and event.type == KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                chat = True
            elif chat == True and chat_lock == True and chat_text == "" and event.type == KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                chat = False
                chat_lock = False
            elif chat == True and chat_lock == True and chat_text != "" and event.type == KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                if chat_buff2 != []:
                    Chat("",chat_text2)
                    Chat("player1"+": ",chat_text)
                else:
                    Chat("player1"+": ",chat_text)
                chat = False
                chat_lock = False
                chat_buff = []
                chat_buff2 = []
                chat_text = ""
                chat_text2 = ""

                
            elif event.type == QUIT:
                return
        for z in zeton_list:
            globals()[z].update()

#Screen flip
        pygame.display.flip()

if __name__ == '__main__':
    main()
