# src/gamelogic/hud.py
import pygame

CORES = {
    "ambiental": (60, 180, 90),
    "social":    (80, 140, 220),
    "economico": (220, 180, 50),
}

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font   = pygame.font.SysFont(None, 22)

    def draw(self, atributos):
        W, H = self.screen.get_size()

        largura_barra = int(W * 0.18)
        espacamento   = W // 3
        x_inicio      = espacamento // 2 - largura_barra // 2
        y             = int(H * 0.03)

        for i, (nome, valor) in enumerate(atributos.items()):
            x = x_inicio + i * espacamento

            label = self.font.render(nome.capitalize(), True, (220, 220, 220))
            self.screen.blit(label, (x, y))

            pygame.draw.rect(self.screen, (60, 60, 60),
                             (x, y + 18, largura_barra, 10), border_radius=4)

            preenchimento = int(largura_barra * valor / 100)
            pygame.draw.rect(self.screen, CORES[nome],
                             (x, y + 18, preenchimento, 10), border_radius=4)