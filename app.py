from flask import Flask, render_template, request, jsonify
from BFS import buscar_solucion_BFS, buscar_solucion_BFS_grafo, conexiones
from DFS import buscar_solucion_DFS
from dfs_rec import buscar_solucion_DFS_rec
from DFS_Iteractiva import buscar_solucion_DFS_iter
from puzzleLinealHeuistico import buscar_solucion_heuristica, Nodo as NodoHeuristico
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import Vuelos_BPI
import Vuelos_BPS
import Carretera_UCS
import Carretera_Astar
from dfs_backtraking import buscar_mejor_valor_backtracking
from arbol import Nodo

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bfs')
def bfs_ciudades():
    cities = sorted(list(conexiones.keys()))
    return render_template('bfs.html', cities=cities)

@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.json
    origen = data.get('origen')
    destino = data.get('destino')
    
    if not origen or not destino:
        return jsonify({'error': 'Faltan parámetros de origen o destino', 'success': False}), 400
        
    nodo_solucion = buscar_solucion_BFS(origen.strip().upper(), destino.strip().upper())
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        costo_total = nodo.costo
        while nodo is not None: 
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'cost': costo_total, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución de ruta', 'success': False})

@app.route('/vuelos')
def vuelos():
    all_cities = set()
    for origen, destinos in Vuelos_BPS.conexiones_b.items():
        all_cities.add(origen)
        all_cities.update(destinos)
    cities = sorted(list(all_cities))
    return render_template('vuelos.html', cities=cities)

@app.route('/api/solve_secuencial', methods=['POST'])
def solve_secuencial():
    data = request.json
    nodos = data.get('nodos')
    
    if not nodos or len(nodos) < 2:
        return jsonify({'error': 'Se requieren al menos dos ciudades.', 'success': False}), 400
        
    path_total = []
    
    for i in range(len(nodos) - 1):
        origen = nodos[i]
        destino = nodos[i+1]
        nodo_solucion = Vuelos_BPS.Buscar_solucion_BFS(Vuelos_BPS.conexiones_b, origen, destino)
        
        if nodo_solucion:
            resultado = []
            nodo = nodo_solucion
            while nodo is not None:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
            
            if i == 0:
                path_total.extend(resultado)
            else:
                path_total.extend(resultado[1:])
        else:
            return jsonify({'error': f'No se encontró ruta entre {origen} y {destino}.', 'success': False})
            
    return jsonify({'path': path_total, 'success': True})

@app.route('/carretera-ucs')
def carretera_ucs():
    all_cities = set()
    for origen, destinos in Carretera_UCS.conexiones.items():
        all_cities.add(origen)
        all_cities.update(destinos)
    cities = sorted(list(all_cities))
    return render_template('carretera_ucs.html', cities=cities)

@app.route('/api/solve_carretera_ucs', methods=['POST'])
def solve_carretera_ucs():
    data = request.json
    nodos = data.get('nodos')
    
    if not nodos:
        origen = data.get('origen')
        destino = data.get('destino')
        if origen and destino:
            nodos = [origen, destino]
            
    if not nodos or len(nodos) < 2:
        return jsonify({'error': 'Se requieren al menos dos ciudades.', 'success': False}), 400
        
    path_total = []
    costo_total = 0
    
    for i in range(len(nodos) - 1):
        sub_origen = nodos[i]
        sub_destino = nodos[i+1]
        
        nodo_solucion = Carretera_UCS.buscar_solucion_UCS(sub_origen, sub_destino)
        
        if nodo_solucion:
            resultado = []
            nodo = nodo_solucion
            sub_costo = nodo.costo
            costo_total += sub_costo
            while nodo:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
            
            if i == 0:
                path_total.extend(resultado)
            else:
                path_total.extend(resultado[1:])
        else:
            return jsonify({'error': f'No se encontró una ruta óptima entre {sub_origen} y {sub_destino}.', 'success': False})
            
    return jsonify({'path': path_total, 'cost': costo_total, 'success': True})

