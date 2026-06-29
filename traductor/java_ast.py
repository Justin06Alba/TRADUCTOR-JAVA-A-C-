"""Nodos del AST de Java (subconjunto OO).

Cada nodo es un @dataclass con 'line'/'column' y cubre la estructura de Java:
clases, miembros, sentencias y expresiones.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------- Tipos

@dataclass
class Tipo:
    """Representa un tipo Java: int, String, List<String>, int[], etc."""
    nombre: str
    genericos: List["Tipo"] = field(default_factory=list)
    dims: int = 0          # numero de '[]'

    def __str__(self) -> str:
        base = self.nombre
        if self.genericos:
            gen = ", ".join(str(g) for g in self.genericos)
            base = f"{base}<{gen}>"
        return base + "[]" * self.dims


# ---------------------------------------------------------------- Base

@dataclass
class NodoAST:
    line: int = 0
    column: int = 0


# ---------------------------------------------------------------- Unidad

@dataclass
class CompilationUnit(NodoAST):
    package: Optional["PackageDecl"] = None
    imports: List["ImportDecl"] = field(default_factory=list)
    tipos: List[NodoAST] = field(default_factory=list)


@dataclass
class PackageDecl(NodoAST):
    nombre: str = ""


@dataclass
class ImportDecl(NodoAST):
    nombre: str = ""
    estatico: bool = False
    wildcard: bool = False


# ---------------------------------------------------------------- Tipos (decl)

@dataclass
class ClassDecl(NodoAST):
    nombre: str = ""
    modificadores: List[str] = field(default_factory=list)
    superclase: Optional[Tipo] = None
    interfaces: List[Tipo] = field(default_factory=list)
    miembros: List[NodoAST] = field(default_factory=list)


@dataclass
class InterfaceDecl(NodoAST):
    nombre: str = ""
    modificadores: List[str] = field(default_factory=list)
    interfaces: List[Tipo] = field(default_factory=list)
    miembros: List[NodoAST] = field(default_factory=list)


# ---------------------------------------------------------------- Miembros

@dataclass
class FieldDecl(NodoAST):
    nombre: str = ""
    tipo: Optional[Tipo] = None
    valor: Optional[NodoAST] = None
    modificadores: List[str] = field(default_factory=list)


@dataclass
class MethodDecl(NodoAST):
    nombre: str = ""
    tipo_retorno: Optional[Tipo] = None     # None => void
    parametros: List["Parameter"] = field(default_factory=list)
    cuerpo: Optional["Block"] = None        # None => metodo abstracto/interfaz
    modificadores: List[str] = field(default_factory=list)


@dataclass
class ConstructorDecl(NodoAST):
    nombre: str = ""
    parametros: List["Parameter"] = field(default_factory=list)
    cuerpo: Optional["Block"] = None
    modificadores: List[str] = field(default_factory=list)


@dataclass
class Parameter(NodoAST):
    nombre: str = ""
    tipo: Optional[Tipo] = None
    modificadores: List[str] = field(default_factory=list)


# ---------------------------------------------------------------- Sentencias

@dataclass
class Block(NodoAST):
    sentencias: List[NodoAST] = field(default_factory=list)


@dataclass
class LocalVarDecl(NodoAST):
    nombre: str = ""
    tipo: Optional[Tipo] = None
    valor: Optional[NodoAST] = None


@dataclass
class IfStmt(NodoAST):
    condicion: Optional[NodoAST] = None
    entonces: Optional[NodoAST] = None
    sino: Optional[NodoAST] = None


@dataclass
class ForStmt(NodoAST):
    init: List[NodoAST] = field(default_factory=list)   # decls o exprs
    condicion: Optional[NodoAST] = None
    update: List[NodoAST] = field(default_factory=list)
    cuerpo: Optional[NodoAST] = None


@dataclass
class ForEachStmt(NodoAST):
    tipo: Optional[Tipo] = None
    nombre: str = ""
    iterable: Optional[NodoAST] = None
    cuerpo: Optional[NodoAST] = None


@dataclass
class WhileStmt(NodoAST):
    condicion: Optional[NodoAST] = None
    cuerpo: Optional[NodoAST] = None


@dataclass
class DoWhileStmt(NodoAST):
    cuerpo: Optional[NodoAST] = None
    condicion: Optional[NodoAST] = None


@dataclass
class ReturnStmt(NodoAST):
    valor: Optional[NodoAST] = None


@dataclass
class BreakStmt(NodoAST):
    pass


@dataclass
class ContinueStmt(NodoAST):
    pass


@dataclass
class ThrowStmt(NodoAST):
    valor: Optional[NodoAST] = None


@dataclass
class ExprStmt(NodoAST):
    expr: Optional[NodoAST] = None


# ---------------------------------------------------------------- Expresiones

@dataclass
class IntLiteral(NodoAST):
    valor: str = "0"


@dataclass
class FloatLiteral(NodoAST):
    valor: str = "0.0"


@dataclass
class CharLiteral(NodoAST):
    valor: str = ""


@dataclass
class StringLiteral(NodoAST):
    valor: str = ""          # contenido sin comillas


@dataclass
class BoolLiteral(NodoAST):
    valor: bool = False


@dataclass
class NullLiteral(NodoAST):
    pass


@dataclass
class VarRef(NodoAST):
    nombre: str = ""


@dataclass
class ThisExpr(NodoAST):
    pass


@dataclass
class SuperExpr(NodoAST):
    pass


@dataclass
class FieldAccess(NodoAST):
    objeto: Optional[NodoAST] = None
    nombre: str = ""


@dataclass
class MethodCall(NodoAST):
    objeto: Optional[NodoAST] = None     # None => llamada sin receptor
    nombre: str = ""
    argumentos: List[NodoAST] = field(default_factory=list)


@dataclass
class ArrayAccess(NodoAST):
    objeto: Optional[NodoAST] = None
    indice: Optional[NodoAST] = None


@dataclass
class NewObject(NodoAST):
    tipo: Optional[Tipo] = None
    argumentos: List[NodoAST] = field(default_factory=list)


@dataclass
class NewArray(NodoAST):
    tipo: Optional[Tipo] = None          # tipo base (sin dims)
    dims_exprs: List[NodoAST] = field(default_factory=list)
    inicializador: Optional["ArrayInit"] = None


@dataclass
class ArrayInit(NodoAST):
    elementos: List[NodoAST] = field(default_factory=list)


@dataclass
class Cast(NodoAST):
    tipo: Optional[Tipo] = None
    expr: Optional[NodoAST] = None


@dataclass
class BinaryOp(NodoAST):
    op: str = ""
    izq: Optional[NodoAST] = None
    der: Optional[NodoAST] = None


@dataclass
class UnaryOp(NodoAST):
    op: str = ""
    operando: Optional[NodoAST] = None
    prefijo: bool = True


@dataclass
class InstanceOf(NodoAST):
    expr: Optional[NodoAST] = None
    tipo: Optional[Tipo] = None


@dataclass
class Ternary(NodoAST):
    condicion: Optional[NodoAST] = None
    si: Optional[NodoAST] = None
    no: Optional[NodoAST] = None


@dataclass
class Assign(NodoAST):
    op: str = "="
    destino: Optional[NodoAST] = None
    valor: Optional[NodoAST] = None
