# Manual de Práctica 7: Carretera A\* (Búsqueda Informada con Distancias Geodésicas)

## 1. Objetivo
Implementar el algoritmo de búsqueda informada **A\*** sobre el grafo de carreteras de México, utilizando la fórmula matemática de distancia geodésica (Haversine/círculo máximo) sobre coordenadas geográficas reales de latitud y longitud como función heurística $h(n)$.

## 2. Fundamento Teórico
El algoritmo A\* evalúa los nodos usando la función:
$$f(n) = g(n) + h(n)$$
- $g(n)$: El costo real acumulado en kilómetros para viajar desde el origen hasta el nodo actual $n$.
- $h(n)$: La estimación heurística del costo restante desde el nodo actual $n$ hasta la meta.
Para que A\* sea óptimo, la heurística $h(n)$ debe ser **admisible** (nunca sobreestimar el costo real). La distancia geodésica cumple con esta condición, ya que representa la distancia mínima en línea recta sobre la curvatura de la Tierra ("a vuelo de pájaro").

## 3. Estructura del Código

### Backend (Algoritmo A\* y Heurística en `Carretera_Astar.py`)
```python
# Carretera_Astar.py
from arbol import Nodo
from math import sin, cos, acos

coord = {
    'Jiloyork': (19.9524089, -99.5330457),
    'CDMX': (19.4326849, -99.1333370),
    'QRO': (20.5879565, -100.3879329),
    # ... otras coordenadas reales
}

def geodist(lat1, lon1, lat2, lon2):
    grad_rad = 0.0174539
    rad_grad = 57.29577951
    longitud = lon1 - lon2
    val = (sin(lat1 * grad_rad) * sin(lat2 * grad_rad)) + (cos(lat1 * grad_rad) * cos(lat2 * grad_rad) * cos(longitud * grad_rad))
    val = max(-1.0, min(1.0, val)) # Acotar rango
    return (acos(val) * rad_grad) * 111.32

def buscar_solucion_USC(conexiones, estado_inicial, solucion):
    # Función de evaluación f(n) = g(n) + h(n)
    def evalua(x):
        lat1 = coord[x.get_datos()][0]
        lon1 = coord[x.get_datos()][1]
        lat2 = coord[solucion][0]
        lon2 = coord[solucion][1]
        d = int(geodist(lat1, lon1, lat2, lon2))
        return x.get_costo() + d

    nodos_frontera = [Nodo(estado_inicial)]
    nodos_frontera[0].set_costo(0)
    nodos_visitados = []
    
    while len(nodos_frontera) != 0:
        nodos_frontera = sorted(nodos_frontera, key=evalua)
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            return nodo
            
        dato_nodo = nodo.get_datos()
        if dato_nodo in conexiones:
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo, nodo)
                costo = conexiones[dato_nodo][un_hijo]
                hijo.set_costo(nodo.get_costo() + costo)
                
                if not hijo.en_lista(nodos_visitados):
                    en_frontera = False
                    for n in nodos_frontera:
                        if n.igual(hijo):
                            en_frontera = True
                            if n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                            break
                    if not en_frontera:
                        nodos_frontera.append(hijo)
    return None
```

### Frontend (`templates/carretera_astar.html`)
Un panel interactivo que conecta al endpoint `/api/solve_carretera_astar` y permite visualizar la ruta secuencial más óptima en kilómetros calculada por A\*.

## 4. Guía de Ejecución y Pruebas
1. Levanta el servidor Flask (`python app.py`).
2. Ve a `http://localhost:5000/carretera-astar`.
3. Elige **Jiloyork** como punto de origen y **MTY** (Monterrey) como punto de destino.
4. Presiona el botón **Buscar Ruta Óptima (A\*)**.
5. Valida el costo total reportado y comprueba cómo el número de nodos expandidos por A\* es menor que en UCS clásico gracias a la guía de la heurística geodésica.
