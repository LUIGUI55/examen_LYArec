# Documentación y Cronología del Proyecto LyAII (Recuperación)

Este documento contiene la clasificación cronológica de todas las prácticas realizadas en el proyecto, desde la primera implementación hasta la última, detallando el objetivo de cada una, su código en Python, sus plantillas HTML asociadas y su lógica de integración.

---

## Índice Cronológico de Prácticas

| N° | Práctica / Módulo | Algoritmo principal | Descripción / Objetivo |
|---|---|---|---|
| **1** | **Puzzle Lineal (4 dígitos) en Netlify** | BFS (Breadth-First Search) | Ordenar la lista `[4, 2, 3, 1]` a `[1, 2, 3, 4]` usando swaps adyacentes. |
| **2** | **Buscador de Rutas en Ciudades de México** | BFS (Breadth-First Search) | Encontrar la ruta con menor número de tramos entre ciudades mexicanas. |
| **3** | **Buscador de Rutas Ponderadas en Ciudades** | UCS (Uniform Cost Search) | Encontrar la ruta óptima por menor distancia en kilómetros acumulados. |
| **4** | **Buscador de Vuelos con Escalas Limitadas** | BFS (Breadth-First Search) | Búsqueda de rutas de vuelo respetando un tope máximo de segmentos. |
| **5** | **Puzzle Lineal DFS (Pila y Recursivo)** | DFS (Depth-First Search) | Resolver el puzzle de 4 dígitos usando estrategias de profundidad. |
| **6** | **Comparador Paralelo de Algoritmos** | Multithreading (BFS/DFS/Hill Climbing) | Ejecutar y medir tiempos de 3 algoritmos corriendo de forma concurrente en hilos. |
| **7** | **Carretera A\* con Distancias Geodésicas** | A\* (Costo Uniforme + Heurística) | Búsqueda óptima de carreteras usando la distancia geodésica (Haversine) como heurística. |
| **8** | **Generación Dinámica de Ubicaciones** | Backend APIs (Flask) + Forms | Crear ubicaciones en tiempo real y posicionarlas aleatoriamente en el mapa. |
| **9** | **BRP Voraz (VRP) y Selección de Ruedas A\*** | Heurística de Ahorros + Búsqueda A\* | Resolver ruteo de vehículos (Clarke & Wright) y asignación óptima de proveedores de ruedas. |

---

## Detalle y Documentación de las Prácticas

