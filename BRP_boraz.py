# creacion de un brp boraz
from Carretera_Astar import coord
import math
from operator import itemgetter

def distancia(coord1, coord2):
   lat1 = coord1[0]
   lon1 = coord1[1]
   lat2 = coord2[0]
   lon2 = coord2[1]
   return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

def en_ruta(rutas, cliente):
    ruta = None
    for n in rutas:
        if cliente in n:
            return n
    return ruta

def peso_ruta(ruta, pedidos):
    total = 0 
    for c in ruta:
        if c in pedidos:
            total = total + pedidos[c]
    return total

def vrp_voraz(pedidos, almacen, max_carga):
    # calcular los ahorros
    s={}
    clientes = list(pedidos.keys())
    for c1 in clientes:
        for c2 in clientes:
            if c1 != c2:
                if not (c1, c2) in s and not (c2, c1) in s:
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_almacen = distancia(coord[c1], coord[almacen])
                    d_c2_almacen = distancia(coord[c2], coord[almacen])
                    s[(c1, c2)] = d_c1_almacen + d_c2_almacen - d_c1_c2
    # ordenar los ahorros 
    s = sorted(s.items(), key=itemgetter(1), reverse=True)

    # Construir Rutas
    rutas = []
    pasos = [] # Log para el front
    for k,v in s:
        rc1 = en_ruta(rutas, k[0])
        rc2 = en_ruta(rutas, k[1])
        if rc1 == None and rc2 == None:
            # Regla 1: Si ni i ni j están en ninguna ruta, se crea una ruta con i y j.
            if peso_ruta([k[0], k[1]], pedidos) <= max_carga:
                rutas.append([k[0], k[1]])
                pasos.append(f"Regla 1: Como ni {k[0]} ni {k[1]} estaban en ruta, se creó una nueva con ambos (Ahorro: {v:.2f}).")
        elif rc1 != None and rc2 == None:
            # Regla 2: Si i o j están en una ruta (pero no las dos) y además es el primero o el ultimo cliente...
            if rc1[0] == k[0]:
                if peso_ruta(rc1, pedidos) + peso_ruta([k[1]], pedidos) <= max_carga:
                    rutas[rutas.index(rc1)].insert(0, k[1])
                    pasos.append(f"Regla 2: Se añadió {k[1]} al inicio de la ruta de {k[0]} (Ahorro: {v:.2f}).")
            elif rc1[-1] == k[0]:
                if peso_ruta(rc1, pedidos) + peso_ruta([k[1]], pedidos) <= max_carga:
                    rutas[rutas.index(rc1)].append(k[1])
                    pasos.append(f"Regla 2: Se añadió {k[1]} al final de la ruta de {k[0]} (Ahorro: {v:.2f}).")
        elif rc1 == None and rc2 != None:
            # Regla 2 equivalente para el otro extremo
            if rc2[0] == k[1]:
                if peso_ruta(rc2, pedidos) + peso_ruta([k[0]], pedidos) <= max_carga:
                    rutas[rutas.index(rc2)].insert(0, k[0])
                    pasos.append(f"Regla 2: Se añadió {k[0]} al inicio de la ruta de {k[1]} (Ahorro: {v:.2f}).")
            elif rc2[-1] == k[1]:
                if peso_ruta(rc2, pedidos) + peso_ruta([k[0]], pedidos) <= max_carga:
                    rutas[rutas.index(rc2)].append(k[0])
                    pasos.append(f"Regla 2: Se añadió {k[0]} al final de la ruta de {k[1]} (Ahorro: {v:.2f}).")
        elif rc1 != None and rc2 != None and rc1 != rc2:
            # Regla 3: Si tanto i como j pertenecen a una ruta y ambos son exteriores... se unen ambas rutas
            if rc1[0] == k[0] and rc2[-1] == k[1]:
                if peso_ruta(rc1, pedidos) + peso_ruta(rc2, pedidos) <= max_carga:
                    rutas[rutas.index(rc2)].extend(rc1)
                    rutas.remove(rc1)
                    pasos.append(f"Regla 3: Se unieron la ruta de {k[1]} y {k[0]} de forma que queden juntas (Ahorro: {v:.2f}).")
            elif rc1[-1] == k[0] and rc2[0] == k[1]:
                if peso_ruta(rc1, pedidos) + peso_ruta(rc2, pedidos) <= max_carga:
                    rutas[rutas.index(rc1)].extend(rc2)
                    rutas.remove(rc2)
                    pasos.append(f"Regla 3: Se unieron la ruta de {k[0]} y {k[1]} de forma que queden juntas (Ahorro: {v:.2f}).")
                    
    # Regla 4: Si quedan vehiculas sin asignar a una ruta, se crea una...
    for c in clientes:
        if en_ruta(rutas, c) is None:
            if peso_ruta([c], pedidos) <= max_carga:
                rutas.append([c])
                pasos.append(f"Regla 4: El cliente {c} quedó sin asignar. Se creó una ruta individual para este vehículo.")
        
    return rutas, pasos