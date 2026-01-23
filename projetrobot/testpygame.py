import pygame as pg
from classrobot import Robot

pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
running = True
robot1 = Robot("best_robot", 400, 300, 0)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))

    robot1.draw(screen)

    pg.display.flip()

    clock.tick(60)
pg.quit()