"""Resolución de Sudoku mediante Backtracking con heurística MRV."""

from time import perf_counter

from utils.sudoku_utils import VACIO, copiar_tablero, candidatos
from validacion.validador import validar_tablero


def seleccionar_celda_mrv(tablero):
    """Devuelve (fila, columna, candidatos) de la casilla vacía más restringida.

    MRV (Minimum Remaining Values) elige la casilla con menos candidatos.
    Si una casilla no tiene candidatos, la devuelve inmediatamente para
    detectar el callejón sin salida.
    """
    mejor = None
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == VACIO:
                opciones = candidatos(tablero, fila, col)
                if mejor is None or len(opciones) < len(mejor[2]):
                    mejor = (fila, col, opciones)
                    if len(opciones) <= 1:
                        if not opciones:
                            return mejor
                        # Un candidato es lo mejor posible, pero seguimos
                        # buscando una casilla con cero candidatos.
    return mejor


def _buscar(tablero, estadisticas):
    seleccion = seleccionar_celda_mrv(tablero)
    if seleccion is None:
        return True

    fila, col, opciones = seleccion
    if not opciones:
        return False

    for numero in opciones:
        estadisticas["nodos"] += 1
        tablero[fila][col] = numero
        if _buscar(tablero, estadisticas):
            return True
        tablero[fila][col] = VACIO
        estadisticas["retrocesos"] += 1
    return False


def resolver_mrv(tablero):
    """Resuelve sin modificar el tablero original y devuelve solución y métricas."""
    estadisticas = {"nodos": 0, "retrocesos": 0, "tiempo": 0.0}
    valido, mensaje = validar_tablero(tablero)
    if not valido:
        estadisticas["mensaje"] = mensaje
        return None, estadisticas

    copia = copiar_tablero(tablero)
    inicio = perf_counter()
    encontrado = _buscar(copia, estadisticas)
    estadisticas["tiempo"] = perf_counter() - inicio

    if encontrado:
        estadisticas["mensaje"] = "Se encontró una solución con MRV."
        return copia, estadisticas

    estadisticas["mensaje"] = "El tablero no tiene solución."
    return None, estadisticas