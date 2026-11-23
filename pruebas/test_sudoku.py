"""Pruebas unitarias de validación y de los tres resolutores."""

import unittest

from algoritmos.backtracking import resolver_backtracking
from algoritmos.heuristica_mrv import resolver_mrv
from algoritmos.propagacion import resolver_propagacion
from validacion.validador import validar_tablero
from utils.sudoku_utils import copiar_tablero


SUDOKU_VALIDO = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class TestValidacionSudoku(unittest.TestCase):
    def test_tablero_correcto(self):
        valido, _ = validar_tablero(SUDOKU_VALIDO)
        self.assertTrue(valido)

    def test_caso_adverso_numero_repetido_en_fila(self):
        tablero = copiar_tablero(SUDOKU_VALIDO)
        tablero[0][2] = 5
        valido, mensaje = validar_tablero(tablero)
        self.assertFalse(valido)
        self.assertIn("repetido", mensaje)

    def test_caso_adverso_numero_repetido_en_columna(self):
        tablero = copiar_tablero(SUDOKU_VALIDO)
        tablero[2][0] = 5
        valido, _ = validar_tablero(tablero)
        self.assertFalse(valido)

    def test_caso_adverso_tablero_con_dimension_incorrecta(self):
        valido, _ = validar_tablero([[0] * 8 for _ in range(9)])
        self.assertFalse(valido)

    def test_caso_adverso_valor_fuera_de_rango(self):
        tablero = copiar_tablero(SUDOKU_VALIDO)
        tablero[0][2] = 10
        valido, _ = validar_tablero(tablero)
        self.assertFalse(valido)


class TestResolutores(unittest.TestCase):
    def _comprobar_solucion(self, resolver):
        original = copiar_tablero(SUDOKU_VALIDO)
        solucion, estadisticas = resolver(original)
        self.assertIsNotNone(solucion, estadisticas.get("mensaje"))
        self.assertTrue(validar_tablero(solucion, permitir_vacios=False)[0])
        self.assertEqual(original, SUDOKU_VALIDO)  # No modifica el original

    def test_backtracking(self):
        self._comprobar_solucion(resolver_backtracking)

    def test_mrv(self):
        self._comprobar_solucion(resolver_mrv)

    def test_propagacion(self):
        self._comprobar_solucion(resolver_propagacion)

    def test_rechaza_tablero_invalido(self):
        tablero = copiar_tablero(SUDOKU_VALIDO)
        tablero[0][2] = 5
        for resolver in (resolver_backtracking, resolver_mrv, resolver_propagacion):
            solucion, _ = resolver(tablero)
            self.assertIsNone(solucion)


if __name__ == "__main__":
    unittest.main(verbosity=2)