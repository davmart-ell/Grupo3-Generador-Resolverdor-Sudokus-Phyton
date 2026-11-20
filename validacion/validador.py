from utils.sudoku_utils import TAMANO, VACIO


def es_seguro(tablero, fila, columna, numero):
    if fila < 0 or fila >= TAMANO:
        return False

    if columna < 0 or columna >= TAMANO:
        return False

    if type(numero) is not int or numero < 1 or numero > TAMANO:
        return False

    # Comprobar que no se repita en la misma fila.
    for c in range(TAMANO):

        if c != columna and tablero[fila][c] == numero:
            return False

    # Comprobar que no se repita en la misma columna.
    for f in range(TAMANO):

        if f != fila and tablero[f][columna] == numero:
            return False

    # Identificar el inicio del subcuadro 3x3.
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3

    # Comprobar los numeros del subcuadro.
    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_columna, inicio_columna + 3):

            if (f != fila or c != columna) and tablero[f][c] == numero:
                return False

    return True


def validar_tablero(tablero, permitir_vacios=True):
    # Comprobar que existan exactamente 9 filas.
    if not isinstance(tablero, (list, tuple)) or len(tablero) != TAMANO:
        return False, "El tablero debe tener 9 filas y 9 columnas."

    # Comprobar que cada fila tenga 9 columnas.
    for fila in tablero:

        if not isinstance(fila, (list, tuple)) or len(fila) != TAMANO:
            return False, "El tablero debe tener 9 filas y 9 columnas."

    # Comprobar los valores permitidos.
    for f in range(TAMANO):
        for c in range(TAMANO):

            numero = tablero[f][c]

            if type(numero) is not int:
                return False, "Solo se permiten numeros enteros."

            if numero < 0 or numero > TAMANO:
                return False, "Los valores permitidos son del 1 al 9 y 0 para vacio."

            if numero == VACIO and not permitir_vacios:
                return False, "El tablero todavia contiene casillas vacias."

    # Comprobar que no existan numeros repetidos.
    for f in range(TAMANO):
        for c in range(TAMANO):

            numero = tablero[f][c]

            if numero != VACIO:

                if not es_seguro(tablero, f, c, numero):
                    mensaje = "Hay un numero repetido en una fila, columna o subcuadro."
                    return False, mensaje

    return True, "El tablero es valido."