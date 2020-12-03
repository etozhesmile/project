import pygame as pg

# Цвета
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
brown = pg.Color(165, 42, 42)
# Размеры
W = 400
H = 400

pg.init()
# Экран
wn = pg.display.set_mode((W, H))
pg.display.set_caption('Змейка')
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    wn.fill(black)
pg.quit()