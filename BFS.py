from arbol import Nodo

# Grafo ponderado con las ciudades de México solicitadas (distancias relativas en KM o Costos)
conexiones = {
    'CDMX': {'MORELOS': 85, 'HIDALGO': 90, 'QUERETARO': 210, 'JILOTEPEC': 100},
    'JILOTEPEC': {'CDMX': 100, 'HIDALGO': 80, 'QUERETARO': 110},
    'HIDALGO': {'CDMX': 90, 'JILOTEPEC': 80, 'SLP': 300, 'QUERETARO': 200, 'TAMAULIPAS': 450},
    'QUERETARO': {'CDMX': 210, 'JILOTEPEC': 110, 'HIDALGO': 200, 'SLP': 200, 'GDL': 350},
    'MORELOS': {'CDMX': 85},
    'SLP': {'HIDALGO': 300, 'QUERETARO': 200, 'ZACATECAS': 190, 'MONTERREY': 500, 'TAMAULIPAS': 350},
    'ZACATECAS': {'SLP': 190, 'GDL': 320, 'MONTERREY': 460},
    'GDL': {'QUERETARO': 350, 'ZACATECAS': 320},
    'MONTERREY': {'SLP': 500, 'ZACATECAS': 460, 'TAMAULIPAS': 280},
    'TAMAULIPAS': {'SLP': 350, 'MONTERREY': 280, 'HIDALGO': 450}
}

def buscar_solucion_BFS_grafo(grafo, estado_inicial, solucion):
    # Implementación de BFS / Dijkstra sobre grafo de entrada
    nodos_visitados = []
    nodos_frontera = []
    
    nodoInicial = Nodo(estado_inicial)
    nodoInicial.set_costo(0)
    nodos_frontera.append(nodoInicial)

    if estado_inicial == solucion:
        return nodoInicial

    while len(nodos_frontera) != 0:
        nodos_frontera.sort(key=lambda x: x.costo)
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()
        if dato_nodo in grafo:
            hijos_datos = grafo[dato_nodo]
        else:
            hijos_datos = {}

        for un_hijo, peso in hijos_datos.items():
            hijo = Nodo(un_hijo, padre=nodo)
            costo_acumulado = nodo.costo + peso
            hijo.set_costo(costo_acumulado)

            if not hijo.en_lista(nodos_visitados):
                agregado = False
                for n in nodos_frontera:
                    if n.get_datos() == un_hijo:
                        if hijo.costo < n.costo:
                            n.set_costo(hijo.costo)
                            n.set_padre(nodo)
                        agregado = True
                        break

                if not agregado:
                    nodos_frontera.append(hijo)

    return None


def buscar_solucion_BFS(estado_inicial, solucion):
    return buscar_solucion_BFS_grafo(conexiones, estado_inicial, solucion)


if __name__ == "__main__":
    estado_inicial = 'CDMX'
    solucion = 'MONTERREY'
    
    print(f"Buscando solucion para ir de {estado_inicial} a {solucion} con pesos...")
    nodo_solucion = buscar_solucion_BFS(estado_inicial, solucion)

    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        coste_total = nodo.costo
        while nodo is not None: 
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print("Ruta encontrada:")
        print(" -> ".join(resultado))
        print(f"Costo Total: {coste_total}")
    else:
        print("No se encontró solución.")
