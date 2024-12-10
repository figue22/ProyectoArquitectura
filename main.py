# Programa principal
from Modelos.computador import Computador
from Vistas.interfaz import Interfaz



if __name__ == "__main__":
      comp = Computador()
      interfaz = Interfaz(comp)
      interfaz.iniciar()