@app.route('/api/add_location', methods=['POST'])
def add_location():
    data = request.json
    raw_name = data.get('name', '').strip()
    try:
        lat = float(data.get('lat'))
        lon = float(data.get('lon'))
        weight = int(data.get('weight'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Parámetros numéricos inválidos.', 'success': False}), 400
        
    connected_to = data.get('connected_to', '').strip()
    req_type = data.get('type', 'astar')
    
    if not raw_name or not connected_to:
        return jsonify({'error': 'Faltan parámetros requeridos.', 'success': False}), 400
        
    # Definir nombres para A* (preserva mayúsculas/minúsculas)
    name_astar = raw_name[0].upper() + raw_name[1:] if len(raw_name) > 0 else raw_name
    conn_astar = connected_to
    
    # Definir nombres para UCS (siempre en mayúsculas)
    name_ucs = raw_name.upper()
    conn_ucs = connected_to.upper()
    
    # Validar si ya existe en A* o UCS
    if name_astar in Carretera_Astar.coord or name_ucs in Carretera_UCS.conexiones:
        return jsonify({'error': 'La ubicación ya existe.', 'success': False}), 400
        
    # Agregar a Carretera_Astar (Coordenadas y conexiones)
    Carretera_Astar.coord[name_astar] = (lat, lon)
    if name_astar not in Carretera_Astar.conexiones:
        Carretera_Astar.conexiones[name_astar] = {}
    Carretera_Astar.conexiones[name_astar][conn_astar] = weight
    
    if conn_astar not in Carretera_Astar.conexiones:
        Carretera_Astar.conexiones[conn_astar] = {}
    Carretera_Astar.conexiones[conn_astar][name_astar] = weight
    
    # Agregar a Carretera_UCS (conexiones)
    if name_ucs not in Carretera_UCS.conexiones:
        Carretera_UCS.conexiones[name_ucs] = {}
    Carretera_UCS.conexiones[name_ucs][conn_ucs] = weight
    
    if conn_ucs not in Carretera_UCS.conexiones:
        Carretera_UCS.conexiones[conn_ucs] = {}
    Carretera_UCS.conexiones[conn_ucs][name_ucs] = weight
    
    # Devolver la lista correspondiente según el origen de la petición
    if req_type == 'ucs':
        all_cities = set()
        for origen, destinos in Carretera_UCS.conexiones.items():
            all_cities.add(origen)
            all_cities.update(destinos)
        cities = sorted(list(all_cities))
    else:
        all_cities = set()
        for origen, destinos in Carretera_Astar.conexiones.items():
            all_cities.add(origen)
            all_cities.update(destinos)
        cities = sorted(list(all_cities))
        
    return jsonify({'success': True, 'cities': cities})

@app.route('/carretera-astar')
def carretera_astar():
    all_cities = set()
    for origen, destinos in Carretera_Astar.conexiones.items():
        all_cities.add(origen)
        all_cities.update(destinos)
    cities = sorted(list(all_cities))
    return render_template('carretera_astar.html', cities=cities)

@app.route('/api/solve_carretera_astar', methods=['POST'])
def solve_carretera_astar():
    data = request.json
    nodos = data.get('nodos')
    
    if not nodos:
        origen = data.get('origen')
        destino = data.get('destino')
        if origen and destino:
            nodos = [origen, destino]
            
    if not nodos or len(nodos) < 2:
        return jsonify({'error': 'Se requieren al menos dos ciudades.', 'success': False}), 400
        
    path_total = []
    costo_total = 0
    
    for i in range(len(nodos) - 1):
        sub_origen = nodos[i]
        sub_destino = nodos[i+1]
        
        nodo_solucion = Carretera_Astar.buscar_solucion_USC(Carretera_Astar.conexiones, sub_origen, sub_destino)
        
        if nodo_solucion:
            resultado = []
            nodo = nodo_solucion
            sub_costo = nodo.get_costo()
            costo_total += sub_costo
            while nodo:
                resultado.append(nodo.get_datos())
                nodo = nodo.get_padre()
            resultado.reverse()
            
            if i == 0:
                path_total.extend(resultado)
            else:
                path_total.extend(resultado[1:])
        else:
            return jsonify({'error': f'No se encontró una ruta óptima entre {sub_origen} y {sub_destino}.', 'success': False})
            
    return jsonify({'path': path_total, 'cost': costo_total, 'success': True})

@app.route('/vuelos-bpi')
def vuelos_bpi():
    all_cities = set()
    for origen, destinos in Vuelos_BPI.conexiones.items():
        all_cities.add(origen)
        all_cities.update(destinos)
    cities = sorted(list(all_cities))
    return render_template('vuelos_bpi.html', cities=cities)

@app.route('/api/solve_vuelos_bpi', methods=['POST'])
def solve_vuelos_bpi():
    data = request.json
    origen = data.get('origen')
    destino = data.get('destino')
    
    if not origen or not destino:
        return jsonify({'error': 'Faltan parámetros de origen o destino', 'success': False}), 400
        
    nodo_inicial = Vuelos_BPI.Nodo(origen)
    nodo_solucion = Vuelos_BPI.DFS_prof_iter(nodo_inicial, destino)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None: 
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución de ruta con profundidad iterativa', 'success': False})

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html')

@app.route('/puzzle-recursive')
def puzzle_recursive():
    return render_template('puzzle-recursive.html')

@app.route('/api/solve_puzzle_recursive', methods=['POST'])
def solve_puzzle_recursive():
    data = request.json
    estado_inicial = data.get('estado_inicial')
    solucion = data.get('solucion')
    
    if not estado_inicial or not solucion or len(estado_inicial) != 4 or len(solucion) != 4:
        return jsonify({'error': 'Se requieren arreglos de 4 elementos para origen y meta.', 'success': False}), 400
    
    try:
        estado_inicial = [int(x) for x in estado_inicial]
        solucion = [int(x) for x in solucion]
    except ValueError:
        return jsonify({'error': 'Los elementos deben ser números enteros.', 'success': False}), 400
        
    nodo_solucion = buscar_solucion_DFS_rec(estado_inicial, solucion)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución (o límite de recursión alcanzado).', 'success': False})

@app.route('/puzzle-iterative')
def puzzle_iterative():
    return render_template('puzzle-iterative.html')

@app.route('/api/solve_puzzle_iterative', methods=['POST'])
def solve_puzzle_iterative():
    data = request.json
    estado_inicial = data.get('estado_inicial')
    solucion = data.get('solucion')
    
    if not estado_inicial or not solucion or len(estado_inicial) != 4 or len(solucion) != 4:
        return jsonify({'error': 'Se requieren arreglos de 4 elementos para origen y meta.', 'success': False}), 400
    
    try:
        estado_inicial = [int(x) for x in estado_inicial]
        solucion = [int(x) for x in solucion]
    except ValueError:
        return jsonify({'error': 'Los elementos deben ser números enteros.', 'success': False}), 400
        
    nodo_solucion = buscar_solucion_DFS_iter(estado_inicial, solucion)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución.', 'success': False})

@app.route('/puzzle-premium')
def puzzle_premium():
    return render_template('puzzle-premium.html')

@app.route('/api/solve_puzzle', methods=['POST'])
def solve_puzzle():
    data = request.json
    estado_inicial = data.get('estado_inicial')
    solucion = data.get('solucion')
    
    if not estado_inicial or not solucion or len(estado_inicial) != 4 or len(solucion) != 4:
        return jsonify({'error': 'Se requieren arreglos de 4 elementos para origen y meta.', 'success': False}), 400
    
    # Conversión a enteros en caso de que vengan como strings
    try:
        estado_inicial = [int(x) for x in estado_inicial]
        solucion = [int(x) for x in solucion]
    except ValueError:
        return jsonify({'error': 'Los elementos deben ser números enteros.', 'success': False}), 400
        
    nodo_solucion = buscar_solucion_DFS(estado_inicial, solucion)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución (quizás es imposible de resolver).', 'success': False})

@app.route('/puzzle-heuristico')
def puzzle_heuristico():
    return render_template('puzzle-heuristico.html')

@app.route('/api/solve_puzzle_heuristico', methods=['POST'])
def solve_puzzle_heuristico():
    data = request.json
    estado_inicial = data.get('estado_inicial')
    solucion = data.get('solucion')
    
    if not estado_inicial or not solucion or len(estado_inicial) != 4 or len(solucion) != 4:
        return jsonify({'error': 'Se requieren arreglos de 4 elementos para origen y meta.', 'success': False}), 400
    
    try:
        estado_inicial = [int(x) for x in estado_inicial]
        solucion = [int(x) for x in solucion]
    except ValueError:
        return jsonify({'error': 'Los elementos deben ser números enteros.', 'success': False}), 400
        
    nodo_inicial = NodoHeuristico(estado_inicial)
    nodo_solucion = buscar_solucion_heuristica(nodo_inicial, solucion)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        return jsonify({'path': resultado, 'success': True})
    else:
        return jsonify({'error': 'No se encontró solución con la búsqueda heurística (Hill Climbing).', 'success': False})

@app.route('/backtracking')
def backtracking_view():
    return render_template('backtracking.html')

@app.route('/api/solve_backtracking', methods=['POST'])
def solve_backtracking_api():
    try:
        data = request.json
        rangos = data.get('rangos')
        beneficios = data.get('beneficios', [6, 4])
        limites = data.get('limites', [150, 160])
        coefs = data.get('coefs', [[7, 4], [6, 5]])
        
        if rangos:
            rangos = [[int(r[0]), int(r[1])] for r in rangos]
        
        beneficios = [float(b) for b in beneficios]
        limites = [float(l) for l in limites]
        coefs = [[float(c) for c in row] for row in coefs]
            
        resultado = buscar_mejor_valor_backtracking(rangos, beneficios, limites, coefs)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e), 'success': False})

