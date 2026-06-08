# Manual de Práctica 9: Algoritmos Avanzados (VRP Voraz y Selección de Ruedas A\*)

## 1. Objetivo
Implementar y documentar dos problemas de optimización avanzada:
1. **Problema de Enrutamiento de Vehículos (VRP/BRP)** mediante la heurística voraz de ahorros de Clarke y Wright.
2. **Selección de Ruedas Óptima** a través del algoritmo de búsqueda informada **A\*** en un árbol de asignación de proveedores sin duplicación.

## 2. Fundamento Teórico

### VRP (Vehicle Routing Problem) Voraz
El algoritmo de ahorros de Clarke y Wright evalúa el ahorro obtenido al consolidar entregas en una misma ruta en lugar de realizar viajes individuales de ida y vuelta al almacén central ($0$). El ahorro de enlazar el cliente $i$ con el cliente $j$ se define como:
$$S(i, j) = d(i, 0) + d(j, 0) - d(i, j)$$
Los ahorros se ordenan de mayor a menor y se enlazan las rutas respetando la capacidad máxima de carga del vehículo.

### Selección de Ruedas A\*
Busca adjudicar 4 tipos de ruedas ('t', 'h', 'v', 'w') a 4 fabricantes diferentes, de forma que el costo total sea mínimo y ningún fabricante sea seleccionado más de una vez. Utiliza una heurística admisible $h(n)$ que calcula la suma de los costos mínimos posibles para las ruedas pendientes utilizando únicamente las empresas aún no adjudicadas.

## 3. Estructura del Código

### Backend (VRP Voraz en `BRP_boraz.py` & Selección A\* en `SeleccionRuedas_Astar.py`)
```python
# BRP_boraz.py (Fragmento clave del cálculo de ahorros)
def vrp_voraz(pedidos, almacen, max_carga):
    s = {}
    clientes = list(pedidos.keys())
    for c1 in clientes:
        for c2 in clientes:
            if c1 != c2:
                if not (c1, c2) in s and not (c2, c1) in s:
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_alm = distancia(coord[c1], coord[almacen])
                    d_c2_alm = distancia(coord[c2], coord[almacen])
                    s[(c1, c2)] = d_c1_alm + d_c2_alm - d_c1_c2
                    
    s = sorted(s.items(), key=lambda x: x[1], reverse=True) # Ordenar ahorros
    # Construir rutas iterando sobre los ahorros bajo límites de max_carga...
    return rutas, pasos
```

```python
# SeleccionRuedas_Astar.py (Cálculo de la heurística h(n) admisible)
def calcular_h(estado, matriz):
    empresas_asignadas = set(emp for emp in estado if emp is not None)
    empresas_libres = [emp for emp in EMPRESAS if emp not in empresas_asignadas]
    
    if not empresas_libres:
        return 0, []
        
    h_total = 0
    for i in range(len(TIPOS_RUEDA)):
        if estado[i] is None: # Rueda no asignada aún
            tipo = TIPOS_RUEDA[i]
            precio_min = min(matriz[emp][tipo] for emp in empresas_libres)
            h_total += precio_min
    return h_total, []
```

### Frontend (`templates/brp_boraz.html` & `templates/seleccion_ruedas.html`)
- **BRP Voraz UI**: Panel para introducir pesos de pedidos por ciudad, definir capacidad máxima del vehículo y ejecutar la optimización mostrando un registro detallado de reglas de consolidación aplicadas.
- **Asignador de Ruedas A\* UI**: Permite configurar una matriz de costos por empresa y muestra visualmente la traza de búsqueda del árbol A\* con los valores detallados de $g$, $h$ y $f$ de cada nodo.

## 4. Guía de Ejecución y Pruebas
1. Ejecuta el servidor Flask (`python app.py`).
2. Navega a `http://localhost:5000/brp-voraz` para resolver la logística de reparto.
3. Navega a `http://localhost:5000/seleccion-ruedas` para la adjudicación de proveedores.
4. Experimenta alterando la matriz de costos de las ruedas y observa cómo el árbol A* modifica su camino de expansión en tiempo real buscando siempre el costo óptimo de producción.
