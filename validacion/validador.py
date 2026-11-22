from utils.sudoku_utils import TAMANO, VACIO


def es_seguro(tablero, fila, col, numero):
    if not (0 <= fila < TAMANO and 0 <= col < TAMANO):
        return False
    if type(numero) is not int or not (1 <= numero <= TAMANO):
        return False

    for i in range(TAMANO):
        misma_fila = (i != col and tablero[fila][i] == numero)
        misma_columna = (i != fila and tablero[i][col] == numero)
        if misma_fila or misma_columna:
            return False

    f0 = (fila // 3) * 3
    c0 = (col // 3) * 3
    for f in range(f0, f0 + 3):
        for c in range(c0, c0 + 3):
            misma_casilla = (f == fila and c == col)
            if not misma_casilla and tablero[f][c] == numero:
                return False
    return True


def validar_tablero(tablero, permitir_vacios=True):
    if not isinstance(tablero, (list, tuple)) or len(tablero) != TAMANO:
        return False, "El tablero debe tener 9 filas y 9 columnas."
    for fila in tablero:
        if not isinstance(fila, (list, tuple)) or len(fila) != TAMANO:
            return False, "El tablero debe tener 9 filas y 9 columnas."

    for f in range(TAMANO):
        for c in range(TAMANO):
            numero = tablero[f][c]
            if type(numero) is not int:
                return False, "Solo se permiten numeros enteros."
            if numero < 0 or numero > TAMANO:
                return False, "Los valores permitidos son del 1 al 9 y 0 para vacio."
            if numero == VACIO and not permitir_vacios:
                return False, "El tablero todavia contiene casillas vacias."

    for f in range(TAMANO):
        for c in range(TAMANO):
            numero = tablero[f][c]
            if numero != VACIO and not es_seguro(tablero, f, c, numero):
                return False, "Hay un numero repetido en una fila, columna o subcuadro."
    return True, "El tablero es valido."