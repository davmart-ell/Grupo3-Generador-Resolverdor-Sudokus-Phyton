import tkinter as tk
from tkinter import ttk

from algoritmos.backtracking import resolver_backtracking
from generador import GeneradorSudoku
from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero


class AplicacionSudoku(tk.Tk):
    def __init__(self, tablero):
        super().__init__()
        self.tablero = copiar_tablero(tablero)
        self.celdas = []
        self.generador = GeneradorSudoku()
        self.dificultad = tk.StringVar(value="Medio")

        self.title("Generador y Resolutor de Sudoku")
        self.configure(bg="white")
        self.resizable(False, False)

        tk.Label(
            self, text="GENERADOR Y RESOLVEDOR DE SUDOKU",
            font=("Arial", 18, "bold"), bg="white"
        ).pack(pady=15)

        tk.Label(
            self, text="Selecciona la dificultad y genera un Sudoku haciendo click en el tablero.",
            font=("Arial", 11, "bold"), bg="white"
        ).pack()

        ttk.Combobox(
            self, textvariable=self.dificultad,
            values=list(GeneradorSudoku.NIVELES) +
                   [GeneradorSudoku.DIFICULTAD_EXTREMA],
            state="readonly", width=15
        ).pack(pady=7)

        marco = tk.Frame(self, bg="#64748B", padx=3, pady=3, cursor="hand2")
        marco.pack(pady=5)
        marco.bind("<Button-1>", self.generar)

        for fila in range(TAMANO):
            self.celdas.append([])
            for columna in range(TAMANO):
                numero = self.tablero[fila][columna]
                celda = tk.Label(
                    marco, text="" if numero == VACIO else numero,
                    width=2, font=("Arial", 15, "bold"), padx=5, pady=5,
                    bg="#DCE7F5" if numero else "white",
                    fg="#17365D" if numero else "#0F172A"
                )
                celda.grid(
                    row=fila, column=columna,
                    padx=(1, 4 if columna in (2, 5) else 1),
                    pady=(1, 4 if fila in (2, 5) else 1)
                )
                celda.bind("<Button-1>", self.generar)
                self.celdas[fila].append(celda)

        tk.Button(
            self, text="Resolver con Backtracking", command=self.resolver,
            font=("Arial", 11, "bold"), bg="#0F766E", fg="white",
            padx=12, pady=7
        ).pack(pady=4)

        self.resultado = tk.Label(
            self, text="Selecciona la dificultad y genera un Sudoku.",
            font=("Arial", 10), bg="white", fg="#0F172A",
            justify="left", width=43, height=5, anchor="w", padx=10
        )
        self.resultado.pack(padx=15, pady=(8, 15))

    def dibujar_tablero(self, tablero, resuelto=False):
        for fila in range(TAMANO):
            for columna in range(TAMANO):
                es_pista = self.tablero[fila][columna] != VACIO
                self.celdas[fila][columna].config(
                    text="" if tablero[fila][columna] == VACIO
                         else tablero[fila][columna],
                    bg="#DCE7F5" if es_pista else
                       ("#E4F5E9" if resuelto else "white"),
                    fg="#17365D" if es_pista else
                       ("#176B3A" if resuelto else "#0F172A")
                )

    def generar(self, evento=None):
        self.tablero, _ = self.generador.generar(self.dificultad.get())
        self.tablero = copiar_tablero(self.tablero)
        self.dibujar_tablero(self.tablero)

        ocupadas = sum(n != VACIO for fila in self.tablero for n in fila)
        self.resultado.config(
            text=f"Sudoku generado correctamente.\n"
                 f"Dificultad: {self.dificultad.get()}\n"
                 f"Casillas ocupadas: {ocupadas}\n"
                 f"Casillas vacías: {81 - ocupadas}"
        )

    def resolver(self):
        solucion, datos = resolver_backtracking(copiar_tablero(self.tablero))
        if solucion is not None:
            self.dibujar_tablero(solucion, resuelto=True)
            mensaje = "Sudoku resuelto correctamente."
        else:
            self.dibujar_tablero(self.tablero)
            mensaje = "No se encontró una solución."

        self.resultado.config(text=(
            f"{mensaje}\nNodos: {datos['nodos']}\n"
            f"Retrocesos: {datos['retrocesos']}\n"
            f"Tiempo: {datos['tiempo']:.6f} segundos"
        ))