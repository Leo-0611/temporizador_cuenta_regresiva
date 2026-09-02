import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os


ARCHIVO_EVENTOS = "events.json"


# ==========================================
# SISTEMA DE DISEÑO (paleta, tipografía)
# ==========================================
# Paleta "slate + indigo": fondo azul-carbón muy oscuro, tarjetas
# ligeramente más claras y un acento índigo, un lenguaje visual
# habitual en herramientas de productividad actuales (Linear,
# Notion, apps de escritorio modernas), pensado para transmitir
# calma y precisión en algo que el usuario mirará repetidamente.

BG = "#0F1420"            # fondo general
BG_PANEL = "#171E2E"      # tarjetas
BG_INPUT = "#1E2739"      # campos de entrada
BORDER = "#2A3346"        # bordes sutiles
BORDER_FOCUS = "#6366F1"  # borde al enfocar

ACCENT = "#6366F1"        # índigo — acción principal
ACCENT_HOVER = "#818CF8"
ACCENT_PRESSED = "#4F46E5"

DANGER = "#F87171"
DANGER_HOVER = "#FCA5A5"
DANGER_PRESSED = "#EF4444"

SUCCESS = "#34D399"

TEXT = "#F1F5F9"           # texto principal
TEXT_MUTED = "#94A3B8"     # texto secundario
TEXT_FAINT = "#5B6478"     # texto terciario / placeholders

FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"


