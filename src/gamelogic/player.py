class Player():
    #valor default
    #0-100
    def _init__(self):
        self.economia = 50
        self.social = 50
        self.ambiente = 50
    
    def update(self,tipo:str,valor:int):
        if tipo == "economia":
            self.economia += valor
        elif tipo == "social":
            self.social += valor
        elif tipo == "ambiente":
            self.economia += valor

    def get_stats(self):
        return {"economia": self.economia, "social": self.social, "ambiente": self.ambiente}