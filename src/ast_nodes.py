from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    line: int
    column: int

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    @staticmethod
    def _indentar(texto: str, nivel: int) -> str:
        sangria = "  " * nivel
        return "\n".join(sangria + l for l in texto.splitlines())


@dataclass
class ProgramaNode(ASTNode):
    declaraciones: list[ASTNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo": "ProgramaNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "Programa",
            "hijos": [d.to_dict() for d in self.declaraciones],
        }

    def __repr__(self) -> str:
        hijos = "\n".join(ASTNode._indentar(repr(d), 1) for d in self.declaraciones)
        return f"ProgramaNode(\n{hijos}\n)" if hijos else "ProgramaNode()"


@dataclass
class DeclaracionVarNode(ASTNode):
    tipo: str = ""
    nombre: str = ""
    valor_inicial: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        hijos = [self.valor_inicial.to_dict()] if self.valor_inicial else []
        return {
            "tipo": "DeclaracionVarNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": f"var {self.tipo} {self.nombre}",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        vi = ASTNode._indentar(repr(self.valor_inicial), 1) if self.valor_inicial else "  None"
        return f"DeclaracionVarNode(tipo='{self.tipo}', nombre='{self.nombre}',\n{vi}\n)"


@dataclass
class AsignacionNode(ASTNode):
    nombre: str = ""
    valor: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        hijos = [self.valor.to_dict()] if self.valor else []
        return {
            "tipo": "AsignacionNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": f"{self.nombre} =",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        val = ASTNode._indentar(repr(self.valor), 1) if self.valor else "  None"
        return f"AsignacionNode(nombre='{self.nombre}',\n{val}\n)"


@dataclass
class SiNode(ASTNode):
    condicion: ASTNode | None = None
    entonces: "BloqueNode | None" = None
    sino: "BloqueNode | None" = None

    def to_dict(self) -> dict[str, Any]:
        hijos = []
        if self.condicion:
            d = self.condicion.to_dict()
            d["etiqueta"] = "[condicion] " + d["etiqueta"]
            hijos.append(d)
        if self.entonces:
            d = self.entonces.to_dict()
            d["etiqueta"] = "[entonces] " + d["etiqueta"]
            hijos.append(d)
        if self.sino:
            d = self.sino.to_dict()
            d["etiqueta"] = "[sino] " + d["etiqueta"]
            hijos.append(d)
        return {
            "tipo": "SiNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "si",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        cond = ASTNode._indentar(repr(self.condicion), 1)
        ent = ASTNode._indentar(repr(self.entonces), 1)
        s = ASTNode._indentar(repr(self.sino), 1) if self.sino else "  None"
        return f"SiNode(\n{cond},\n{ent},\n{s}\n)"


@dataclass
class MientrasNode(ASTNode):
    condicion: ASTNode | None = None
    cuerpo: "BloqueNode | None" = None

    def to_dict(self) -> dict[str, Any]:
        hijos = []
        if self.condicion:
            d = self.condicion.to_dict()
            d["etiqueta"] = "[condicion] " + d["etiqueta"]
            hijos.append(d)
        if self.cuerpo:
            hijos.append(self.cuerpo.to_dict())
        return {
            "tipo": "MientrasNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "mientras",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        cond = ASTNode._indentar(repr(self.condicion), 1)
        cuerpo = ASTNode._indentar(repr(self.cuerpo), 1)
        return f"MientrasNode(\n{cond},\n{cuerpo}\n)"


@dataclass
class ParaNode(ASTNode):
    inicio: ASTNode | None = None
    condicion: ASTNode | None = None
    paso: ASTNode | None = None
    cuerpo: "BloqueNode | None" = None

    def to_dict(self) -> dict[str, Any]:
        hijos = []
        for etiq, nodo in [("[inicio]", self.inicio), ("[condicion]", self.condicion),
                           ("[paso]", self.paso), ("[cuerpo]", self.cuerpo)]:
            if nodo:
                d = nodo.to_dict()
                d["etiqueta"] = etiq + " " + d["etiqueta"]
                hijos.append(d)
        return {
            "tipo": "ParaNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "para",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        ini = ASTNode._indentar(repr(self.inicio), 1)
        cond = ASTNode._indentar(repr(self.condicion), 1)
        paso = ASTNode._indentar(repr(self.paso), 1)
        cuerpo = ASTNode._indentar(repr(self.cuerpo), 1)
        return f"ParaNode(\n{ini},\n{cond},\n{paso},\n{cuerpo}\n)"


@dataclass
class RetornarNode(ASTNode):
    valor: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        hijos = [self.valor.to_dict()] if self.valor else []
        return {
            "tipo": "RetornarNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "retornar",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        val = ASTNode._indentar(repr(self.valor), 1) if self.valor else "  None"
        return f"RetornarNode(\n{val}\n)"


@dataclass
class BloqueNode(ASTNode):
    declaraciones: list[ASTNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo": "BloqueNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": "{ bloque }",
            "hijos": [d.to_dict() for d in self.declaraciones],
        }

    def __repr__(self) -> str:
        hijos = "\n".join(ASTNode._indentar(repr(d), 1) for d in self.declaraciones)
        return f"BloqueNode(\n{hijos}\n)" if hijos else "BloqueNode()"


@dataclass
class BinOpNode(ASTNode):
    operador: str = ""
    izquierda: ASTNode | None = None
    derecha: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        hijos = []
        if self.izquierda:
            hijos.append(self.izquierda.to_dict())
        if self.derecha:
            hijos.append(self.derecha.to_dict())
        return {
            "tipo": "BinOpNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": self.operador,
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        izq = ASTNode._indentar(repr(self.izquierda), 1)
        der = ASTNode._indentar(repr(self.derecha), 1)
        return f"BinOpNode(op='{self.operador}',\n{izq},\n{der}\n)"


@dataclass
class UnOpNode(ASTNode):
    operador: str = ""
    operando: ASTNode | None = None

    def to_dict(self) -> dict[str, Any]:
        hijos = [self.operando.to_dict()] if self.operando else []
        return {
            "tipo": "UnOpNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": f"! {self.operador}",
            "hijos": hijos,
        }

    def __repr__(self) -> str:
        op = ASTNode._indentar(repr(self.operando), 1)
        return f"UnOpNode(op='{self.operador}',\n{op}\n)"


@dataclass
class LiteralNode(ASTNode):
    valor: str = ""
    tipo_literal: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo": "LiteralNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": f"{self.valor} ({self.tipo_literal})",
            "hijos": [],
        }

    def __repr__(self) -> str:
        return f"LiteralNode(valor='{self.valor}', tipo='{self.tipo_literal}')"


@dataclass
class IdentificadorNode(ASTNode):
    nombre: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "tipo": "IdentificadorNode",
            "linea": self.line,
            "columna": self.column,
            "etiqueta": self.nombre,
            "hijos": [],
        }

    def __repr__(self) -> str:
        return f"IdentificadorNode(nombre='{self.nombre}')"
