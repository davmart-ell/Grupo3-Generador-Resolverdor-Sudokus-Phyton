# Generador y Resolvedor de Sudokus | Grupo 3

Proyecto académico en Python para el curso An.De Algor.Y Estrat. De Prog..

## 1\. Requisitos

* Python 3.10 o superior.
* Tkinter (Normalmente viene incluido con la instalación de Python).

## 2\. Ejecución

\-Ejecutar main.py

\-Seleccionar dificultad del sudoku a generar

\-Presionar sobre el tablero para generar

\-Presionar el método a resolver

## 3\. Archivos y módulos pendientes de implementar

* heuristica\_mrv.py | Implementar la resolución mediante Backtracking con la heurística MRV, seleccionando en cada paso la casilla vacía con menos candidatos posibles.
* propagacion.py | Implementar Backtracking + MRV + propagación de restricciones (o alternativamente Backtracking + propagación)  : primero realizar asignaciones obligatorias mediante propagación y, cuando ya no sea posible avanzar, seleccionar una casilla con MRV y continuar la búsqueda con retroceso.
* test\_sudoku.py | Incorporar prueba para comprobar la validación (caso adverso).

