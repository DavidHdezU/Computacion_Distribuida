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

    def conoce_vecinos(self, env: simpy.Environment, canal: simpy.Store) -> None:
        """Algoritmo para conocer a los vecinos de mis vecinos."""
        raise NotImplementedError('Conoce_vecinos de Grafica no implementado')

    def genera_arbol_generador(self, env: simpy.Environment, canal: simpy.Store) \
            -> None:
        """Algoritmo para generar el arbol generador."""
        raise NotImplementedError('Get_arbol_generador de Grafica no implementado')

    def broadcast(self, env: simpy.Environment, canal: simpy.Store,
            adyacencias_arbol: list()) -> None:
        """Algoritmo de broadcast.
        
        Atributos:
        adyacencias_arbol -- Las aristas que forman el arbol sobre el que 
                              vamos a hacer el broadcast del mensaje.
        """
        raise NotImplementedError('Broadcast de Grafica no implementado')