# ─── COMPARADOR: 3 modelos en paralelo ───────────────────────────

def _run_heuristico(estado_inicial, solucion):
    start = time.perf_counter()
    nodo_inicial = NodoHeuristico(estado_inicial)
    nodo_sol = buscar_solucion_heuristica(nodo_inicial, solucion)
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    if nodo_sol:
        path = []
        n = nodo_sol
        while n is not None:
            path.append(n.get_datos())
            n = n.get_padre()
        path.reverse()
        return {'name': 'Heurístico (Hill Climbing)', 'success': True, 'path': path, 'steps': len(path) - 1, 'time_ms': elapsed}
    return {'name': 'Heurístico (Hill Climbing)', 'success': False, 'error': 'Sin solución', 'time_ms': elapsed}

def _run_iterativo(estado_inicial, solucion):
    start = time.perf_counter()
    nodo_sol = buscar_solucion_DFS_iter(estado_inicial, solucion)
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    if nodo_sol:
        path = []
        n = nodo_sol
        while n is not None:
            path.append(n.get_datos())
            n = n.get_padre()
        path.reverse()
        return {'name': 'Iterativo (IDDFS)', 'success': True, 'path': path, 'steps': len(path) - 1, 'time_ms': elapsed}
    return {'name': 'Iterativo (IDDFS)', 'success': False, 'error': 'Sin solución', 'time_ms': elapsed}

