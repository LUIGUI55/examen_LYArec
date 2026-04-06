/**
 * Linear Puzzle DFS Solver - JS Translation
 */

// Basic Node class for BFS Tree
class Nodo {
    constructor(datos, padre = null) {
        this.datos = datos; // array format tracking
        this.padre = padre;
    }

    // Convert array to string for easy comparison and Set storage
    getString() {
        return this.datos.join(',');
    }
}

// Operators (Izquierdo, Central, Derecho)
function operadorIzquierdo(estado) {
    let nuevoEstado = [...estado];
    [nuevoEstado[0], nuevoEstado[1]] = [nuevoEstado[1], nuevoEstado[0]];
    return nuevoEstado;
}

function operadorCentral(estado) {
    let nuevoEstado = [...estado];
    [nuevoEstado[1], nuevoEstado[2]] = [nuevoEstado[2], nuevoEstado[1]];
    return nuevoEstado;
}

function operadorDerecho(estado) {
    let nuevoEstado = [...estado];
    [nuevoEstado[2], nuevoEstado[3]] = [nuevoEstado[3], nuevoEstado[2]];
    return nuevoEstado;
}

// DFS Implementation
function buscarSolucionDFS(estadoInicial, solucionMeta) {
    const solucionStr = solucionMeta.join(',');

    let nodosVisitados = new Set();
    let nodosFrontera = [];

    let nodoInicial = new Nodo(estadoInicial);
    nodosFrontera.push(nodoInicial);
    nodosVisitados.add(nodoInicial.getString());

    while (nodosFrontera.length > 0) {
        // En DFS usamos pop() para extraer el último (Stack / LIFO)
        let nodo = nodosFrontera.pop();

        // If we found the solution
        if (nodo.getString() === solucionStr) {
            return nodo;
        }

        let datoNodo = nodo.datos;

        // Generate children
        let hijosDatos = [
            operadorIzquierdo(datoNodo),
            operadorCentral(datoNodo),
            operadorDerecho(datoNodo)
        ];

        for (let unHijo of hijosDatos) {
            let stringHijo = unHijo.join(',');

            // Check if visited 
            if (!nodosVisitados.has(stringHijo)) {
                nodosVisitados.add(stringHijo);

                // Add to frontier
                let hijoObj = new Nodo(unHijo, nodo);
                nodosFrontera.push(hijoObj);
            }
        }
    }

    return null; // No solution found
}

// Parse input string "4,2,3,1" -> [4,2,3,1] or ["4", "2", "3", "1"]
function parseInput(val) {
    return val.split(',').map(s => s.trim()).filter(s => s !== "");
}

// Find diff indices between two arrays
function getDiffIndices(arr1, arr2) {
    if (!arr1) return [];
    let diffs = [];
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) {
            diffs.push(i);
        }
    }
    return diffs;
}

// UI Binding
document.addEventListener('DOMContentLoaded', () => {
    const solveBtn = document.getElementById('solve-btn');
    const clearBtn = document.getElementById('clear-btn');
    const initialInput = document.getElementById('initial-state');
    const goalInput = document.getElementById('goal-state');
    const alertBox = document.getElementById('alert-message');
    const pathContainer = document.getElementById('path-container');
    const stepCountBadg = document.getElementById('step-count');

    clearBtn.addEventListener('click', () => {
        alertBox.className = 'alert hidden';
        pathContainer.innerHTML = '<div class="placeholder-text">Presiona "Encontrar Solución" para comenzar...</div>';
        stepCountBadg.textContent = '0 Pasos';
        initialInput.value = '4,2,3,1';
        goalInput.value = '1,2,3,4';
    });

    solveBtn.addEventListener('click', () => {
        // Reset UI
        alertBox.className = 'alert hidden';
        pathContainer.innerHTML = '';
        stepCountBadg.textContent = 'Calculando...';

        const initArr = parseInput(initialInput.value);
        const goalArr = parseInput(goalInput.value);

        // Validation
        if (initArr.length !== 4 || goalArr.length !== 4) {
            showAlert('Error: Por favor ingresa exactamente 4 elementos separados por coma.', 'error');
            stepCountBadg.textContent = '0 Pasos';
            return;
        }

        // Disable button during execution
        solveBtn.disabled = true;
        solveBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> Buscando...';

        // Slight delay to allow UI to render computing state
        setTimeout(() => {
            const resultNode = buscarSolucionDFS(initArr, goalArr);

            if (resultNode) {
                // Reconstruct path
                let path = [];
                let current = resultNode;
                while (current !== null) {
                    path.push(current.datos);
                    current = current.padre;
                }
                path.reverse();

                // Show result
                renderPath(path);
                showAlert('¡Solución encontrada con éxito!', 'success');
                stepCountBadg.textContent = `${path.length - 1} Pasos`;
            } else {
                showAlert('No se encontró ninguna solución posible para llegar al objetivo.', 'error');
                stepCountBadg.textContent = 'Camino sin salida';
            }

            // Restore button
            solveBtn.disabled = false;
            solveBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Encontrar Solución';

        }, 300); // 300ms aesthetic delay
    });

    function showAlert(msg, type) {
        alertBox.textContent = msg;
        alertBox.className = `alert ${type}`;

        // Add minimal custom styling for spinner
        if (document.querySelector('style#spin')) return;
        const style = document.createElement('style');
        style.id = 'spin';
        style.textContent = `
            .animate-spin { animation: spin 1s linear infinite; }
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        `;
        document.head.appendChild(style);
    }

    function renderPath(pathArrays) {
        let delay = 0;

        pathArrays.forEach((stateArr, index) => {
            let prevArr = index > 0 ? pathArrays[index - 1] : null;
            let diffIndices = getDiffIndices(prevArr, stateArr);

            // Create card
            const stepDiv = document.createElement('div');
            stepDiv.className = 'step-card';
            stepDiv.style.animationDelay = `${delay}s`;

            // Generate Number
            const numDiv = document.createElement('div');
            numDiv.className = 'step-number';
            numDiv.textContent = index;
            stepDiv.appendChild(numDiv);

            // Generate Array Items
            const arrDiv = document.createElement('div');
            arrDiv.className = 'step-array';

            stateArr.forEach((item, itemIdx) => {
                const b = document.createElement('div');
                b.className = 'array-item';

                // Highlight elements that moved compared to previous step
                if (diffIndices.includes(itemIdx)) {
                    b.classList.add('moved');
                }

                b.textContent = item;
                arrDiv.appendChild(b);
            });

            stepDiv.appendChild(arrDiv);
            pathContainer.appendChild(stepDiv);

            delay += 0.15; // Staggered animation
        });
    }
});
