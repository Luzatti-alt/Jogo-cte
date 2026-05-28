import pygame
from src.gamelogic.player import Player
from src.gamelogic.hud import HUD
from src.gamelogic.npcs import Npc,Dialogo,GerenciadorNPCs


def wrap_text(texto, font, max_largura):
    #Quebra texto em linhas que cabem em max_largura
    palavras = texto.split(" ")
    linhas, linha_atual = [], ""
    for palavra in palavras:
        teste = linha_atual + (" " if linha_atual else "") + palavra
        if font.size(teste)[0] <= max_largura:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas


class Jogo:
    def __init__(self, screen):
        self.screen  = screen
        self.running = True
        self.player  = Player()
        self.hud     = HUD(screen)
        self.npcs    = GerenciadorNPCs("empresario")
        self.font    = pygame.font.SysFont(None, 26)
        self.font_op = pygame.font.SysFont(None, 22)

    def handle_events(self):
        npc = self.npcs.atual()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:      # janela foi redimensionada
                self.screen = pygame.display.set_mode(
                   (event.w, event.h), pygame.RESIZABLE
               )
            if event.type == pygame.KEYDOWN:
                opcoes = npc.dialog.opcoes()
                if event.key == pygame.K_LEFT and len(opcoes) > 0:
                    self.Escolha(0)
                elif event.key == pygame.K_RIGHT and len(opcoes) > 1:
                    self.Escolha(1)

                
    def Escolha(self, idx):
        npc = self.npcs.atual()
        efeitos = npc.dialog.escolher(idx)
        for e in efeitos.get("aumenta", []):
            self.player.update(e["tipo"], +e["quantidade"])
        for e in efeitos.get("diminui", []):
           self.player.update(e["tipo"], -e["quantidade"])
        if not npc.dialog.ativa:
           self.npcs.proximo()
          # vai para o próximo NPC
        if self.player.reset():
            self.running = False

    def update(self):
        pass  # física, animações, etc.

    def draw(self):
        W, H = self.screen.get_size()
        self.screen.fill((30, 30, 40))
        self.hud.screen = self.screen
        npc = self.npcs.atual()

        # sprite do NPC centralizado
        npc_h = int(H * 0.40)
        npc_w = int(npc_h * (npc.imagem.get_width() / npc.imagem.get_height()))
        img   = pygame.transform.scale(npc.imagem, (npc_w, npc_h))
        self.screen.blit(img, (W // 2 - npc_w // 2, int(H * 0.35)))

        # caixa de fala
        caixa_w = int(W * 0.80)
        caixa_x = W // 2 - caixa_w // 2
        caixa_y = int(H * 0.12)
        linhas  = wrap_text(npc.dialog.texto(), self.font, caixa_w - 20)
        caixa_h = len(linhas) * 28 + 20
        pygame.draw.rect(self.screen, (240, 230, 190),
                         (caixa_x, caixa_y, caixa_w, caixa_h), border_radius=8)
        pygame.draw.rect(self.screen, (100, 80, 40),
                         (caixa_x, caixa_y, caixa_w, caixa_h), 2, border_radius=8)
        for i, linha in enumerate(linhas):
            surf = self.font.render(linha, True, (40, 30, 20))
            self.screen.blit(surf, (caixa_x + 10, caixa_y + 10 + i * 28))

        # opções esquerda / direita  ← fora do for
        opcoes = npc.dialog.opcoes()
        op_y   = int(H * 0.78)
        op_w   = int(W * 0.35)
        op_h   = int(H * 0.10)

        if len(opcoes) > 0:
            pygame.draw.rect(self.screen, (80, 60, 30),
                             (10, op_y, op_w, op_h), border_radius=6)
            seta = self.font.render("← " + opcoes[0]["texto"], True, (240, 220, 160))
            self.screen.blit(seta, (20, op_y + op_h // 2 - 10))

        if len(opcoes) > 1:
            op_x2 = W - op_w - 10
            pygame.draw.rect(self.screen, (80, 60, 30),
                             (op_x2, op_y, op_w, op_h), border_radius=6)
            seta = self.font.render(opcoes[1]["texto"] + " →", True, (240, 220, 160))
            self.screen.blit(seta, (op_x2 + 10, op_y + op_h // 2 - 10))

        self.hud.draw(self.player.get_stats())
        pygame.display.flip()

