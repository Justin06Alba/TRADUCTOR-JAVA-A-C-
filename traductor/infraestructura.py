"""Infraestructura comun: errores, resultados de fase y tabla de simbolos."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------- Errores

@dataclass
class Error:
    """Error generico de cualquier fase (lexico, sintactico, semantico)."""
    fase: str            # "LEXICO" | "SINTACTICO" | "SEMANTICO"
    mensaje: str
    line: int = 0
    column: int = 0
    token_encontrado: str = ""

    def __str__(self) -> str:
        return f"[{self.fase}] {self.line}:{self.column} {self.mensaje}"


# ---------------------------------------------------------------- Resultados

@dataclass
class ParseResult:
    """Resultado del analisis sintactico."""
    ast: Optional[object]
    errores: List[Error] = field(default_factory=list)

    @property
    def exitoso(self) -> bool:
        return self.ast is not None and not self.errores


@dataclass
class SemanticResult:
    """Resultado del analisis semantico."""
    ast_validado: Optional[object]
    simbolos: List["Simbolo"] = field(default_factory=list)
    errores: List[Error] = field(default_factory=list)

    @property
    def exitoso(self) -> bool:
        return not self.errores


# ---------------------------------------------------------------- Simbolos

@dataclass
class Simbolo:
    nombre: str
    categoria: str       # "clase" | "interfaz" | "campo" | "metodo" |
                         # "parametro" | "variable"
    tipo: str = ""       # representacion textual del tipo, si aplica
    line: int = 0
    column: int = 0
    ambito: int = 0


class TablaSimbolos:
    """Pila de ambitos.

    El indice 0 es el ambito global. Cada bloque '{ }', clase o metodo crea
    su propio ambito.
    """

    def __init__(self) -> None:
        self._scopes: List[Dict[str, Simbolo]] = [{}]
        self._historico: List[Simbolo] = []

    @property
    def nivel_actual(self) -> int:
        return len(self._scopes) - 1

    def entrar_ambito(self) -> None:
        self._scopes.append({})

    def salir_ambito(self) -> None:
        if len(self._scopes) > 1:
            self._scopes.pop()

    def declarar(self, simbolo: Simbolo) -> bool:
        """Declara un simbolo en el ambito actual.

        Retorna False si ya existia en el ambito actual (redeclaracion).
        """
        actual = self._scopes[-1]
        if simbolo.nombre in actual:
            return False
        simbolo.ambito = self.nivel_actual
        actual[simbolo.nombre] = simbolo
        self._historico.append(simbolo)
        return True

    def buscar(self, nombre: str) -> Optional[Simbolo]:
        """Busca desde el ambito mas interno hacia el global."""
        for scope in reversed(self._scopes):
            if nombre in scope:
                return scope[nombre]
        return None

    def existe(self, nombre: str) -> bool:
        return self.buscar(nombre) is not None

    def declarado_en_actual(self, nombre: str) -> bool:
        return nombre in self._scopes[-1]

    def todos(self) -> List[Simbolo]:
        return list(self._historico)
