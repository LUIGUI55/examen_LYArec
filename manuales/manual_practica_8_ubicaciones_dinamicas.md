# Manual de Práctica 8: Generación Dinámica de Ubicaciones en el Grafo

## 1. Objetivo
Permitir a los usuarios extender la red de búsqueda en tiempo real, registrando de forma interactiva nuevas ubicaciones con sus coordenadas (latitud/longitud), distancias de conexión o generando automáticamente ciudades reales mexicanas mediante un botón de autocompletado aleatorio.

## 2. Fundamento Teórico
Los grafos estáticos en algoritmos de inteligencia artificial limitan la escalabilidad del sistema. Modificar dinámicamente el espacio de estados en tiempo de ejecución (runtime) requiere de APIs seguras que inyecten nuevos nodos y aristas (conexiones ponderadas) en las variables globales cargadas en memoria del servidor web, y actualicen instantáneamente la UI del cliente sin requerir un reinicio del sistema.

## 3. Estructura del Código

### Backend (APIs en `app.py` modificando variables globales)
```python
# app.py (Inyección dinámica)
import random

RANDOM_CITIES_POOL = [
    {"name": "Guadalajara", "lat": 20.671956, "lon": -103.348822},
    {"name": "Puebla", "lat": 19.04144, "lon": -98.20627},
    # ... pool de ciudades reales
]

@app.route('/api/add_location', methods=['POST'])
def add_location():
    data = request.json
    raw_name = data.get('name', '').strip()
    lat = float(data.get('lat'))
    lon = float(data.get('lon'))
    weight = int(data.get('weight'))
    connected_to = data.get('connected_to', '').strip()
    
    # Agregar a Carretera_Astar (Coordenadas y conexiones bidireccionales)
    name_astar = raw_name.capitalize()
    Carretera_Astar.coord[name_astar] = (lat, lon)
    if name_astar not in Carretera_Astar.conexiones:
        Carretera_Astar.conexiones[name_astar] = {}
    Carretera_Astar.conexiones[name_astar][connected_to] = weight
    Carretera_Astar.conexiones[connected_to][name_astar] = weight

    # Retorna las ciudades actualizadas para refrescar la interfaz
    all_cities = sorted(list(Carretera_Astar.coord.keys()))
    return jsonify({'success': True, 'cities': all_cities})
```

### Frontend (`templates/carretera_astar.html` - Segmento de autocompletado)
```javascript
// Autocompletado desde el cliente
document.getElementById('randomLocationBtn').onclick = () => {
    // Escoge una ciudad del pool disponible que no se repita
    const chosen = poolCities[Math.floor(Math.random() * poolCities.length)];
    
    document.getElementById('new-name').value = chosen.name.toUpperCase();
    document.getElementById('new-lat').value = chosen.lat;
    document.getElementById('new-lon').value = chosen.lon;
    document.getElementById('new-weight').value = Math.floor(Math.random() * 500) + 150;
};
```

## 4. Guía de Ejecución y Pruebas
1. Inicia el servidor (`python app.py`).
2. Entra a `http://localhost:5000/carretera-astar` o `/carretera-ucs`.
3. Dirígete a la tarjeta inferior **Añadir Nueva Ubicación**.
4. Haz clic en **Generar Ubicación Aleatoria**. Observa cómo los campos de Latitud, Longitud, Nombre y Peso de conexión se autocompletan de manera coherente con datos geográficos reales de México.
5. Selecciona la ciudad a la cual deseas enlazar este nuevo nodo y presiona **Añadir Ubicación**.
6. Sube al formulario de rutas y comprueba que la nueva ubicación ahora está disponible en las opciones y participa activamente en los cálculos del algoritmo.
