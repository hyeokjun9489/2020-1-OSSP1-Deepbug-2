#!/usr/bin/env python
# coding: utf-8

# In[1]:


#-*- coding: utf-8 -*-
import pygame
import random
import time
import sys
from pygame.locals import *
from os import path
import datetime


pygame.init()


# 게임 화면 크기 지정
size = (800, 600)
screen = pygame.display.set_mode(size)

# 컬러지정
yellow = (250, 250, 20)
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
orange = (255,127,0)
grey = (50,50,50)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_orange = (255,215,0)

# 게임 속도(fps)지정
clock = pygame.time.Clock()
clock.tick(60)

# 키보드 연속입력
pygame.key.set_repeat(1,1)

# 파일 경로 지정
file_path = "C:/Users/user_pc/Documents/GitHub/2020-1-OSSP1-Deepbug-2/Dodge-game/"
#file_path = "C:/Users/82109/Documents/GitHub/2020-1-OSSP1-Deepbug-2/Dodge-game/"
#file_path = "C:/Users/DHKim/Documents/GitHub/2020-1-OSSP1-Deepbug-2/팀프로젝트/2020-1-OSSP1-Deepbug-2/"

# Load the background image 
background_image = pygame.image.load(file_path+"background.jpg").convert()
pygame.display.set_caption("OSSP - DeepBug - Dodge v0.0.7")

# 비행기 이미지
playerImg = pygame.image.load(file_path+"spaceship.png")
playerimg1 = pygame.image.load(file_path+"type1.png")
playerimg2 = pygame.image.load(file_path+"type2.png")
playerimg3 = pygame.image.load(file_path+"type3.png")
playerimg4 = pygame.image.load(file_path+"type4.png")

# 매뉴에 쓰는 비행기 이미지
type1_big = pygame.image.load(file_path+"type1_big.png")
type2_big = pygame.image.load(file_path+"type2_big.png")
type3_big = pygame.image.load(file_path+"type3_big.png")
type4_big = pygame.image.load(file_path+"type4_big.png")

# 운석 이미지
fireball_w = pygame.image.load(file_path+"meteor_w.png")
fireball_r = pygame.image.load(file_path+"meteor_r.png")
fireball_p = pygame.image.load(file_path+"meteor_p.png")
fireball_g = pygame.image.load(file_path+"meteor_g.png")
fireball_w_big = pygame.image.load(file_path+"meteor_w_big.png")
fireball_r_big = pygame.image.load(file_path+"meteor_r_big.png")
fireball_p_big = pygame.image.load(file_path+"meteor_p_big.png")
fireball_g_big = pygame.image.load(file_path+"meteor_g_big.png")


# 인트로 배경 이미지
intro_image = pygame.image.load(file_path+"intro_image.jpg")

display_color = (255, 255, 255)

########게임 내에 text를 넣을때 쓰는 함수
def draw_text(text,font,surface,x,y,main_color) :
    text_obj = font.render(text,True,main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj,text_rect)

# 비행기 크기는 다르게 설정함. 크기에 따라 움직임이는 방법이 달라짐
# 비행기 속도는 일정, 아이템 먹을때만 빨라지거나 느려짐
class Player(object):
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    speed_bonus = 0
    width = 40
    height = 40
    mode = 0

    def __init__(self, x, y, mode):
        self.x = x
        self.y = y
        self.mode = mode

