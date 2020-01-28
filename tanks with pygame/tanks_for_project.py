# created by zxccdw | support: zxccdw@mail.ru | vk.com/klychkov2000

import pygame
import sys
import time
from random import randint
import sqlite3


def del_tank(j):
    global players
    players = players[:players.index(j)] + players[players.index(j) + 1::]


def restarting():
    pygame.display.update()
    win.blit(f1.render('The game is restarting in 3', 1, (168, 0, 255)), (50, 100))
    pygame.display.update()
    time.sleep(1)
    win.blit(f1.render('2', 1, (168, 0, 255)), (500, 99))
    pygame.display.update()
    time.sleep(1)
    win.blit(f1.render('1', 1, (168, 0, 255)), (525, 99))
    pygame.display.update()
    time.sleep(1)


class Bullet:
    def __init__(self, x, y, side, who):
        self.x = x
        self.y = y
        self.side = side
        self.who = who
        self.speed = 20
        self.damage = 50

    def bullet_forward(self):
        if self.side == "left":
            self.x -= self.speed
        if self.side == "right":
            self.x += self.speed
        if self.side == "up":
            self.y -= self.speed
        if self.side == "down":
            self.y += self.speed

    def get_number_side(self):
        if self.side == "left":
            return 2
        if self.side == "right":
            return 3
        if self.side == "up":
            return 0
        if self.side == "down":
            return 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def bool_delete(self):
        if 0 <= self.x <= 768 and 0 <= self.y <= 432:
            return 0
        return 1

    def get_who(self):
        return self.who


def intersect(x1, x2, y1, y2, width, height, width2, height2):  # функция столкновения
    if (x2 < x1 + width) and (x2 > x1 - width2) and (y2 < y1 + height) and (y2 > y1 - height2):
        return 0
    else:
        return 1


def travel():
    global first_x, first_y
    global first_forward, first_side
    global first_sch_bullets, all_bullets
    global t_first
    first_forward = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        sys.exit()
    elif keys[pygame.K_LEFT] and first_x > speed:
        first_x -= speed
        first_side = 'left'
    elif keys[pygame.K_RIGHT] and first_x < 768 - width - 7.5:
        first_x += speed
        first_side = 'right'
    elif keys[pygame.K_UP] and first_y > speed:
        first_y -= speed
        first_side = 'up'
    elif keys[pygame.K_DOWN] and first_y < 432 - height - 7.5:
        first_y += speed
        first_side = 'down'
    else:
        first_forward = False

    for i in players:
        i.forwards()

    if keys[pygame.K_m] and first_sch_bullets < len_bullets and time.time() - t_first > 0.3:
        t_first = time.time()
        if first_side == "right":
            all_bullets.append([1, Bullet(first_x + width, first_y + (height - bullet_height) / 2,
                                          first_side, "first")])
        if first_side == "left":
            all_bullets.append([1, Bullet(first_x, first_y + (height - bullet_height) / 2, first_side, "first")])
        if first_side == "up":
            all_bullets.append([1, Bullet(first_x + (width - bullet_width) / 2, first_y, first_side, "first")])
        if first_side == "down":
            all_bullets.append([1, Bullet(first_x + (width - bullet_width) / 2, first_y + height / 2,
                                          first_side, "first")])
        first_sch_bullets += 1

    for i in players:
        i.generate_bullets()

    for i in range(len(all_bullets)):  # forward and delete bullets
        if not all_bullets[i][0]:
            continue
        if all_bullets[i][1].bool_delete():
            if all_bullets[i][1].get_who() == "first":
                first_sch_bullets -= 1

            all_bullets[i][0] = 0
        all_bullets[i][1].bullet_forward()


