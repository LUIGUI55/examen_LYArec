from arbol import Nodo

def buscar_solucion_DFS_rec(estado_inicial, solucion, visitados=None):
    if visitados is None:
        visitados = []
        nodo_inicial = Nodo(estado_inicial)
    else:
        nodo_inicial = estado_inicial # In recursive calls, the first arg is already a Nodo

    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        # Expandir los nodos sucesores (hijos)
        dato_nodo = nodo_inicial.get_datos()
        hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izq = Nodo(hijo)
            
        # Operador medio
        hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_medio = Nodo(hijo)

        # Operador derecho
        hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_der = Nodo(hijo)

        nodo_inicial.set_hijos([hijo_izq, hijo_medio, hijo_der])

    for nodo_hijo in nodo_inicial.get_hijos():
        if not nodo_hijo.get_datos() in visitados:
            # Llamada recursiva
            S = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if S != None:
                return S
        
    return None

if __name__ == "__main__":
    estado_inicial = [4,2,3,1]
    solucion = [1,2,3,4]
    nodo = buscar_solucion_DFS_rec(estado_inicial, solucion)
    # Mostrar resultado 
    resultado = []
    if nodo:
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()

        resultado.append(estado_inicial)
        resultado.reverse()
        print(resultado)
    else:
        print("No solution found")
        