# 비행기의 속도를 조절할 수 있는 요소
    def update(self):
        # if self.x_speed > 0:
        #     self.x_speed += self.speed_bonus
        # elif self.x_speed < 0:
        #     self.x_speed -= self.speed_bonus
        # if self.y_speed > 0:
        #     self.y_speed += self.speed_bonus
        # elif self.y_speed < 0:
        #     self.y_speed -= self.speed_bonus
        self.x += self.x_speed
        self.y += self.y_speed
        #screen.blit(playerImg, (self.x, self.y))
        global p_img, p_img2
        if self.mode == 1:
            if p_img == 1:
                screen.blit(playerimg1, (self.x, self.y))
            elif p_img == 2:
                screen.blit(playerimg2, (self.x, self.y))
            elif p_img == 3:
                screen.blit(playerimg3, (self.x, self.y))
            elif p_img == 4:
                screen.blit(playerimg4, (self.x, self.y))
        elif self.mode == 2:
            if p_img2 == 1:
                screen.blit(playerimg1, (self.x, self.y))
            elif p_img2 == 2:
                screen.blit(playerimg2, (self.x, self.y))
            elif p_img2 == 3:
                screen.blit(playerimg3, (self.x, self.y))
            elif p_img2 == 4:
                screen.blit(playerimg4, (self.x, self.y))

# 비행기위 위치를 업데이트 하는 과정
    def left_bound(self):
        if self.x <= 0:
            self.x = 0
            #self.x_speed = self.x_speed * -1
    def right_bound(self):
        if self.x > size[0] - self.width:
            self.x = size[0] - self.width
            #self.x_speed = self.x_speed * -1
    def top_bound(self):
        if self.y <= 0:
            self.y = 0
            #self.y_speed = self.y_speed * -1
    def bottom_bound(self):
        if self.y >= size[1] - self.height:
            self.y = size[1] - self.height
            #self.y_speed = self.y_speed * -1

    def bound(self):
        self.left_bound()
        self.right_bound()
        self.top_bound()
        self.bottom_bound()

    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

#운석 속도는 레벨에 따라 점점 빨라지게
# 아이템 먹으면 빨라지거나 느려짐
class Fireball(object):
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    width = 40
    height = 40
    has_reached_limit = False #This will let us know if it can de-spawn
    side = 0
    col = 0
    direction = 0

    # 암석 스폰 위치&색
    def __init__(self):
        self.side = random.randint(1,4)
        # 1 - left # 2 - top # 3 - right # 4 - bottom
        self.col = random.randint(1,8)
        # 1 - white # 2 - red # 3 - puple # 4 - green # 5 - whitebig # 6 - redbig # 7 - pupplebig # 8 - greenbig
        self.direction = random.randint(1,4)

        # 왼쪽에서 스폰. 위아래는 랜덤출력. 운석의 속도는 10으로 고정
        # 그 밑에도 출력되는 방향만 다르고 나머진 동일
        if self.side == 1:
            self.x = -60 # get to the left of the window
            self.y = random.randint(0, size[1]-self.height)
            if self.direction == 2:
                self.x_speed = 1.4142135623731*5/2
                self.y_speed = -1.4142135623731*5/2
            elif self.direction == 4:
                self.x_speed = 1.4142135623731*5/2
                self.y_speed = 1.4142135623731*5/2
            else:
                self.x_speed = 5

        elif self.side == 2:
            self.x = random.randint(0, size[0]-self.width)
            self.y = -60
            if self.direction == 1:
                self.x_speed = -1.4142135623731*5/2
                self.y_speed = 1.4142135623731*5/2
            elif self.direction == 3:
                self.x_speed = 1.4142135623731*5/2
                self.y_speed = 1.4142135623731*5/2
            else:
                self.y_speed = 5

        elif self.side == 3:
            self.x = size[0] + 60
            self.y = random.randint(0, size[1]-self.height)
            if self.direction == 2:
                self.x_speed = -1.4142135623731*5/2
                self.y_speed = -1.4142135623731*5/2
            elif self.direction == 4:
                self.x_speed = -1.4142135623731*5/2
                self.y_speed = 1.4142135623731*5/2
            else:
                self.x_speed = -5

        elif self.side == 4:
            self.x = random.randint(0, size[0]-self.width)
            self.y = size[1] + 60
            if self.direction == 1:
                self.x_speed = -1.4142135623731*5/2
                self.y_speed = -1.4142135623731*5/2
            elif self.direction == 3:
                self.x_speed = 1.4142135623731*5/2
                self.y_speed = -1.4142135623731*5/2
            else:
                self.y_speed = -5
            
    #암석 움직이는 파트 - 속도조절
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        # 운석 색상 다양화
        if self.col == 1:
            screen.blit(fireball_w, (self.x, self.y))
        elif self.col == 2:
            screen.blit(fireball_r, (self.x, self.y))
        elif self.col == 3:
            screen.blit(fireball_p, (self.x, self.y))
        elif self.col == 4:
            screen.blit(fireball_g, (self.x, self.y))
        elif self.col == 5:
            screen.blit(fireball_w_big, (self.x, self.y))
        elif self.col == 6:
            screen.blit(fireball_r_big, (self.x, self.y))
        elif self.col == 7:
            screen.blit(fireball_p_big, (self.x, self.y))
        elif self.col == 8:
            screen.blit(fireball_g_big, (self.x, self.y))

        if self.side == 1 and self.x > size[0]:
            self.has_reached_limit = True
        if self.side == 2 and self.y > size[1]:
            self.has_reached_limit = True
        if self.side == 3 and self.x < -40:
            self.has_reached_limit = True
        if self.side == 4 and self.y < -40:
            self.has_reached_limit = True

    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# 게임진행