def draw():
    global first_Animation, first_side, first_forward, flag, score, first_sch_bullets
    win.blit(bg, (0, 0))
    first_Animation %= 8
    if first_forward:
        first_Animation += 1
    if first_side == 'left':
        win.blit(walk_left_first[first_Animation // 3], (first_x, first_y))
    elif first_side == 'right':
        win.blit(walk_right_first[first_Animation // 3], (first_x, first_y))
    elif first_side == 'up':
        win.blit(walk_up_first[first_Animation // 3], (first_x, first_y))
    elif first_side == 'down':
        win.blit(walk_down_first[first_Animation // 3], (first_x, first_y))

    for i in players:
        i.draw()

    for i in all_bullets:
        if i[0]:
            if not intersect(first_x, i[1].get_x(), first_y, i[1].get_y(), width, height, bullet_width,
                             bullet_height) and i[1].get_who() == "bot":
                upd_db(1)
                restarting()
                flag = False
                return

            for j in players:
                if not intersect(j.get_x(), i[1].get_x(), j.get_y(), i[1].get_y(),
                                 width, height, bullet_width, bullet_height) and i[1].get_who() == "first":
                    del_tank(j)
                    first_sch_bullets -= 1
                    i[0] = 0
                    upd_db(2)

                    if len(players) == 0:
                        restarting()
                        flag = False
                        upd_db(3)
                        return
            win.blit(bullet_sprites[i[1].get_number_side()], (i[1].get_x(), i[1].get_y()))
    result_with_db()


class Bot():
    def __init__(self, x, y):
        self.side = 'Right'
        self.forward = False
        self.animation = 0
        self.sch_bullets = 0
        self.x = x
        self.y = y
        self.t = 0
        self.t_second = 0
        self.t_bull = 0
        self.a = 4

    def get_len_bul(self):
        return len(self.bullets)

    def forwards(self):
        if time.time() - self.t > 1:
            self.a = randint(0, 4)
            self.t = time.time()
        self.forward = True
        if self.a == 1 and self.y > speed:
            self.y -= speed
            self.side = "up"
        elif self.a == 2 and self.x > speed:
            self.x -= speed
            self.side = "left"
        elif self.a == 3 and self.y < 432 - height - 7.5:
            self.y += speed

            self.side = "down"
        elif self.a == 4 and self.x < 768 - width - 7.5:
            self.x += speed
            self.side = "right"
        else:
            self.forward = False
        self.draw()

    def generate_bullets(self):
        if time.time() - self.t_second > 0.3 and randint(0, 10) == 5:
            self.t_second = time.time()
            if self.side == "right":
                all_bullets.append(
                    [1, Bullet(self.x + width, self.y + (height - bullet_height) / 2, self.side, "bot")])
            if self.side == "left":
                all_bullets.append(
                    [1, Bullet(self.x, self.y + (height - bullet_height) / 2, self.side, "bot")])
            if self.side == "up":
                all_bullets.append([1, Bullet(self.x + (width - bullet_width) / 2, self.y, self.side, "bot")])
            if self.side == "down":
                all_bullets.append(
                    [1, Bullet(self.x + (width - bullet_width) / 2, self.y + height / 2, self.side, "bot")])
            self.sch_bullets += 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def draw(self):
        self.animation %= 8
        if self.forward:
            self.animation += 1
        if self.side == 'left':
            win.blit(walk_left_second[self.animation // 3], (self.x, self.y))
        elif self.side == 'right':
            win.blit(walk_right_second[self.animation // 3], (self.x, self.y))
        elif self.side == 'up':
            win.blit(walk_up_second[self.animation // 3], (self.x, self.y))
        elif self.side == 'down':
            win.blit(walk_down_second[self.animation // 3], (self.x, self.y))


def result_with_db():
    con = sqlite3.connect(name)  # bz.db
    cur = con.cursor()
    res_second = cur.execute("""
            SELECT rec FROM Label """).fetchall()
    res_third = cur.execute("""
            SELECT games FROM Label""").fetchall()
    score_text = "Bots killed : " + str(res_second[0][0]) + " " * 10 + "Games won : " + str(res_third[0][0])
    con.close()
    win.blit(score_f.render(score_text, 1, (168, 0, 255)), (220, 10))


def upd_db(b):
    con = sqlite3.connect(name)
    cur = con.cursor()
    if b == 1:
        cur.execute("""UPDATE Label
                        SET games = 0""")
    if b == 2:
        cur.execute("""
        UPDATE Label
        SET rec = (SELECT rec FROM Label) + 1""").fetchall()
    if b == 3:
        cur.execute("""
        UPDATE Label
        SET games = (SELECT games FROM Label) + 1""").fetchall()
    con.commit()
    con.close()


# animations | sprites
walk_left_first = [pygame.image.load('sprites/LeftTank1.bmp'), pygame.image.load('sprites/LeftTank2.bmp'),
                   pygame.image.load('sprites/LeftTank3.bmp')]
walk_right_first = [pygame.image.load('sprites/RightTank1.bmp'), pygame.image.load('sprites/RightTank2.bmp'),
                    pygame.image.load('sprites/RightTank3.bmp')]
walk_up_first = [pygame.image.load('sprites/UpTank1.bmp'), pygame.image.load('sprites/UpTank2.bmp'),
                 pygame.image.load('sprites/UpTank3.bmp')]
walk_down_first = [pygame.image.load('sprites/DownTank1.bmp'), pygame.image.load('sprites/DownTank2.bmp'),
                   pygame.image.load('sprites/DownTank3.bmp')]
walk_left_second = [pygame.image.load('sprites/Left Second 1.bmp'), pygame.image.load('sprites/Left Second 2.bmp'),
                    pygame.image.load('sprites/Left Second 3.bmp')]
walk_right_second = [pygame.image.load('sprites/Right Second 1.bmp'), pygame.image.load('sprites/Right Second 2.bmp'),
                     pygame.image.load('sprites/Right Second 3.bmp')]
walk_up_second = [pygame.image.load('sprites/Up Second 1.bmp'), pygame.image.load('sprites/Up Second 2.bmp'),
                  pygame.image.load('sprites/Up Second 3.bmp')]
walk_down_second = [pygame.image.load('sprites/Down Second 1.bmp'), pygame.image.load('sprites/Down Second 2.bmp'),
                    pygame.image.load('sprites/Down Second 3.bmp')]
bullet_sprites = [pygame.image.load('sprites/up bullet.bmp'), pygame.image.load('sprites/down bullet.bmp'),
                  pygame.image.load('sprites/left bullet.bmp'), pygame.image.load('sprites/right bullet.bmp')]

# side on tanks
first_side = 'Left'
first_forward = False
first_Animation = 0

# bullets
bullet_height = 8
bullet_width = 8
len_bullets = 5  # limit bullets
first_sch_bullets = 0
all_bullets = []

# coordinats
width = 40
height = 40
speed = 5
FPS = 30
clock = pygame.time.Clock()

pygame.init()
win = pygame.display.set_mode((768, 432))
pygame.display.set_caption("Танчики")
bg = pygame.Surface((768, 432))
bg.fill(pygame.Color("#000000"))
f1 = pygame.font.Font(None, 50)
score_f = pygame.font.Font(None, 25)
t_first = 0
coord = [[20, 20], [720, 380], [720, 20], [20, 380], [380, 20], [380, 380], [192, 215],
         [576, 215], [370, 60], [500, 345]]
name = "bz.db"

while 1:
    all_bullets = []
    first_x = 400
    t = 0
    first_y = 216
    flag = True
    first_sch_bullets = 0
    a = 4
    pygame.display.update()
    players = []
    for i in range(0, randint(4, 9)):
        players.append(Bot(coord[i][0], coord[i][1]))
    while flag:
        clock.tick(FPS)
        travel()
        draw()
        pygame.display.update()
