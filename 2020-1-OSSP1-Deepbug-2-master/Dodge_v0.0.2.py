#-*- coding: utf-8 -*-
import pygame
import random
import time
import sys
from pygame.locals import *
from os import path


pygame.init()

#####FPS
clock = pygame.time.Clock()

# ######Highscore File#######
# def save_highscore(new_highscore):
#     highscore_file = open("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/highscore.txt", "w")
#     highscore_file.write(str(new_highscore))
#     highscore_file.close()

# def get_highscore():
#     highscore = 0
#     highscore_file = open("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/highscore.txt", "r")
#     highscore = int(highscore_file.read())
#     highscore_file.close()
# ############################

# 게임 화면 크기 지정
size = (800, 600)
screen = pygame.display.set_mode(size)

#########컬러지정
YELLOW = (250, 250, 20)
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
orange = (255,127,0)
grey = (50,50,50)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_orange = (255,215,0)

# Load the background image 
background_image = pygame.image.load("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/background.jpg").convert()
pygame.display.set_caption("ELLAK - Pyhton Course - Avoid The Rocks v1.0.2")
clock = pygame.time.Clock()
playerImg = pygame.image.load("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/spaceship.png")
fireballImg = pygame.image.load("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/meteor.png")
intro_image = pygame.image.load("C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/intro_image.jpg")

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

    def __init__(self, x, y):
        self.x = x
        self.y = y
# 비행기의 속도를 조절할 수 있는 요소
    def update(self):
        if self.x_speed > 0:
            self.x_speed += self.speed_bonus
        elif self.x_speed < 0:
            self.x_speed -= self.speed_bonus
        if self.y_speed > 0:
            self.y_speed += self.speed_bonus
        elif self.y_speed < 0:
            self.y_speed -= self.speed_bonus
        self.x += self.x_speed
        self.y += self.y_speed
        screen.blit(playerImg, (self.x, self.y))
# 비행기위 위치를 업데이트 하는 과정
    def left_bound(self):
        if self.x <= 0:
            self.x = 0
            self.x_speed = self.x_speed * -1
    def right_bound(self):
        if self.x > size[0] - self.width:
            self.x = size[0] - self.width
            self.x_speed = self.x_speed * -1
    def top_bound(self):
        if self.y <= 0:
            self.y = 0
            self.y_speed = self.y_speed * -1
    def bottom_bound(self):
        if self.y >= size[1] - self.height:
            self.y = size[1] - self.height
            self.y_speed = self.y_speed * -1

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
    
    # 암석 스폰 위치
    def __init__(self):
        self.side = random.randint(1,4)
        # 1 - left
        # 2 - top
        # 3 - right
        # 4 - bottom

        # 왼쪽에서 스폰. 위아래는 랜덤출력. 운석의 속도는 10으로 고정
        # 그 밑에도 출력되는 방향만 다르고 나머진 동일
        if self.side == 1:
            self.x = -60 # get to the left of the window
            self.y = random.randint(0, size[1]-self.height)
            self.x_speed = 10

        elif self.side == 2:
            self.x = random.randint(0, size[0]-self.width)
            self.y = -60
            self.y_speed = 10

        elif self.side == 3:
            self.x = size[0] + 60
            self.y = random.randint(0, size[1]-self.height)
            self.x_speed = -10

        elif self.side == 4:
            self.x = random.randint(0, size[0]-self.width)
            self.y = size[1] + 60
            self.y_speed = -10
    #암석 속도 조절 파트
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        screen.blit(fireballImg, (self.x, self.y))
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

def game_loop():
    pygame.mixer.music.load('C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/whilegame.wav')
    pygame.mixer.music.play(-1)
    ##############충돌사운드
    global explosion_sound
    explosion_sound=pygame.mixer.Sound('C:/Users/82109/Desktop/오픈소스프로젝트 자료/avoid-rocks-master/explosion.wav')
    global score
    score = 0
    player = Player(size[0]/2, size[1]/2)
    fireballs = []
    difficulty = 1.0

    # ####################################
    # highscore = get_highscore()
    # if score > int(highscore,base=10) :
    #     save_highscore(score)
    # ####################################



    default_font = pygame.font.SysFont('Monospace', 28)
    screen.blit(background_image, [0, 0])

    player.update()
    pygame.display.update()

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.x_speed = 2
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.x_speed = -2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.y_speed = 2
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.y_speed = -2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.x_speed = 0
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player.x_speed = 0
                
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_speed = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.y_speed = 0


        screen.blit(background_image, [0, 0])
        draw_text('Score : {}'.format(score),default_font,screen,80,20,YELLOW)
        # draw_text('High Score : {}'.format(highscore),default_font,screen, 400,20,WHITE)
        player.bound()
        player.update()



        if len(fireballs) < difficulty:
            fireballs.append(Fireball())

        for index, fireball in enumerate(fireballs):
            fireball.update()

            if fireball.rectangle().colliderect(player.rectangle()):

                pygame.mixer.Sound.play(explosion_sound)
                pygame.mixer.music.stop()
                death_screen(score)

            if fireball.has_reached_limit:
                fireballs.pop(index)
                score += 1
                difficulty += 0.1
                player.speed_bonus += 0.01

                print (score)
                print (player.speed_bonus)

        pygame.display.update()
        clock.tick(60)
#첫 화면에 들어가야할 것 : 1P 버전 or 2P 버전, 랭킹 확인
# 1P화면에 들어갈 때 : 비행기 선택창 떠야함
# 2P화면에 들어갈 때 : 각각의 비행기 선택창 떠야함
# 랭킹화면 : 랭킹이 떠야함

def text_objects(text, font):
       textSurface = font.render(text, True, (white))
       return textSurface, textSurface.get_rect()

def message_display(text):
       largeText = pygame.font.Font('Creepster-Regular.ttf',115)
       TextSurf, TextRect = text_objects(text, largeText)
       TextRect.center = ((size[0]/2),(size[1]/3))
       gameDisplay.blit(TextSurf, TextRect,)

# 버튼 함수들 구현 부분
def start_game1():
    main_screen()
    print("start")

def start_game2():
    # 2p mode 시작 호출
    print("2p mode")

def show_ranking():
    # ranking 호출
    print("Ranking list")

def quit_game():
    pygame.quit()
    sys.exit()

def menu():
    game_intro()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
       pygame.draw.rect(screen, ac,(x,y,w,h))

       if click[0] == 1 and action != None:
           action()

    smallText = pygame.font.SysFont("monospace.ttf", 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def game_intro():
    screen.blit(intro_image, [0, 0])
    # 사운드 넣으면 됨

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

            button("1 Play",300,300,95,50,green,bright_green,start_game1)
            button("2 Play",405,300,95,50,green,bright_green,start_game2)
            button("Ranking",300,370,200,50,orange,bright_orange, show_ranking)
            button("Quit",300,440,200,50,red,bright_red, quit_game)

        pygame.display.update()
    
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
    game_loop()
    
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

def dead():
    screen.fill((0,0,0))

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        button("Restrat",150,300,200,50,green,bright_green,start_game1)
        button("Menu",450,300,200,50,green,bright_green,game_intro)
        button("Quit",300,400,200,50,red,bright_red, quit_game)

        pygame.display.update()

game_intro()