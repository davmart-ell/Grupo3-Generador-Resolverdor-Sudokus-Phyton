import tkinter as tk

from algoritmos.backtracking import resolver_backtracking
from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero

#De momento la interfaz solo contiene "resolver con backtrcking" (mientras se crean los demas métodos)
class AplicacionSudoku(tk.Tk):
    def __init__(self, tablero):
        super().__init__()
        self.tablero = copiar_tablero(tablero)
        self.celdas = []

        self.title("Resolvedor de Sudoku")
        self.configure(bg="#F1F5F9")
        self.resizable(False, False)

        tk.Label(
            self, text="RESOLVEDOR DE SUDOKU",
            font=("Arial", 18, "bold"), bg="#F1F5F9", fg="#17324D"
        ).pack(pady=15)

        marco = tk.Frame(self, bg="#64748B", padx=3, pady=3)
        marco.pack(pady=5)

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
                self.celdas[fila].append(celda)

        tk.Button(
            self, text="Resolver con Backtracking", command=self.resolver,
            font=("Arial", 11, "bold"), bg="#2563EB", fg="white",
            padx=12, pady=7
        ).pack(pady=12)

        self.resultado = tk.Label(
            self, text="Presiona el botón para resolver el Sudoku.",
            font=("Arial", 10), bg="white", fg="#0F172A",
            justify="left", width=43, height=5, anchor="w", padx=10
        )
        self.resultado.pack(padx=15, pady=(0, 15))

    def resolver(self):
        solucion, datos = resolver_backtracking(copiar_tablero(self.tablero))
        mensaje = "Sudoku resuelto correctamente." if solucion else "No se encontró una solución."
        tablero = solucion if solucion else self.tablero

        for fila in range(TAMANO):
            for columna in range(TAMANO):
                es_pista = self.tablero[fila][columna] != VACIO
                self.celdas[fila][columna].config(
                    text="" if tablero[fila][columna] == VACIO else tablero[fila][columna],
                    bg="#DCE7F5" if es_pista else ("#E4F5E9" if solucion else "white"),
                    fg="#17365D" if es_pista else ("#176B3A" if solucion else "#0F172A")
                )

        self.resultado.config(text=(
            f"{mensaje}\nNodos: {datos['nodos']}\n"
            f"Retrocesos: {datos['retrocesos']}\n"
            f"Tiempo: {datos['tiempo']:.6f} segundos"
        ))