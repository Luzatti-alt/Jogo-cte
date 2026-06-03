import pygame as pg
from src.gamelogic.Tela import Jogo
import sys, os
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