def game_loop():
    pygame.mixer.music.load(file_path+"whilegame.wav")
    pygame.mixer.music.play(-1)

    global explosion_sound
    explosion_sound=pygame.mixer.Sound(file_path+"explosion.wav")

    global score
    global highscore
    score = 0
    highscore=0
    player = Player(size[0]/2, size[1]/2, 1)
    fireballs = []
    difficulty = 1.0

    # 랭킹구현
    if p_img == 1 :
        with open(file_path+"highscore_type1.txt", "r") as f :
            highscore = f.read()
    elif p_img == 2 :
        with open(file_path+"highscore_type2.txt", "r") as f :
            highscore = f.read()
    elif p_img == 3 :
        with open(file_path+"highscore_type3.txt", "r") as f :
            highscore = f.read()
    elif p_img == 4 :
        with open(file_path+"highscore_type4.txt", "r") as f :
            highscore = f.read()
    ##

    default_font = pygame.font.SysFont('Monospace', 28)
    screen.blit(background_image, [0, 0])

    player.update()
    pygame.display.update()

    speed = 1

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # 스페이스바로 게임 속도 조절 추가                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.x_speed = 2
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.x_speed = -2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.y_speed = 2
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.y_speed = -2
                if event.key == pygame.K_SPACE:
                    speed = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.x_speed = 0
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player.x_speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_speed = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.y_speed = 0
                if event.key == pygame.K_SPACE:
                    speed = 1

        screen.blit(background_image, [0, 0])
        draw_text('Score : {}'.format(score),default_font,screen,80,20,yellow)
        draw_text("High Score : "+str(highscore),default_font,screen,400,20,yellow)
        player.bound()
        player.update()

        ###
        now= datetime.datetime.now()
        DateAndTime = now.strftime('%Y-%m-%d %H:%M:%S')
        ##

        if len(fireballs) < difficulty:
            fireballs.append(Fireball())

        for index, fireball in enumerate(fireballs):
            fireball.update()

            if fireball.rectangle().colliderect(player.rectangle()):
                
                # 랭킹 갱신 #############
                if p_img == 1:
                    with open(file_path+"score_type1.txt","a") as v :
                        v.writelines(str(score))
                        v.write('\n')
                        v.writelines(DateAndTime)
                        v.write('\n')
                    if score > int(highscore) :
                        highscore = score
                    with open(file_path+"highscore_type1.txt", "w") as f :
                        f.write(str(highscore))
                elif p_img == 2:
                    with open(file_path+"score_type2.txt","a") as v :
                        v.writelines(str(score))
                        v.write('\n')
                        v.writelines(DateAndTime)
                        v.write('\n')
                    if score > int(highscore) :
                        highscore = score
                    with open(file_path+"highscore_type2.txt", "w") as f :
                        f.write(str(highscore))
                elif p_img == 3:
                    with open(file_path+"score_type3.txt","a") as v :
                        v.writelines(str(score))
                        v.write('\n')
                        v.writelines(DateAndTime)
                        v.write('\n')
                    if score > int(highscore) :
                        highscore = score
                    with open(file_path+"highscore_type3.txt", "w") as f :
                        f.write(str(highscore))
                elif p_img == 4:
                    with open(file_path+"score_type4.txt","a") as v :
                        v.writelines(str(score))
                        v.write('\n')
                        v.writelines(DateAndTime)
                        v.write('\n')
                    if score > int(highscore) :
                        highscore = score
                    with open(file_path+"highscore_type4.txt", "w") as f :
                        f.write(str(highscore))

                pygame.mixer.Sound.play(explosion_sound)
                pygame.mixer.music.stop()
                death_screen(score)

            if fireball.has_reached_limit:
                fireballs.pop(index)
                score += 1
                difficulty += 0.1
                player.speed_bonus += 0.5

                print (score)
                print (player.speed_bonus)

        pygame.display.update()
        if speed == 2:
            clock.tick(120)
        elif speed == 1:
            clock.tick(60)


