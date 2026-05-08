# dfs-backtracking.py
# Optimización mediante backtracking (Búsqueda en espacio de estados con poda)

class BacktrackingOptimizer:
    def __init__(self):
        self.mejor_val = -1
        self.mejor_sol = None
        # Rangos por defecto del problema planteado
        self.rango_variables = [(0, 51), (0, 76)] # (min, max+1)

    def es_completable(self, variables):
        x1, x2 = variables
        # Restricciones del problema:
        # 1. 7x1 + 4x2 <= 150
        # 2. 6x1 + 5x2 <= 160
        val1 = 7 * x1 + 4 * x2
        val2 = 6 * x1 + 5 * x2
        return val1 <= 150 and val2 <= 160

    def evalua_solucion(self, variables):
        x1, x2 = variables
        # Función objetivo: Z = (12-6)x1 + (8-4)x2 = 6x1 + 4x2
        return 6 * x1 + 4 * x2

    def resolver(self, variables, profundidad):
        if profundidad == len(variables):
            val = self.evalua_solucion(variables)
            if val > self.mejor_val:
                self.mejor_val = val
                self.mejor_sol = list(variables)
            return

        min_val, max_val = self.rango_variables[profundidad]
        for v in range(min_val, max_val):
            variables[profundidad] = v
            # Poda básica: si ya no cumple las restricciones con el valor actual, 
            # y asumiendo coeficientes positivos, incrementar v no ayudará.
            if self.es_completable(variables):
                self.resolver(variables, profundidad + 1)
            else:
                # Si los coeficientes son positivos, al aumentar 'v' la suma solo aumenta.
                # Podemos dejar de iterar en esta rama.
                break

def buscar_mejor_valor_backtracking():
    opt = BacktrackingOptimizer()
    variables = [0, 0]
    opt.resolver(variables, 0)
    return {
        "x1": opt.mejor_sol[0],
        "x2": opt.mejor_sol[1],
        "z": opt.mejor_val,
        "restricciones": [
            "7x1 + 4x2 <= 150",
            "6x1 + 5x2 <= 160"
        ],
        "objetivo": "Z = 6x1 + 4x2"
    }

if __name__ == "__main__":
    resultado = buscar_mejor_valor_backtracking()
    print(f"Mejor solución encontrada: x1={resultado['x1']}, x2={resultado['x2']}")
    print(f"Valor máximo (Z): {resultado['z']}")