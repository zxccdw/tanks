# creating by zxccdw | support: zxccdw@mail.ru | vk.com/klychkov2000

import pygame
import sys
import time


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

    def get_coord(self):
        return self.x, self.y

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
    global first_x, first_y, second_x, second_y
    global first_forward, first_side
    global second_forward, second_side
    global first_sch_bullets, second_sch_bullets, all_bullets
    first_forward = True
    second_forward = True
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

    if keys[pygame.K_w] and second_y > speed:
        second_y -= speed
        second_side = "up"
    elif keys[pygame.K_a] and second_x > speed:
        second_x -= speed
        second_side = "left"
    elif keys[pygame.K_s] and second_y < 432 - height - 7.5:
        second_y += speed
        second_side = "down"
    elif keys[pygame.K_d] and second_x < 768 - width - 7.5:
        second_x += speed
        second_side = "right"
    else:
        second_forward = False

    if keys[pygame.K_m] and first_sch_bullets < len_bullets:
        if first_side == "right":
            all_bullets.append([1, Bullet(first_x + width, first_y + (height - bullet_height) / 2, first_side, "first")])
        if first_side == "left":
            all_bullets.append([1, Bullet(first_x, first_y + (height - bullet_height) / 2, first_side, "first")])
        if first_side == "up":
            all_bullets.append([1, Bullet(first_x + (width - bullet_width) / 2, first_y, first_side, "first")])
        if first_side == "down":
            all_bullets.append([1, Bullet(first_x + (width - bullet_width) / 2, first_y + height / 2, first_side, "first")])
        first_sch_bullets += 1

    if keys[pygame.K_SPACE] and second_sch_bullets < len_bullets:
        if second_side == "right":
            all_bullets.append([1, Bullet(second_x + width, second_y + (height - bullet_height) / 2, second_side, "second")])
        if second_side == "left":
            all_bullets.append([1, Bullet(second_x, second_y + (height - bullet_height) / 2, second_side, "second")])
        if second_side == "up":
            all_bullets.append([1, Bullet(second_x + (width - bullet_width) / 2, second_y, second_side, "second")])
        if second_side == "down":
            all_bullets.append([1, Bullet(second_x + (width - bullet_width) / 2, second_y + height / 2, second_side, "second")])
        second_sch_bullets += 1

    for i in range(len(all_bullets)):  # forward and delete bullets
        if not all_bullets[i][0]:
            continue
        if all_bullets[i][1].bool_delete():
            if all_bullets[i][1].get_who() == "first":
                first_sch_bullets -= 1
            else:
                second_sch_bullets -= 1
            all_bullets[i][0] = 0
        all_bullets[i][1].bullet_forward()


def draw():
    global second_Animation, second_side, first_Animation, first_side, first_forward, second_forward, flag, score
    win.blit(bg, (0, 0))
    first_Animation %= 8
    second_Animation %= 8
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

    if second_forward:
        second_Animation += 1
    if second_side == 'left':
        win.blit(walk_left_second[second_Animation // 3], (second_x, second_y))
    elif second_side == 'right':
        win.blit(walk_right_second[second_Animation // 3], (second_x, second_y))
    elif second_side == 'up':
        win.blit(walk_up_second[second_Animation // 3], (second_x, second_y))
    elif second_side == 'down':
        win.blit(walk_down_second[second_Animation // 3], (second_x, second_y))

    for i in all_bullets:
        if i[0]:
            if not intersect(first_x, i[1].get_coord()[0], first_y, i[1].get_coord()[1], width, height, bullet_width,
                             bullet_height):
                restarting()
                score[0] += 1
                flag = False
                return
            if not intersect(second_x, i[1].get_coord()[0], second_y, i[1].get_coord()[1], width, height, bullet_width,
                             bullet_height):
                restarting()
                score[1] += 1
                flag = False
                return
            win.blit(bullet_sprites[i[1].get_number_side()], i[1].get_coord())
    score_text = "Score " + str(score[0]) + " : " + str(score[1])
    win.blit(score_f.render(score_text, 1, (168, 0, 255)), (320, 10))


# animations | sprites
walk_left_first = [pygame.image.load('LeftTank1.bmp'), pygame.image.load('LeftTank2.bmp'),
                   pygame.image.load('LeftTank3.bmp')]
walk_right_first = [pygame.image.load('RightTank1.bmp'), pygame.image.load('RightTank2.bmp'),
                    pygame.image.load('RightTank3.bmp')]
walk_up_first = [pygame.image.load('UpTank1.bmp'), pygame.image.load('UpTank2.bmp'), pygame.image.load('UpTank3.bmp')]
walk_down_first = [pygame.image.load('DownTank1.bmp'), pygame.image.load('DownTank2.bmp'),
                   pygame.image.load('DownTank3.bmp')]
walk_left_second = [pygame.image.load('Left Second 1.bmp'), pygame.image.load('Left Second 2.bmp'),
                    pygame.image.load('Left Second 3.bmp')]
walk_right_second = [pygame.image.load('Right Second 1.bmp'), pygame.image.load('Right Second 2.bmp'),
                     pygame.image.load('Right Second 3.bmp')]
walk_up_second = [pygame.image.load('Up Second 1.bmp'), pygame.image.load('Up Second 2.bmp'),
                  pygame.image.load('Up Second 3.bmp')]
walk_down_second = [pygame.image.load('Down Second 1.bmp'), pygame.image.load('Down Second 2.bmp'),
                    pygame.image.load('Down Second 3.bmp')]
bullet_sprites = [pygame.image.load('up bullet.bmp'), pygame.image.load('down bullet.bmp'),
                  pygame.image.load('left bullet.bmp'), pygame.image.load('right bullet.bmp')]

# side on tanks
first_side = 'Left'
first_forward = False
first_Animation = 0


second_side = 'Right'
second_forward = False
second_Animation = 0


# bullets
bullet_height = 8
bullet_width = 8
len_bullets = 5  # limit bullets
first_sch_bullets = 0
second_sch_bullets = 0
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
# background
# bg = pygame.image.load('background.jpg')
bg = pygame.Surface((768, 432))
bg.fill(pygame.Color("#000000"))
f1 = pygame.font.Font(None, 50)
score_f = pygame.font.Font(None, 25)

# text1 = f1.render('Red is winner!!!', 1, (168, 0, 255))
# win.blit(text1, (50, 50))
# win.blit(f1.render('Yellow is winner!', 1, (168, 0, 255)), (50, 50))

score = [0, 0]


while 1:
    all_bullets = []
    first_x = 700
    first_y = 350
    second_x = 20
    second_y = 20
    flag = True
    first_sch_bullets = 0
    second_sch_bullets = 0
    pygame.display.update()
    while flag:
        clock.tick(FPS)
        travel()
        draw()
        pygame.display.update()
