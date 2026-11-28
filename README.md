# Generador y Resolvedor de Sudokus | Grupo 3
Proyecto académico en Python para el curso An.De Algor.Y Estrat. De Prog..

## 1\. Requisitos

* Python 3.10 o superior.
* Tkinter (Normalmente viene incluido con la instalación de Python).
* No se requieren paquetes externos o bibliotecas adicionales.

## 2\. Funcionalidades implementadas

* Generación de sudokus: crea tableros a partir de una solución completa generada aleatoriamente. En los niveles normales, el generador conserva los tableros que tienen una única solución.
* Niveles de dificultad: permite seleccionar 1 casilla, Muy fácil, Medio o Difícil.
* Resolución y comparación: ejecuta los tres métodos de resolución y presenta sus resultados en el panel de comparación.
* Caso adverso: carga un tablero válido en su estructura, pero que no tiene solución, para comprobar cómo responden los algoritmos.
* Validación: comprueba las dimensiones del tablero, los valores permitidos y que no existan números repetidos en una fila, columna o subcuadro.

## 3\. Algoritmos de resolución usados

* Backtracking | Prueba valores posibles en las casillas vacías y retrocede cuando una asignación impide completar el tablero.
* Backtracking + MRV | Utiliza la heurística Minimum Remaining Values para seleccionar primero la casilla vacía que tiene menos candidatos posibles.
* Backtracking + MRV + Propagación | Asigna repetidamente las casillas que tienen un único candidato y, cuando necesita continuar la búsqueda, utiliza alternativamente MRV junto con backtracking.

## 4\. Uso y funcionamiento dentro de la aplicación

\-Ejecuta main.py para abrir la interfaz.
\-Comienza seleccionando el nivel de dificultad en la barra situado por encima del tablero de Sudoku.
\-Haz clic en el tablero para generar un nuevo Sudoku.
\-Pulsa uno de los botones Resolver con... para resolver y ejecutar la comparación.
\-En la sección de la derecha, podrás consultar el estado, las métricas y el tiempo de cada algoritmo en el panel de comparación. El tablero mostrará la solución del método seleccionado cuando encuentre una.
\-Con fines de probar los algoritmos, puedes pulsar el botón Caso adverso (cosa que genera un tablero sin solución pero valido) y luego ejecuta cualquiera de los métodos.

## 5\. Niveles de dificultad (Generador)
* 1 casilla | Genera un tablero con una sola pista inicial. (Pensado como caso límite)
* Muy fácil | Retira una pista de la solución completa. (Pensado como caso límite)
* Medio | Intenta retirar hasta 45 pistas, conservando la solución única.
* Difícil| Intenta retirar hasta 52 pistas, conservando la solución única.
