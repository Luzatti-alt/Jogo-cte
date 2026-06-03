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
    def ResetarTurno(self):
        global turno
        turno = 0
        return True
    def ProximoTurno(self):
        global turno
        turno += 1 
        self.turno = turno
        return int(self.turno)
    
    def VerTurno(self):
        global turno
        return int(self.turno)
