"""Interfaz grafica del traductor Java -> C#."""

from __future__ import annotations

import os
from tkinter import filedialog

import customtkinter as ctk

from traductor.main import traducir_texto

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

_FUENTE_CODIGO = ("Consolas", 13)

_EJEMPLO = """public class Hola {
    private String nombre;

    public Hola(String nombre) {
        this.nombre = nombre;
    }

    public void saludar() {
        System.out.println("Hola, " + nombre);
    }
}
"""


class TraductorGUI(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Traductor Java -> C#")
        self.geometry("1180x780")
        self.minsize(900, 600)

        self._crear_widgets()
        self.entrada.insert("1.0", _EJEMPLO)

    # ------------------------------------------------------------------ UI

    def _crear_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Java (entrada)",
                     font=("Consolas", 13, "bold"), anchor="w").grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 0))
        ctk.CTkLabel(self, text="C# (salida)",
                     font=("Consolas", 13, "bold"), anchor="w").grid(
            row=0, column=1, sticky="w", padx=12, pady=(10, 0))

        self.entrada = ctk.CTkTextbox(self, font=_FUENTE_CODIGO, wrap="none")
        self.entrada.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=6)

        self.salida = ctk.CTkTextbox(self, font=_FUENTE_CODIGO, wrap="none")
        self.salida.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=6)

        # Botones
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=4)

        ctk.CTkButton(barra, text="Abrir .java", width=120,
                      command=self.on_abrir).pack(side="left", padx=(0, 8))
        ctk.CTkButton(barra, text="Traducir  ->", width=140,
                      command=self.on_traducir).pack(side="left", padx=8)
        ctk.CTkButton(barra, text="Guardar .cs", width=120,
                      command=self.on_guardar).pack(side="left", padx=8)
        ctk.CTkButton(barra, text="Limpiar", width=100, fg_color="gray30",
                      hover_color="gray25",
                      command=self.on_limpiar).pack(side="left", padx=8)

        # Consola de mensajes / errores
        ctk.CTkLabel(self, text="Mensajes",
                     font=("Consolas", 12, "bold"), anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="w", padx=12, pady=(6, 0))
        self.consola = ctk.CTkTextbox(self, height=140, font=("Consolas", 12))
        self.consola.grid(row=4, column=0, columnspan=2, sticky="ew",
                          padx=12, pady=(0, 12))
        self.consola.configure(state="disabled")

    # ------------------------------------------------------------ acciones

    def on_abrir(self) -> None:
        ruta = filedialog.askopenfilename(
            title="Abrir archivo Java",
            filetypes=[("Archivos Java", "*.java"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except OSError as e:
            self._mensaje(f"No se pudo abrir el archivo: {e}", error=True)
            return
        self.entrada.delete("1.0", "end")
        self.entrada.insert("1.0", contenido)
        self._mensaje(f"Archivo cargado: {ruta}")

    def on_traducir(self) -> None:
        fuente = self.entrada.get("1.0", "end-1c")
        if not fuente.strip():
            self._mensaje("No hay codigo Java para traducir.", error=True)
            return

        resultado = traducir_texto(fuente)
        self.salida.delete("1.0", "end")

        if resultado.exitoso:
            self.salida.insert("1.0", resultado.codigo)
            self._mensaje("Traduccion correcta.")
        else:
            lineas = ["Se encontraron errores:"]
            lineas += [f"  {e}" for e in resultado.errores]
            self._mensaje("\n".join(lineas), error=True)

    def on_guardar(self) -> None:
        codigo = self.salida.get("1.0", "end-1c")
        if not codigo.strip():
            self._mensaje("No hay codigo C# para guardar. Traduce primero.",
                          error=True)
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo C#", defaultextension=".cs",
            filetypes=[("Archivos C#", "*.cs"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(codigo)
        except OSError as e:
            self._mensaje(f"No se pudo guardar el archivo: {e}", error=True)
            return
        self._mensaje(f"Guardado en: {ruta}")

    def on_limpiar(self) -> None:
        self.entrada.delete("1.0", "end")
        self.salida.delete("1.0", "end")
        self._mensaje("")

    # ------------------------------------------------------------- helpers

    def _mensaje(self, texto: str, error: bool = False) -> None:
        self.consola.configure(state="normal")
        self.consola.delete("1.0", "end")
        self.consola.insert("1.0", texto)
        self.consola.configure(
            state="disabled",
            text_color="#ff6b6b" if error else "#9ad19a")


def main() -> None:
    app = TraductorGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
