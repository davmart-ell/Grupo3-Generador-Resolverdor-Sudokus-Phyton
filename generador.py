import random

from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero
from validacion.validador import validar_tablero, es_seguro


def llenar(tablero, fila, col):
    if fila == TAMANO:
        return True

    if col == TAMANO:
        return llenar(tablero, fila + 1, 0)

    numeros = list(range(1, TAMANO + 1))
    random.shuffle(numeros)

    for numero in numeros:
        if es_seguro(tablero, fila, col, numero):
            tablero[fila][col] = numero
            if llenar(tablero, fila, col + 1):
                return True
            tablero[fila][col] = VACIO  # Deshacer
    return False


def contar(tablero, fila, col, limite):
    if fila == TAMANO:
        return 1

    if col == TAMANO:
        return contar(tablero, fila + 1, 0, limite)

    if tablero[fila][col] != VACIO:
        return contar(tablero, fila, col + 1, limite)

    total = 0
    for numero in range(1, TAMANO + 1):
        if es_seguro(tablero, fila, col, numero):
            tablero[fila][col] = numero
            total += contar(tablero, fila, col + 1, limite)
            tablero[fila][col] = VACIO  # Deshacer
            if total >= limite:
                return limite
    return total


class GeneradorSudoku:
    NIVELES = {"Muy fácil": 1, "Medio": 45, "Difícil": 52}
    DIFICULTAD_EXTREMA = "Muy difícil"

    def generar_tablero_completo(self):
        tablero = [[VACIO] * TAMANO for _ in range(TAMANO)]
        if not llenar(tablero, 0, 0):
            raise RuntimeError("No se pudo generar un tablero completo.")
        return tablero

    def contar_soluciones(self, tablero, limite=2):
        if type(limite) is not int or limite < 1:
            raise ValueError("El límite debe ser un entero mayor que cero.")

        valido, _ = validar_tablero(tablero)
        if not valido:
            return 0

        return contar(copiar_tablero(tablero), 0, 0, limite)

    def generar(self, dificultad="Medio"):
        dificultades = list(self.NIVELES) + [self.DIFICULTAD_EXTREMA]
        if dificultad not in dificultades:
            raise ValueError(
                "Dificultad no válida. Elige: " + ", ".join(dificultades)
            )

        solucion = self.generar_tablero_completo()

        if dificultad == self.DIFICULTAD_EXTREMA:
            tablero = [[VACIO] * TAMANO for _ in range(TAMANO)]
            fila = random.randrange(TAMANO)
            col = random.randrange(TAMANO)
            tablero[fila][col] = solucion[fila][col]
            return tablero, solucion

        tablero = copiar_tablero(solucion)
        posiciones = [(f, c) for f in range(TAMANO) for c in range(TAMANO)]
        random.shuffle(posiciones)

        retiradas = 0
        for fila, col in posiciones:
            if retiradas >= self.NIVELES[dificultad]:
                break

            anterior = tablero[fila][col]
            tablero[fila][col] = VACIO

            if self.contar_soluciones(tablero, 2) == 1:
                retiradas += 1
            else:
                tablero[fila][col] = anterior  # Deshacer
        return tablero, solucion