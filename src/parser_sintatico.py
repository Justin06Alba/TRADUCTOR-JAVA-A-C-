from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.models import Token
from src.ast_nodes import (
    ASTNode, ProgramaNode, DeclaracionVarNode, AsignacionNode,
    SiNode, MientrasNode, ParaNode, RetornarNode, BloqueNode,
    BinOpNode, UnOpNode, LiteralNode, IdentificadorNode,
)

_TIPOS_VAR = {"entero", "decimal", "texto"}
_SINCRONIZADORES = {";", "}"}
_LIMITE_ERRORES = 20


@dataclass
class ErrorSintactico:
    mensaje: str
    line: int
    column: int
    token_encontrado: str


@dataclass
class ParseResult:
    ast: ProgramaNode | None
    errores: List[ErrorSintactico]
    exitoso: bool


class _ParseError(Exception):
    pass


class SintacticoParser:

    LIMITE_ERRORES: int = _LIMITE_ERRORES
    SINCRONIZADORES: frozenset = frozenset(_SINCRONIZADORES)

    def __init__(self, tokens: List[Token]) -> None:
        self._tokens: List[Token] = [
            t for t in tokens
            if t.token_type not in ("COMENTARIO", "ERROR_LEXICO")
        ]
        self._pos: int = 0
        self._errores: List[ErrorSintactico] = []

    def _actual(self) -> Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _consumir(self, tipo: str, lexema: str | None = None) -> Token:
        token = self._actual()
        coincide_tipo = token is not None and token.token_type == tipo
        coincide_lexema = lexema is None or (token is not None and token.lexeme == lexema)

        if coincide_tipo and coincide_lexema:
            self._pos += 1
            return token

        if token is not None:
            encontrado_lexema = token.lexeme
            linea = token.line
            columna = token.column
        else:
            encontrado_lexema = "<fin de archivo>"
            if self._pos > 0:
                ultimo = self._tokens[self._pos - 1]
                linea = ultimo.line
                columna = ultimo.column
            else:
                linea = 0
                columna = 0

        esperado = f"'{lexema}'" if lexema else tipo

        if encontrado_lexema == "<fin de archivo>":
            msg = f"Fin de archivo inesperado. Se esperaba {esperado}."
        else:
            msg = f"Se esperaba {esperado}, pero se encontró '{encontrado_lexema}'."

        self._registrar_error(msg, linea, columna, encontrado_lexema)
        raise _ParseError(msg)

    def _es(self, tipo: str, lexema: str | None = None) -> bool:
        token = self._actual()
        if token is None:
            return False
        if token.token_type != tipo:
            return False
        if lexema is not None and token.lexeme != lexema:
            return False
        return True

    def _sincronizar(self, sincronizadores: set | None = None) -> None:
        if sincronizadores is None:
            sincronizadores = _SINCRONIZADORES
        while self._actual() is not None:
            if self._actual().lexeme in sincronizadores:
                self._pos += 1
                return
            self._pos += 1

    def _registrar_error(self, mensaje: str, linea: int, columna: int, token_encontrado: str) -> None:
        self._errores.append(ErrorSintactico(
            mensaje=mensaje,
            line=linea,
            column=columna,
            token_encontrado=token_encontrado,
        ))

    def _limite_alcanzado(self) -> bool:
        return len(self._errores) >= self.LIMITE_ERRORES

    def parsear(self) -> ParseResult:
        try:
            ast = self._programa()
            return ParseResult(ast=ast, errores=self._errores, exitoso=len(self._errores) == 0)
        except Exception:
            return ParseResult(ast=None, errores=self._errores, exitoso=False)

    def _programa(self) -> ProgramaNode:
        linea = self._actual().line if self._actual() else 1
        columna = self._actual().column if self._actual() else 1
        declaraciones: List[ASTNode] = []

        while self._actual() is not None:
            if self._limite_alcanzado():
                t = self._actual()
                self._registrar_error(
                    f"Limite de {self.LIMITE_ERRORES} errores. Analisis detenido.",
                    t.line if t else 0, t.column if t else 0, t.lexeme if t else "",
                )
                break
            try:
                declaraciones.append(self._declaracion())
            except _ParseError:
                self._sincronizar()

        return ProgramaNode(line=linea, column=columna, declaraciones=declaraciones)

    def _declaracion(self) -> ASTNode:
        if self._es("PALABRA_RESERVADA") and self._actual().lexeme in _TIPOS_VAR:
            return self._declaracion_var()
        return self._sentencia()

    def _declaracion_var(self) -> DeclaracionVarNode:
        token_tipo = self._actual()
        linea = token_tipo.line
        columna = token_tipo.column
        tipo = token_tipo.lexeme

        self._consumir("PALABRA_RESERVADA")

        try:
            tok_nombre = self._consumir("IDENTIFICADOR")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En declaracion '{tipo}': se esperaba un IDENTIFICADOR, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        nombre = tok_nombre.lexeme
        valor_inicial: ASTNode | None = None

        if self._es("OPERADOR_ASIG", "="):
            self._pos += 1
            try:
                valor_inicial = self._expresion()
            except _ParseError:
                if self._errores:
                    u = self._errores[-1]
                    self._errores[-1] = ErrorSintactico(
                        mensaje=f"En declaracion '{nombre}': se esperaba una expresion tras '=', se encontro '{u.token_encontrado}'.",
                        line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                    )
                raise

        try:
            self._consumir("DELIMITADOR", ";")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"Se esperaba ';' al final de la declaracion de '{nombre}', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        return DeclaracionVarNode(line=linea, column=columna, tipo=tipo, nombre=nombre, valor_inicial=valor_inicial)

    def _sentencia(self) -> ASTNode:
        token = self._actual()

        if token is None:
            self._registrar_error("Se esperaba una sentencia pero se llego al fin del archivo.", 0, 0, "<EOF>")
            raise _ParseError()

        if token.token_type == "PALABRA_RESERVADA":
            if token.lexeme == "si":
                return self._sent_si()
            elif token.lexeme == "mientras":
                return self._sent_mientras()
            elif token.lexeme == "para":
                return self._sent_para()
            elif token.lexeme == "retornar":
                return self._sent_retornar()

        if token.token_type == "DELIMITADOR" and token.lexeme == "{":
            return self._bloque()

        if token.token_type == "IDENTIFICADOR":
            return self._sent_asignacion()

        self._registrar_error(
            f"Token inesperado '{token.lexeme}' ({token.token_type}).",
            token.line, token.column, token.lexeme,
        )
        raise _ParseError()

    def _sent_asignacion(self) -> AsignacionNode:
        tok_id = self._actual()
        linea = tok_id.line
        columna = tok_id.column
        tok_nombre = self._consumir("IDENTIFICADOR")
        nombre = tok_nombre.lexeme

        try:
            self._consumir("OPERADOR_ASIG", "=")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En asignacion a '{nombre}': se esperaba '=', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        try:
            valor = self._expresion()
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En asignacion a '{nombre}': se esperaba una expresion, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        try:
            self._consumir("DELIMITADOR", ";")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"Se esperaba ';' al final de la asignacion a '{nombre}', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        return AsignacionNode(line=linea, column=columna, nombre=nombre, valor=valor)

    def _sent_si(self) -> SiNode:
        tok = self._actual()
        linea = tok.line
        columna = tok.column
        self._consumir("PALABRA_RESERVADA", "si")

        try:
            self._consumir("DELIMITADOR", "(")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'si': se esperaba '(', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        condicion = self._expresion()

        try:
            self._consumir("DELIMITADOR", ")")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'si': se esperaba ')' para cerrar la condicion, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        entonces = self._bloque()
        sino: BloqueNode | None = None

        if self._es("PALABRA_RESERVADA", "sino"):
            self._pos += 1
            sino = self._bloque()

        return SiNode(line=linea, column=columna, condicion=condicion, entonces=entonces, sino=sino)

    def _sent_mientras(self) -> MientrasNode:
        tok = self._actual()
        linea = tok.line
        columna = tok.column
        self._consumir("PALABRA_RESERVADA", "mientras")

        try:
            self._consumir("DELIMITADOR", "(")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'mientras': se esperaba '(', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        condicion = self._expresion()

        try:
            self._consumir("DELIMITADOR", ")")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'mientras': se esperaba ')' para cerrar la condicion, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        cuerpo = self._bloque()
        return MientrasNode(line=linea, column=columna, condicion=condicion, cuerpo=cuerpo)

    def _sent_para(self) -> ParaNode:
        tok = self._actual()
        linea = tok.line
        columna = tok.column
        self._consumir("PALABRA_RESERVADA", "para")

        try:
            self._consumir("DELIMITADOR", "(")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'para': se esperaba '(', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        if self._es("PALABRA_RESERVADA") and self._actual().lexeme in _TIPOS_VAR:
            inicio = self._declaracion_var()
        else:
            inicio = self._sent_asignacion()

        condicion = self._expresion()

        try:
            self._consumir("DELIMITADOR", ";")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'para': se esperaba ';' tras la condicion, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        if (self._es("IDENTIFICADOR") and
                self._pos + 1 < len(self._tokens) and
                self._tokens[self._pos + 1].token_type == "OPERADOR_ASIG" and
                self._tokens[self._pos + 1].lexeme == "="):
            tok_id = self._actual()
            p_linea = tok_id.line
            p_col = tok_id.column
            tok_n = self._consumir("IDENTIFICADOR")
            self._consumir("OPERADOR_ASIG", "=")
            val_paso = self._expresion()
            paso: ASTNode = AsignacionNode(line=p_linea, column=p_col, nombre=tok_n.lexeme, valor=val_paso)
        else:
            paso = self._expresion()

        try:
            self._consumir("DELIMITADOR", ")")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"En sentencia 'para': se esperaba ')' para cerrar la cabecera, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        cuerpo = self._bloque()
        return ParaNode(line=linea, column=columna, inicio=inicio, condicion=condicion, paso=paso, cuerpo=cuerpo)

    def _sent_retornar(self) -> RetornarNode:
        tok = self._actual()
        linea = tok.line
        columna = tok.column
        self._consumir("PALABRA_RESERVADA", "retornar")

        valor: ASTNode | None = None
        if not self._es("DELIMITADOR", ";"):
            valor = self._expresion()

        try:
            self._consumir("DELIMITADOR", ";")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"Se esperaba ';' al final de 'retornar', se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        return RetornarNode(line=linea, column=columna, valor=valor)

    def _bloque(self) -> BloqueNode:
        tok = self._actual()
        if tok is None:
            self._registrar_error("Fin de archivo inesperado. Se esperaba '{'.", 0, 0, "<EOF>")
            raise _ParseError()

        linea = tok.line
        columna = tok.column

        try:
            self._consumir("DELIMITADOR", "{")
        except _ParseError:
            if self._errores:
                u = self._errores[-1]
                self._errores[-1] = ErrorSintactico(
                    mensaje=f"Se esperaba '{{' para iniciar un bloque, se encontro '{u.token_encontrado}'.",
                    line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                )
            raise

        declaraciones: List[ASTNode] = []
        while not self._es("DELIMITADOR", "}") and self._actual() is not None:
            if self._limite_alcanzado():
                break
            try:
                declaraciones.append(self._declaracion())
            except _ParseError:
                self._sincronizar()

        try:
            self._consumir("DELIMITADOR", "}")
        except _ParseError:
            raise

        return BloqueNode(line=linea, column=columna, declaraciones=declaraciones)

    def _expresion(self) -> ASTNode:
        return self._expr_log()

    def _expr_log(self) -> ASTNode:
        izq = self._expr_rel()
        while self._es("OPERADOR_LOG") and self._actual().lexeme in ("&&", "||"):
            tok_op = self._actual()
            self._pos += 1
            der = self._expr_rel()
            izq = BinOpNode(line=tok_op.line, column=tok_op.column,
                            operador=tok_op.lexeme, izquierda=izq, derecha=der)
        return izq

    def _expr_rel(self) -> ASTNode:
        izq = self._expr_arit()
        if self._es("OPERADOR_REL"):
            tok_op = self._actual()
            self._pos += 1
            der = self._expr_arit()
            return BinOpNode(line=tok_op.line, column=tok_op.column,
                             operador=tok_op.lexeme, izquierda=izq, derecha=der)
        return izq

    def _expr_arit(self) -> ASTNode:
        izq = self._termino()
        while self._es("OPERADOR_ARIT") and self._actual().lexeme in ("+", "-"):
            tok_op = self._actual()
            self._pos += 1
            der = self._termino()
            izq = BinOpNode(line=tok_op.line, column=tok_op.column,
                            operador=tok_op.lexeme, izquierda=izq, derecha=der)
        return izq

    def _termino(self) -> ASTNode:
        izq = self._factor()
        while self._es("OPERADOR_ARIT") and self._actual().lexeme in ("*", "/", "%"):
            tok_op = self._actual()
            self._pos += 1
            der = self._factor()
            izq = BinOpNode(line=tok_op.line, column=tok_op.column,
                            operador=tok_op.lexeme, izquierda=izq, derecha=der)
        return izq

    def _factor(self) -> ASTNode:
        token = self._actual()

        if token is None:
            self._registrar_error("Fin de archivo inesperado en expresion.", 0, 0, "<EOF>")
            raise _ParseError()

        if token.token_type == "ENTERO":
            self._pos += 1
            return LiteralNode(line=token.line, column=token.column, valor=token.lexeme, tipo_literal="ENTERO")

        if token.token_type == "DECIMAL":
            self._pos += 1
            return LiteralNode(line=token.line, column=token.column, valor=token.lexeme, tipo_literal="DECIMAL")

        if token.token_type == "CADENA":
            self._pos += 1
            return LiteralNode(line=token.line, column=token.column, valor=token.lexeme, tipo_literal="CADENA")

        if token.token_type == "PALABRA_RESERVADA":
            if token.lexeme == "verdad":
                self._pos += 1
                return LiteralNode(line=token.line, column=token.column, valor="verdad", tipo_literal="BOOL")
            if token.lexeme == "falso":
                self._pos += 1
                return LiteralNode(line=token.line, column=token.column, valor="falso", tipo_literal="BOOL")
            if token.lexeme == "nulo":
                self._pos += 1
                return LiteralNode(line=token.line, column=token.column, valor="nulo", tipo_literal="NULO")

        if token.token_type == "IDENTIFICADOR":
            self._pos += 1
            return IdentificadorNode(line=token.line, column=token.column, nombre=token.lexeme)

        if token.token_type == "DELIMITADOR" and token.lexeme == "(":
            self._pos += 1
            expr = self._expresion()
            try:
                self._consumir("DELIMITADOR", ")")
            except _ParseError:
                if self._errores:
                    u = self._errores[-1]
                    self._errores[-1] = ErrorSintactico(
                        mensaje=f"Se esperaba ')' para cerrar el grupo, se encontro '{u.token_encontrado}'.",
                        line=u.line, column=u.column, token_encontrado=u.token_encontrado,
                    )
                raise
            return expr

        if token.token_type == "OPERADOR_LOG" and token.lexeme == "!":
            linea = token.line
            columna = token.column
            self._pos += 1
            operando = self._factor()
            return UnOpNode(line=linea, column=columna, operador="!", operando=operando)

        self._registrar_error(
            f"En expresion: se esperaba un valor o '(' pero se encontro '{token.lexeme}'.",
            token.line, token.column, token.lexeme,
        )
        raise _ParseError()
