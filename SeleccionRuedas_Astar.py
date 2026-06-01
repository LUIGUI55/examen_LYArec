# -*- coding: utf-8 -*-
"""
Módulo para resolver el problema de Selección de Ruedas utilizando búsqueda A*.
Reutiliza la clase Nodo del archivo arbol.py como en el resto de prácticas de la materia.
"""

from arbol import Nodo

# Variables globales para ruedas y fabricantes
TIPOS_RUEDA = ['t', 'h', 'v', 'w']
EMPRESAS = ['Empresa 1', 'Empresa 2', 'Empresa 3', 'Empresa 4']

# Matriz de costos por defecto del enunciado
MATRIZ_DEFECTO = {
    'Empresa 1': {'t': 20, 'h': 30, 'v': 20, 'w': 40},
    'Empresa 2': {'t': 50, 'h': 50, 'v': 40, 'w': 50},
    'Empresa 3': {'t': 60, 'h': 55, 'v': 50, 'w': 60},
    'Empresa 4': {'t': 100, 'h': 80, 'v': 60, 'w': 70}
}

def calcular_h(estado, matriz):
    """
    Calcula la heurística admisible h(n):
    Suma de los precios más bajos de los tipos de rueda aún no asignados,
    tomando solo aquellas empresas que no han sido adjudicadas aún.
    """
    # Encontrar qué empresas ya tienen asignada alguna rueda en este estado
    empresas_asignadas = set()
    for emp in estado:
        if emp is not None:
            empresas_asignadas.add(emp)
            
    # Filtrar empresas que quedan disponibles
    empresas_libres = []
    for emp in EMPRESAS:
        if emp not in empresas_asignadas:
            empresas_libres.append(emp)
            
    h_total = 0
    detalles = []
    
    # Si ya no hay empresas libres, la estimación es 0
    if not empresas_libres:
        return 0, []
        
    # Para cada rueda que falte por asignar, buscamos el costo mínimo en las empresas libres
    for i in range(len(TIPOS_RUEDA)):
        if estado[i] is None:  # Rueda no asignada aún
            tipo_rueda = TIPOS_RUEDA[i]
            precio_min = float('inf')
            empresa_min = None
            
            for emp in empresas_libres:
                precio = matriz[emp][tipo_rueda]
                if precio < precio_min:
                    precio_min = precio
                    empresa_min = emp
            
            if empresa_min is not None:
                h_total += precio_min
                detalles.append({
                    'wheel': tipo_rueda,
                    'min_price': precio_min,
                    'company': empresa_min
                })
                
    return h_total, detalles