# 게임진행 2p일때
def game_loop2():
    pygame.mixer.music.load(file_path+"whilegame.wav")
    pygame.mixer.music.play(-1)

    global explosion_sound
    explosion_sound=pygame.mixer.Sound(file_path+"explosion.wav")

    global score
    global highscore
    score = 0
    highscore=0

    player = Player(size[0]/3, size[1]/2, 1)
    player_2 = Player(size[0]*2/3, size[1]/2, 2)

    fireballs = []
    difficulty = 1.0

    # 랭킹구현
    with open(file_path+"highscore_2P.txt", "r") as f :
        highscore = f.read()

    default_font = pygame.font.SysFont('Monospace', 28)
    screen.blit(background_image, [0, 0])

    player.update()
    player_2.update()
    pygame.display.update()

    speed = 1

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # 1p키, 2p키 분할               
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_2.x_speed = 2
                if event.key == pygame.K_LEFT:
                    player_2.x_speed = -2
                if event.key == pygame.K_DOWN:
                    player_2.y_speed = 2
                if event.key == pygame.K_UP:
                    player_2.y_speed = -2

                if event.key == pygame.K_d:
                    player.x_speed = 2
                if event.key == pygame.K_a:
                    player.x_speed = -2
                if event.key == pygame.K_s:
                    player.y_speed = 2
                if event.key == pygame.K_w:
                    player.y_speed = -2

                if event.key == pygame.K_SPACE:
                    speed = 2
        

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player_2.x_speed = 0
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player.x_speed = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_2.y_speed = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.y_speed = 0
                    
                if event.key == pygame.K_SPACE:
                    speed = 1


        screen.blit(background_image, [0, 0])
        draw_text('Score : {}'.format(score),default_font,screen,80,20,yellow)
        draw_text("High Score : "+str(highscore),default_font,screen,400,20,yellow)
        player.bound()
        player_2.bound()
        player.update()
        player_2.update()

        now= datetime.datetime.now()
        DateAndTime = now.strftime('%Y-%m-%d %H:%M:%S')


        if len(fireballs) < difficulty:
            fireballs.append(Fireball())

        for index, fireball in enumerate(fireballs):
            fireball.update()

            if fireball.rectangle().colliderect(player.rectangle()) or fireball.rectangle().colliderect(player_2.rectangle()):
               #랭킹 갱신
                with open(file_path+"score_2P.txt","a") as v :
                    v.writelines(str(score))
                    v.write('\n')
                    v.writelines(DateAndTime)
                    v.write('\n')
                if score > int(highscore) :
                    highscore = score
                with open(file_path+"highscore_2P.txt", "w") as f :
                    f.write(str(highscore))


                pygame.mixer.Sound.play(explosion_sound)
                pygame.mixer.music.stop()
                death_screen(score)

            if fireball.has_reached_limit:
                fireballs.pop(index)
                score += 1
                difficulty += 0.1
                player.speed_bonus += 0.01
                player_2.speed_bonus += 0.01


        pygame.display.update()
        if speed == 2:
            clock.tick(120)
        elif speed == 1:
            clock.tick(60)


