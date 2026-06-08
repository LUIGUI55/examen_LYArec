# Manual de Práctica 4: Vuelos BFS (Buscador de Vuelos con Escalas)

## 1. Objetivo
Aplicar el algoritmo de **Búsqueda en Anchura (BFS)** sobre un grafo de destinos aéreos y aeropuertos interconectados para diseñar un motor de búsqueda de vuelos que encuentre la ruta óptima de trayectos aéreos.

## 2. Fundamento Teórico
En la navegación aérea, los vuelos directos y las escalas mínimas representan la optimización óptima de saltos en un grafo. Dado que cada vuelo representa una arista sin ponderación de costo variable en este problema, la búsqueda en amplitud (BFS) garantiza de forma nativa hallar la combinación de vuelos que requiera la menor cantidad de escalas intermedias desde el origen hasta el aeropuerto destino.

## 3. Estructura del Código

### Backend (Grafo de Vuelos y Algoritmo en `Vuelos_BPS.py`)
```python
# Vuelos_BPS.py
from arbol import Nodo

conexiones_brutas = {
    'Jilotepec': {'CELAYA','CDMX','Queretaro'},
    'Sonora':{'Zacatecas','Sinaloa'},
    'Guanajuato':{'Aguascalientes', 'Queretaro'},
    'Oaxaca':{'Queretaro'},
    'Sinaloa':{'Celaya','Sonora','jilotepec'},
    'Queretaro':{'Monterrey'},
    'Celaya':{'Jilotepec','Sinaloa'},
    'Zacatecas':{'Sonora','Monterrey','Queretaro'},
    'Monterrey':{'Zacatecas','Sinaloa'},
    'Tamaulipas':{'Queretaro'},
    'CDMX':{'Tamaulipas','Zacatecas','Sinaloa','Jilotepec','Oaxaca'}
}

# Normalización bidireccional de destinos aéreos
conexiones_b = {}
for origen, destinos in conexiones_brutas.items():
    ou = origen.upper()
    if ou not in conexiones_b:
        conexiones_b[ou] = set()
    for dest in destinos:
        du = dest.upper()
        conexiones_b[ou].add(du)
        if du not in conexiones_b:
            conexiones_b[du] = set()
        conexiones_b[du].add(ou)

def Buscar_solucion_BFS(conexiones, estado_inicial, solucion):
    estado_inicial = estado_inicial.upper()
    solucion = solucion.upper()
    nodos_frontera = [Nodo(estado_inicial)]
    nodos_visitados = []

    while len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)
        
        if nodo.get_datos() == solucion:
            return nodo
        
        dato_nodo = nodo.get_datos()
        if dato_nodo in conexiones:
            for una_ciudad in conexiones[dato_nodo]:
                hijo = Nodo(una_ciudad, nodo)
                if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                    nodos_frontera.append(hijo)
    return None
```

### Frontend (`templates/vuelos.html` - Script de llamada AJAX)
```javascript
const response = await fetch('/api/solve_secuencial', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nodos: ciudadesSeleccionadas })
});
const data = await response.json();
if (data.success) {
    // Renderizado secuencial de vuelos y escalas
}
```

## 4. Guía de Ejecución y Pruebas
1. Ejecuta el servidor Flask (`python app.py`).
2. Entra a `http://localhost:5000/vuelos`.
3. Selecciona **JILOTEPEC** como punto de origen de partida y **ZACATECAS** como punto final de llegada.
4. Presiona **Buscar Vuelo**. Verás el listado de conexiones ordenadas que representan el itinerario de vuelos óptimo con menos escalas intermedias.
