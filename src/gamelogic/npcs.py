import json
import os
import pygame
import random


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
        """Recria o Dialogo do zero sem corromper o estado do objeto."""
        self.dialog = Dialogo(self.char)


class GerenciadorNPCs:
    def __init__(self, *chars: str):
        self.npcs   = [Npc(char) for char in chars]
        self.indice = 0

    def atual(self) -> Npc:
        return self.npcs[self.indice]

    def proximo(self):
        self.indice = random.randint(0, len(self.npcs) - 1)
        self.npcs[self.indice].resetar_dialogo()  # sempre começa do zero


class Dialogo:
    def __init__(self, char):
        BASE = os.path.dirname(os.path.abspath(__file__))
        caminho_json = os.path.join(BASE, "chars", char, f"{char}.json")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)

        self.sprite_info = dados["sprite"]
        self.falas       = {d["id"]: d for d in dados["dialogos"]}
        self.fala_atual  = self.falas[next(iter(self.falas))]
        self.ativa       = True

    def opcoes(self):
        return self.fala_atual.get("opcoes", [])

    def escolher(self, indice):
        opcao   = self.fala_atual["opcoes"][indice]
        efeitos = opcao.get("efeitos", {})

        # troca para uma fala aleatória diferente da atual
        outras = [k for k in self.falas if k != self.fala_atual["id"]]
        if outras:
            self.fala_atual = self.falas[random.choice(outras)]
        else:
            self.ativa = False  # só encerra se não houver mais falas

        return efeitos

    def texto(self):
        return self.fala_atual["fala"]