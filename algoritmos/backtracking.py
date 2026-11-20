from time import perf_counter

from utils.sudoku_utils import (
    VACIO,
    copiar_tablero,
    encontrar_vacio
)

from validacion.validador import (
    validar_tablero,
    es_seguro
)


def _buscar_solucion(tablero, estadisticas):
    # Buscar una casilla vacia.
    posicion = encontrar_vacio(tablero)

    # CASO BASE: no quedan casillas vacias.
    if posicion is None:
        return True

    fila, columna = posicion

    # Probar los numeros del 1 al 9.
    for numero in range(1, 10):

        # VALIDAR: comprobar si el numero es permitido.
        if es_seguro(tablero, fila, columna, numero):

            estadisticas["nodos"] += 1

            # ELEGIR: colocar el numero en la casilla.
            tablero[fila][columna] = numero

            # EXPLORAR: avanzar recursivamente.
            if _buscar_solucion(tablero, estadisticas):
                return True

            # DESHACER: restaurar la casilla.
            tablero[fila][columna] = VACIO

            estadisticas["retrocesos"] += 1

    # Ninguna alternativa permitio completar esta rama.
    return False


def resolver_backtracking(tablero):
    estadisticas = {
        "nodos": 0,
        "retrocesos": 0,
        "tiempo": 0.0
    }

    # Validar el tablero antes de iniciar la busqueda.
    valido, mensaje = validar_tablero(tablero)

    if not valido:
        estadisticas["mensaje"] = mensaje
        return None, estadisticas

    # Trabajar sobre una copia del tablero original.
    copia = copiar_tablero(tablero)

    # Medir el tiempo de ejecucion del algoritmo.
    inicio = perf_counter()

    encontrado = _buscar_solucion(copia, estadisticas)

    estadisticas["tiempo"] = perf_counter() - inicio

    # Devolver la solucion si fue encontrada.
    if encontrado:
        estadisticas["mensaje"] = "Se encontro una solucion."
        return copia, estadisticas

    # No se encontraron soluciones.
    estadisticas["mensaje"] = "El tablero no tiene solucion."

    return None, estadisticas