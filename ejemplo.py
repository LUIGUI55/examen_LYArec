# Vuelos con busqueda en amplitud 
from BFS import estado_inicial
from arbol import Nodo

def Buscar_solucion_BFS(conexiones,estado_inicial,solucion,Estado_final):
    solucionado = False
    nodos_visitados = []
    nodos_fonrtera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while (not solucionado and len(nodos_frontera) != 0):
        nodo = nodos_fonrtera.pop(0)
        # vamos a exteaer el nodo y anadirlo a visitados
        nodos_visitados.append(nodo)
        # si el nodo es la solucion
        if nodo.get_datos() == solucion:
            solucionado = True
        else:
            # expandir los nodos hijo que en nuestro caso se llaman ciudades con conexion
            ciudades = conexiones[nodo.get_datos()]
            for una_ciudad in ciudades:
                hijo = Nodo(una_ciudad, nodo)
                if not hijo.en_lista(nodos_visitados):
                    nodo_frontera.append(hijo)
    return nodo_solucion

if _name__ == "__main__":
    conexiones = {
        'Jilotepec': {'CELAYA','CDMX','Queretaro'},
        'Sonora':{'Zacatecas','Sinaloa'},
        'Guanajuato':{'Aguascalientes'},
        'Oaxaca':{'Queretaro'},
        'Sinaloa':{'Celaya','Sonora','jilotepec'},
        'Queretaro':{'Monterrey'},
        'Celaya':{'Jilotepec','Sinaloa'},
        'Zacatecas':{'Sonora','Monterrey','Queretaro'},
        'Monterrey':{'Zacatecas','Sinaloa'},
        'Tamaulipas':{'Queretaro'},
        'CDMX':{'Tamaulipas','Zacatecas','Sinaloa',\
            'Jilotepec','Oaxaca'}
    }
    estado_inicial = 'Jilotepec'
    solucion = 'Zacatecas'
    nodo_solucion = Buscar_solucion_BFS(conexiones,estado_inicial,solucion)

    #mostrar resultado
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_padre())
            nodo = nodo.get_padre()
        resultado.reverse()
        print("Ruta encontrada:")
        print(" -> ".join(resultado))
    