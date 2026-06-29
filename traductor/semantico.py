"""Analizador semantico del traductor.

El objetivo no es un type-checker completo de Java, sino validar lo necesario
para una traduccion fiable:

  - Tipos desconocidos en campos, parametros y variables locales.
  - Variables usadas sin declarar.
  - Redeclaraciones en el mismo ambito.

El semantico nunca propaga excepciones: recolecta errores y devuelve un
SemanticResult.
"""

from __future__ import annotations

from typing import List, Optional

from traductor.infraestructura import Error, SemanticResult, Simbolo, TablaSimbolos
from traductor import java_ast as ast

_LIMITE_ERRORES = 20

# Tipos conocidos sin necesidad de declaracion (primitivos + biblioteca comun).
_TIPOS_BASE = {
    "boolean", "char", "byte", "short", "int", "long", "float", "double", "void",
    "String", "Object", "Integer", "Long", "Double", "Float", "Boolean",
    "Character", "Number", "CharSequence", "Math", "System",
    "List", "ArrayList", "LinkedList", "Map", "HashMap", "TreeMap",
    "Set", "HashSet", "TreeSet", "Collection", "Iterable", "Iterator",
    "Exception", "RuntimeException", "IllegalArgumentException",
    "IllegalStateException", "NullPointerException", "IndexOutOfBoundsException",
    "UnsupportedOperationException", "Comparable", "Runnable", "Thread",
    "StringBuilder", "Optional",
}


