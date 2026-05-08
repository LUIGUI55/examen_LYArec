# viaje por carretera con busqueda de costo uniforme 
from arbol import Nodo

# Conexiones con sus costos
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
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)

    while len(nodos_frontera) > 0:
        # Ordenar por costo para obtener el menor (UCS)
        nodos_frontera = sorted(nodos_frontera, key=lambda x: x.costo)
        
        # Extraer el nodo con menor costo
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo.get_datos())
        
        if nodo.get_datos() == solucion:
            return nodo
        else:
            dato_nodo = nodo.get_datos()
            if dato_nodo in conexiones:
                lista_hijos = []
                for un_hijo, costo in conexiones[dato_nodo].items():
                    hijo = Nodo(un_hijo)
                    hijo.set_costo(nodo.costo + costo)
                    
                    if un_hijo not in nodos_visitados:
                        # Si ya está en la frontera, ver si el nuevo costo es menor
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

if __name__ == "__main__":
    origen = 'JILOYORK'
    destino = 'SLP'
    nodo_sol = buscar_solucion_UCS(origen, destino)
    if nodo_sol:
        resultado = []
        nodo = nodo_sol
        while nodo:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print(f"Ruta: {resultado}, Costo: {nodo_sol.costo}")
    else:
        print("No se encontró solución")
