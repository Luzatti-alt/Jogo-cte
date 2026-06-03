import sys

def resource_path(relative):
    if getattr(sys, 'frozen', False):
        return os.path.normpath(os.path.join(sys._MEIPASS, relative))
    return os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", relative
    ))

import json
import os
import pygame
from src.gamelogic.gamestate import RNG

class Npc:
    def __init__(self, char):
        self.char   = char
        self.dialog = Dialogo(char)
        BASE = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.normpath(
            os.path.join(BASE, "chars", char, self.dialog.sprite_info["imagem"])
        )
        self.imagem = pygame.image.load(caminho_img).convert_alpha()
        self.nome   = self.dialog.sprite_info["nome"]

    def resetar_dialogo(self):
        self.dialog = Dialogo(self.char)


class GerenciadorNPCs:
    def __init__(self, *chars: str):
        self.chars      = list(chars)
        self.npcs       = {char: Npc(char) for char in chars}
        self.atual_char = RNG.EscolherNpc(self.chars)

    def atual(self) -> Npc:
        return self.npcs[self.atual_char]

    def proximo(self):
        outros = [c for c in self.chars if c != self.atual_char]
        self.atual_char = RNG.EscolherNpc(outros) if outros else self.atual_char
        self.npcs[self.atual_char].resetar_dialogo()


class Dialogo:
    def __init__(self, char):
        BASE = os.path.dirname(os.path.abspath(__file__))
        caminho_json = os.path.join(BASE, "chars", char, f"{char}.json")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        self.sprite_info = dados["sprite"]
        self.falas       = {d["id"]: d for d in dados["dialogos"]}
        fala_inicial     = RNG.sortear_fala(list(self.falas.keys()))
        self.fala_atual  = self.falas[fala_inicial]   # CORRIGIDO: usa fala_inicial
        self.ativa       = True

    def opcoes(self):
        return self.fala_atual.get("opcoes", [])

    def escolher(self, indice):
        opcao   = self.fala_atual["opcoes"][indice]
        efeitos = opcao.get("efeitos", {})

        proxima = RNG.sortear_fala(list(self.falas.keys()), excluir=self.fala_atual["id"])
        if proxima is not None:
            self.fala_atual = self.falas[proxima]
        else:
            self.ativa = False

        return efeitos

    def texto(self):
        return self.fala_atual["fala"]