### Práctica 1: Puzzle Lineal BFS (Breadth-First Search)
* **Objetivo**: Resolver un puzzle de 4 dígitos (`[4,2,3,1]` -> `[1,2,3,4]`) usando tres operadores de intercambio adyacente (izquierdo, medio, derecho) y búsqueda en amplitud.
* **Componente Python (`BFS.py` & `arbol.py`)**:
  ```python
  # arbol.py - Clase base para los nodos
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
  # BFS.py - Algoritmo inicial del puzzle lineal
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
* **Interfaz HTML (`puzzle-dashboard/index.html`)**:
  ```html
  <!DOCTYPE html>
  <html lang="es">
  <head>
      <meta charset="UTF-8">
      <title>BFS Linear Puzzle Solver</title>
      <link rel="stylesheet" href="styles.css">
  </head>
  <body>
      <div class="dashboard-container">
          <header>
              <h1>Puzzle Lineal <span>BFS</span></h1>
          </header>
          <main class="glass-card">
              <section class="controls">
                  <input type="text" id="initial-state" value="4,2,3,1">
                  <input type="text" id="goal-state" value="1,2,3,4">
              </section>
              <button id="solve-btn">Encontrar Solución</button>
              <div id="path-container"></div>
          </main>
      </div>
      <script src="script.js"></script>
  </body>
  </html>
  ```

---

### Práctica 2: Buscador de Rutas BFS (Ciudades Mexicanas)
* **Objetivo**: Aplicar el algoritmo BFS sobre un grafo que representa la interconexión de varias ciudades de la República Mexicana para hallar el camino con la menor cantidad de conexiones intermedias.
* **Componente Python (`BFS.py` Modificado & API en `app.py`)**:
  ```python
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
  
  # La búsqueda de solución BFS extrae del grafo conexiones[dato_nodo]
  # y verifica si se alcanzó la ciudad destino.
  ```
* **Interfaz HTML (`templates/bfs.html`)**:
  Formulario de dos desplegables dinámicos (Origen y Destino) que consulta a `/api/solve` mediante un POST de AJAX, devolviendo un arreglo animado de nodos con flechas de recorrido.

---

### Práctica 3: Búsqueda de Costo Uniforme (UCS)
* **Objetivo**: Migrar el buscador de rutas de BFS a UCS (Costo Uniforme) agregando ponderación (kilómetros reales entre ciudades) para encontrar el trayecto más corto en distancia total acumulada, no en menor número de tramos.
* **Componente Python (`Carretera_UCS.py`)**:
  ```python
  conexiones = {
      'JILOYORK': {'CDMX': 125, 'QRO': 513},
      'CDMX': {'JILOYORK': 125, 'QRO': 423, 'HGO': 491},
      # ... resto de distancias reales
  }

  def buscar_solucion_UCS(estado_inicial, solucion):
      nodos_visitados = []
      nodos_frontera = []
      nodo_inicial = Nodo(estado_inicial)
      nodo_inicial.set_costo(0)
      nodos_frontera.append(nodo_inicial)

      while len(nodos_frontera) > 0:
          nodos_frontera = sorted(nodos_frontera, key=lambda x: x.costo) # Orden UCS
          nodo = nodos_frontera.pop(0)
          nodos_visitados.append(nodo.get_datos())
          
          if nodo.get_datos() == solucion:
              return nodo
          
          for un_hijo, costo in conexiones[nodo.get_datos()].items():
              hijo = Nodo(un_hijo, nodo)
              hijo.set_costo(nodo.costo + costo)
              # ... lógica para reemplazar en la frontera si el costo es menor
  ```
* **Interfaz HTML (`templates/carretera_ucs.html`)**:
  Dashboard de modo oscuro que muestra el mapa lógico de rutas de costo uniforme y permite concatenar múltiples escalas sumando la distancia total óptima en kilómetros.

---

### Práctica 4: Vuelos BFS con Límite de Escalas
* **Objetivo**: Buscar rutas aéreas entre aeropuertos respetando un límite máximo de segmentos o escalas permitidas (un problema con restricciones sobre el árbol BFS).
* **Componente Python (`Vuelos_BPS.py`)**:
  ```python
  conexiones_b = {
      'Tijuana': {'Monterrey', 'Guadalajara'},
      'DF': {'Monterrey', 'Guadalajara', 'Cancun', 'Merida'},
      # ...
  }
  # BFS limitado: se añade un contador de profundidad o saltos al nodo de búsqueda.
  ```
* **Interfaz HTML (`templates/vuelos.html`)**:
  Dashboard inspirado en agencias de aerolíneas con un selector dinámico de escalas secuenciales.

---

### Práctica 5: Puzzle Lineal DFS (Depth-First Search)
* **Objetivo**: Resolver el rompecabezas de ordenación de 4 dígitos utilizando la estrategia de profundidad (DFS) en dos variantes: Iterativa con Pila explícita y Recursiva pura.
* **Componente Python (`DFS.py` & `dfs_rec.py`)**:
  ```python
  # DFS Iterativo con pila (LIFO)
  def buscar_solucion_DFS(estado_inicial, solucion):
      nodos_frontera = [Nodo(estado_inicial)]
      # ...
      while len(nodos_frontera) != 0:
          nodo = nodos_frontera.pop() # LIFO
          # ...
  ```
  ```python
  # DFS Recursivo
  def buscar_solucion_DFS_rec(estado_inicial, solucion, visitados=None):
      # ...
      for nodo_hijo in nodo_inicial.get_hijos():
          if not nodo_hijo.get_datos() in visitados:
              S = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
              if S is not None: return S
      return None
  ```
* **Interfaz HTML (`templates/puzzle.html` & `templates/puzzle-recursive.html`)**:
  Lienzo interactivo de celdas ordenables que muestra el paso a paso del árbol recorrido mediante DFS.

---

### Práctica 6: Comparador Paralelo de Algoritmos
* **Objetivo**: Medir y evaluar de forma concurrente el rendimiento (tiempo en milisegundos y número de pasos) de tres algoritmos diferentes: Heurístico (Hill Climbing), Iterativo (IDDFS) y Recursivo (DFS).
* **Componente Python (`app.py` / `ThreadPoolExecutor`)**:
  ```python
  @app.route('/api/solve_parallel', methods=['POST'])
  def solve_parallel():
      # ...
      with ThreadPoolExecutor(max_workers=3) as pool:
          futures = {
              pool.submit(_run_heuristico, init, goal): 'heuristico',
              pool.submit(_run_iterativo, init, goal): 'iterativo',
              pool.submit(_run_recursivo, init, goal): 'recursivo',
          }
          # Retorna una lista con la velocidad de ejecución y pasos de cada uno
  ```
* **Interfaz HTML (`templates/comparador.html`)**:
  Página premium que ejecuta en tiempo real los 3 algoritmos y los grafica lado a lado en un panel comparativo con barras de progreso y tiempos precisos.

---

### Práctica 7: Carretera A\* con Distancias Geodésicas
* **Objetivo**: Utilizar el algoritmo A\* para la navegación terrestre óptima, combinando el costo real acumulado $g(n)$ y el costo estimado restante $h(n)$ calculado a partir de la distancia matemática en línea recta utilizando coordenadas de latitud y longitud reales (Fórmula de Haversine).
* **Componente Python (`Carretera_Astar.py` & `DistanciasGeo.py`)**:
  ```python
  # DistanciasGeo.py - Fórmula matemática de distancia geodésica
  from math import sin, cos, acos

  def geo_dist(lat1, lon1, lat2, lon2):
      grad_rad = 0.0174539
      rad_grad = 57.29577951
      longitud = lon1 - lon2
      val = (sin(lat1 * grad_rad) * sin(lat2 * grad_rad)) + (cos(lat1 * grad_rad) * cos(lat2 * grad_rad) * cos(longitud * grad_rad))
      return (acos(val) * rad_grad) * 111.32
  ```
  ```python
  # Carretera_Astar.py - Búsqueda A*
  def buscar_solucion_USC(conexiones, origen, destino):
      # f(n) = g(n) + h(n)
      # donde h(n) = geo_dist(ciudad, destino)
      # ... ordena la frontera según la evaluación total
  ```
* **Interfaz HTML (`templates/carretera_astar.html`)**:
  Vista avanzada con un mapa y visualizador interactivo de caminos geográficos.

---

### Práctica 8: Generación Dinámica de Ubicaciones en el Mapa
* **Objetivo**: Permitir al usuario interactuar directamente con el grafo agregando nuevas ciudades personalizadas (con coordenadas reales de México y pesos de conexión) o generando ubicaciones aleatorias reales de forma instantánea.
* **Componente Python (APIs en `app.py`)**:
  Endpoints `/api/add_location` y `/api/add_random_location` que modifican en tiempo de ejecución las variables globales de coordenadas y conexiones en memoria de los módulos `Carretera_Astar` and `Carretera_UCS`.
* **Interfaz HTML (`templates/carretera_astar.html` / `templates/carretera_ucs.html`)**:
  Formulario premium de inserción que incluye un botón de "Generar Ubicación Aleatoria" con autocompletado automático de coordenadas y selección manual del nodo de enlace inicial.

---

### Práctica 9: Algoritmos Greedy (BRP Voraz) y Selección de Ruedas A\*
* **Objetivo**: Implementar ruteo de vehículos (VRP) mediante el algoritmo de ahorros voraz de Clarke & Wright y la asignación óptima de proveedores de neumáticos sin repetir proveedor mediante A\* en un espacio bidimensional.
* **Componente Python (`BRP_boraz.py` & `SeleccionRuedas_Astar.py`)**:
  - `BRP_boraz.py`: Calcula los ahorros entre clientes respecto al almacén central, los ordena de mayor a menor y aplica las 4 reglas del algoritmo para conformar rutas bajo límites de capacidad de carga.
  - `SeleccionRuedas_Astar.py`: Encuentra la combinación óptima de costos mínimos para la compra de 4 tipos de llantas ('t', 'h', 'v', 'w') distribuidas en 4 empresas diferentes.
* **Interfaz HTML (`templates/brp_boraz.html` & `templates/seleccion_ruedas.html`)**:
  - El simulador BRP permite registrar pedidos y trazar el mapa de despacho.
  - El asignador de ruedas A\* despliega el árbol de búsqueda paso a paso indicando los valores $g(n)$, $h(n)$ y $f(n)$ calculados dinámicamente.
