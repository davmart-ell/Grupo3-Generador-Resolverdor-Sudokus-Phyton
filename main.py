from interfaz import AplicacionSudoku
from utils.sudoku_utils import TAMANO, VACIO

def main():
    tablero_inicial = [
        [VACIO for _ in range(TAMANO)]
        for _ in range(TAMANO)
    ]
    aplicacion = AplicacionSudoku(tablero_inicial)
    aplicacion.mainloop()


if __name__ == "__main__":
    main()