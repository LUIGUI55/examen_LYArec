# Manual de Práctica 2: Buscador de Rutas BFS (Ciudades de México)

## 1. Objetivo
Implementar un resolvedor de caminos entre ciudades mexicanas usando el algoritmo de **Búsqueda en Anchura (BFS)** integrado a un servidor web Flask, permitiendo a los usuarios visualizar el trayecto con el menor número de saltos.

## 2. Fundamento Teórico
En esta práctica se aplica BFS sobre un grafo dirigido/no dirigido donde las ciudades representan los nodos y las carreteras representan las aristas. BFS recorre exhaustivamente todos los nodos adyacentes al origen antes de profundizar, garantizando el camino óptimo en términos de "menor cantidad de conexiones" entre dos ciudades del grafo.

## 3. Estructura del Código

### Backend (Grafo y Algoritmo en `BFS.py` & API Flask en `app.py`)
```python
# BFS.py
from arbol import Nodo

conexiones = {
    'CDMX': {'MORELOS', 'HIDALGO', 'QUERETARO', 'JILOTEPEC'},
    'JILOTEPEC': {'CDMX', 'HIDALGO', 'QUERETARO'},
    'HIDALGO': {'CDMX', 'JILOTEPEC', 'SLP', 'QUERETARO', 'TAMAULIPAS'},
    'QUERETARO': {'CDMX', 'JILOTEPEC', 'HIDALGO', 'SLP', 'GDL'},
    'MORELOS': {'CDMX'},
    'SLP': {'HIDALGO', 'QUERETARO', 'ZACATECAS', 'MONTERREY', 'TAMAULIPAS'},
    'ZACATECAS': {'SLP', 'GDL', 'MONTERREY'},
    'GDL': {'QUERETARO', 'ZACATECAS'},
    'MONTERREY': {'SLP', 'ZACATECAS', 'TAMAULIPAS'},
    'TAMAULIPAS': {'SLP', 'MONTERREY', 'HIDALGO'}
}

def buscar_solucion_BFS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = [Nodo(estado_inicial)]

    if estado_inicial == solucion:
        return nodos_frontera[0]

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        
        dato_nodo = nodo.get_datos()
        hijos_datos = conexiones.get(dato_nodo, set())
            
        for un_hijo in hijos_datos:
            hijo = Nodo(un_hijo, padre=nodo)
            if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                if un_hijo == solucion:
                    return hijo
                nodos_frontera.append(hijo)
    return None
```

```python
# app.py (Rutas asociadas)
@app.route('/bfs')
def bfs_ciudades():
    cities = sorted(list(conexiones.keys()))
    return render_template('bfs.html', cities=cities)

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    origen = data.get('origen')
    destino = data.get('destino')
    nodo_solucion = buscar_solucion_BFS(origen.strip().upper(), destino.strip().upper())
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'cost': len(resultado) - 1, 'success': True})
    return jsonify({'error': 'No se encontró solución', 'success': False})
```

### Frontend (`templates/bfs.html`)
Contiene los menús desplegables para seleccionar la ciudad de origen y destino, interactuando con el backend:
```html
<form id="bfsForm">
    <select id="origen" name="origen" required>
        {% for city in cities %}
        <option value="{{ city }}">{{ city }}</option>
        {% endfor %}
    </select>
    <select id="destino" name="destino" required>
        {% for city in cities %}
        <option value="{{ city }}">{{ city }}</option>
        {% endfor %}
    </select>
    <button type="submit" class="btn-primary">Buscar Ruta</button>
</form>
```

## 4. Guía de Ejecución y Pruebas
1. Ejecuta el servidor local (`python app.py`).
2. Accede a `http://localhost:5000/bfs`.
3. Selecciona **CDMX** como origen y **MONTERREY** como destino.
4. Presiona **Buscar Ruta**. Verás las ciudades intermedias animadas en un contenedor con efectos de desenfoque y cristal (*Glassmorphism*).