class BotonPlano(tk.Button):
    """Botón plano con esquinas rectas pero interacción moderna:
    cambia de color al pasar el mouse y al presionar."""

    def __init__(self, master, texto, comando, color_base,
                 color_hover, color_presionado, color_texto="#FFFFFF",
                 ancho=None, grande=False, **kwargs):
        fuente = (FONT_FAMILY, 12 if grande else 10, "bold")
        super().__init__(
            master,
            text=texto,
            command=comando,
            font=fuente,
            bg=color_base,
            fg=color_texto,
            activebackground=color_presionado,
            activeforeground=color_texto,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=10 if grande else 8,
            width=ancho,
            **kwargs
        )
        self._base = color_base
        self._hover = color_hover
        self.bind("<Enter>", lambda e: self.config(bg=self._hover))
        self.bind("<Leave>", lambda e: self.config(bg=self._base))


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cuenta Regresiva")
        self.root.geometry("760x720")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.evento_actual = None
        self.contando = False

        self.crear_interfaz()
        self.cargar_eventos()

    # ==========================================
    # INTERFAZ
    # ==========================================

    def crear_interfaz(self):

        contenedor = tk.Frame(self.root, bg=BG)
        contenedor.pack(fill="both", expand=True, padx=32, pady=28)

        # ---------- Encabezado ----------
        encabezado = tk.Frame(contenedor, bg=BG)
        encabezado.pack(fill="x", pady=(0, 22))

        tk.Label(
            encabezado,
            text="Cuenta regresiva",
            font=(FONT_FAMILY, 24, "bold"),
            bg=BG,
            fg=TEXT,
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            encabezado,
            text="Crea un evento y sigue el tiempo que falta para que ocurra.",
            font=(FONT_FAMILY, 11),
            bg=BG,
            fg=TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(2, 0))

        # ---------- Tarjeta: nuevo evento ----------
        tarjeta_form = self._crear_tarjeta(contenedor)
        tarjeta_form.pack(fill="x", pady=(0, 18))

        tk.Label(
            tarjeta_form,
            text="Nuevo evento",
            font=(FONT_FAMILY, 13, "bold"),
            bg=BG_PANEL,
            fg=TEXT
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 14))

        self.nombre_entry = self._crear_campo(
            tarjeta_form, "Nombre del evento", 1
        )
        self.fecha_entry = self._crear_campo(
            tarjeta_form, "Fecha (DD/MM/AAAA)", 2
        )
        self.hora_entry = self._crear_campo(
            tarjeta_form, "Hora (HH:MM) — opcional", 3
        )

        boton_iniciar = BotonPlano(
            tarjeta_form,
            texto="Iniciar cuenta regresiva",
            comando=self.iniciar_evento,
            color_base=ACCENT,
            color_hover=ACCENT_HOVER,
            color_presionado=ACCENT_PRESSED,
            grande=True
        )
        boton_iniciar.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=(6, 20))

        tarjeta_form.grid_columnconfigure(0, weight=1)
        tarjeta_form.grid_columnconfigure(1, weight=1)

        # ---------- Tarjeta: temporizador ----------
        tarjeta_contador = self._crear_tarjeta(contenedor)
        tarjeta_contador.pack(fill="x", pady=(0, 18))

        self.evento_label = tk.Label(
            tarjeta_contador,
            text="Ningún evento seleccionado",
            font=(FONT_FAMILY, 12, "bold"),
            bg=BG_PANEL,
            fg=TEXT_MUTED
        )
        self.evento_label.pack(pady=(20, 6))

        self.contador_label = tk.Label(
            tarjeta_contador,
            text="00 : 00 : 00 : 00",
            font=(FONT_MONO, 40, "bold"),
            bg=BG_PANEL,
            fg=ACCENT_HOVER
        )
        self.contador_label.pack(pady=(0, 4))

        etiquetas = tk.Frame(tarjeta_contador, bg=BG_PANEL)
        etiquetas.pack(pady=(0, 22))

        for texto in ("DÍAS", "HORAS", "MINUTOS", "SEGUNDOS"):
            tk.Label(
                etiquetas,
                text=texto,
                font=(FONT_FAMILY, 9, "bold"),
                bg=BG_PANEL,
                fg=TEXT_FAINT,
                width=13
            ).pack(side="left")

        # ---------- Tarjeta: eventos guardados ----------
        tarjeta_lista = self._crear_tarjeta(contenedor)
        tarjeta_lista.pack(fill="both", expand=True)

        tk.Label(
            tarjeta_lista,
            text="Eventos guardados",
            font=(FONT_FAMILY, 13, "bold"),
            bg=BG_PANEL,
            fg=TEXT
        ).pack(anchor="w", padx=20, pady=(18, 10))

        zona_lista = tk.Frame(tarjeta_lista, bg=BG_PANEL)
        zona_lista.pack(fill="both", expand=True, padx=20)

        barra_scroll = tk.Scrollbar(zona_lista, bg=BG_PANEL, troughcolor=BG_PANEL, bd=0)
        barra_scroll.pack(side="right", fill="y")

        self.lista_eventos = tk.Listbox(
            zona_lista,
            font=(FONT_FAMILY, 11),
            bg=BG_INPUT,
            fg=TEXT,
            selectbackground=ACCENT,
            selectforeground="#FFFFFF",
            activestyle="none",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BORDER_FOCUS,
            height=7,
            yscrollcommand=barra_scroll.set
        )
        self.lista_eventos.pack(side="left", fill="both", expand=True)
        barra_scroll.config(command=self.lista_eventos.yview)

        botones = tk.Frame(tarjeta_lista, bg=BG_PANEL)
        botones.pack(fill="x", padx=20, pady=18)

        BotonPlano(
            botones,
            texto="Seleccionar evento",
            comando=self.seleccionar_evento,
            color_base=BG_INPUT,
            color_hover=BORDER,
            color_presionado=BORDER,
            color_texto=TEXT
        ).pack(side="left")

        BotonPlano(
            botones,
            texto="Eliminar evento",
            comando=self.eliminar_evento,
            color_base=DANGER_PRESSED,
            color_hover=DANGER_HOVER,
            color_presionado=DANGER
        ).pack(side="left", padx=(10, 0))

    # ---------- utilidades de interfaz ----------

    def _crear_tarjeta(self, master):
        return tk.Frame(
            master,
            bg=BG_PANEL,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BORDER
        )

    def _crear_campo(self, master, etiqueta, fila):
        envoltorio = tk.Frame(master, bg=BG_PANEL)
        envoltorio.grid(row=fila, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 12))

        tk.Label(
            envoltorio,
            text=etiqueta,
            font=(FONT_FAMILY, 10),
            bg=BG_PANEL,
            fg=TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        entrada = tk.Entry(
            envoltorio,
            font=(FONT_FAMILY, 12),
            bg=BG_INPUT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BORDER_FOCUS
        )
        entrada.pack(fill="x", ipady=8)
        return entrada

    # ==========================================
    # INICIAR EVENTO
    # ==========================================

    def iniciar_evento(self):

        nombre = self.nombre_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        hora = self.hora_entry.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Advertencia",
                "El nombre del evento no puede estar vacío."
            )
            return

        if hora == "":
            hora = "00:00"

        try:
            fecha_evento = datetime.strptime(
                fecha + " " + hora,
                "%d/%m/%Y %H:%M"
            )

        except ValueError:
            messagebox.showwarning(
                "Fecha incorrecta",
                "La fecha debe tener el formato DD/MM/AAAA "
                "y la hora HH:MM."
            )
            return

        ahora = datetime.now()

        if fecha_evento <= ahora:
            messagebox.showwarning(
                "Evento inválido",
                "La fecha y hora del evento deben ser futuras."
            )
            return

        evento = {
            "nombre": nombre,
            "fecha": fecha_evento.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.evento_actual = evento
        self.contando = True

        self.guardar_evento(evento)
        self.actualizar_lista()

        self.evento_label.config(
            text="Evento: " + nombre,
            fg=TEXT
        )

        self.actualizar_contador()

    # ==========================================
    # CUENTA REGRESIVA
    # ==========================================

    def actualizar_contador(self):

        if not self.contando or self.evento_actual is None:
            return

        fecha_evento = datetime.strptime(
            self.evento_actual["fecha"],
            "%Y-%m-%d %H:%M:%S"
        )

        ahora = datetime.now()

        diferencia = fecha_evento - ahora

        segundos_totales = int(diferencia.total_seconds())

        if segundos_totales <= 0:

            self.contador_label.config(
                text="00 : 00 : 00 : 00",
                fg=SUCCESS
            )

            self.contando = False

            messagebox.showinfo(
                "¡Evento!",
                "¡Ha llegado el momento de: "
                + self.evento_actual["nombre"]
                + "!"
            )

            return

        dias = segundos_totales // 86400
        segundos_restantes = segundos_totales % 86400

        horas = segundos_restantes // 3600
        segundos_restantes %= 3600

        minutos = segundos_restantes // 60
        segundos = segundos_restantes % 60

        self.contador_label.config(
            text=f"{dias:02d} : {horas:02d} : "
                 f"{minutos:02d} : {segundos:02d}",
            fg=ACCENT_HOVER
        )

        self.root.after(
            1000,
            self.actualizar_contador
        )

    # ==========================================
    # GUARDAR EVENTOS
    # ==========================================

    def guardar_evento(self, nuevo_evento):

        eventos = []

        if os.path.exists(ARCHIVO_EVENTOS):

            try:
                with open(
                    ARCHIVO_EVENTOS,
                    "r",
                    encoding="utf-8"
                ) as archivo:

                    eventos = json.load(archivo)

            except:
                eventos = []

        existe = False

        for evento in eventos:

            if (
                evento["nombre"] == nuevo_evento["nombre"]
                and
                evento["fecha"] == nuevo_evento["fecha"]
            ):
                existe = True
                break

        if not existe:
            eventos.append(nuevo_evento)

        with open(
            ARCHIVO_EVENTOS,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                eventos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    # ==========================================
    # CARGAR EVENTOS
    # ==========================================

    def cargar_eventos(self):

        if not os.path.exists(ARCHIVO_EVENTOS):
            return

        try:

            with open(
                ARCHIVO_EVENTOS,
                "r",
                encoding="utf-8"
            ) as archivo:

                eventos = json.load(archivo)

            for evento in eventos:

                fecha = datetime.strptime(
                    evento["fecha"],
                    "%Y-%m-%d %H:%M:%S"
                )

                texto = (
                    evento["nombre"]
                    + "  ·  "
                    + fecha.strftime("%d/%m/%Y %H:%M")
                )

                self.lista_eventos.insert(
                    tk.END,
                    texto
                )

        except:
            pass

    # ==========================================
    # ACTUALIZAR LISTA
    # ==========================================

    def actualizar_lista(self):

        self.lista_eventos.delete(
            0,
            tk.END
        )

        if not os.path.exists(ARCHIVO_EVENTOS):
            return

        try:

            with open(
                ARCHIVO_EVENTOS,
                "r",
                encoding="utf-8"
            ) as archivo:

                eventos = json.load(archivo)

            for evento in eventos:

                fecha = datetime.strptime(
                    evento["fecha"],
                    "%Y-%m-%d %H:%M:%S"
                )

                texto = (
                    evento["nombre"]
                    + "  ·  "
                    + fecha.strftime("%d/%m/%Y %H:%M")
                )

                self.lista_eventos.insert(
                    tk.END,
                    texto
                )

        except:
            pass

    # ==========================================
    # SELECCIONAR EVENTO
    # ==========================================

    def seleccionar_evento(self):

        seleccion = self.lista_eventos.curselection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un evento."
            )
            return

        indice = seleccion[0]

        try:

            with open(
                ARCHIVO_EVENTOS,
                "r",
                encoding="utf-8"
            ) as archivo:

                eventos = json.load(archivo)

            evento = eventos[indice]

            self.evento_actual = evento
            self.contando = True

            fecha = datetime.strptime(
                evento["fecha"],
                "%Y-%m-%d %H:%M:%S"
            )

            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(
                0,
                evento["nombre"]
            )

            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(
                0,
                fecha.strftime("%d/%m/%Y")
            )

            self.hora_entry.delete(0, tk.END)
            self.hora_entry.insert(
                0,
                fecha.strftime("%H:%M")
            )

            self.evento_label.config(
                text="Evento: " + evento["nombre"],
                fg=TEXT
            )

            self.actualizar_contador()

        except Exception as error:

            messagebox.showerror(
                "Error",
                "No se pudo seleccionar el evento."
            )

    # ==========================================
    # ELIMINAR EVENTO
    # ==========================================

    def eliminar_evento(self):

        seleccion = self.lista_eventos.curselection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un evento para eliminar."
            )
            return

        indice = seleccion[0]

        if not messagebox.askyesno(
            "Confirmar",
            "¿Quieres eliminar este evento?"
        ):
            return

        try:

            with open(
                ARCHIVO_EVENTOS,
                "r",
                encoding="utf-8"
            ) as archivo:

                eventos = json.load(archivo)

            eventos.pop(indice)

            with open(
                ARCHIVO_EVENTOS,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    eventos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            self.contando = False
            self.evento_actual = None

            self.actualizar_lista()

            self.contador_label.config(
                text="00 : 00 : 00 : 00",
                fg=ACCENT_HOVER
            )

            self.evento_label.config(
                text="Ningún evento seleccionado",
                fg=TEXT_MUTED
            )

        except Exception:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el evento."
            )


# ==========================================
# EJECUTAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CountdownTimer(root)

    root.mainloop()
