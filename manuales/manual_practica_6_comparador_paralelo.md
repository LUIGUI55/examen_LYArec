# Manual de Práctica 6: Comparador Paralelo de Algoritmos (Heurístico vs Iterativo vs Recursivo)

## 1. Objetivo
Evaluar y comparar el desempeño computacional (en tiempo de ejecución y número de pasos) de tres enfoques de resolución de problemas (Hill Climbing Heurístico, DFS Iterativo con profundidad limitada e IDDFS, y DFS Recursivo) ejecutados de forma concurrente mediante hilos en Python Flask.

## 2. Fundamento Teórico
El multithreading permite ejecutar código simultáneamente en múltiples hilos aprovechando las CPUs multinúcleo. En esta práctica, se comparan:
- **Heurístico (Hill Climbing / A* Simplificado)**: Utiliza una función heurística de desorden (piezas fuera de lugar) para guiar la búsqueda con una cola de prioridades.
- **Iterativo (IDDFS - Iterative Deepening DFS)**: Combina la completitud de BFS con el bajo consumo espacial de DFS incrementando progresivamente el límite de profundidad en cada iteración.
- **Recursivo (DFS)**: Búsqueda en profundidad clásica implementada de forma recursiva.

## 3. Estructura del Código

### Backend (Lógica Multihilo en `app.py`)
```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def _run_heuristico(estado_inicial, solucion):
    start = time.perf_counter()
    nodo_inicial = NodoHeuristico(estado_inicial)
    nodo_sol = buscar_solucion_heuristica(nodo_inicial, solucion)
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    # Reconstruir camino...
    return {'name': 'Heurístico (Hill Climbing)', 'success': True, 'time_ms': elapsed}

# Equivalentes para _run_iterativo y _run_recursivo

@app.route('/api/solve_parallel', methods=['POST'])
def solve_parallel():
    data = request.json
    init = data.get('estado_inicial')
    goal = data.get('solucion')

    total_start = time.perf_counter()
    results = []
    # Lanzar los 3 algoritmos concurrentemente en hilos
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(_run_heuristico, list(init), list(goal)): 'heuristico',
            pool.submit(_run_iterativo, list(init), list(goal)): 'iterativo',
            pool.submit(_run_recursivo, list(init), list(goal)): 'recursivo',
        }
        for future in as_completed(futures):
            results.append(future.result())
            
    total_elapsed = round((time.perf_counter() - total_start) * 1000, 3)
    return jsonify({'success': True, 'results': results, 'total_time_ms': total_elapsed})
```

### Frontend (`templates/comparador.html`)
Diseña un panel con barras comparativas que realiza la consulta POST a `/api/solve_parallel`, recibiendo los tiempos precisos de ejecución y el total de pasos de cada uno para graficarlos dinámicamente.

## 4. Guía de Ejecución y Pruebas
1. Levanta el servidor Flask (`python app.py`).
2. Entra a `http://localhost:5000/comparador`.
3. Ingresa el estado inicial `4,2,3,1` y el estado meta `1,2,3,4`.
4. Haz clic en **Iniciar Comparador Paralelo**.
5. Analiza la gráfica resultante. Observa qué algoritmo resuelve el puzzle con la menor cantidad de pasos y cuál lo hace en el menor tiempo computacional.
