import random

from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero
from validacion.validador import validar_tablero, es_seguro

CAJA = int(TAMANO ** 0.5)  # 3 para un tablero 9x9


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


def contar(tablero, limite):
    """Cuenta soluciones (hasta 'limite') usando MRV y máscaras de bits.
    No modifica el tablero recibido."""
    filas = [0] * TAMANO
    cols = [0] * TAMANO
    cajas = [0] * TAMANO

    for f in range(TAMANO):
        for c in range(TAMANO):
            v = tablero[f][c]
            if v != VACIO:
                bit = 1 << v
                filas[f] |= bit
                cols[c] |= bit
                cajas[(f // CAJA) * CAJA + c // CAJA] |= bit

    vacias = [(f, c) for f in range(TAMANO) for c in range(TAMANO)
              if tablero[f][c] == VACIO]

    TODOS = (1 << (TAMANO + 1)) - 2  # bits del 1 al TAMANO

    def resolver(restantes):
        if not restantes:
            return 1

        # MRV: elegir la celda con menos candidatos
        mejor_i = -1
        mejor_mask = 0
        mejor_n = TAMANO + 1
        for i, (f, c) in enumerate(restantes):
            usados = filas[f] | cols[c] | cajas[(f // CAJA) * CAJA + c // CAJA]
            mask = TODOS & ~usados
            n = bin(mask).count("1")
            if n < mejor_n:
                mejor_n, mejor_mask, mejor_i = n, mask, i
                if n <= 1:
                    break

        if mejor_n == 0:
            return 0

        f, c = restantes[mejor_i]
        b = (f // CAJA) * CAJA + c // CAJA
        resto = restantes[:mejor_i] + restantes[mejor_i + 1:]

        total = 0
        for num in range(1, TAMANO + 1):
            bit = 1 << num
            if mejor_mask & bit:
                filas[f] |= bit
                cols[c] |= bit
                cajas[b] |= bit
                total += resolver(resto)
                filas[f] &= ~bit
                cols[c] &= ~bit
                cajas[b] &= ~bit
                if total >= limite:
                    return total
        return total

    return resolver(vacias)


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

        return contar(tablero, limite)

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