def text_objects(text, font):
       textSurface = font.render(text, True, (white))
       return textSurface, textSurface.get_rect()

def message_display(text):
       largeText = pygame.font.Font('Creepster-Regular.ttf',115)
       TextSurf, TextRect = text_objects(text, largeText)
       TextRect.center = ((size[0]/2),(size[1]/3))
       gameDisplay.blit(TextSurf, TextRect,)

def text_objects(text, font):
       textSurface = font.render(text, True, (white))
       return textSurface, textSurface.get_rect()

def message_display(text):
       largeText = pygame.font.Font('Creepster-Regular.ttf',115)
       TextSurf, TextRect = text_objects(text, largeText)
       TextRect.center = ((size[0]/2),(size[1]/3))
       gameDisplay.blit(TextSurf, TextRect,)

## 게임 매뉴 구성 부분
# 1p 모드 선택창
def select_type():
    screen.blit(intro_image, [0, 0])
    screen.blit(type1_big, [285, 90])
    screen.blit(type2_big, [395, 90])
    screen.blit(type3_big, [285, 290])
    screen.blit(type4_big, [395, 290])

    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)

    go = True
    while go:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            button("Type 1",300,200,95,50,green,black,start_game1_1)
            button("Type 2",405,200,95,50,green,black,start_game1_2)
            button("Type 3",300,400,95,50,green,black,start_game1_3)
            button("Type 4",405,400,95,50,green,black,start_game1_4)

        pygame.display.update()

# 2p모드 선택창
def select_type2():
    screen.blit(intro_image, [0, 0])
    screen.blit(type1_big, [285, 90])
    screen.blit(type2_big, [395, 90])
    screen.blit(type3_big, [285, 290])
    screen.blit(type4_big, [395, 290])

    select_font = pygame.font.SysFont('Monospace', 40)
    if choose == 1:
        draw_text('1P choose',select_font,screen,400,50,white)
    elif choose == 2:
        draw_text('2P choose',select_font,screen,400,50,white)

    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)

    go = True
    while go:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            button("Type 1",300,200,95,50,green,black,start_game2_1)
            button("Type 2",405,200,95,50,green,black,start_game2_2)
            button("Type 3",300,400,95,50,green,black,start_game2_3)
            button("Type 4",405,400,95,50,green,black,start_game2_4)

        pygame.display.update()

# 1p mode일때
def start_game1_1():
    global p_img
    p_img = 1
    main_screen()
def start_game1_2():
    global p_img
    p_img = 2
    main_screen()
def start_game1_3():
    global p_img
    p_img = 3
    main_screen()
def start_game1_4():
    global p_img
    p_img = 4
    main_screen()

# 2p mode 일때
def start_game2_1():
    global p_img, p_img2
    global choose
    if choose == 1:
        p_img = 1
        choose = 2
        select_type2()
    elif choose == 2:
        p_img2 = 1
        main_screen()
def start_game2_2():
    global p_img, p_img2
    global choose
    if choose == 1:
        p_img = 2
        choose = 2
        select_type2()
    elif choose == 2:
        p_img2 = 2
        main_screen()
def start_game2_3():
    global p_img, p_img2
    global choose
    if choose == 1:
        p_img = 3
        choose = 2
        select_type2()
    elif choose == 2:
        p_img2 = 3
        main_screen()
def start_game2_4():
    global p_img, p_img2
    global choose
    if choose == 1:
        p_img = 4
        choose = 2
        select_type2()
    elif choose == 2:
        p_img2 = 4
        main_screen()    

def select_ranking():
    screen.blit(intro_image, [0, 0])
    screen.blit(type1_big, [285, 90])
    screen.blit(type2_big, [395, 90])
    screen.blit(type3_big, [285, 290])
    screen.blit(type4_big, [395, 290])

    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)

    go = True
    while go:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            button("Type 1",300,200,95,50,green,black,show_ranking1)
            button("Tpye 2",405,200,95,50,green,black,show_ranking2)
            button("Type 3",300,400,95,50,green,black,show_ranking3)
            button("Type 4",405,400,95,50,green,black,show_ranking4)

        pygame.display.update()

