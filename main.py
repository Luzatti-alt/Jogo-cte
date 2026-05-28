import pygame as pg
from src.gamelogic.Tela import Jogo

pg.init()
screen = pg.display.set_mode((800, 600),pg.RESIZABLE)
pg.display.set_caption("Um jogo")#dps eu troco
clock = pg.time.Clock()

Tela = Jogo(screen)

while Tela.running:
    Tela.handle_events()
    Tela.update()
    Tela.draw()
    clock.tick(60)

pg.quit()
