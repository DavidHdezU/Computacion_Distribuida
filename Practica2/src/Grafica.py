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
        self.nombre = nombre
        self.adyacencias = adyacencias
        self.nodos = []

    def __str__(self):
        return f"Gráfica: {self.nombre} \n Nodos: {self.nodos}"

    def get_nombre(self) -> str:
        """
        Regresa el nombre de la gráfica

        Returns:
            str: nombre de la gráfica
        """
        return self.nombre

    def get_adyacencias(self) -> list:
        """
        Regresa la lista de adyacencias

        Returns:
            list: lista de adyancencias
        """
        return self.adyacencias
    
    def get_nodos(self) -> list:
        """
        Regresa la lista de nodos de la gráfica

        Returns:
            list: La lista de nodos
        """
        return self.nodos

    def bfs(self, env: simpy.Environment, canal: Canal) -> None:
        """Algoritmo de bfs."""
        self.nodos.clear()
        
        for i, vecinos in enumerate(self.adyacencias):
            canal_entrada = canal.crea_canal_de_entrada()
            nodo = NodoBFS(i, vecinos, (canal_entrada, canal))
            
            self.nodos.append(nodo)
            
        for v in self.nodos:
            env.process(v.bfs(env))

        yield env.timeout(0)

    def dfs(self, env: simpy.Environment, canal: Canal) -> None:
        """Algoritmo de dfs."""
        self.nodos.clear()
        
        for i, vecinos in enumerate(self.adyacencias):
            canal_entrada = canal.crea_canal_de_entrada()
            nodo = NodoDFS(i, vecinos, (canal_entrada, canal))
            
            self.nodos.append(nodo)
            
        for v in self.nodos:
            env.process(v.dfs(env))

        yield env.timeout(0)