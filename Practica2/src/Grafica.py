from Canales import *
from Nodos import *
import simpy

class Grafica:
    """Representa una grafica.

    Atributos:
    nombre -- cadena que identifica a la grafica
    adyacencias -- lista de listas, adyacencias[i] representa las adyacencias
                    del i-esimo nodo
    nodos -- lista de nodos de la grafica. Dependiendo el algoritmo que hayamos
              corrido, el tipo de nodo sera distinto.
    """
    def __init__(self, nombre: str, adyacencias: list):
        raise NotImplementedError('Constructor de Grafica no implementado')

    def __str__(self):
        raise NotImplementedError('Str de Grafica no implementado')

    def get_nombre(self) -> str:
        raise NotImplementedError('Get_nombre de Grafica no implementado')

    def get_adyacencias(self) -> list:
        raise NotImplementedError('Get_adyacencias de Grafica no implementado')

    def get_nodos(self) -> list:
        raise NotImplementedError('Get_nodos de Grafica no implementado')

    def bfs(self, env: simpy.Environment, canal: Canal) -> None:
        """Algoritmo de bfs."""
        raise NotImplementedError('Bfs de Grafica no implementado')