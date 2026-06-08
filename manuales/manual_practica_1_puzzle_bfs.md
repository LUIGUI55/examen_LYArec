# Manual de Práctica 1: Puzzle Lineal BFS

## 1. Objetivo
Resolver un rompecabezas lineal de 4 dígitos mediante el algoritmo de **Búsqueda en Anchura (BFS - Breadth-First Search)**, aplicando operadores de intercambio adyacentes e ilustrando visualmente el árbol de expansión de estados en un dashboard moderno.

## 2. Fundamento Teórico
La Búsqueda en Anchura (BFS) es un algoritmo de búsqueda no informada que expande los nodos de un árbol nivel por nivel de manera uniforme. Garantiza encontrar la ruta con menor número de arcos (tramos) si todas las transiciones tienen el mismo costo. Utiliza una estructura de **Cola (FIFO - First-In First-Out)** para gestionar la frontera de búsqueda.

## 3. Estructura del Código

### Backend / Lógica de Búsqueda (`BFS.py` & `arbol.py`)
```python
# arbol.py
class Nodo:
    def __init__(self, datos, padre=None, hijos=None):
        self.datos = datos
        self.padre = padre
        self.hijos = None
        self.costo = None
        self.set_hijos(hijos)

    def set_hijos(self, hijos):
        self.hijos = hijos
        if self.hijos is not None:
            for h in self.hijos:
                h.padre = self

    def get_datos(self): return self.datos
    def get_padre(self): return self.padre
    def igual(self, nodo): return self.get_datos() == nodo.get_datos()
    def en_lista(self, lista_nodos):
        for n in lista_nodos:
            if self.igual(n): return True
        return False
```

```python
# BFS.py
from arbol import Nodo

def operador_izquierdo(estado):
    nuevo = estado.copy()
    nuevo[0], nuevo[1] = nuevo[1], nuevo[0]
    return nuevo

def operador_central(estado):
    nuevo = estado.copy()
    nuevo[1], nuevo[2] = nuevo[2], nuevo[1]
    return nuevo

def operador_derecho(estado):
    nuevo = estado.copy()
    nuevo[2], nuevo[3] = nuevo[3], nuevo[2]
    return nuevo

def buscar_solucion_BFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            return nodo
        
        dato_nodo = nodo.get_datos()
        hijos_datos = [
            operador_izquierdo(dato_nodo),
            operador_central(dato_nodo),
            operador_derecho(dato_nodo)
        ]
        for un_hijo in hijos_datos:
            hijo = Nodo(un_hijo, padre=nodo)
            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                nodos_frontera.append(hijo)
    return None
```

### Frontend (`puzzle-dashboard/index.html` & JS clave)
```html
<main class="glass-card">
    <section class="controls">
        <input type="text" id="initial-state" value="4,2,3,1">
        <input type="text" id="goal-state" value="1,2,3,4">
    </section>
    <button id="solve-btn">Encontrar Solución</button>
    <div id="path-container"></div>
</main>
```
```javascript
// script.js (Fragmento clave del resolvedor en el cliente)
function buscarSolucionBFS(estadoInicial, solucionMeta) {
    const solucionStr = solucionMeta.join(',');
    let nodosVisitados = new Set();
    let nodosFrontera = [new Nodo(estadoInicial)];
    nodosVisitados.add(estadoInicial.join(','));

    while (nodosFrontera.length > 0) {
        let nodo = nodosFrontera.shift();
        if (nodo.getString() === solucionStr) return nodo;
        
        let hijos = [
            operadorIzquierdo(nodo.datos),
            operadorCentral(nodo.datos),
            operadorDerecho(nodo.datos)
        ];
        for (let hijo of hijos) {
            let sHijo = hijo.join(',');
            if (!nodosVisitados.has(sHijo)) {
                nodosVisitados.add(sHijo);
                nodosFrontera.push(new Nodo(hijo, nodo));
            }
        }
    }
    return null;
}
```

## 4. Guía de Ejecución y Pruebas
1. Abre la carpeta `puzzle-dashboard` y ejecuta `index.html` directamente en el navegador.
2. Ingresa `4,2,3,1` como estado inicial y `1,2,3,4` como estado meta.
3. Haz clic en **Encontrar Solución**.
4. Observa el recorrido animado por pasos donde los bloques que cambiaron de posición se resaltan visualmente.
