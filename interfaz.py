import tkinter as tk
from tkinter import font as tkfont
import math

from comparador import RESOLUTORES, comparar_resolutores
from generador import GeneradorSudoku
from utils.sudoku_utils import TAMANO, VACIO, copiar_tablero
from pruebas.test_sudoku import SUDOKU_SIN_SOLUCION

COLOR_PANEL = "#E2E8F0"

def puntos_redondeados(x1, y1, x2, y2, r):
    puntos = []
    for cx, cy, inicio in [(x2 - r, y1 + r, 270), (x2 - r, y2 - r, 0),
                           (x1 + r, y2 - r, 90), (x1 + r, y1 + r, 180)]:
        for angulo in range(inicio, inicio + 91, 15):
            rad = math.radians(angulo)
            puntos.extend((cx + r * math.cos(rad), cy + r * math.sin(rad)))
    return puntos


def formatear(valor):
    if isinstance(valor, int):
        return f"{valor:,}".replace(",", ".")
    return str(valor)


class CanvasCuadricula(tk.Canvas):

    PASO = 24

    def __init__(self, master, **kw):
        kw.setdefault("highlightthickness", 0)
        kw.setdefault("bd", 0)
        super().__init__(master, **kw)
        self.bind("<Configure>", self.pintar_cuadricula, add="+")

    def pintar_cuadricula(self, evento=None):
        self.delete("cuadricula")
        ancho, alto = self.winfo_width(), self.winfo_height()
        if ancho <= 1 or alto <= 1:
            return

        raiz = self.winfo_toplevel()
        ox = self.winfo_rootx() - raiz.winfo_rootx()
        oy = self.winfo_rooty() - raiz.winfo_rooty()
        paso = self.PASO

        for k in range(ox // paso, (ox + ancho) // paso + 1):
            x = k * paso - ox
            if 0 <= x <= ancho:
                color = "#E7ECF3" if k % 3 == 0 else "#E2E8F0"
                self.create_line(x, 0, x, alto, fill=color, tags="cuadricula")

        for k in range(oy // paso, (oy + alto) // paso + 1):
            y = k * paso - oy
            if 0 <= y <= alto:
                color = "#E7ECF3" if k % 3 == 0 else "#E2E8F0"
                self.create_line(0, y, ancho, y, fill=color, tags="cuadricula")

        self.tag_lower("cuadricula")

    def limpiar(self):
        for item in self.find_all():
            if "cuadricula" not in self.gettags(item):
                self.delete(item)


class TarjetaAlgoritmo(tk.Canvas):
    ANCHO = 404
    ALTO = 150

    TONOS = {
        "pendiente": ("#E2E8F0", "#64748B"),
        "ok": ("#DCFCE7", "#15803D"),
        "rapido": ("#16A34A", "#FFFFFF"),
        "error": ("#FEE2E2", "#B91C1C"),
    }
    ETIQUETAS = ("NODOS", "RETROCESOS", "PROPAGACIONES")

    def __init__(self, master, nombre):
        super().__init__(master, width=self.ANCHO, height=self.ALTO,
                         bg=COLOR_PANEL, highlightthickness=0, bd=0)
        self.nombre = nombre
        self.fuente_pildora = tkfont.Font(family="Arial", size=8, weight="bold")
        self.reiniciar()

    def rect(self, x1, y1, x2, y2, radio, fondo, borde="", ancho=1):
        return self.create_polygon(
            *puntos_redondeados(x1, y1, x2, y2, radio),
            fill=fondo, outline=borde, width=ancho
        )

    def reiniciar(self):
        self._dibujar("PENDIENTE", "pendiente", ("—", "—", "—"), "—", 0)

    def mostrar(self, resultado, es_mas_rapido, fraccion):
        if resultado["resuelto"]:
            texto = "MÁS RÁPIDO" if es_mas_rapido else "RESUELTO"
            tono = "rapido" if es_mas_rapido else "ok"
        else:
            texto, tono = "SIN SOLUCIÓN", "error"

        valores = (
            formatear(resultado["nodos"]),
            formatear(resultado["retrocesos"]),
            formatear(resultado.get("propagaciones", "—")),
        )
        self._dibujar(
            texto, tono, valores,
            f"{resultado['tiempo']:.6f} s", fraccion,
            ganador=es_mas_rapido
        )

    def _dibujar(self, texto_estado, tono, valores, tiempo_txt, fraccion,
                 ganador=False):
        self.delete("all")
        W, H = self.ANCHO, self.ALTO

        fondo = "#F0FDF4" if ganador else "#F8FAFC"
        borde = "#16A34A" if ganador else "#CBD5E1"
        self.rect(1, 1, W - 2, H - 2, 14, fondo, borde, 2 if ganador else 1)

        self.create_text(16, 22, text=self.nombre, anchor="w",
                         fill="#0F172A", font=("Arial", 11, "bold"))

        fondo_p, texto_p = self.TONOS[tono]
        ancho_p = self.fuente_pildora.measure(texto_estado) + 20
        self.rect(16, 36, 16 + ancho_p, 52, 8, fondo_p)
        self.create_text(16 + ancho_p / 2, 44, text=texto_estado,
                         fill=texto_p, font=self.fuente_pildora)

        margen, hueco = 16, 8
        ancho_b = (W - 2 * margen - 2 * hueco) / 3
        fondo_b = "#DCFCE7" if ganador else "#EEF2F6"
        for i, (etiqueta, valor) in enumerate(zip(self.ETIQUETAS, valores)):
            x1 = margen + i * (ancho_b + hueco)
            self.rect(x1, 60, x1 + ancho_b, 102, 8, fondo_b)
            cx = x1 + ancho_b / 2
            self.create_text(
                cx, 77, text=valor, font=("Arial", 14, "bold"),
                fill="#CBD5E1" if valor == "—" else "#0F172A"
            )
            self.create_text(cx, 93, text=etiqueta, fill="#94A3B8",
                             font=("Arial", 7, "bold"))

        self.create_text(16, 116, text="TIEMPO", anchor="w", fill="#94A3B8",
                         font=("Arial", 7, "bold"))
        self.create_text(W - 16, 116, text=tiempo_txt, anchor="e",
                         fill="#0F172A", font=("Arial", 9, "bold"))

        x0, x1 = 19, W - 19
        self.create_line(x0, 134, x1, 134, fill="#E2E8F0",
                         width=6, capstyle="round")
        if fraccion > 0:
            fin = x0 + max(4, (x1 - x0) * fraccion)
            self.create_line(x0, 134, fin, 134,
                             fill="#16A34A", width=6, capstyle="round")


class AplicacionSudoku(tk.Tk):
    def __init__(self, tablero):
        super().__init__()
        self.lienzos = []
        self.tablero = copiar_tablero(tablero)
        self.celdas = []
        self.generador = GeneradorSudoku()
        self.dificultad = tk.StringVar(value="Medio")
        self.dificultad_tablero = self.dificultad.get()
        self.niveles_dificultad = [
                                      GeneradorSudoku.DIFICULTAD_1CASILLA
                                  ] + list(GeneradorSudoku.NIVELES)

        self.nivel_dificultad = tk.IntVar(value=2)
        self.colores_dificultad = {
            "1 casilla": "#64748B",
            "Muy fácil": "#2E7D32",
            "Medio": "#9A7200",
            "Difícil": "#C0392B",
        }
        self.fondos_tablero = {
            "1 casilla": ("#CBD5E1", "#F1F5F9"),
            "Muy fácil": ("#C8E6C9", "#F5FBF5"),
            "Medio": ("#FFF8E1", "#FFFCF2"),
            "Difícil": ("#FBE9E7", "#FFF7F5"),
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

        contenido = self.nuevo_lienzo(self)
        contenido.pack(padx=20, pady=10)

        columna_izquierda = self.nuevo_lienzo(contenido)
        columna_izquierda.pack(side="left", anchor="n")

        self.panel_comparacion = self.nuevo_lienzo(
            contenido, width=440, height=600
        )
        self.panel_comparacion.pack(side="left", padx=(22, 0), fill="y")

        contenido_panel = tk.Frame(self.panel_comparacion, bg=COLOR_PANEL)

        self.ventana_panel = self.panel_comparacion.create_window(
            18, 16, anchor="nw",
            window=contenido_panel,
            width=404, height=568
        )
        self.panel_comparacion.bind(
            "<Configure>", self.redibujar_panel, add="+"
        )

        contenido_panel.grid_columnconfigure(0, weight=1)
        for r in range(1, len(RESOLUTORES) + 1):
            contenido_panel.grid_rowconfigure(r, weight=1)

        encabezado = tk.Canvas(
            contenido_panel, width=404, height=64,
            bg=COLOR_PANEL, highlightthickness=0
        )
        encabezado.grid(row=0, column=0, sticky="w")

        encabezado.create_polygon(
            *puntos_redondeados(0, 8, 36, 44, 9),
            fill="#15803D", outline="#15803D"
        )
        for x1, y1, x2 in [(8, 28, 14), (16, 22, 22), (24, 16, 30)]:
            encabezado.create_rectangle(x1, y1, x2, 38,
                                        fill="white", outline="")
        encabezado.create_text(
            46, 20, text="COMPARACIÓN DE ALGORITMOS", anchor="w",
            font=("Arial", 15, "bold"), fill="#0F172A"
        )
        encabezado.create_text(
            46, 43, text="Resultados de los tres métodos de resolución",
            anchor="w", font=("Arial", 9), fill="#64748B"
        )
        encabezado.create_line(0, 61, 404, 61, fill="#CBD5E1")

        self.resultados_comparacion = {}
        for i, (nombre, _) in enumerate(RESOLUTORES):
            tarjeta = TarjetaAlgoritmo(contenido_panel, nombre)
            tarjeta.grid(row=i + 1, column=0, pady=4)
            self.resultados_comparacion[nombre] = tarjeta

        titulo = self.nuevo_lienzo(columna_izquierda, width=1, height=60)
        titulo.pack(fill="x", padx=20, pady=(15, 5))

        g3 = titulo.create_text(
            0, 2, text="G3", anchor="nw",
            font=("Arial", 23, "bold"), fill="#14532D"
        )
        x_doku = titulo.bbox(g3)[2]
        titulo.create_text(
            x_doku, 2, text="Doku", anchor="nw",
            font=("Arial", 23, "bold"), fill="#15803D"
        )
        titulo.create_text(
            0, 42, text="Generador y resolvedor de sudokus", anchor="nw",
            font=("Arial", 8), fill="#94A3B8"
        )

        self.etiqueta_dificultad = self.nuevo_lienzo(
            columna_izquierda, width=1, height=22
        )
        self.etiqueta_dificultad.pack(fill="x")
        self.texto_dificultad = self.etiqueta_dificultad.create_text(
            0, 11, text=self.dificultad.get(),
            font=("Arial", 11, "bold"),
            fill=self.colores_dificultad[self.dificultad.get()]
        )
        self.etiqueta_dificultad.bind(
            "<Configure>",
            lambda e: self.etiqueta_dificultad.coords(
                self.texto_dificultad, e.width / 2, 11
            ),
            add="+"
        )

        self.control_dificultad = self.nuevo_lienzo(
            columna_izquierda, width=260, height=34, cursor="hand2"
        )
        self.control_dificultad.pack(pady=(2, 7))

        self.control_dificultad.bind("<Button-1>", self.mover_dificultad)
        self.control_dificultad.bind("<B1-Motion>", self.mover_dificultad)

        self.dibujar_control_dificultad()

        fila_tablero = self.nuevo_lienzo(columna_izquierda)
        fila_tablero.pack(pady=5)

        izquierda = self.nuevo_lienzo(fila_tablero, width=65, height=60)
        izquierda.pack(side="left", anchor="nw")
        izquierda.pack_propagate(False)

        circulo = izquierda.create_oval(
            2, 2, 52, 52, fill="#C4B5FD", outline="#8B5CF6",
            width=1, tags="caso"
        )
        izquierda.create_text(
            28, 29, text="CASO\nADVERSO", font=("Arial", 7, "bold"),
            fill="#312E81", justify="center", tags="caso"
        )

        def color(evento):
            hover = evento.type == tk.EventType.Enter
            izquierda.itemconfig(
                circulo,
                fill="#A78BFA" if hover else "#C4B5FD",
                outline="#7C3AED" if hover else "#8B5CF6"
            )
            izquierda.config(cursor="hand2" if hover else "")

        izquierda.tag_bind("caso", "<Button-1>",
                           lambda e: self.cargar_caso_adverso())
        izquierda.tag_bind("caso", "<Enter>", color)
        izquierda.tag_bind("caso", "<Leave>", color)

        marco = tk.Frame(fila_tablero, bg="#64748B", padx=3, pady=3, cursor="hand2")
        marco.pack(side="left", padx=(8, 8))

        self.marco = marco
        marco.bind("<Button-1>", self.generar)

        derecha = self.nuevo_lienzo(fila_tablero, width=65, height=60)
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
            boton = self.nuevo_lienzo(
                columna_izquierda, width=360, height=32, cursor="hand2"
            )
            boton.pack(pady=2)

            puntos = []
            for x, y, inicio in [(352, 6, -90), (352, 26, 0),
                                 (8, 26, 90), (8, 6, 180)]:
                for angulo in range(inicio, inicio + 91, 15):
                    rad = math.radians(angulo)
                    puntos.extend((x + 6 * math.cos(rad),
                                   y + 6 * math.sin(rad)))

            fondo = boton.create_polygon(
                *puntos, fill="#0F766E", outline="#0F766E"
            )

            boton.create_text(
                180, 16, text=f"Resolver con {nombre}",
                font=("Arial", 11, "bold"), fill="white"
            )

            boton.bind("<Button-1>", lambda e: funcion())
            boton.bind("<Enter>", lambda e: boton.itemconfig(
                fondo, fill="#0D665F", outline="#0D665F"))
            boton.bind("<Leave>", lambda e: boton.itemconfig(
                fondo, fill="#0F766E", outline="#0F766E"))

        for nombre, _ in RESOLUTORES:
            crear_boton(
                nombre,
                lambda n=nombre: self.resolver(n)
            )

        self.update_idletasks()

        ancho = self.winfo_width()
        alto = self.winfo_height()

        x = (self.winfo_screenwidth() - ancho) // 2
        y = 50

        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.update_idletasks()
        for lienzo in self.lienzos:
            lienzo.pintar_cuadricula()

    def nuevo_lienzo(self, master, **kw):
        lienzo = CanvasCuadricula(master, bg=self.color_fondo, **kw)
        self.lienzos.append(lienzo)
        return lienzo

    def redibujar_panel(self, evento):
        canvas = self.panel_comparacion
        canvas.delete("fondo_panel")

        self.dibujar_redondeado(
            canvas, 0, 0, evento.width - 1, evento.height - 1,
            18, COLOR_PANEL, etiqueta="fondo_panel"
        )
        canvas.tag_lower("fondo_panel")
        canvas.tag_lower("cuadricula")

        canvas.itemconfigure(
            self.ventana_panel,
            width=evento.width - 36,
            height=evento.height - 32
        )

    def dibujar_redondeado(self, canvas, x1, y1, x2, y2, radio, color,
                           etiqueta=""):
        puntos = []

        for x, y, inicio in [
            (x1 + radio, y1 + radio, 180),
            (x2 - radio, y1 + radio, 270),
            (x2 - radio, y2 - radio, 0),
            (x1 + radio, y2 - radio, 90)
        ]:
            for angulo in range(inicio, inicio + 91, 10):
                rad = math.radians(angulo)
                puntos.extend((x + radio * math.cos(rad),
                               y + radio * math.sin(rad)))

        canvas.create_polygon(
            *puntos, fill=color, outline=color, smooth=True, tags=etiqueta
        )

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
        self.limpiar_comparacion()

    def resolver(self, nombre):
        resultados = comparar_resolutores(self.tablero)
        resueltos = [r for r in resultados if r["resuelto"]]

        mas_rapido = min(
            resueltos,
            key=lambda r: r["tiempo"]
        ) if resueltos else None

        mayor_tiempo = max((r["tiempo"] for r in resultados), default=0)

        for resultado in resultados:
            algoritmo = resultado["algoritmo"]
            tarjeta = self.resultados_comparacion[algoritmo]

            es_mas_rapido = (
                    mas_rapido is not None
                    and algoritmo == mas_rapido["algoritmo"]
            )
            fraccion = (
                resultado["tiempo"] / mayor_tiempo if mayor_tiempo > 0 else 0
            )
            tarjeta.mostrar(resultado, es_mas_rapido, fraccion)

        elegido = next(r for r in resultados if r["algoritmo"] == nombre)

        self.dibujar_tablero(
            elegido["solucion"] if elegido["solucion"] is not None
            else self.tablero,
            resuelto=elegido["solucion"] is not None
        )

    def limpiar_comparacion(self):
        for tarjeta in self.resultados_comparacion.values():
            tarjeta.reiniciar()

    def cargar_caso_adverso(self):
        self.es_caso_adverso = True
        self.tablero = copiar_tablero(SUDOKU_SIN_SOLUCION)
        self.dibujar_tablero(self.tablero)
        self.limpiar_comparacion()

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
        self.etiqueta_dificultad.itemconfig(
            self.texto_dificultad,
            text=nombre,
            fill=self.colores_dificultad[nombre]
        )

        self.dibujar_control_dificultad()

    def dibujar_control_dificultad(self):
        barra = self.control_dificultad
        barra.limpiar()

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
            color = "#E7ECF3" if (x // paso) % 3 == 0 else "#C0CAD6"
            fondo.create_line(x, 0, x, evento.height, fill=color)

        for y in range(0, evento.height, paso):
            color = "#E7ECF3" if (y // paso) % 3 == 0 else "#C0CAD6"
            fondo.create_line(0, y, evento.width, y, fill=color)