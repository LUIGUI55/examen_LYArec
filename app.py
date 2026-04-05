from flask import Flask, render_template, request, jsonify
from BFS import buscar_solucion_BFS, buscar_solucion_BFS_grafo, conexiones
import os
import Vuelos_BPS

app = Flask(__name__)

@app.route('/')
def home():
    cities = sorted(list(conexiones.keys()))
    return render_template('index.html', cities=cities)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