def show_ranking1():
    screen.blit(intro_image, [0, 0])
    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)
    
    default_font = pygame.font.SysFont('Monospace', 28)
    f = open(file_path+"score_type1.txt")
    for i in range(20) :
        if i%2 == 1 :
            timing = f.readline()
            timing = timing.rstrip()
            draw_text(timing,default_font,screen,300,160+30+15*i,white)
        elif i%2 == 0 :
            scoring = f.readline()
            scoring = scoring.rstrip()
            draw_text("Score:"+scoring,default_font,screen,590,160+30+15*(i+1),white)

    rank = True
    while rank:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            largeText = pygame.font.SysFont('Creepster-Regular.ttf', 100)
            TextSurf, TextRect = text_objects("Score Board",   largeText)
            TextRect.center = ((size[0]/2),(size[1]/(4.5)))
            screen.blit(TextSurf, TextRect)
            
            button("Menu",250,500,95,50,green,bright_green,game_intro)
            button("Ranking",350,500,150,50,orange,bright_orange,select_ranking)
            button("Quit",505,500,95,50,red,bright_red, quit_game)

        pygame.display.update()
def show_ranking2():
    screen.blit(intro_image, [0, 0])
    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)
    
    default_font = pygame.font.SysFont('Monospace', 28)
    f = open(file_path+"score_type2.txt")
    for i in range(20) :
        if i%2 == 1 :
            timing = f.readline()
            timing = timing.rstrip()
            draw_text(timing,default_font,screen,300,160+30+15*i,white)
        elif i%2 == 0 :
            scoring = f.readline()
            scoring = scoring.rstrip()
            draw_text("Score:"+scoring,default_font,screen,590,160+30+15*(i+1),white)

    rank = True
    while rank:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            largeText = pygame.font.SysFont('Creepster-Regular.ttf', 100)
            TextSurf, TextRect = text_objects("Score Board",   largeText)
            TextRect.center = ((size[0]/2),(size[1]/(4.5)))
            screen.blit(TextSurf, TextRect)
            
            button("Menu",250,500,95,50,green,bright_green,game_intro)
            button("Ranking",350,500,150,50,orange,bright_orange,select_ranking)
            button("Quit",505,500,95,50,red,bright_red, quit_game)

        pygame.display.update()

def show_ranking3():
    screen.blit(intro_image, [0, 0])
    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)
    
    default_font = pygame.font.SysFont('Monospace', 28)
    f = open(file_path+"score_type3.txt")
    for i in range(20) :
        if i%2 == 1 :
            timing = f.readline()
            timing = timing.rstrip()
            draw_text(timing,default_font,screen,300,160+30+15*i,white)
        elif i%2 == 0 :
            scoring = f.readline()
            scoring = scoring.rstrip()
            draw_text("Score:"+scoring,default_font,screen,590,160+30+15*(i+1),white)

    rank = True
    while rank:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            largeText = pygame.font.SysFont('Creepster-Regular.ttf', 100)
            TextSurf, TextRect = text_objects("Score Board",   largeText)
            TextRect.center = ((size[0]/2),(size[1]/(4.5)))
            screen.blit(TextSurf, TextRect)
            
            button("Menu",250,500,95,50,green,bright_green,game_intro)
            button("Ranking",350,500,150,50,orange,bright_orange,select_ranking)
            button("Quit",505,500,95,50,red,bright_red, quit_game)

        pygame.display.update()
