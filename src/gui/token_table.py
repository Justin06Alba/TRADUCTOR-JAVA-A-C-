import customtkinter as ctk
from tkinter import ttk
from src.models import Token

TOKEN_COLORS = {
    "PALABRA_RESERVADA": "#569CD6",
    "IDENTIFICADOR":     "#004A72",
    "ENTERO":            "#B5CEA8",
    "DECIMAL":           "#B5CEA8",
    "CADENA":            "#CE9178",
    "OPERADOR_ARIT":     "#D4D4D4",
    "OPERADOR_REL":      "#D4D4D4",
    "OPERADOR_ASIG":     "#D4D4D4",
    "OPERADOR_LOG":      "#D4D4D4",
    "DELIMITADOR":       "#DA70D6",
    "COMENTARIO":        "#6A9955",
    "ERROR_LEXICO":      "#F44747",
}


class TokenTable(ctk.CTkFrame):
    """Tabla de tokens con colorización por tipo y resaltado de errores."""

    TOKEN_COLORS = TOKEN_COLORS

    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(
            self,
            columns=("num", "line", "col", "type", "lexeme"),
            show="headings",
            height=15,
        )

        self.tree.heading("num",    text="N°")
        self.tree.heading("line",   text="Línea")
        self.tree.heading("col",    text="Columna")
        self.tree.heading("type",   text="Tipo")
        self.tree.heading("lexeme", text="Lexema")

        self.tree.column("num",    width=50,  anchor="center", stretch=False)
        self.tree.column("line",   width=80,  anchor="center", stretch=False)
        self.tree.column("col",    width=80,  anchor="center", stretch=False)
        self.tree.column("type",   width=200, anchor="w",      stretch=True)
        self.tree.column("lexeme", width=200, anchor="w",      stretch=True)

        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._configure_token_tags()

    def _configure_token_tags(self):
        for token_type, color in TOKEN_COLORS.items():
            if token_type == "ERROR_LEXICO":
                self.tree.tag_configure(token_type, foreground=color, background="#3D1F1F")
            else:
                self.tree.tag_configure(token_type, foreground=color)

    def display_tokens(self, tokens: list[Token]):
        self.tree.delete(*self.tree.get_children())
        for i, token in enumerate(tokens, start=1):
            tag = token.token_type
            if tag not in TOKEN_COLORS:
                self.tree.tag_configure(tag, foreground="#FFFFFF")
            self.tree.insert(
                "", "end",
                values=(i, token.line, token.column, token.token_type, token.lexeme),
                tags=(tag,),
            )

    def clear(self):
        self.tree.delete(*self.tree.get_children())
