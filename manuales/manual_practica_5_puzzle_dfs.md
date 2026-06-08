# Manual de Práctica 5: Puzzle Lineal DFS (Iterativo y Recursivo)

## 1. Objetivo
Resolver el rompecabezas lineal de 4 dígitos utilizando la estrategia de **Búsqueda en Profundidad (DFS - Depth-First Search)**, analizando las diferencias de comportamiento, consumo de memoria y orden de expansión entre la versión con pila iterativa y la versión recursiva.

## 2. Fundamento Teórico
La Búsqueda en Profundidad (DFS) explora lo más profundo posible a lo largo de cada rama de un árbol de búsqueda antes de dar marcha atrás (backtracking). 
- **Versión Iterativa**: Se gestiona una pila explícita **LIFO (Last-In First-Out)** de manera que los últimos nodos agregados a la frontera son los primeros en extraerse.
- **Versión Recursiva**: Se apoya en la **pila de llamadas (Call Stack)** del sistema operativo para descender por las ramas de ejecución recursivamente.
DFS no garantiza el camino más corto o solución óptima, pero puede requerir menos memoria en espacios de búsqueda específicos si hay muchas soluciones distribuidas profundamente.

## 3. Estructura del Código

### Backend (DFS Iterativo en `DFS.py` y DFS Recursivo en `dfs_rec.py`)
```python
# DFS.py (Iterativo)
from arbol import Nodo

def buscar_solucion_DFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = [Nodo(estado_inicial)]

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop() # LIFO (Extrae del final)
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            return nodo
            
        dato_nodo = nodo.get_datos()
        
        # Generar hijos por intercambios adyacentes
        hijo_izq = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_cen = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_der = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        
        for h in [hijo_izq, hijo_cen, hijo_der]:
            n_hijo = Nodo(h, padre=nodo)
            if not n_hijo.en_lista(nodos_visitados) and not n_hijo.en_lista(nodos_frontera):
                nodos_frontera.append(n_hijo)
    return None
```

```python
# dfs_rec.py (Recursivo)
from arbol import Nodo

def buscar_solucion_DFS_rec(estado_inicial, solucion, visitados=None):
    if visitados is None:
        visitados = []
        nodo_inicial = Nodo(estado_inicial)
    else:
        nodo_inicial = estado_inicial

    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
        
    dato_nodo = nodo_inicial.get_datos()
    hijo_izq = Nodo([dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]])
    hijo_med = Nodo([dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]])
    hijo_der = Nodo([dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]])
    
    nodo_inicial.set_hijos([hijo_izq, hijo_med, hijo_der])

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados:
            S = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if S is not None:
                return S
    return None
```

### Frontend (`templates/puzzle.html` / `templates/puzzle-recursive.html`)
Formulario premium para introducir combinaciones numéricas que se comunica con los endpoints correspondientes `/api/solve_puzzle` y `/api/solve_puzzle_recursive`.

## 4. Guía de Ejecución y Pruebas
1. Ejecuta el servidor Flask (`python app.py`).
2. Visita `http://localhost:5000/puzzle` para probar el DFS Iterativo.
3. Visita `http://localhost:5000/puzzle-recursive` para probar el DFS Recursivo.
4. Ingresa el estado inicial `4,2,3,1` y meta `1,2,3,4`.
5. Ejecuta la búsqueda y analiza la cantidad total de pasos requeridos por DFS en comparación con BFS (DFS típicamente encuentra caminos más largos pero con diferente orden de expansión).