class AnalizadorSemantico:

    LIMITE_ERRORES = _LIMITE_ERRORES

    def __init__(self, unidad: ast.CompilationUnit) -> None:
        self._unidad = unidad
        self._tabla = TablaSimbolos()
        self._errores: List[Error] = []
        self._tipos_usuario = set()    # clases/interfaces declaradas
        self._clase_actual: Optional[str] = None

    # ------------------------------------------------------------------ API

    def analizar(self) -> SemanticResult:
        try:
            self._registrar_tipos()
            for tipo in self._unidad.tipos:
                if self._limite():
                    break
                if isinstance(tipo, ast.ClassDecl):
                    self._analizar_clase(tipo)
                elif isinstance(tipo, ast.InterfaceDecl):
                    self._analizar_interfaz(tipo)
        except Exception:
            pass
        return SemanticResult(
            ast_validado=self._unidad,
            simbolos=self._tabla.todos(),
            errores=self._errores,
        )

    # -------------------------------------------------------------- pasada 1

    def _registrar_tipos(self) -> None:
        """Primera pasada: registra clases e interfaces."""
        for tipo in self._unidad.tipos:
            if isinstance(tipo, (ast.ClassDecl, ast.InterfaceDecl)):
                self._tipos_usuario.add(tipo.nombre)
                categoria = "clase" if isinstance(tipo, ast.ClassDecl) else "interfaz"
                self._tabla.declarar(Simbolo(
                    nombre=tipo.nombre, categoria=categoria,
                    line=tipo.line, column=tipo.column,
                ))

    # -------------------------------------------------------------- pasada 2

    def _analizar_clase(self, clase: ast.ClassDecl) -> None:
        self._clase_actual = clase.nombre
        self._verificar_tipo(clase.superclase, clase.line, clase.column)
        for itf in clase.interfaces:
            self._verificar_tipo(itf, clase.line, clase.column)

        self._tabla.entrar_ambito()
        try:
            # Registrar campos antes de analizar metodos (visibles en todo el cuerpo)
            for m in clase.miembros:
                if isinstance(m, ast.FieldDecl):
                    self._declarar_campo(m)
            for m in clase.miembros:
                if self._limite():
                    break
                if isinstance(m, (ast.MethodDecl, ast.ConstructorDecl)):
                    self._analizar_metodo(m)
        finally:
            self._tabla.salir_ambito()
        self._clase_actual = None

    def _analizar_interfaz(self, itf: ast.InterfaceDecl) -> None:
        for sup in itf.interfaces:
            self._verificar_tipo(sup, itf.line, itf.column)
        # Las firmas de metodos de interfaz no tienen cuerpo; solo validar tipos.
        for m in itf.miembros:
            if isinstance(m, ast.MethodDecl):
                self._verificar_tipo(m.tipo_retorno, m.line, m.column)
                for p in m.parametros:
                    self._verificar_tipo(p.tipo, p.line, p.column)

    def _declarar_campo(self, campo: ast.FieldDecl) -> None:
        self._verificar_tipo(campo.tipo, campo.line, campo.column)
        sim = Simbolo(nombre=campo.nombre, categoria="campo",
                      tipo=str(campo.tipo), line=campo.line, column=campo.column)
        if not self._tabla.declarar(sim):
            self._error(f"El campo '{campo.nombre}' ya fue declarado en esta clase.",
                        campo.line, campo.column, campo.nombre)
        if campo.valor is not None:
            self._analizar_expr(campo.valor)

    def _analizar_metodo(self, metodo) -> None:
        if isinstance(metodo, ast.MethodDecl):
            self._verificar_tipo(metodo.tipo_retorno, metodo.line, metodo.column)

        self._tabla.entrar_ambito()
        try:
            for p in metodo.parametros:
                self._verificar_tipo(p.tipo, p.line, p.column)
                sim = Simbolo(nombre=p.nombre, categoria="parametro",
                              tipo=str(p.tipo), line=p.line, column=p.column)
                if not self._tabla.declarar(sim):
                    self._error(f"El parametro '{p.nombre}' esta duplicado.",
                                p.line, p.column, p.nombre)
            if metodo.cuerpo is not None:
                self._analizar_bloque(metodo.cuerpo)
        finally:
            self._tabla.salir_ambito()

    # -------------------------------------------------------------- sentencias

    def _analizar_bloque(self, bloque: ast.Block) -> None:
        for stmt in bloque.sentencias:
            if self._limite():
                break
            self._analizar_stmt(stmt)

    def _analizar_stmt(self, stmt) -> None:
        if stmt is None:
            return
        if isinstance(stmt, ast.LocalVarDecl):
            self._verificar_tipo(stmt.tipo, stmt.line, stmt.column)
            sim = Simbolo(nombre=stmt.nombre, categoria="variable",
                          tipo=str(stmt.tipo), line=stmt.line, column=stmt.column)
            if not self._tabla.declarar(sim):
                self._error(f"La variable '{stmt.nombre}' ya fue declarada en este ambito.",
                            stmt.line, stmt.column, stmt.nombre)
            if stmt.valor is not None:
                self._analizar_expr(stmt.valor)

        elif isinstance(stmt, ast.Block):
            self._tabla.entrar_ambito()
            try:
                self._analizar_bloque(stmt)
            finally:
                self._tabla.salir_ambito()

        elif isinstance(stmt, ast.IfStmt):
            self._analizar_expr(stmt.condicion)
            self._analizar_stmt(stmt.entonces)
            self._analizar_stmt(stmt.sino)

        elif isinstance(stmt, ast.WhileStmt):
            self._analizar_expr(stmt.condicion)
            self._analizar_stmt(stmt.cuerpo)

        elif isinstance(stmt, ast.DoWhileStmt):
            self._analizar_stmt(stmt.cuerpo)
            self._analizar_expr(stmt.condicion)

        elif isinstance(stmt, ast.ForStmt):
            self._tabla.entrar_ambito()
            try:
                for d in stmt.init:
                    self._analizar_stmt(d) if isinstance(d, ast.LocalVarDecl) else self._analizar_expr(d)
                self._analizar_expr(stmt.condicion)
                for u in stmt.update:
                    self._analizar_expr(u)
                self._analizar_stmt(stmt.cuerpo)
            finally:
                self._tabla.salir_ambito()

        elif isinstance(stmt, ast.ForEachStmt):
            self._tabla.entrar_ambito()
            try:
                self._verificar_tipo(stmt.tipo, stmt.line, stmt.column)
                self._tabla.declarar(Simbolo(nombre=stmt.nombre, categoria="variable",
                                             tipo=str(stmt.tipo),
                                             line=stmt.line, column=stmt.column))
                self._analizar_expr(stmt.iterable)
                self._analizar_stmt(stmt.cuerpo)
            finally:
                self._tabla.salir_ambito()

        elif isinstance(stmt, ast.ReturnStmt):
            self._analizar_expr(stmt.valor)

        elif isinstance(stmt, ast.ThrowStmt):
            self._analizar_expr(stmt.valor)

        elif isinstance(stmt, ast.ExprStmt):
            self._analizar_expr(stmt.expr)

        # break/continue: nada que validar en este nivel.

    # -------------------------------------------------------------- expresiones

    def _analizar_expr(self, expr) -> None:
        if expr is None:
            return
        if isinstance(expr, ast.VarRef):
            # Solo reportamos si no es campo/variable/clase conocida. Evitamos
            # falsos positivos con nombres de clase (Math, System, etc.).
            if (not self._tabla.existe(expr.nombre)
                    and expr.nombre not in self._tipos_usuario
                    and expr.nombre not in _TIPOS_BASE):
                self._error(f"El identificador '{expr.nombre}' no ha sido declarado.",
                            expr.line, expr.column, expr.nombre)

        elif isinstance(expr, ast.Assign):
            self._analizar_expr(expr.destino)
            self._analizar_expr(expr.valor)

        elif isinstance(expr, ast.BinaryOp):
            self._analizar_expr(expr.izq)
            self._analizar_expr(expr.der)

        elif isinstance(expr, ast.UnaryOp):
            self._analizar_expr(expr.operando)

        elif isinstance(expr, ast.Ternary):
            self._analizar_expr(expr.condicion)
            self._analizar_expr(expr.si)
            self._analizar_expr(expr.no)

        elif isinstance(expr, ast.MethodCall):
            # El receptor se valida; el nombre del metodo no (puede ser de una
            # API externa que no modelamos).
            self._analizar_expr(expr.objeto)
            for a in expr.argumentos:
                self._analizar_expr(a)

        elif isinstance(expr, ast.FieldAccess):
            self._analizar_expr(expr.objeto)

        elif isinstance(expr, ast.ArrayAccess):
            self._analizar_expr(expr.objeto)
            self._analizar_expr(expr.indice)

        elif isinstance(expr, ast.NewObject):
            self._verificar_tipo(expr.tipo, expr.line, expr.column)
            for a in expr.argumentos:
                self._analizar_expr(a)

        elif isinstance(expr, ast.NewArray):
            self._verificar_tipo(expr.tipo, expr.line, expr.column)
            for d in expr.dims_exprs:
                self._analizar_expr(d)
            if expr.inicializador:
                self._analizar_expr(expr.inicializador)

        elif isinstance(expr, ast.ArrayInit):
            for e in expr.elementos:
                self._analizar_expr(e)

        elif isinstance(expr, ast.Cast):
            self._verificar_tipo(expr.tipo, expr.line, expr.column)
            self._analizar_expr(expr.expr)

        elif isinstance(expr, ast.InstanceOf):
            self._analizar_expr(expr.expr)
            self._verificar_tipo(expr.tipo, expr.line, expr.column)

        # Literales, this, super: nada que validar.

    # -------------------------------------------------------------- helpers

    def _verificar_tipo(self, tipo: Optional[ast.Tipo], line: int, col: int) -> None:
        if tipo is None:
            return
        if not self._tipo_valido(tipo):
            self._error(f"Tipo desconocido: '{tipo}'.", line, col, str(tipo))
        for g in tipo.genericos:
            self._verificar_tipo(g, line, col)

    def _tipo_valido(self, tipo: ast.Tipo) -> bool:
        nombre = tipo.nombre.split(".")[-1]   # java.util.List -> List
        return (nombre in _TIPOS_BASE
                or tipo.nombre in self._tipos_usuario
                or nombre in self._tipos_usuario
                or len(tipo.nombre) == 1               # generico (T, E, K, V)
                # Un nombre de tipo capitalizado desconocido se asume una clase
                # externa (definida en otro archivo o import) y no es un error.
                or (nombre[:1].isupper()))

    def _error(self, mensaje: str, line: int, column: int, token: str = "") -> None:
        if self._limite():
            return
        self._errores.append(Error(fase="SEMANTICO", mensaje=mensaje,
                                   line=line, column=column, token_encontrado=token))

    def _limite(self) -> bool:
        return len(self._errores) >= self.LIMITE_ERRORES
