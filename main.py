import pygame as pg
import app

pg.init()
displaySize = (1000, 850)
BG = pg.display.set_mode(displaySize)
DISPLAY = pg.Surface(displaySize, pg.SRCALPHA)
clock = pg.time.Clock()

appObj = app.App()

run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                appObj.mouseClick(event.pos)

    BG.fill((130, 130, 130, 0))
    appObj.display(DISPLAY)
    BG.blit(DISPLAY, (0, 0))
    pg.display.flip()
    clock.tick(144)