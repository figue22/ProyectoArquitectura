class Registro:
    def __init__(self, nombre):
        self.nombre = nombre
        self.valor = 0

    def set(self, valor):
        self.valor = valor

    def get(self):
        return self.valor