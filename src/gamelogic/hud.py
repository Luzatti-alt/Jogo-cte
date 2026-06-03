import sys, os

def resource_path(relative):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, "..", "..")  # sobe de gamelogic/ para raiz
    return os.path.normpath(os.path.join(base, relative))

IconsPath = {
    "social":    resource_path("src/gui/social.png"),
    "ambiental": resource_path("src/gui/ambiente.png"),
    "economico": resource_path("src/gui/economico.png"),
}
# src/gamelogic/hud.py
import pygame

CORES = {
    "ambiental": (60, 180, 90),
    "social":    (80, 140, 220),
    "economico": (220, 180, 50),
}
ICON_SIZE = 64

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font   = pygame.font.SysFont(None, 22)
        self.icons  = {}

        for nome, path in IconsPath.items():
            img = pygame.image.load(path).convert()
            self.icons[nome] = pygame.transform.scale(img, (ICON_SIZE, ICON_SIZE))
            img.set_colorkey((0, 0, 0))  # torna o preto transparente


    def draw(self, atributos):
        W, H = self.screen.get_size()

        espacamento = W // 3
        x_inicio    = espacamento // 2 - ICON_SIZE // 2
        y           = int(H * 0.02)

        for i, (nome, valor) in enumerate(atributos.items()):
            x    = x_inicio + i * espacamento
            icon = self.icons[nome]
            cor  = CORES[nome]

            # quantos pixels do ícone ficam visíveis (de baixo pra cima)
            fill_px  = int(ICON_SIZE * valor / 100)
            empty_px = ICON_SIZE - fill_px

            # parte preenchida: recorta só os pixels de baixo (fill_px altura)
            if fill_px > 0:
                parte_cheia = icon.subsurface(
                    pygame.Rect(0, empty_px, ICON_SIZE, fill_px)
                ).copy()
                # coloriza com a cor do atributo
                parte_cheia.fill((*cor, 255), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(parte_cheia, (x, y + empty_px))

            # porcentagem abaixo do ícone
            txt = self.font.render(f"{valor}%", True, (220, 220, 220))
            self.screen.blit(txt, (x + ICON_SIZE // 2 - txt.get_width() // 2,
                                   y + ICON_SIZE + 4))
