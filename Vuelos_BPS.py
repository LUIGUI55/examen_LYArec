# Vuelos con busqueda en amplitud 
from arbol import Nodo

# Normalizamos las conexiones para que todas estén en mayúsculas
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
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    
    # Normalizar entradas
    estado_inicial = estado_inicial.upper()
    solucion = solucion.upper()

    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado and len(nodos_frontera) != 0):
        nodo = nodos_frontera.pop(0)
        # vamos a exteaer el nodo y anadirlo a visitados
        nodos_visitados.append(nodo)
        # si el nodo es la solucion
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo
        else:
            # expandir los nodos hijo que en nuestro caso se llaman ciudades con conexion
            dato_nodo = nodo.get_datos()
            if dato_nodo in conexiones:
                ciudades = conexiones[dato_nodo]
                for una_ciudad in ciudades:
                    hijo = Nodo(una_ciudad, nodo)
                    if not hijo.en_lista(nodos_visitados) and not hijo.en_lista(nodos_frontera):
                        nodos_frontera.append(hijo)
    return None

if __name__ == "__main__":
    estado_inicial = 'Jilotepec'
    solucion = 'Zacatecas'
    nodo_solucion = Buscar_solucion_BFS(conexiones_b, estado_inicial, solucion)

    #mostrar resultado
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print("Ruta encontrada:")
        print(" -> ".join(resultado))
    else:
        print("No se encontró ruta.")