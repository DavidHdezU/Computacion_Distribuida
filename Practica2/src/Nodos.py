import Canales
import math
import simpy

class Nodo:
    """Representa un nodo basico.

    Atributos:
    id_nodo -- identificador del nodo
    vecinos -- lista con los ids de nuestros vecinos
    canales -- tupla de la forma (canal_entrada, canal_salida)
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor basico de un Nodo."""
        raise NotImplementedError('Constructor de Nodo no implementado')

    def __str__(self):
        """Regresa la representacion en cadena del nodo."""
        raise NotImplementedError('Str de Nodo no implementado')
    
    def get_id(self) -> int:
        """Regresa el identificador del nodo."""
        raise NotImplementedError('Get_id de Nodo no implementado')
    
    def get_vecinos(self) -> list:
        """Regresa la lista de vecinos del nodo."""
        raise NotImplementedError('Get_vecinos de Nodo no implementado')

    def get_canal_entrada(self) -> simpy.Store:
        """Regresa el canal de entrada del nodo."""
        raise NotImplementedError('Get_canal_entrada de Nodo no implementado')

    def get_canal_salida(self) -> Canales.Canal:
        """Regresa el canal de salida del nodo."""
        raise NotImplementedError('Get_canal_salida de Nodo no implementado')

class NodoBFS(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 1.

    Atributos adicionales:
    padre -- id del nodo que sera su padre en el arbol
    nivel -- entero que representa la distancia del nodo a la raiz
    hijos -- lista de ids de los nodos hijos del nodo
    msjs_esperados -- numero de mensajes que espera el nodo
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo 'bfs'."""
        raise NotImplementedError('Constructor de NodoVecinos no implementado')

    def bfs(self, env: simpy.Environment):
        """Algoritmo de BFS."""