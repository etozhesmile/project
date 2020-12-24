import random
import time

import pygame as pg

score, high_score = (0, 0)

# Цвета
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
brown = pg.Color(165, 42, 42)

W = 400
H = 400


class Food:
    def __init__(self):
        self.x = W / 2
        self.y = H / 4
        self.color = red
        self.width = 10
        self.height = 10

    def draw_food(self, surface):
        self.food = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.color, self.food)

    def is_eaten(self, head):
        return self.food.colliderect(head)

    def new_pos(self):
        self.x = random.randint(0, W - self.width)
        self.y = random.randint(0, H - self.height)


class Snake:
    def __init__(self):
        self.x = W / 2
        self.y = H / 2
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = 'stop'
        self.body = []
        self.head_color = green
        self.body_color = brown

    def draw_snake(self, surface):
        self.seg = []
        self.head = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.head_color, self.head)
        if len(self.body) > 0:
            for unit in self.body:
                segment = pg.Rect(unit[0], unit[1], self.width, self.height)
                pg.draw.rect(surface, self.body_color, segment)
                self.seg.append(segment)

    def add_unit(self):
        if len(self.body) != 0:
            index = len(self.body) - 1
            x = self.body[index][0]
            y = self.body[index][1]
            self.body.append([x, y])
        else:
            self.body.append([1000, 1000])

    def is_collision(self):
        for segment in self.seg:
            if self.head.colliderect(segment):
                return True
        if self.y < 0 or self.y > H - self.height or self.x < 0 or self.x > W - self.width:
            return True

    def move(self):
        for index in range(len(self.body) - 1, 0, -1):
            x = self.body[index - 1][0]
            y = self.body[index - 1][1]
            self.body[index] = [x, y]
        if len(self.body) > 0:
            self.body[0] = [self.x, self.y]
        if self.direction == 'up':
            self.y -= self.velocity
        if self.direction == 'down':
            self.y += self.velocity
        if self.direction == 'left':
            self.x -= self.velocity
        if self.direction == 'right':
            self.x += self.velocity

    def change_direction(self, direction):
        if self.direction != 'down' and direction == 'up':
            self.direction = 'up'
        if self.direction != 'right' and direction == 'left':
            self.direction = 'left'
        if self.direction != 'up' and direction == 'down':
            self.direction = 'down'
        if self.direction != 'left' and direction == 'right':
            self.direction = 'right'


def draw_score(surface):
    global high_score
    font_name = pg.font.match_font('arial')
    if score > high_score:
        high_score = score
    font = pg.font.Font(font_name, 18)
    text_surface = font.render(f'Score: {score} High Score: {high_score}', True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (200, 10)
    surface.blit(text_surface, text_rect)


def game_over():
    global score
    gameOverFont = pg.font.Font('freesansbold.ttf', 24)
    gameOverSurf = gameOverFont.render('Game Over', True, white)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (200, 50)
    wn.blit(gameOverSurf, gameOverRect)
    score = 0
    pg.display.flip()
    time.sleep(2)
    run = True
    fd = Food()
    s = Snake()
    play_game(fd, s)


def play_game(fd, p):
    global score
    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(20)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        wn.fill(black)
        fd.draw_food(wn)
        p.draw_snake(wn)
        draw_score(wn)
        pressed = pg.key.get_pressed()
        if pressed[pg.K_UP]:
            p.change_direction('up')
        if pressed[pg.K_LEFT]:
            p.change_direction('left')
        if pressed[pg.K_DOWN]:
            p.change_direction('down')
        if pressed[pg.K_RIGHT]:
            p.change_direction('right')
        p.move()
        if fd.is_eaten(p.head):
            fd.new_pos()
            p.add_unit()
            score += 10
        if p.is_collision():
            run = False
            game_over()

        pg.display.update()


pg.init()
wn = pg.display.set_mode((W, H))
pg.display.set_caption('Змейка')
fd = Food()
p = Snake()
play_game(fd, p)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    wn.fill(black)
pg.quit()
