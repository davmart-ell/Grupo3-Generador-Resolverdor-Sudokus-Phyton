from algoritmos.backtracking import resolver_backtracking
from validacion.validador import validar_tablero
from utils.sudoku_utils import imprimir_tablero

# Sudoku de ejemplo.
TABLERO_EJEMPLO = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Salida por consola es temporal para pruebas, los resultados se mostraran mediante una interfaz grafica.
def mostrar_estadisticas(estadisticas):
    print("\nESTADISTICAS DEL ALGORITMO")
    print("--------------------------")

    print("Nodos explorados:", estadisticas["nodos"])
    print("Retrocesos:", estadisticas["retrocesos"])

    tiempo = estadisticas["tiempo"]
    print("Tiempo de ejecucion:", round(tiempo, 6), "segundos")


def main():
    print("======================================")
    print("   GENERADOR Y RESOLUTOR DE SUDOKU")
    print("======================================")

    print("\nTABLERO INICIAL:")
    imprimir_tablero(TABLERO_EJEMPLO)

    valido, mensaje = validar_tablero(TABLERO_EJEMPLO)

    print("\nVALIDACION INICIAL:")
    print(mensaje)

    if not valido:
        print("No se puede resolver el tablero.")
        return

    print("\nRESOLVIENDO SUDOKU...")

    solucion, estadisticas = resolver_backtracking(TABLERO_EJEMPLO)

    if solucion is None:
        print("\nNo se encontro una solucion.")
        print(estadisticas["mensaje"])
        mostrar_estadisticas(estadisticas)
        return

    print("\nSOLUCION ENCONTRADA:")
    imprimir_tablero(solucion)

    valido, mensaje = validar_tablero(
        solucion,
        permitir_vacios=False
    )

    print("\nVALIDACION DE LA SOLUCION:")
    print(mensaje)

    if valido:
        print("Resultado: Sudoku resuelto correctamente.")
    else:
        print("Resultado: La solucion no es valida.")

    mostrar_estadisticas(estadisticas)

if __name__ == "__main__":
    main()