def resolver_seleccion_ruedas(matriz=None):
    """
    Busca la solución óptima usando el algoritmo A*.
    Devuelve los datos de la solución y una traza de ejecución paso a paso.
    """
    if matriz is None:
        matriz = MATRIZ_DEFECTO
        
    id_contador = 0
    
    # Estado inicial: una lista con 4 posiciones sin asignar [None, None, None, None]
    estado_inicial = [None, None, None, None]
    
    # Crear el nodo raíz usando la clase Nodo del proyecto
    nodo_raiz = Nodo(estado_inicial)
    nodo_raiz.set_costo(0)  # g(raiz) = 0
    
    # Añadimos atributos auxiliares al objeto nodo para el algoritmo A*
    nodo_raiz.id = f"n{id_contador}"
    id_contador += 1
    
    h_raiz, h_detalles_raiz = calcular_h(estado_inicial, matriz)
    nodo_raiz.h = h_raiz
    nodo_raiz.h_detalles = h_detalles_raiz
    nodo_raiz.f = nodo_raiz.get_costo() + nodo_raiz.h
    nodo_raiz.depth = 0
    
    # Listas de la búsqueda A*
    frontera = [nodo_raiz]
    visitados = []
    pasos = []
    
    nodo_solucion = None
    paso_num = 0
    
    # Función de ayuda para convertir el objeto Nodo a un diccionario (JSON) para JS
    def nodo_a_dict(nodo):
        return {
            'id': nodo.id,
            'state': nodo.get_datos(),
            'parent_id': nodo.get_padre().id if nodo.get_padre() else None,
            'g': nodo.get_costo(),
            'h': nodo.h,
            'f': nodo.f,
            'depth': nodo.depth,
            'h_details': nodo.h_detalles
        }
        
    while len(frontera) > 0:
        paso_num += 1
        
        # Ordenar frontera por f(n) (costo estimado total). 
        # Si f es igual, elegimos el de mayor profundidad (más avanzado en la búsqueda)
        frontera.sort(key=lambda x: (x.f, -x.depth))
        
        # Extraer el nodo con menor f(n)
        nodo_actual = frontera.pop(0)
        visitados.append(nodo_actual)
        
        # Registrar el estado actual de la búsqueda en este paso
        registro_paso = {
            'step_number': paso_num,
            'expanded_node': nodo_a_dict(nodo_actual),
            'children': [],
            'frontier': [nodo_a_dict(n) for n in frontera],
            'explored': [nodo_a_dict(n) for n in visitados]
        }
        
        # Si la profundidad es 4, ya asignamos las 4 ruedas. ¡Solución encontrada!
        if nodo_actual.depth == 4:
            nodo_solucion = nodo_actual
            pasos.append(registro_paso)
            break
            
        # Determinar el tipo de rueda a asignar en este nivel (0=t, 1=h, 2=v, 3=w)
        rueda_por_asignar = TIPOS_RUEDA[nodo_actual.depth]
        
        # Ver qué empresas no han sido asignadas en el camino hasta nodo_actual
        empresas_ocupadas = set(emp for emp in nodo_actual.get_datos() if emp is not None)
        empresas_disponibles = [emp for emp in EMPRESAS if emp not in empresas_ocupadas]
        
        hijos_nodos = []
        for emp in empresas_disponibles:
            # Crear nuevo estado haciendo la asignación
            nuevo_estado = list(nodo_actual.get_datos())
            nuevo_estado[nodo_actual.depth] = emp
            
            # Crear nodo hijo
            nodo_hijo = Nodo(nuevo_estado, padre=nodo_actual)
            nodo_hijo.id = f"n{id_contador}"
            id_contador += 1
            
            # g(hijo) = g(padre) + costo de asignar esta empresa a la rueda actual
            costo_g = nodo_actual.get_costo() + matriz[emp][rueda_por_asignar]
            nodo_hijo.set_costo(costo_g)
            
            # h(hijo) y f(hijo)
            h_hijo, h_detalles_hijo = calcular_h(nuevo_estado, matriz)
            nodo_hijo.h = h_hijo
            nodo_hijo.h_detalles = h_detalles_hijo
            nodo_hijo.f = costo_g + h_hijo
            nodo_hijo.depth = nodo_actual.depth + 1
            
            hijos_nodos.append(nodo_hijo)
            
            # Verificar si este estado ya fue visitado
            ya_visitado = False
            for v in visitados:
                if v.get_datos() == nuevo_estado:
                    ya_visitado = True
                    break
                    
            if not ya_visitado:
                # Verificar si ya está en frontera
                en_frontera_idx = -1
                for idx, f_node in enumerate(frontera):
                    if f_node.get_datos() == nuevo_estado:
                        en_frontera_idx = idx
                        break
                        
                if en_frontera_idx == -1:
                    frontera.append(nodo_hijo)
                else:
                    # Si el nuevo camino es más barato, actualizamos
                    if frontera[en_frontera_idx].get_costo() > costo_g:
                        frontera.pop(en_frontera_idx)
                        frontera.append(nodo_hijo)
                        
        nodo_actual.set_hijos(hijos_nodos)
        registro_paso['children'] = [nodo_a_dict(n) for n in hijos_nodos]
        registro_paso['frontier_after'] = [nodo_a_dict(n) for n in frontera]
        
        pasos.append(registro_paso)
        
    # Reconstruir camino de la solución óptima
    camino = []
    if nodo_solucion is not None:
        n = nodo_solucion
        while n is not None:
            camino.append(nodo_a_dict(n))
            n = n.get_padre()
        camino.reverse()
        
    return {
        'success': nodo_solucion is not None,
        'path': camino,
        'steps': pasos,
        'total_cost': nodo_solucion.get_costo() if nodo_solucion else 0,
        'total_nodes_generated': id_contador
    }

if __name__ == "__main__":
    res = resolver_seleccion_ruedas()
    print("Exito:", res['success'])
    print("Costo Optimo:", res['total_cost'])
    print("Camino:")
    for step in res['path']:
        print("  Estado:", step['state'], "g =", step['g'], "h =", step['h'], "f =", step['f'])
