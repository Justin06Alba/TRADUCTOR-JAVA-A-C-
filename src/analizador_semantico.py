"""Analizador semantico para MiniLex.

Tercera fase del compilador. Recorre el AST producido por el parser sintactico
(ver src/parser_sintatico.py) y valida el *significado* del programa:

  - Variables usadas sin declarar.
  - Variables redeclaradas en el mismo ambito.
  - Incompatibilidades de tipos en declaraciones, asignaciones y operaciones.

Maneja ambitos anidados con una pila de tablas de simbolos: cada bloque '{ }'
(y la cabecera de 'para') crea su propio ambito.

Modelo de tipos (estilo C): los booleanos 'verdad'/'falso' se modelan como
'entero'. Se permite la promocion entero -> decimal, pero no la inversa.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.ast_nodes import (
    ASTNode, ProgramaNode, DeclaracionVarNode, AsignacionNode,
    SiNode, MientrasNode, ParaNode, RetornarNode, BloqueNode,
    BinOpNode, UnOpNode, LiteralNode, IdentificadorNode,
)

# Tipos de dato del lenguaje
_TIPO_ENTERO = "entero"
_TIPO_DECIMAL = "decimal"
_TIPO_TEXTO = "texto"
_TIPO_NULO = "nulo"

_TIPOS_NUMERICOS = frozenset({_TIPO_ENTERO, _TIPO_DECIMAL})

_OPS_ARITMETICOS = frozenset({"+", "-", "*", "/", "%"})
_OPS_RELACIONALES = frozenset({"==", "!=", "<", ">", "<=", ">="})
_OPS_LOGICOS = frozenset({"&&", "||"})

_LIMITE_ERRORES = 20

# Categorias de error semantico
CAT_DECLARACION = "declaracion"
CAT_USO = "uso"
CAT_TIPO = "tipo"


@dataclass
class ErrorSemantico:
    mensaje: str
    line: int
    column: int
    categoria: str
    # Texto del lexema asociado, para resaltar en el editor (analogo a
    # ErrorSintactico.token_encontrado).
    token_encontrado: str = ""


@dataclass
class Simbolo:
    nombre: str
    tipo: str
    line: int
    column: int
    inicializado: bool
    ambito: int


@dataclass
class SemanticResult:
    simbolos: List[Simbolo]
    errores: List[ErrorSemantico]
    exitoso: bool


class TablaSimbolos:
    """Pila de ambitos. El indice 0 es el ambito global."""

    def __init__(self) -> None:
        self._scopes: List[dict[str, Simbolo]] = [{}]
        # Acumula todos los simbolos declarados (aunque su ambito ya se haya
        # cerrado) para poder mostrarlos en la GUI.
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
        actual[simbolo.nombre] = simbolo
        self._historico.append(simbolo)
        return True

    def buscar(self, nombre: str) -> Optional[Simbolo]:
        """Busca un simbolo desde el ambito mas interno hacia el global."""
        for scope in reversed(self._scopes):
            if nombre in scope:
                return scope[nombre]
        return None

    def declarado_en_actual(self, nombre: str) -> bool:
        return nombre in self._scopes[-1]

    def todos(self) -> List[Simbolo]:
        return list(self._historico)


class AnalizadorSemantico:

    LIMITE_ERRORES: int = _LIMITE_ERRORES

    def __init__(self, ast: ProgramaNode) -> None:
        self._ast = ast
        self._tabla = TablaSimbolos()
        self._errores: List[ErrorSemantico] = []

    # ------------------------------------------------------------------ API

    def analizar(self) -> SemanticResult:
        try:
            if self._ast is not None:
                self._visit_programa(self._ast)
        except Exception:
            # El semantico nunca debe propagar excepciones: en el peor caso
            # devuelve lo que haya recolectado hasta el momento.
            pass

        return SemanticResult(
            simbolos=self._tabla.todos(),
            errores=self._errores,
            exitoso=len(self._errores) == 0,
        )

    # --------------------------------------------------------------- helpers

    def _registrar_error(self, mensaje: str, line: int, column: int,
                         categoria: str, token: str = "") -> None:
        if len(self._errores) >= self.LIMITE_ERRORES:
            return
        self._errores.append(ErrorSemantico(
            mensaje=mensaje, line=line, column=column,
            categoria=categoria, token_encontrado=token,
        ))

    def _limite_alcanzado(self) -> bool:
        return len(self._errores) >= self.LIMITE_ERRORES

    @staticmethod
    def _es_numerico(tipo: Optional[str]) -> bool:
        return tipo in _TIPOS_NUMERICOS

    @staticmethod
    def _compatible_asignacion(destino: str, origen: Optional[str]) -> bool:
        """Indica si un valor de tipo 'origen' puede asignarse a 'destino'."""
        if origen is None:
            # Tipo desconocido (por un error previo): no encadenar mas errores.
            return True
        if destino == origen:
            return True
        # Promocion: decimal <- entero
        if destino == _TIPO_DECIMAL and origen == _TIPO_ENTERO:
            return True
        # nulo solo es asignable a texto
        if destino == _TIPO_TEXTO and origen == _TIPO_NULO:
            return True
        return False

    # ------------------------------------------------------- visitantes nodo

    def _visit_programa(self, nodo: ProgramaNode) -> None:
        for decl in nodo.declaraciones:
            if self._limite_alcanzado():
                break
            self._visit(decl)

    def _visit(self, nodo: Optional[ASTNode]) -> None:
        if nodo is None:
            return
        if isinstance(nodo, DeclaracionVarNode):
            self._visit_declaracion_var(nodo)
        elif isinstance(nodo, AsignacionNode):
            self._visit_asignacion(nodo)
        elif isinstance(nodo, SiNode):
            self._visit_si(nodo)
        elif isinstance(nodo, MientrasNode):
            self._visit_mientras(nodo)
        elif isinstance(nodo, ParaNode):
            self._visit_para(nodo)
        elif isinstance(nodo, RetornarNode):
            self._visit_retornar(nodo)
        elif isinstance(nodo, BloqueNode):
            self._visit_bloque(nodo)
        else:
            # Una expresion suelta como sentencia: solo verificar su tipo.
            self._tipo_de(nodo)

    def _visit_declaracion_var(self, nodo: DeclaracionVarNode) -> None:
        tipo_valor: Optional[str] = None
        if nodo.valor_inicial is not None:
            tipo_valor = self._tipo_de(nodo.valor_inicial)
            if not self._compatible_asignacion(nodo.tipo, tipo_valor):
                self._registrar_error(
                    f"No se puede asignar un valor de tipo '{tipo_valor}' a la "
                    f"variable '{nodo.nombre}' de tipo '{nodo.tipo}'.",
                    nodo.line, nodo.column, CAT_TIPO, nodo.nombre,
                )

        simbolo = Simbolo(
            nombre=nodo.nombre, tipo=nodo.tipo,
            line=nodo.line, column=nodo.column,
            inicializado=nodo.valor_inicial is not None,
            ambito=self._tabla.nivel_actual,
        )
        if not self._tabla.declarar(simbolo):
            self._registrar_error(
                f"La variable '{nodo.nombre}' ya fue declarada en este ambito.",
                nodo.line, nodo.column, CAT_DECLARACION, nodo.nombre,
            )

    def _visit_asignacion(self, nodo: AsignacionNode) -> None:
        simbolo = self._tabla.buscar(nodo.nombre)
        tipo_valor = self._tipo_de(nodo.valor) if nodo.valor is not None else None

        if simbolo is None:
            self._registrar_error(
                f"La variable '{nodo.nombre}' no ha sido declarada.",
                nodo.line, nodo.column, CAT_USO, nodo.nombre,
            )
            return

        if not self._compatible_asignacion(simbolo.tipo, tipo_valor):
            self._registrar_error(
                f"No se puede asignar un valor de tipo '{tipo_valor}' a la "
                f"variable '{nodo.nombre}' de tipo '{simbolo.tipo}'.",
                nodo.line, nodo.column, CAT_TIPO, nodo.nombre,
            )

        simbolo.inicializado = True

    def _visit_si(self, nodo: SiNode) -> None:
        self._verificar_condicion(nodo.condicion, "si")
        self._visit(nodo.entonces)
        if nodo.sino is not None:
            self._visit(nodo.sino)

    def _visit_mientras(self, nodo: MientrasNode) -> None:
        self._verificar_condicion(nodo.condicion, "mientras")
        self._visit(nodo.cuerpo)

    def _visit_para(self, nodo: ParaNode) -> None:
        # La cabecera del 'para' abre su propio ambito para que la variable de
        # inicializacion sea visible en condicion, paso y cuerpo.
        self._tabla.entrar_ambito()
        try:
            self._visit(nodo.inicio)
            self._verificar_condicion(nodo.condicion, "para")
            self._visit(nodo.paso)
            self._visit(nodo.cuerpo)
        finally:
            self._tabla.salir_ambito()

    def _visit_retornar(self, nodo: RetornarNode) -> None:
        # MiniLex no tiene firmas de funcion; solo validamos la expresion.
        if nodo.valor is not None:
            self._tipo_de(nodo.valor)

    def _visit_bloque(self, nodo: BloqueNode) -> None:
        self._tabla.entrar_ambito()
        try:
            for decl in nodo.declaraciones:
                if self._limite_alcanzado():
                    break
                self._visit(decl)
        finally:
            self._tabla.salir_ambito()

    def _verificar_condicion(self, condicion: Optional[ASTNode], contexto: str) -> None:
        if condicion is None:
            return
        tipo = self._tipo_de(condicion)
        if tipo is not None and not self._es_numerico(tipo):
            self._registrar_error(
                f"La condicion de '{contexto}' debe ser numerica, pero es de "
                f"tipo '{tipo}'.",
                condicion.line, condicion.column, CAT_TIPO,
            )

    # ------------------------------------------------- inferencia de tipos

    def _tipo_de(self, nodo: Optional[ASTNode]) -> Optional[str]:
        """Infiere el tipo de una expresion y registra errores de uso/tipo.

        Devuelve el nombre del tipo ('entero', 'decimal', 'texto', 'nulo') o
        None si no se pudo determinar (por un error ya reportado).
        """
        if nodo is None:
            return None

        if isinstance(nodo, LiteralNode):
            return self._tipo_de_literal(nodo)

        if isinstance(nodo, IdentificadorNode):
            simbolo = self._tabla.buscar(nodo.nombre)
            if simbolo is None:
                self._registrar_error(
                    f"La variable '{nodo.nombre}' no ha sido declarada.",
                    nodo.line, nodo.column, CAT_USO, nodo.nombre,
                )
                return None
            return simbolo.tipo

        if isinstance(nodo, BinOpNode):
            return self._tipo_de_binop(nodo)

        if isinstance(nodo, UnOpNode):
            return self._tipo_de_unop(nodo)

        return None

    @staticmethod
    def _tipo_de_literal(nodo: LiteralNode) -> str:
        mapa = {
            "ENTERO": _TIPO_ENTERO,
            "DECIMAL": _TIPO_DECIMAL,
            "CADENA": _TIPO_TEXTO,
            "BOOL": _TIPO_ENTERO,   # verdad/falso modelados como entero
            "NULO": _TIPO_NULO,
        }
        return mapa.get(nodo.tipo_literal, _TIPO_ENTERO)

    def _tipo_de_binop(self, nodo: BinOpNode) -> Optional[str]:
        op = nodo.operador
        tipo_izq = self._tipo_de(nodo.izquierda)
        tipo_der = self._tipo_de(nodo.derecha)

        # Si algun operando ya fallo, no encadenar errores.
        if tipo_izq is None or tipo_der is None:
            return None

        if op in _OPS_ARITMETICOS:
            if not self._es_numerico(tipo_izq) or not self._es_numerico(tipo_der):
                self._registrar_error(
                    f"El operador aritmetico '{op}' requiere operandos numericos, "
                    f"pero se encontro '{tipo_izq}' y '{tipo_der}'.",
                    nodo.line, nodo.column, CAT_TIPO, op,
                )
                return None
            # decimal si alguno es decimal, si no entero
            if _TIPO_DECIMAL in (tipo_izq, tipo_der):
                return _TIPO_DECIMAL
            return _TIPO_ENTERO

        if op in _OPS_RELACIONALES:
            ambos_numericos = self._es_numerico(tipo_izq) and self._es_numerico(tipo_der)
            ambos_texto = tipo_izq == _TIPO_TEXTO and tipo_der == _TIPO_TEXTO
            if not (ambos_numericos or ambos_texto):
                self._registrar_error(
                    f"El operador relacional '{op}' no puede comparar '{tipo_izq}' "
                    f"con '{tipo_der}'.",
                    nodo.line, nodo.column, CAT_TIPO, op,
                )
                return None
            return _TIPO_ENTERO  # resultado booleano modelado como entero

        if op in _OPS_LOGICOS:
            if not self._es_numerico(tipo_izq) or not self._es_numerico(tipo_der):
                self._registrar_error(
                    f"El operador logico '{op}' requiere operandos numericos, "
                    f"pero se encontro '{tipo_izq}' y '{tipo_der}'.",
                    nodo.line, nodo.column, CAT_TIPO, op,
                )
                return None
            return _TIPO_ENTERO

        return None

    def _tipo_de_unop(self, nodo: UnOpNode) -> Optional[str]:
        tipo_operando = self._tipo_de(nodo.operando)
        if tipo_operando is None:
            return None
        if nodo.operador == "!":
            if not self._es_numerico(tipo_operando):
                self._registrar_error(
                    f"El operador logico '!' requiere un operando numerico, "
                    f"pero se encontro '{tipo_operando}'.",
                    nodo.line, nodo.column, CAT_TIPO, "!",
                )
                return None
            return _TIPO_ENTERO
        return tipo_operando
