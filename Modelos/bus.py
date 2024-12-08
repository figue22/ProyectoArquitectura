#clase que representa el bus del sistema

class Bus:
    def __init__(self, nombre):
        self.valor = 0
        self.nombre = nombre 
        
    def set(self, valor):
        self.valor = valor

    def get(self):
        return self.valor
    

