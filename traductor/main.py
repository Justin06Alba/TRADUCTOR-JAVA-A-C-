"""Orquestador del traductor Java -> C#.

Fases del pipeline:

    1. Lexico        (ANTLR)
    2. Sintactico    (ANTLR)
    3. Construccion de AST
    4. Semantico
    5. Generacion de C#

Uso:
    python -m traductor.main entrada.java [-o salida.cs]
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))
from JavaSubsetLexer import JavaSubsetLexer            # noqa: E402
from JavaSubsetParser import JavaSubsetParser          # noqa: E402

from traductor.ast_builder import ASTBuilder           # noqa: E402
from traductor.semantico import AnalizadorSemantico    # noqa: E402
from traductor.generador_csharp import GeneradorCSharp # noqa: E402
from traductor.infraestructura import Error            # noqa: E402


class _ColectorErrores(ErrorListener):
    """Captura errores lexicos/sintacticos de ANTLR como objetos Error."""

    def __init__(self, fase: str) -> None:
        super().__init__()
        self.errores: List[Error] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        token = offendingSymbol.text if offendingSymbol is not None else ""
        fase = "LEXICO" if recognizer.__class__.__name__.endswith("Lexer") else "SINTACTICO"
        self.errores.append(Error(fase=fase, mensaje=msg, line=line,
                                  column=column, token_encontrado=token or ""))


@dataclass
class TraduccionResult:
    codigo: Optional[str]
    errores: List[Error] = field(default_factory=list)
    simbolos: list = field(default_factory=list)

    @property
    def exitoso(self) -> bool:
        return self.codigo is not None and not self.errores


def traducir_texto(fuente: str) -> TraduccionResult:
    """Traduce codigo Java (texto) a C#. No lanza excepciones."""
    # --- 1. Lexico ---
    lexer = JavaSubsetLexer(InputStream(fuente))
    col_lex = _ColectorErrores("LEXICO")
    lexer.removeErrorListeners()
    lexer.addErrorListener(col_lex)

    # --- 2. Sintactico ---
    parser = JavaSubsetParser(CommonTokenStream(lexer))
    col_sin = _ColectorErrores("SINTACTICO")
    parser.removeErrorListeners()
    parser.addErrorListener(col_sin)

    tree = parser.compilationUnit()
    errores = col_lex.errores + col_sin.errores
    if errores:
        return TraduccionResult(codigo=None, errores=errores)

    # --- 3. Construccion de AST ---
    try:
        unidad = ASTBuilder().visit(tree)
    except Exception as e:  # pragma: no cover - defensivo
        return TraduccionResult(codigo=None, errores=[
            Error(fase="AST", mensaje=f"Error construyendo AST: {e}")])

    # --- 4. Semantico ---
    resultado = AnalizadorSemantico(unidad).analizar()
    if not resultado.exitoso:
        return TraduccionResult(codigo=None, errores=resultado.errores,
                                simbolos=resultado.simbolos)

    # --- 5. Generacion C# ---
    codigo = GeneradorCSharp().generar(resultado.ast_validado)
    return TraduccionResult(codigo=codigo, errores=[],
                            simbolos=resultado.simbolos)


def traducir_archivo(ruta_entrada: str, ruta_salida: Optional[str] = None) -> TraduccionResult:
    with open(ruta_entrada, "r", encoding="utf-8") as f:
        fuente = f.read()
    resultado = traducir_texto(fuente)
    if resultado.exitoso:
        if ruta_salida is None:
            ruta_salida = os.path.splitext(ruta_entrada)[0] + ".cs"
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(resultado.codigo)
    return resultado


def main(argv: List[str]) -> int:
    if len(argv) < 1:
        print("Uso: python -m traductor.main <archivo.java> [-o <salida.cs>]")
        return 2

    entrada = argv[0]
    salida = None
    if len(argv) >= 3 and argv[1] == "-o":
        salida = argv[2]

    if not os.path.isfile(entrada):
        print(f"No se encontro el archivo: {entrada}")
        return 2

    print(f"Traduciendo {entrada} ...")
    resultado = traducir_archivo(entrada, salida)

    if not resultado.exitoso:
        print("\nErrores:")
        for e in resultado.errores:
            print(f"  {e}")
        return 1

    destino = salida or (os.path.splitext(entrada)[0] + ".cs")
    print(f"OK -> {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
