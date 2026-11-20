from time import perf_counter

from utils.sudoku_utils import VACIO, copiar_tablero
from validacion.validador import validar_tablero, es_seguro


def sudoku(tablero, fila, col, estadisticas):
    if fila == 9:
        return True

    if col == 9:
        return sudoku(tablero, fila + 1, 0, estadisticas)

    if tablero[fila][col] != VACIO:
        return sudoku(tablero, fila, col + 1, estadisticas)

    for numero in range(1, 10):
        if es_seguro(tablero, fila, col, numero):
            estadisticas["nodos"] += 1
            tablero[fila][col] = numero
            if sudoku(tablero, fila, col + 1, estadisticas):
                return True
            tablero[fila][col] = VACIO  # Deshacer
            estadisticas["retrocesos"] += 1
    return False


def resolver_backtracking(tablero):
    estadisticas = {"nodos": 0, "retrocesos": 0, "tiempo": 0.0}

    valido, mensaje = validar_tablero(tablero)
    if not valido:
        estadisticas["mensaje"] = mensaje
        return None, estadisticas

    copia = copiar_tablero(tablero)

    inicio = perf_counter()
    encontro = sudoku(copia, 0, 0, estadisticas)
    estadisticas["tiempo"] = perf_counter() - inicio

    if encontro:
        estadisticas["mensaje"] = "Se encontro una solucion."
        return copia, estadisticas

    estadisticas["mensaje"] = "El tablero no tiene solucion."
    return None, estadisticas