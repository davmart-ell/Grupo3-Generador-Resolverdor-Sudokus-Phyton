"""Ejecuta y compara Backtracking, MRV y Propagación + MRV."""

from algoritmos.backtracking import resolver_backtracking
from algoritmos.heuristica_mrv import resolver_mrv
from algoritmos.propagacion import resolver_propagacion
from utils.sudoku_utils import copiar_tablero


RESOLUTORES = (
    ("Backtracking", resolver_backtracking),
    ("Backtracking + MRV", resolver_mrv),
    ("Propagación + MRV", resolver_propagacion),
)


def comparar_resolutores(tablero):
    """Devuelve una lista de resultados, conservando intacto el tablero recibido."""
    resultados = []
    for nombre, funcion in RESOLUTORES:
        solucion, estadisticas = funcion(copiar_tablero(tablero))
        resultados.append({
            "algoritmo": nombre,
            "solucion": solucion,
            "resuelto": solucion is not None,
            "nodos": estadisticas.get("nodos", 0),
            "retrocesos": estadisticas.get("retrocesos", 0),
            "propagaciones": estadisticas.get("propagaciones", 0),
            "tiempo": estadisticas.get("tiempo", 0.0),
            "mensaje": estadisticas.get("mensaje", ""),
        })
    return resultados


def imprimir_comparacion(tablero):
    """Imprime una tabla sencilla para la demostración del proyecto."""
    resultados = comparar_resolutores(tablero)
    print("\nCOMPARACIÓN DE ALGORITMOS")
    print("-" * 88)
    print(f"{'Algoritmo':<25} {'Resuelto':<10} {'Nodos':>10} {'Retrocesos':>12} {'Tiempo (s)':>14}")
    print("-" * 88)
    for r in resultados:
        print(
            f"{r['algoritmo']:<25} {('Sí' if r['resuelto'] else 'No'):<10} "
            f"{r['nodos']:>10} {r['retrocesos']:>12} {r['tiempo']:>14.6f}"
        )
        if r["propagaciones"]:
            print(f"  Asignaciones por propagación: {r['propagaciones']}")
        if r["mensaje"]:
            print(f"  {r['mensaje']}")
    return resultados


if __name__ == "__main__":
    # Ejemplo de ejecución desde la raíz del proyecto:
    ejemplo = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    imprimir_comparacion(ejemplo)