def show_ranking4():
    screen.blit(intro_image, [0, 0])
    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)
    
    default_font = pygame.font.SysFont('Monospace', 28)
    f = open(file_path+"score_type4.txt")
    for i in range(20) :
        if i%2 == 1 :
            timing = f.readline()
            timing = timing.rstrip()
            draw_text(timing,default_font,screen,300,160+30+15*i,white)
        elif i%2 == 0 :
            scoring = f.readline()
            scoring = scoring.rstrip()
            draw_text("Score:"+scoring,default_font,screen,590,160+30+15*(i+1),white)

    rank = True
    while rank:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            largeText = pygame.font.SysFont('Creepster-Regular.ttf', 100)
            TextSurf, TextRect = text_objects("Score Board",   largeText)
            TextRect.center = ((size[0]/2),(size[1]/(4.5)))
            screen.blit(TextSurf, TextRect)
            
            button("Menu",250,500,95,50,green,bright_green,game_intro)
            button("Ranking",350,500,150,50,orange,bright_orange,select_ranking)
            button("Quit",505,500,95,50,red,bright_red, quit_game)

        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def menu():
    game_intro()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, ac,(x,y,w,h))

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action != None:
           action()

    smallText = pygame.font.SysFont("monospace.ttf", 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

# 게임 매뉴 선택 화면
def game_intro():
    screen.blit(intro_image, [0, 0])
    pygame.mixer.music.load(file_path+"intro.wav")
    pygame.mixer.music.play(-1)

    global choose
    choose = 1

    intro = True
    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            largeText = pygame.font.SysFont('Creepster-Regular.ttf', 100)
            TextSurf, TextRect = text_objects("Select Menu",   largeText)
            TextRect.center = ((size[0]/2),(size[1]/3))
            screen.blit(TextSurf, TextRect)

            button("1 Play",300,300,95,50,green,bright_green,select_type)
            button("2 Play",405,300,95,50,green,bright_green,select_type2)
            button("Ranking",300,370,200,50,orange,bright_orange,select_ranking)
            button("Quit",300,440,200,50,red,bright_red, quit_game)

        pygame.display.update()

# 게임 시작전 화면    
def main_screen():
    
    screen.fill((0,0,0))
    messages = ["Let's Play!",
                "Ready?",
                "Watch out!",]
    message = messages[random.randint(0, len(messages) - 1)]
    text = pygame.font.SysFont('Monospace', 60)
    text_on_screen = text.render(message, True, (255, 255, 255))
    text_rect = text_on_screen.get_rect()
    text_rect.center = ((size[0]/2),(size[1]/2))
    screen.blit(text_on_screen, text_rect)
    pygame.display.update()
    time.sleep(2)
    
    global choose
    if choose == 2:
        game_loop2()
    else: 
        game_loop()

# 게임 오버 화면
def death_screen(score):
    screen.fill((0,0,0))
    text = pygame.font.SysFont('Monospace', 60)
    messages = ['Is it over yet?',
                'Is that all?',
                'Try harder...',]
    message = messages[random.randint(0,(len(messages)-1))]
    message_on_screen = text.render(message, True, (255, 255, 255))
    score_message = "Score: {}".format(score)
    score_on_screen = text.render(score_message, True, (255, 255, 255))
    message_rect = message_on_screen.get_rect()
    message_rect.center = ((size[0]/2),(size[1]/2 + 40))
    screen.blit(message_on_screen, message_rect)

    score_rect = score_on_screen.get_rect()
    score_rect.center = ((size[0]/2), (size[1]/2 - 40))
    screen.blit(score_on_screen, score_rect)

    pygame.display.update()
    time.sleep(3)

    dead()

# 게임 오버후 선택 화면
def dead():
    screen.blit(intro_image, [0, 0])
    
    global choose
    if choose == 2:
        choose = 1
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                button("Restart",150,300,200,50,green,bright_green,select_type2)
                button("Menu",450,300,200,50,green,bright_green,game_intro)
                button("Quit",300,400,200,50,red,bright_red, quit_game)
            pygame.display.update()
    else: 
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                button("Restart",150,300,200,50,green,bright_green,select_type)
                button("Menu",450,300,200,50,green,bright_green,game_intro)
                button("Quit",300,400,200,50,red,bright_red, quit_game)
            pygame.display.update()

# 프로그램 시작
game_intro()


# In[ ]:




