"""Backtracking con MRV y propagación de restricciones (singles)."""

from time import perf_counter

from utils.sudoku_utils import VACIO, copiar_tablero, candidatos
from validacion.validador import validar_tablero
from algoritmos.heuristica_mrv import seleccionar_celda_mrv


def _propagar(tablero, estadisticas):
    """Asigna repetidamente casillas con un único candidato.

    Devuelve False si detecta una contradicción. Las asignaciones quedan en
    el tablero actual y serán deshechas por el nivel de búsqueda que las tomó.
    """
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] != VACIO:
                    continue
                opciones = candidatos(tablero, fila, col)
                if not opciones:
                    return False
                if len(opciones) == 1:
                    tablero[fila][col] = opciones[0]
                    estadisticas["propagaciones"] += 1
                    hubo_cambio = True
    return True


def _buscar(tablero, estadisticas):
    # Cada llamada conserva una copia para poder deshacer todas las
    # propagaciones realizadas dentro de esta rama si resulta inconsistente.
    estado_anterior = copiar_tablero(tablero)
    if not _propagar(tablero, estadisticas):
        for f in range(9):
            tablero[f][:] = estado_anterior[f]
        return False

    seleccion = seleccionar_celda_mrv(tablero)
    if seleccion is None:
        return True

    fila, col, opciones = seleccion
    if not opciones:
        for f in range(9):
            tablero[f][:] = estado_anterior[f]
        return False

    for numero in opciones:
        estadisticas["nodos"] += 1
        tablero[fila][col] = numero
        if _buscar(tablero, estadisticas):
            return True
        tablero[fila][col] = VACIO
        estadisticas["retrocesos"] += 1

    for f in range(9):
        tablero[f][:] = estado_anterior[f]
    return False


def resolver_propagacion(tablero):
    """Resuelve con propagación de candidatos y búsqueda MRV."""
    estadisticas = {
        "nodos": 0, "retrocesos": 0, "propagaciones": 0, "tiempo": 0.0
    }
    valido, mensaje = validar_tablero(tablero)
    if not valido:
        estadisticas["mensaje"] = mensaje
        return None, estadisticas

    copia = copiar_tablero(tablero)
    inicio = perf_counter()
    encontrado = _buscar(copia, estadisticas)
    estadisticas["tiempo"] = perf_counter() - inicio

    if encontrado:
        estadisticas["mensaje"] = "Se encontró una solución con propagación y MRV."
        return copia, estadisticas

    estadisticas["mensaje"] = "El tablero no tiene solución."
    return None, estadisticas