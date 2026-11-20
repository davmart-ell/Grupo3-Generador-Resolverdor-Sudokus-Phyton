TAMANO = 9
VACIO = 0


def copiar_tablero(tablero):
    copia = []

    for fila in tablero:
        nueva_fila = []

        for numero in fila:
            nueva_fila.append(numero)

        copia.append(nueva_fila)

    return copia


def encontrar_vacio(tablero):
    for fila in range(TAMANO):
        for columna in range(TAMANO):

            if tablero[fila][columna] == VACIO:
                return fila, columna

    return None


def candidatos(tablero, fila, columna):
    if fila < 0 or fila >= TAMANO:
        return []

    if columna < 0 or columna >= TAMANO:
        return []

    if tablero[fila][columna] != VACIO:
        return []

    usados = set()

    # Registrar los numeros de la fila.
    for numero in tablero[fila]:

        if numero != VACIO:
            usados.add(numero)

    # Registrar los numeros de la columna.
    for f in range(TAMANO):

        numero = tablero[f][columna]

        if numero != VACIO:
            usados.add(numero)

    # Identificar el inicio del subcuadro 3x3.
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3

    # Registrar los numeros del subcuadro.
    for f in range(inicio_fila, inicio_fila + 3):
        for c in range(inicio_columna, inicio_columna + 3):

            numero = tablero[f][c]

            if numero != VACIO:
                usados.add(numero)

    # Construir la lista de candidatos.
    opciones = []

    for numero in range(1, TAMANO + 1):

        if numero not in usados:
            opciones.append(numero)

    return opciones


def tablero_completo(tablero):
    for fila in tablero:
        for numero in fila:

            if numero == VACIO:
                return False

    return True


def imprimir_tablero(tablero):
    for fila in range(TAMANO):

        for columna in range(TAMANO):

            numero = tablero[fila][columna]

            if numero == VACIO:
                print(".", end=" ")
            else:
                print(numero, end=" ")

            if (columna + 1) % 3 == 0 and columna < TAMANO - 1:
                print("|", end=" ")

        print()

        if (fila + 1) % 3 == 0 and fila < TAMANO - 1:
            print("-" * 21)