import tkinter as tk
from tkinter import ttk

from comparador import RESOLUTORES
from generador import GeneradorSudoku
from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero
from pruebas.test_sudoku import SUDOKU_SIN_SOLUCION


class AplicacionSudoku(tk.Tk):
    def __init__(self, tablero):
        super().__init__()
        self.tablero = copiar_tablero(tablero)
        self.celdas = []
        self.generador = GeneradorSudoku()
        self.dificultad = tk.StringVar(value="Medio")
        self.niveles_dificultad = list(GeneradorSudoku.NIVELES) + [
            GeneradorSudoku.DIFICULTAD_EXTREMA
        ]
        self.nivel_dificultad = tk.IntVar(value=1)
        self.colores_dificultad = {
            "Muy fácil": "#2E7D32", 
            "Medio": "#9A7200",
            "Difícil": "#C0392B",
            "Muy difícil": "#B71C1C"
        }
        self.generando = False #false, es una forma vaga de cubrir el lag al generar en dificultad (aplicado en dificultad dificil)

        self.title("Generador y Resolutor de Sudoku")
        self.configure(bg="white")
        self.resizable(False, False)

        tk.Label(
            self, text="GENERADOR Y RESOLVEDOR DE SUDOKU",
            font=("Arial", 18, "bold"), bg="white"
        ).pack(pady=15)

        tk.Button(
            self,
            text="Cargar caso adverso",
            command=self.cargar_caso_adverso,
            font=("Arial", 11, "bold"),
            bg="#B45309",
            fg="white",
            padx=1,
            pady=1
        ).pack(pady=7)

        tk.Label(
            self, text="Dificultad", font=("Arial", 10, "bold"), bg="white"
        ).pack(pady=(7, 0))

        self.etiqueta_dificultad = tk.Label(
            self,
            textvariable=self.dificultad,
            font=("Arial", 11, "bold"),
            bg="white",
            fg=self.colores_dificultad["Medio"]
        )
        self.etiqueta_dificultad.pack()

        tk.Scale(
            self,
            from_=0,
            to=3,
            orient="horizontal",
            resolution=1,
            showvalue=False,
            variable=self.nivel_dificultad,
            length=250,
            bg="white",
            fg="#17365D",
            troughcolor="#DCE7F5",
            activebackground="#0F766E",
            highlightthickness=0,
            bd=0,
            command=self.actualizar_dificultad
        ).pack(pady=(0, 7))

        marco = tk.Frame(self, bg="#64748B", padx=3, pady=3, cursor="hand2")
        marco.pack(pady=5, padx=8)
        self.marco = marco
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

        for nombre, funcion in RESOLUTORES:
            tk.Button(
                self,
                text=f"Resolver con {nombre}",
                command=lambda f=funcion, n=nombre: self.resolver(f, n),
                font=("Arial", 11, "bold"),
                bg="#0F766E",
                fg="white",
                padx=1,
                pady=1
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
        self.sacudir_tablero()
        self.tablero, _ = self.generador.generar(self.dificultad.get())
        self.tablero = copiar_tablero(self.tablero)
        self.dibujar_tablero(self.tablero)
        self.tablero, _ = self.generador.generar(self.dificultad.get())

        ocupadas = sum(n != VACIO for fila in self.tablero for n in fila)
        self.resultado.config(
            text=f"Sudoku generado correctamente.\n"
                 f"Dificultad: {self.dificultad.get()}\n"
                 f"Casillas ocupadas: {ocupadas}\n"
                 f"Casillas vacías: {81 - ocupadas}"
        )


    def resolver(self, funcion, nombre):
        solucion, datos = funcion(copiar_tablero(self.tablero))

        if solucion is not None:
            self.dibujar_tablero(solucion, resuelto=True)
            mensaje = "Sudoku resuelto correctamente."
        else:
            self.dibujar_tablero(self.tablero)
            mensaje = datos.get("mensaje", "No se encontró una solución.")

        texto = (
            f"{mensaje}\n"
            f"Algoritmo: {nombre}\n"
            f"Nodos: {datos['nodos']}\n"
            f"Retrocesos: {datos['retrocesos']}\n"
            f"Tiempo: {datos['tiempo']:.6f} segundos"
        )

        if "propagaciones" in datos:
            texto += f"\nPropagaciones: {datos['propagaciones']}"

        self.resultado.config(text=texto)

    def cargar_caso_adverso(self):
        self.tablero = copiar_tablero(SUDOKU_SIN_SOLUCION)
        self.dibujar_tablero(self.tablero)

        self.resultado.config(
            text="Caso adverso cargado.\n"
                 "El tablero es válido, pero no tiene solución.\n"
                 "Prueba los tres algoritmos."
        )

    def sacudir_tablero(self):
        movimientos = [-6, 6, -4, 4, 0]

        def animar(paso=0):
            if paso == len(movimientos):
                self.marco.pack_configure(padx=(8, 8))
                self.generando = False
                return

            desplazamiento = movimientos[paso]

            self.marco.pack_configure(
                padx=(8 + desplazamiento, 8 - desplazamiento)
            )

            self.after(35, lambda: animar(paso + 1))

        animar()

    def actualizar_dificultad(self, valor):
        indice = int(float(valor))
        nombre = self.niveles_dificultad[indice]

        self.dificultad.set(nombre)
        self.etiqueta_dificultad.config(
            fg=self.colores_dificultad[nombre]
        )