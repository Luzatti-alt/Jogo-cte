import json
import os
import pygame

class Npc:
    def __init__(self,char):
        self.dialog = Dialogo(char)
        BASE = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.normpath(
            os.path.join(BASE, "chars", char, self.dialog.sprite_info["imagem"])
        )
        
        self.imagem = pygame.image.load(caminho_img).convert_alpha()
        self.nome   = self.dialog.sprite_info["nome"]

class GerenciadorNPCs:
    def __init__(self, *chars: str):
        self.npcs   = [Npc(char) for char in chars]
        self.indice = 0
    
    def atual(self) -> Npc:
        return self.npcs[self.indice]

    def proximo(self):
        self.indice = (self.indice + 1) % len(self.npcs)


class Dialogo:
    def __init__(self,char):
        BASE = os.path.dirname(os.path.abspath(__file__))
        caminho_json = os.path.join(BASE, "chars", char, f"{char}.json")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        self.sprite_info = dados["sprite"] # {"nome": ..., "imagem": ...}
        self.falas = {d["id"]: d for d in dados["dialogos"]}
        self.fala_atual = self.falas[1]  # trocar o id/fazer evento random 
        self.ativa = True
    
    def opcoes(self):
        return self.fala_atual["opcoes"]

    def escolher(self, indice):
        opcao = self.fala_atual["opcoes"][indice]
        proxima = opcao.get("proxima_fala")
        if proxima and proxima in self.falas:
            self.fala_atual = self.falas[proxima]
        else:
            self.ativa = False                      # fim do diálogo
        return opcao["efeitos"]                     # retorna efeitos para o Player

    def texto(self):
        return self.fala_atual["fala"]
