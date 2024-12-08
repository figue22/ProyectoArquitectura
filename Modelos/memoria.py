# Clase Memoria
class Memoria:
    def __init__(self, tamano):
        self.memoriaDatos = [0] * (tamano//2)
        self.memoriaInstrucciones = [0] * (tamano//2)


    def leerDato(self, direccion):
        return self.memoriaDatos[direccion]

    def escribirDato(self, direccion, valor):
        self.memoriaDatos[direccion] = valor

    def leerInstruccion(self, direccion):
        return self.memoriaInstrucciones[direccion]
    
    def escribirInstruccion(self, direccion, instruccion):
        self.memoriaInstrucciones[direccion] = instruccion
