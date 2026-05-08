from arbol import Nodo

def buscar_solucion_DFS_iter(estado_inicial, solucion):
    for limite in range(0, 100):
        visitados = []
        nodo_inicial = Nodo(estado_inicial)
        sol = buscar_solucion_DFS_Rec(nodo_inicial, solucion, visitados, limite)
        if sol is not None:
            return sol
    return None

def buscar_solucion_DFS_Rec(nodo, solucion, visitados, limite):
    if limite >= 0:
        visitados.append(nodo.get_datos())
        
        if nodo.get_datos() == solucion:
            return nodo
        
        if limite > 0:
            # Expandir nodos sucesores
            dato_nodo = nodo.get_datos()
            
            # Operador izquierdo (intercambia 0 y 1)
            hijo_izq_datos = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
            hijo_izq = Nodo(hijo_izq_datos, padre=nodo)
            
            # Operador central (intercambia 1 y 2)
            hijo_cen_datos = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
            hijo_cen = Nodo(hijo_cen_datos, padre=nodo)
            
            # Operador derecho (intercambia 2 y 3)
            hijo_der_datos = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
            hijo_der = Nodo(hijo_der_datos, padre=nodo)
            
            hijos = [hijo_izq, hijo_cen, hijo_der]
            nodo.set_hijos(hijos)
            
            for nodo_hijo in nodo.get_hijos():
                if not nodo_hijo.get_datos() in visitados:
                    # Llamada recursiva con copia de visitados para permitir re-exploración en otras ramas
                    sol = buscar_solucion_DFS_Rec(nodo_hijo, solucion, list(visitados), limite - 1)
                    if sol is not None:
                        return sol
    return None

if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    
    print(f"Buscando solución para {estado_inicial} -> {solucion} usando IDDFS...")
    nodo_solucion = buscar_solucion_DFS_iter(estado_inicial, solucion)
    
    if nodo_solucion:
        resultado = []
        nodo = nodo_solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print(f"Solución encontrada en {len(resultado)-1} pasos:")
        for r in resultado:
            print(r)
    else:
        print("No se encontró solución.")
