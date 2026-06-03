import random

turno = 0
rng  = random.Random()
class RNG():
    def __init__(self):
        pass
    
    #lista nps + num de falas
    @staticmethod
    def EscolherNpc(lista_chars: list[str]) -> str:
        return rng.choice(lista_chars)
    
    @staticmethod
    def sortear_fala(ids_disponiveis: list, excluir=None) -> int:
        opcoes = [i for i in ids_disponiveis if i != excluir]
        if not opcoes:
            return None
        return rng.choice(opcoes)

class Turno():
    def __init__(self):
        global turno
        self.turno = turno
    
    def ProximoTurno(self):
        global turno
        turno += 1 
        self.turno = turno
        return int(self.turno)
    
    def VerTurno(self):
        global turno
        return int(self.turno)

class Finais():
    def __init__(self):
        pass
    def Bad_ending(self):
        pass
    def Good_ending(self):
        pass
    def Neutral_ending(self):
        pass