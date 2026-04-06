# puzzle lineal con busqueda en profundidad(DFS)
from arbol import Nodo
def buscar_solucion_DFS(estado_inicial, solucion):
    solucionado = False 
    nodos_visitados = []
    nodos_frontera = []
    nodoInicial = Nodo(estado_inicial)
    nodos_frontera.append(nodoInicial)
    while(not solucionado and len(nodos_frontera) != 0):
        # En DFS sacamos el último agregado a la frontera (Pila)
        nodo = nodos_frontera.pop()
        # Extraer el nodo y añadirlo a visitados
        nodos_visitados.append(nodo)
        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo 
        else:
            # Expandir nodos Hijo
            dato_nodo = nodo.get_datos()
            
            # Operador izquierdo (intercambia índices 0 y 1)
            hijo_izq = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            nodo_izquierdo = Nodo(hijo_izq, padre=nodo)
            if not nodo_izquierdo.en_lista(nodos_visitados) and not nodo_izquierdo.en_lista(nodos_frontera):
                nodos_frontera.append(nodo_izquierdo)
            
            # Operador central (intercambia índices 1 y 2)
            hijo_cen = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            nodo_central = Nodo(hijo_cen, padre=nodo)
            if not nodo_central.en_lista(nodos_visitados) and not nodo_central.en_lista(nodos_frontera):
                nodos_frontera.append(nodo_central)
                
            # Operador derecho (intercambia índices 2 y 3)
            hijo_der = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            nodo_derecho = Nodo(hijo_der, padre=nodo)
            if not nodo_derecho.en_lista(nodos_visitados) and not nodo_derecho.en_lista(nodos_frontera):
                nodos_frontera.append(nodo_derecho)
                
    return None

if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    
    print(f"Buscando solucion para: {estado_inicial} -> {solucion} usando DFS...")
    nodo_solucion = buscar_solucion_DFS(estado_inicial, solucion)

    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None: 
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print(f"Ruta encontrada en {len(resultado)-1} pasos:")
        for r in resultado:
            print(r)
    else:
        print("No se encontró solución.")