def _run_recursivo(estado_inicial, solucion):
    start = time.perf_counter()
    nodo_sol = buscar_solucion_DFS_rec(estado_inicial, solucion)
    elapsed = round((time.perf_counter() - start) * 1000, 3)
    if nodo_sol:
        path = []
        n = nodo_sol
        while n is not None:
            path.append(n.get_datos())
            n = n.get_padre()
        path.reverse()
        return {'name': 'Recursivo (DFS)', 'success': True, 'path': path, 'steps': len(path) - 1, 'time_ms': elapsed}
    return {'name': 'Recursivo (DFS)', 'success': False, 'error': 'Sin solución', 'time_ms': elapsed}

@app.route('/comparador')
def comparador():
    return render_template('comparador.html')

@app.route('/api/solve_parallel', methods=['POST'])
def solve_parallel():
    data = request.json
    estado_inicial = data.get('estado_inicial')
    solucion = data.get('solucion')

    if not estado_inicial or not solucion or len(estado_inicial) != 4 or len(solucion) != 4:
        return jsonify({'error': 'Se requieren arreglos de 4 elementos.', 'success': False}), 400
    try:
        estado_inicial = [int(x) for x in estado_inicial]
        solucion = [int(x) for x in solucion]
    except ValueError:
        return jsonify({'error': 'Los elementos deben ser enteros.', 'success': False}), 400

    total_start = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(_run_heuristico, list(estado_inicial), list(solucion)): 'heuristico',
            pool.submit(_run_iterativo, list(estado_inicial), list(solucion)): 'iterativo',
            pool.submit(_run_recursivo, list(estado_inicial), list(solucion)): 'recursivo',
        }
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({'name': futures[future], 'success': False, 'error': str(e), 'time_ms': 0})
    total_elapsed = round((time.perf_counter() - total_start) * 1000, 3)
    return jsonify({'success': True, 'results': results, 'total_time_ms': total_elapsed})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
