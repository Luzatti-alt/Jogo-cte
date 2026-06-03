import sys, os

def resource_path(relative):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, "..", "..")
    return os.path.normpath(os.path.join(base, relative))

import pygame
import json
from src.gamelogic.player import Player
from src.gamelogic.hud import HUD
from src.gamelogic.npcs import Npc, Dialogo, GerenciadorNPCs
from src.gamelogic.gamestate import Turno

def wrap_text(texto, font, max_largura):
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
        self.screen      = screen
        self.running     = True
        self.player      = Player()
        self.hud         = HUD(screen)
        self.npcs        = GerenciadorNPCs(
            "gestor_federal", "cientista", "diretor_saude",
            "dona_conceicao", "startup", "jornalista",
            "secretaria_ambiental", "empresario", "fazendeiro"
        )
        self.font        = pygame.font.SysFont(None, 26)
        self.font_op     = pygame.font.SysFont(None, 22)
        self.font_titulo = pygame.font.SysFont(None, 52)
        self.turno       = Turno()  # instância única

        # finais
        with open(resource_path("src/gamelogic/finais/finais.json"), encoding="utf-8") as f:
            self.finais = json.load(f)
        self.final = None  # None = jogando, dict = tela de final

        # text engine
        self.TextoCompleto = ""
        self.TextoVisivel  = ""
        self.CharIndex     = 0
        self.CharDelay     = 30
        self.LastCharTime  = 0
        self.digitando     = False
        self.IniciarTexto()

    def IniciarTexto(self, texto=None):
        if texto is None:
            texto = self.npcs.atual().dialog.texto()
        self.TextoCompleto = texto
        self.TextoVisivel  = ""
        self.CharIndex     = 0
        self.digitando     = True
        self.LastCharTime  = pygame.time.get_ticks()

    def TextoInstantaneo(self):
        self.TextoVisivel = self.TextoCompleto
        self.CharIndex    = len(self.TextoCompleto)
        self.digitando    = False

    def CalcularFinal(self):
        stats  = self.player.get_stats()
        media  = sum(stats.values()) / len(stats)
        minimo = min(stats.values())
        if media >= 60 and minimo >= 30:
            return "bom"
        elif media >= 35 and minimo >= 15:
            return "neutro"
        else:
            return "ruim"

    def IniciarFinal(self):
        tipo       = self.CalcularFinal()
        self.final = self.finais[tipo]
        self.IniciarTexto(self.final["texto"])

    def handle_events(self):
        if self.final:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.digitando:
                        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                            self.TextoInstantaneo()
                    elif event.key == pygame.K_r:
                        self.Reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            return

        # gameplay normal
        npc = self.npcs.atual()
        if not npc.dialog.ativa:
            self.npcs.proximo()
            npc = self.npcs.atual()
            self.IniciarTexto()

        stats = self.player.get_stats()
        if any(v <= 0 for v in stats.values()):
            self.IniciarFinal()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
            if event.type == pygame.KEYDOWN:
                if self.digitando:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.TextoInstantaneo()
                else:
                    if event.key == pygame.K_r:
                        self.Reset()
                    opcoes = npc.dialog.opcoes()
                    if event.key == pygame.K_LEFT and len(opcoes) > 0:
                        self.Escolha(0)
                    elif event.key == pygame.K_RIGHT and len(opcoes) > 1:
                        self.Escolha(1)

    def Escolha(self, idx):
        npc     = self.npcs.atual()
        efeitos = npc.dialog.escolher(idx)
        for item in efeitos.get("aumenta", []):
            self.player.update(item["tipo"], +item["quantidade"])
        for item in efeitos.get("diminui", []):
            self.player.update(item["tipo"], -item["quantidade"])

        self.npcs.proximo()
        self.turno.ProximoTurno()
        self.IniciarTexto()

        if self.turno.VerTurno() >= 10:
            self.IniciarFinal()

    def Reset(self):
        self.player.reset()
        self.turno.ResetarTurno()
        self.final       = None
        self.npcs        = GerenciadorNPCs(
            "gestor_federal", "cientista", "diretor_saude",
            "dona_conceicao", "startup", "jornalista",
            "secretaria_ambiental", "empresario", "fazendeiro"
        )
        self.IniciarTexto()

    def update(self):
        if self.digitando:
            agora = pygame.time.get_ticks()
            if agora - self.LastCharTime >= self.CharDelay:
                self.CharIndex   += 1
                self.TextoVisivel = self.TextoCompleto[:self.CharIndex]
                self.LastCharTime = agora
                if self.CharIndex >= len(self.TextoCompleto):
                    self.digitando = False

    def draw(self):
        W, H = self.screen.get_size()
        self.screen.fill((0, 0, 0))
        self.hud.screen = self.screen
        self.hud.draw(self.player.get_stats())

        # tela de final
        if self.final:
            titulo = self.font_titulo.render(self.final["titulo"], True, (240, 220, 160))
            self.screen.blit(titulo, (W // 2 - titulo.get_width() // 2, int(H * 0.20)))

            caixa_w = int(W * 0.80)
            caixa_x = W // 2 - caixa_w // 2
            caixa_y = int(H * 0.35)
            linhas  = wrap_text(self.TextoVisivel, self.font, caixa_w - 20)
            caixa_h = max(len(wrap_text(self.TextoCompleto, self.font, caixa_w - 20)) * 28 + 20, 60)
            pygame.draw.rect(self.screen, (240, 230, 190),
                             (caixa_x, caixa_y, caixa_w, caixa_h), border_radius=8)
            pygame.draw.rect(self.screen, (100, 80, 40),
                             (caixa_x, caixa_y, caixa_w, caixa_h), 2, border_radius=8)
            for i, linha in enumerate(linhas):
                surf = self.font.render(linha, True, (40, 30, 20))
                self.screen.blit(surf, (caixa_x + 10, caixa_y + 10 + i * 28))

            if not self.digitando:
                esc = self.font_op.render("Pressione ESC para sair ou aperte R para resetar", True, (180, 180, 180))
                self.screen.blit(esc, (W // 2 - esc.get_width() // 2, int(H * 0.82)))

            pygame.display.flip()
            return

        # jogo normal
        npc = self.npcs.atual()

        # NPC
        npc_h = int(H * 0.40)
        npc_w = int(npc_h * (npc.imagem.get_width() / npc.imagem.get_height()))
        img   = pygame.transform.scale(npc.imagem, (npc_w, npc_h))
        self.screen.blit(img, (W // 2 - npc_w // 2, int(H * 0.40)))

        # caixa de fala — altura fixa pelo texto completo, conteúdo pelo visível
        caixa_w      = int(W * 0.80)
        caixa_x      = W // 2 - caixa_w // 2
        caixa_y      = int(H * 0.18)
        linhas       = wrap_text(self.TextoVisivel,  self.font, caixa_w - 20)
        linhas_total = wrap_text(self.TextoCompleto, self.font, caixa_w - 20)
        caixa_h      = len(linhas_total) * 28 + 20
        pygame.draw.rect(self.screen, (240, 230, 190),
                         (caixa_x, caixa_y, caixa_w, caixa_h), border_radius=8)
        pygame.draw.rect(self.screen, (100, 80, 40),
                         (caixa_x, caixa_y, caixa_w, caixa_h), 2, border_radius=8)
        for i, linha in enumerate(linhas):
            surf = self.font.render(linha, True, (40, 30, 20))
            self.screen.blit(surf, (caixa_x + 10, caixa_y + 10 + i * 28))

        # opções só aparecem quando texto terminou
        if not self.digitando:
            opcoes = npc.dialog.opcoes()
            op_y   = int(H * 0.86)
            op_w   = int(W * 0.35)
            op_h   = int(H * 0.12)

            if len(opcoes) > 0:
                pygame.draw.rect(self.screen, (80, 60, 30),
                                 (10, op_y, op_w, op_h), border_radius=6)
                linhas_op = wrap_text(opcoes[0]["texto"], self.font_op, op_w - 20)
                total_h   = len(linhas_op) * 24
                y_txt     = op_y + (op_h - total_h) // 2
                for linha in linhas_op:
                    surf = self.font_op.render(linha, True, (240, 220, 160))
                    self.screen.blit(surf, (20, y_txt))
                    y_txt += 24

            if len(opcoes) > 1:
                op_x2     = W - op_w - 10
                pygame.draw.rect(self.screen, (80, 60, 30),
                                 (op_x2, op_y, op_w, op_h), border_radius=6)
                linhas_op = wrap_text(opcoes[1]["texto"], self.font_op, op_w - 20)
                total_h   = len(linhas_op) * 24
                y_txt     = op_y + (op_h - total_h) // 2
                for linha in linhas_op:
                    surf = self.font_op.render(linha, True, (240, 220, 160))
                    self.screen.blit(surf, (op_x2 + 10, y_txt))
                    y_txt += 24
        else:
            hint = self.font_op.render("ESPAÇO para pular", True, (120, 120, 120))
            self.screen.blit(hint, (W // 2 - hint.get_width() // 2, int(H * 0.90)))

        pygame.display.flip()