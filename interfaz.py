import tkinter as tk
import math

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
        self.dificultad_tablero = self.dificultad.get()
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
        self.fondos_tablero = {
            "Muy fácil": ("#C8E6C9", "#F5FBF5"),
            "Medio": ("#FFF8E1", "#FFFCF2"),
            "Difícil": ("#FBE9E7", "#FFF7F5"),
            "Muy difícil": ("#FFEBEE", "#FFF5F6")
        }
        self.fondo_caso_adverso = ("#DDD6FE", "#F5F3FF")
        self.es_caso_adverso = False

        self.title("Generador y Resolvedor de Sudoku")
        self.color_fondo = "#F8FAFC"
        self.configure(bg=self.color_fondo)
        self.resizable(False, False)
        self.fondo = tk.Canvas(self, bg=self.color_fondo, highlightthickness=0)
        self.fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.fondo.tk.call("lower", self.fondo._w)
        self.fondo.bind("<Configure>", self.dibujar_fondo)

        titulo = tk.Frame(self, bg=self.color_fondo)
        titulo.pack(fill="x", padx=20, pady=(15, 5))

        marca = tk.Frame(titulo, bg=self.color_fondo)
        marca.pack(anchor="w")

        tk.Label(
            marca, text="G3",
            font=("Arial", 23, "bold"),
            fg="#14532D", bg=self.color_fondo
        ).pack(side="left")

        tk.Label(
            marca, text="Doku",
            font=("Arial", 23, "bold"),
            fg="#15803D", bg=self.color_fondo
        ).pack(side="left")

        tk.Label(
            titulo,
            text="Generador y resolvedor de sudokus",
            font=("Arial", 8),
            fg="#94A3B8",
            bg=self.color_fondo
        ).pack(anchor="w", pady=(0, 2))

        self.etiqueta_dificultad = tk.Label(
            self,
            textvariable=self.dificultad,
            font=("Arial", 11, "bold"),
            bg=self.color_fondo,
            fg=self.colores_dificultad["Medio"]
        )
        self.etiqueta_dificultad.pack()

        self.control_dificultad = tk.Canvas(
            self, width=260, height=34,
            bg=self.color_fondo, highlightthickness=0, cursor="hand2"
        )
        self.control_dificultad.pack(pady=(2, 7))

        self.control_dificultad.bind("<Button-1>", self.mover_dificultad)
        self.control_dificultad.bind("<B1-Motion>", self.mover_dificultad)

        self.dibujar_control_dificultad()

        fila_tablero = tk.Frame(self, bg=self.color_fondo)
        fila_tablero.pack(pady=5)

        izquierda = tk.Frame(fila_tablero, width=65, height=60, bg=self.color_fondo)
        izquierda.pack(side="left", anchor="nw")
        izquierda.pack_propagate(False)

        boton = tk.Canvas(izquierda, width=55, height=55,
                          bg=self.color_fondo, highlightthickness=0, cursor="hand2")
        boton.pack(anchor="nw")

        circulo = boton.create_oval(2, 2, 52, 52, fill="#C4B5FD",
                                    outline="#8B5CF6", width=1)
        boton.create_text(28, 29, text="CASO\nADVERSO", font=("Arial", 7, "bold"),
                          fill="#312E81", justify="center")

        def color(evento):
            hover = evento.type == tk.EventType.Enter
            boton.itemconfig(circulo, fill="#A78BFA" if hover else "#C4B5FD",
                             outline="#7C3AED" if hover else "#8B5CF6")

        boton.bind("<Button-1>", lambda e: self.cargar_caso_adverso())
        boton.bind("<Enter>", color)
        boton.bind("<Leave>", color)

        marco = tk.Frame(fila_tablero, bg="#64748B", padx=3, pady=3, cursor="hand2")
        marco.pack(side="left", padx=(8, 8))

        self.marco = marco
        marco.bind("<Button-1>", self.generar)

        derecha = tk.Frame(fila_tablero, width=65, height=60, bg=self.color_fondo)
        derecha.pack(side="left")
        derecha.pack_propagate(False)
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

        def crear_boton(nombre, funcion):
            boton = tk.Canvas(
                self, width=260, height=32,
                bg=self.color_fondo, highlightthickness=0, cursor="hand2"
            )
            boton.pack(pady=2)

            puntos = []
            for x, y, inicio in [(252, 6, -90), (252, 26, 0),
                                 (8, 26, 90), (8, 6, 180)]:
                for angulo in range(inicio, inicio + 91, 15):
                    rad = math.radians(angulo)
                    puntos.extend((x + 6 * math.cos(rad),
                                   y + 6 * math.sin(rad)))

            fondo = boton.create_polygon(
                *puntos, fill="#0F766E", outline="#0F766E"
            )

            boton.create_text(
                130, 16, text=f"Resolver con {nombre}",
                font=("Arial", 11, "bold"), fill="white"
            )

            boton.bind("<Button-1>", lambda e: funcion())
            boton.bind("<Enter>", lambda e: boton.itemconfig(
                fondo, fill="#0D665F", outline="#0D665F"))
            boton.bind("<Leave>", lambda e: boton.itemconfig(
                fondo, fill="#0F766E", outline="#0F766E"))

        for nombre, funcion in RESOLUTORES:
            crear_boton(
                nombre,
                lambda f=funcion, n=nombre: self.resolver(f, n)
            )

        self.resultado = tk.Label(
            self, text="Selecciona la dificultad y genera un Sudoku.",
            font=("Arial", 10), bg=self.color_fondo, fg="#0F172A",
            justify="left", width=43, height=6, anchor="w", padx=10
        )
        self.resultado.pack(padx=15, pady=(8, 15))
        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        x = (self.winfo_screenwidth() - ancho) // 2
        y = 10

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def dibujar_tablero(self, tablero, resuelto=False):
        color_pistas, color_vacias = (
            self.fondo_caso_adverso if self.es_caso_adverso
            else self.fondos_tablero[self.dificultad_tablero]
        )

        for fila in range(TAMANO):
            for columna in range(TAMANO):
                es_pista = self.tablero[fila][columna] != VACIO

                self.celdas[fila][columna].config(
                    text="" if tablero[fila][columna] == VACIO
                    else tablero[fila][columna],
                    bg=color_pistas if es_pista else
                    ("#E4F5E9" if resuelto else color_vacias),
                    fg=("#6D28D9" if es_pista and self.es_caso_adverso
                        else self.colores_dificultad[self.dificultad_tablero]
                    if es_pista else
                    "#176B3A" if resuelto else "#0F172A")
                )

    def generar(self, evento=None):
        self.es_caso_adverso = False
        self.dificultad_tablero = self.dificultad.get()
        self.sacudir_tablero()
        self.tablero, _ = self.generador.generar(self.dificultad_tablero)
        self.tablero = copiar_tablero(self.tablero)
        self.dibujar_tablero(self.tablero)

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
        self.es_caso_adverso = True
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

        self.dibujar_control_dificultad()

    def dibujar_control_dificultad(self):
        barra = self.control_dificultad
        barra.delete("all")

        x = 15 + 230 * self.nivel_dificultad.get() / 3
        color = self.colores_dificultad[self.dificultad.get()]

        barra.create_line(15, 16, 245, 16, fill="#E2E8F0",
                          width=7, capstyle="round")
        barra.create_line(15, 16, x, 16, fill=color,
                          width=7, capstyle="round")

        for i in range(4):
            punto = 15 + 230 * i / 3
            barra.create_oval(punto - 2, 14, punto + 2, 18,
                              fill="white" if i <= self.nivel_dificultad.get()
                              else "#94A3B8", outline="")

        barra.create_oval(x - 10, 9, x + 10, 29,
                          fill="#CBD5E1", outline="")
        barra.create_oval(x - 9, 7, x + 9, 25,
                          fill="white", outline=color, width=3)
        barra.create_oval(x - 3, 13, x + 3, 19,
                          fill=color, outline="")

    def mover_dificultad(self, evento=None):
        barra = self.control_dificultad

        x = barra.winfo_pointerx() - barra.winfo_rootx()
        x = max(15, min(245, x))

        indice = round((x - 15) * 3 / 230)

        self.nivel_dificultad.set(indice)
        self.actualizar_dificultad(indice)

    def dibujar_fondo(self, evento):
        fondo = self.fondo
        fondo.delete("all")

        paso = 24

        for x in range(0, evento.width, paso):
            color = "#E7ECF3" if (x // paso) % 3 == 0 else "#F0F3F7"
            fondo.create_line(x, 0, x, evento.height, fill=color)

        for y in range(0, evento.height, paso):
            color = "#E7ECF3" if (y // paso) % 3 == 0 else "#F0F3F7"
            fondo.create_line(0, y, evento.width, y, fill=color)