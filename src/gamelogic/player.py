class Player():
    #valor default
    #0-100
    def __init__(self):
        self.economico = 50
        self.social    = 50
        self.ambiental = 50
    
    def update(self,tipo:str,valor:int):
        if tipo == "economico":
            self.economico += valor
        elif tipo == "social":
            self.social += valor
        elif tipo == "ambiental":
            self.ambiental += valor
        #cap
        self.economico = max(0,min(100, self.economico))
        self.social = max(0,min(100, self.social))
        self.ambiental = max(0,min(100, self.ambiental))

    def get_stats(self):
        return {"economico": self.economico, "social": self.social, "ambiental": self.ambiental}
    
    def reset(self):
        self.economico = 50
        self.social = 50
        self.ambiental = 50