# dfs-backtracking.py
# Optimización mediante backtracking (Búsqueda en espacio de estados con poda)

class BacktrackingOptimizer:
    def __init__(self, ranges=None, beneficios=(6, 4), limites=(150, 160), coefs=((7, 4), (6, 5))):
        self.mejor_val = -1
        self.mejor_sol = None
        self.rango_variables = ranges if ranges else [(0, 50), (0, 75)]
        self.beneficios = beneficios
        self.limites = limites
        self.coefs = coefs
        self.error_detail = None

    def es_completable(self, variables):
        x1, x2 = variables
        # Restricciones dinámicas usando coeficientes
        val1 = self.coefs[0][0] * x1 + self.coefs[0][1] * x2
        val2 = self.coefs[1][0] * x1 + self.coefs[1][1] * x2
        
        if val1 > self.limites[0]:
            self.error_detail = f"Recurso A excedido ({val1} > {self.limites[0]})"
            return False
        if val2 > self.limites[1]:
            self.error_detail = f"Recurso B excedido ({val2} > {self.limites[1]})"
            return False
        return True

    def evalua_solucion(self, variables):
        x1, x2 = variables
        return self.beneficios[0] * x1 + self.beneficios[1] * x2

    def resolver(self, variables, profundidad):
        if profundidad == len(variables):
            val = self.evalua_solucion(variables)
            if val > self.mejor_val:
                self.mejor_val = val
                self.mejor_sol = list(variables)
            return

        min_val, max_val = self.rango_variables[profundidad]
        for v in range(int(min_val), int(max_val) + 1):
            # Usamos una copia para evitar que los valores de ramas anteriores
            # afecten la validación de la rama actual (Backtracking real)
            nuevas_variables = list(variables)
            nuevas_variables[profundidad] = v
            
            if self.es_completable(nuevas_variables):
                self.resolver(nuevas_variables, profundidad + 1)
            else:
                # Si el valor mínimo ya excede la restricción, detenemos la búsqueda en este nivel
                if v == int(min_val):
                    break
                # Si v > min_val y falla, también podemos romper (poda)
                break

def buscar_mejor_valor_backtracking(rangos=None, beneficios=(6, 4), limites=(150, 160), coefs=((7, 4), (6, 5))):
    opt = BacktrackingOptimizer(rangos, beneficios, limites, coefs)
    variables = [0, 0]
    opt.resolver(variables, 0)
    
    if opt.mejor_sol is None:
        return {
            "success": False,
            "error": "No hay solución factible.",
            "detalle": opt.error_detail or "Los rangos mínimos exceden los recursos."
        }

    return {
        "success": True,
        "x1": opt.mejor_sol[0],
        "x2": opt.mejor_sol[1],
        "z": opt.mejor_val
    }

if __name__ == "__main__":
    resultado = buscar_mejor_valor_backtracking()
    print(f"Mejor solución encontrada: x1={resultado['x1']}, x2={resultado['x2']}")
    print(f"Valor máximo (Z): {resultado['z']}")
