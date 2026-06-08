# Manual de Práctica 3: Carretera UCS (Búsqueda de Costo Uniforme)

## 1. Objetivo
Desarrollar una aplicación de navegación que calcule la ruta óptima de menor distancia en kilómetros acumulados utilizando el algoritmo de **Búsqueda de Costo Uniforme (UCS - Uniform Cost Search)** sobre un mapa vial ponderado.

## 2. Fundamento Teórico
La Búsqueda de Costo Uniforme es una generalización de BFS para grafos con aristas de distinto peso. En lugar de extraer el primer elemento insertado en la frontera, UCS selecciona y expande siempre el nodo con el menor costo acumulado $g(n)$ desde el origen. Se implementa mediante una **Cola de Prioridades** (ordenada ascendentemente por costo). Es un algoritmo completo y óptimo si los costos de las aristas son estrictamente mayores a cero.

## 3. Estructura del Código

### Backend (Grafo de Carreteras y Algoritmo UCS en `Carretera_UCS.py`)
```python
# Carretera_UCS.py
from arbol import Nodo

conexiones = {
    'JILOYORK': {'CDMX': 125, 'QRO': 513},
    'MORELOS': {'QRO': 524},
    'CDMX': {'JILOYORK': 125, 'QRO': 423, 'HGO': 491},
    'HGO': {'CDMX': 491, 'QRO': 356, 'MEXICALI': 109, 'MONTERREY': 346},
    'QRO': {
        'SLP': 203, 'MORELOS': 514, 'JILOYORK': 513, 'CDMX': 423,
        'MONTERREY': 603, 'SONORA': 437, 'HGO': 356, 'MEXICALI': 313,
        'AGUASCALIENTES': 599
    },
    'SLP': {'AGUASCALIENTES': 399, 'QRO': 203},
    'AGUASCALIENTES': {'SLP': 390, 'QRO': 599},
    'SONORA': {'QRO': 437, 'MEXICALI': 394},
    'MEXICALI': {'MONTERREY': 296, 'HGO': 309, 'QRO': 313},
    'MONTERREY': {'MEXICALI': 296, 'QRO': 603, 'HGO': 346}
}

def buscar_solucion_UCS(estado_inicial, solucion):
    nodos_visitados = []
    nodos_frontera = []
    
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) > 0:
        # Ordenar frontera ascendentemente por costo g(n)
        nodos_frontera = sorted(nodos_frontera, key=lambda x: x.costo)
        
        # Extraer menor costo
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo.get_datos())
        
        if nodo.get_datos() == solucion:
            return nodo
            
        dato_nodo = nodo.get_datos()
        if dato_nodo in conexiones:
            lista_hijos = []
            for un_hijo, costo in conexiones[dato_nodo].items():
                hijo = Nodo(un_hijo)
                hijo.set_costo(nodo.costo + costo)
                
                if un_hijo not in nodos_visitados:
                    # Verificar si existe en frontera con un costo mayor
                    en_frontera = False
                    for n in nodos_frontera:
                        if n.get_datos() == un_hijo:
                            en_frontera = True
                            if n.costo > hijo.costo:
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                            break
                    
                    if not en_frontera:
                        nodos_frontera.append(hijo)
                        lista_hijos.append(hijo)
            nodo.set_hijos(lista_hijos)
    return None
```

### Frontend (`templates/carretera_ucs.html` - Segmento de Envío)
```javascript
document.getElementById('ucsForm').onsubmit = async (e) => {
    e.preventDefault();
    const selects = document.querySelectorAll('.node-select');
    const nodos = Array.from(selects).map(select => select.value);
    
    const response = await fetch('/api/solve_carretera_ucs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodos })
    });
    const data = await response.json();
    if (data.success) {
        document.getElementById('costResult').textContent = `Costo Total: ${data.cost} km`;
        // Inyectar etiquetas html para cada parada en el DOM
    }
};
```

## 4. Guía de Ejecución y Pruebas
1. Levanta el servidor Flask (`python app.py`).
2. Navega a `http://localhost:5000/carretera-ucs`.
3. Selecciona **JILOYORK** en Ciudad de Origen y **SLP** en Ciudad de Destino.
4. Presiona el botón "+ Agregar Destino / Escala" para agregar paradas secuenciales intermedias.
5. Haz clic en **Buscar Ruta Óptima (UCS)** y comprueba el costo mínimo en kilómetros mostrado.
