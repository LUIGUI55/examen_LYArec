from arbol import Nodo
import heapq

def heuristic(estado, estado_final):
    # Heurística de piezas fuera de lugar
    distancia = 0
    for i in range(len(estado)):
        if estado[i] != estado_final[i]:
            distancia += 1
    return distancia

def buscar_solucion_heuristica(nodo_inicial, estado_final):
    visitados = set()
    
    # Priority Queue: (prioridad, contador_unico, nodo)
    # El contador es para desempatar si dos nodos tienen la misma prioridad
    counter = 0
    prioridad_inicial = heuristic(nodo_inicial.get_datos(), estado_final)
    queue = [(prioridad_inicial, counter, nodo_inicial)]
    
    visitados.add(tuple(nodo_inicial.get_datos()))
    
    while queue:
        # Extraer el nodo con menor valor heurístico
        prioridad, _, nodo_actual = heapq.heappop(queue)
        
        if nodo_actual.get_datos() == estado_final:
            return nodo_actual
        
        # Expandir los nodos
        dato_nodo = nodo_actual.get_datos()
        
        # Generar posibles hijos (Swaps adyacentes)
        hijos_datos = [
            [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]], # swap 0-1
            [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]], # swap 1-2
            [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]  # swap 2-3
        ]

        lista_hijos = []
        for h_dato in hijos_datos:
            if tuple(h_dato) not in visitados:
                visitados.add(tuple(h_dato))
                hijo_nodo = Nodo(h_dato, padre=nodo_actual)
                lista_hijos.append(hijo_nodo)
                
                # Calcular heurística para el nuevo nodo
                h_val = heuristic(h_dato, estado_final)
                counter += 1
                heapq.heappush(queue, (h_val, counter, hijo_nodo))
        
        nodo_actual.set_hijos(lista_hijos)
        
    return None

if __name__ == "__main__":
    # El estado [4, 3, 2, 1] requiere exactamente 6 pasos para llegar a [1, 2, 3, 4]
    estado_inicial = [4, 3, 2, 1]
    estado_final = [1, 2, 3, 4]
    
    nodo_inicial = Nodo(estado_inicial)
    solucion = buscar_solucion_heuristica(nodo_inicial, estado_final)
    
    if solucion is not None:
        print("Solución encontrada:")
        resultado = []
        nodo = solucion
        while nodo is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.reverse()
        print(resultado)
        print(f"Número de pasos: {len(resultado) - 1}")
    else:
        print("No se encontró solución")