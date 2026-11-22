TAMANO = 9
VACIO = 0


def copiar_tablero(tablero):
    return [list(fila) for fila in tablero]


def encontrar_vacio(tablero):
    for fila in range(TAMANO):
        for col in range(TAMANO):
            if tablero[fila][col] == VACIO:
                return fila, col
    return None


def candidatos(tablero, fila, col):
    if not (0 <= fila < TAMANO and 0 <= col < TAMANO):
        return []
    if tablero[fila][col] != VACIO:
        return []

    usados = set()
    for i in range(TAMANO):
        usados.add(tablero[fila][i])
        usados.add(tablero[i][col])

    f0 = (fila // 3) * 3
    c0 = (col // 3) * 3
    for f in range(f0, f0 + 3):
        for c in range(c0, c0 + 3):
            usados.add(tablero[f][c])

    opciones = []
    for numero in range(1, TAMANO + 1):
        if numero not in usados:
            opciones.append(numero)
    return opciones


def tablero_completo(tablero):
    for fila in tablero:
        if VACIO in fila:
            return False
    return True


def imprimir_tablero(tablero):
    for fila in range(TAMANO):
        for col in range(TAMANO):
            numero = tablero[fila][col]
            if numero == VACIO:
                print(".", end=" ")
            else:
                print(numero, end=" ")
            if (col + 1) % 3 == 0 and col < TAMANO - 1:
                print("|", end=" ")
        print()
        if (fila + 1) % 3 == 0 and fila < TAMANO - 1:
            print("-" * 21)