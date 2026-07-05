"""Optimizador del AST (fase intermedia del traductor).

Se ejecuta *entre* el analisis semantico y la generacion de C#. Recorre el AST
de `java_ast` y lo reescribe aplicando optimizaciones clasicas de compilador
independientes de la maquina:

  1. Plegado de constantes (constant folding):
         2 + 3          -> 5
         "a" + "b"      -> "ab"
         3 < 4          -> true
         !true          -> false
  2. Simplificacion algebraica (algebraic identities):
         x + 0, 0 + x   -> x
         x * 1, 1 * x   -> x
         x * 0          -> 0     (si x no tiene efectos secundarios)
         x - 0, x / 1   -> x
  3. Simplificacion booleana (con cortocircuito seguro):
         x && true      -> x
         false && x     -> false
         x || false     -> x
         true || x      -> true
         !!x            -> x
  4. Colapso de condicionales constantes / eliminacion de codigo muerto:
         if (true)  A else B   -> A
         if (false) A else B   -> B
         while (false) { ... }  -> (eliminado)
         cond ? a : b  con cond constante -> a / b
         sentencias tras return/throw/break/continue -> (eliminadas)

Reglas de seguridad
-------------------
El optimizador **nunca** descarta una subexpresion que pueda tener efectos
secundarios. Cuando una identidad eliminaria un operando (p. ej. `x * 0 -> 0`
o `x && false -> false`), solo se aplica si ese operando es *puro* (literal,
referencia a variable, `this`/`super`). Ademas la aritmetica entera solo se
pliega si el resultado cabe en el rango de Java (32 bits para `int`, 64 para
`long`), preservando la semantica de desbordamiento.

Cada reescritura se registra en `self.cambios` para poder informarla al usuario.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from traductor import java_ast as ast


_INT32_MIN, _INT32_MAX = -(2 ** 31), 2 ** 31 - 1
_INT64_MIN, _INT64_MAX = -(2 ** 63), 2 ** 63 - 1

# Sentencias que interrumpen el flujo: todo lo que las siga en un bloque es
# codigo inalcanzable.
_TERMINADORES = (ast.ReturnStmt, ast.BreakStmt, ast.ContinueStmt, ast.ThrowStmt)


@dataclass
class Optimizador:
    """Reescribe el AST aplicando optimizaciones y registra los cambios."""

    cambios: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------ API

    def optimizar(self, unidad: ast.CompilationUnit) -> ast.CompilationUnit:
        unidad.tipos = [self._tipo_decl(t) for t in unidad.tipos]
        return unidad

    # -------------------------------------------------------- declaraciones

    def _tipo_decl(self, decl):
        if isinstance(decl, (ast.ClassDecl, ast.InterfaceDecl)):
            decl.miembros = [self._miembro(m) for m in decl.miembros]
        return decl

    def _miembro(self, m):
        if isinstance(m, ast.FieldDecl) and m.valor is not None:
            m.valor = self._expr(m.valor)
        elif isinstance(m, (ast.MethodDecl, ast.ConstructorDecl)) and m.cuerpo is not None:
            m.cuerpo = self._bloque(m.cuerpo)
        return m

    # -------------------------------------------------------- sentencias

    def _bloque(self, bloque: ast.Block) -> ast.Block:
        bloque.sentencias = self._lista_stmts(bloque.sentencias)
        return bloque

    def _lista_stmts(self, stmts: List[ast.NodoAST]) -> List[ast.NodoAST]:
        """Optimiza cada sentencia y elimina el codigo inalcanzable."""
        salida: List[ast.NodoAST] = []
        for s in stmts:
            nuevas = self._stmt(s)
            corte = False
            for n in nuevas:
                salida.append(n)
                if isinstance(n, _TERMINADORES):
                    corte = True
                    break
            if corte:
                # Todo lo que sigue en este bloque es inalcanzable.
                restantes = stmts[stmts.index(s) + 1:]
                if restantes:
                    self.cambios.append(
                        f"Codigo inalcanzable eliminado tras "
                        f"{type(salida[-1]).__name__} ({len(restantes)} sentencia(s)).")
                break
        return salida

    def _stmt(self, stmt) -> List[ast.NodoAST]:
        """Optimiza una sentencia; devuelve una lista (permite eliminar/colapsar)."""
        if stmt is None:
            return []

        if isinstance(stmt, ast.Block):
            return [self._bloque(stmt)]

        if isinstance(stmt, ast.LocalVarDecl):
            if stmt.valor is not None:
                stmt.valor = self._expr(stmt.valor)
            return [stmt]

        if isinstance(stmt, ast.ExprStmt):
            stmt.expr = self._expr(stmt.expr)
            return [stmt]

        if isinstance(stmt, ast.ReturnStmt):
            if stmt.valor is not None:
                stmt.valor = self._expr(stmt.valor)
            return [stmt]

        if isinstance(stmt, ast.ThrowStmt):
            stmt.valor = self._expr(stmt.valor)
            return [stmt]

        if isinstance(stmt, (ast.BreakStmt, ast.ContinueStmt)):
            return [stmt]

        if isinstance(stmt, ast.IfStmt):
            return self._if(stmt)

        if isinstance(stmt, ast.WhileStmt):
            stmt.condicion = self._expr(stmt.condicion)
            # while (false) { ... } nunca ejecuta -> se elimina.
            if isinstance(stmt.condicion, ast.BoolLiteral) and not stmt.condicion.valor:
                self.cambios.append("Bucle 'while (false)' eliminado (nunca se ejecuta).")
                return []
            stmt.cuerpo = self._stmt_unico(stmt.cuerpo)
            return [stmt]

        if isinstance(stmt, ast.DoWhileStmt):
            stmt.cuerpo = self._stmt_unico(stmt.cuerpo)
            stmt.condicion = self._expr(stmt.condicion)
            return [stmt]

        if isinstance(stmt, ast.ForStmt):
            stmt.init = [self._stmt_o_expr(i) for i in stmt.init]
            if stmt.condicion is not None:
                stmt.condicion = self._expr(stmt.condicion)
            stmt.update = [self._expr(u) for u in stmt.update]
            stmt.cuerpo = self._stmt_unico(stmt.cuerpo)
            return [stmt]

        if isinstance(stmt, ast.ForEachStmt):
            stmt.iterable = self._expr(stmt.iterable)
            stmt.cuerpo = self._stmt_unico(stmt.cuerpo)
            return [stmt]

        return [stmt]

    def _if(self, stmt: ast.IfStmt) -> List[ast.NodoAST]:
        stmt.condicion = self._expr(stmt.condicion)
        # Colapso de condicion constante.
        if isinstance(stmt.condicion, ast.BoolLiteral):
            if stmt.condicion.valor:
                self.cambios.append("'if (true)' colapsado a la rama verdadera.")
                return self._stmt(stmt.entonces)
            self.cambios.append("'if (false)' colapsado a la rama falsa.")
            return self._stmt(stmt.sino) if stmt.sino is not None else []
        stmt.entonces = self._stmt_unico(stmt.entonces)
        if stmt.sino is not None:
            stmt.sino = self._stmt_unico(stmt.sino)
        return [stmt]

    def _stmt_unico(self, stmt):
        """Optimiza una sentencia que ocupa la posicion de una sola (cuerpo de
        if/for/while). Si se expande a varias, se envuelve en un Block."""
        if stmt is None:
            return None
        resultado = self._stmt(stmt)
        if len(resultado) == 1:
            return resultado[0]
        return ast.Block(line=getattr(stmt, "line", 0),
                         column=getattr(stmt, "column", 0), sentencias=resultado)

    def _stmt_o_expr(self, nodo):
        if isinstance(nodo, ast.LocalVarDecl):
            return self._stmt(nodo)[0]
        return self._expr(nodo)

    # -------------------------------------------------------- expresiones

    def _expr(self, expr):
        if expr is None:
            return None

        if isinstance(expr, ast.BinaryOp):
            expr.izq = self._expr(expr.izq)
            expr.der = self._expr(expr.der)
            return self._simplificar_binaria(expr)

        if isinstance(expr, ast.UnaryOp):
            expr.operando = self._expr(expr.operando)
            return self._simplificar_unaria(expr)

        if isinstance(expr, ast.Ternary):
            expr.condicion = self._expr(expr.condicion)
            expr.si = self._expr(expr.si)
            expr.no = self._expr(expr.no)
            if isinstance(expr.condicion, ast.BoolLiteral):
                self.cambios.append("Ternario con condicion constante colapsado.")
                return expr.si if expr.condicion.valor else expr.no
            return expr

        if isinstance(expr, ast.Assign):
            expr.destino = self._expr(expr.destino)
            expr.valor = self._expr(expr.valor)
            return expr

        if isinstance(expr, ast.MethodCall):
            expr.objeto = self._expr(expr.objeto)
            expr.argumentos = [self._expr(a) for a in expr.argumentos]
            return expr

        if isinstance(expr, ast.FieldAccess):
            expr.objeto = self._expr(expr.objeto)
            return expr

        if isinstance(expr, ast.ArrayAccess):
            expr.objeto = self._expr(expr.objeto)
            expr.indice = self._expr(expr.indice)
            return expr

        if isinstance(expr, ast.Cast):
            expr.expr = self._expr(expr.expr)
            return expr

        if isinstance(expr, ast.InstanceOf):
            expr.expr = self._expr(expr.expr)
            return expr

        if isinstance(expr, ast.NewObject):
            expr.argumentos = [self._expr(a) for a in expr.argumentos]
            return expr

        if isinstance(expr, ast.NewArray):
            expr.dims_exprs = [self._expr(d) for d in expr.dims_exprs]
            if expr.inicializador is not None:
                expr.inicializador = self._expr(expr.inicializador)
            return expr

        if isinstance(expr, ast.ArrayInit):
            expr.elementos = [self._expr(e) for e in expr.elementos]
            return expr

        # Literales, VarRef, this, super, null: nada que optimizar.
        return expr

    # ----------------------------------------- simplificacion de operadores

    def _simplificar_binaria(self, expr: ast.BinaryOp):
        op, izq, der = expr.op, expr.izq, expr.der

        # 1) Plegado de constantes.
        plegado = self._plegar_binaria(op, izq, der, expr)
        if plegado is not None:
            self.cambios.append(f"Constante plegada: ({self._txt(izq)} {op} "
                                f"{self._txt(der)}) -> {self._txt(plegado)}.")
            return plegado

        # 2) Identidades algebraicas.
        ident = self._identidad(op, izq, der)
        if ident is not None:
            self.cambios.append(f"Identidad algebraica aplicada en '{op}'.")
            return ident

        return expr

    def _plegar_binaria(self, op, izq, der, expr):
        # --- Concatenacion de cadenas: "a" + 1 -> "a1"
        if op == "+" and (isinstance(izq, ast.StringLiteral) or isinstance(der, ast.StringLiteral)):
            ti, td = self._texto_literal(izq), self._texto_literal(der)
            if ti is not None and td is not None:
                return ast.StringLiteral(line=expr.line, column=expr.column, valor=ti + td)
            return None

        # --- Logica booleana entre literales.
        if isinstance(izq, ast.BoolLiteral) and isinstance(der, ast.BoolLiteral):
            if op == "&&":
                return ast.BoolLiteral(valor=izq.valor and der.valor)
            if op == "||":
                return ast.BoolLiteral(valor=izq.valor or der.valor)
            if op == "==":
                return ast.BoolLiteral(valor=izq.valor == der.valor)
            if op == "!=":
                return ast.BoolLiteral(valor=izq.valor != der.valor)
            if op in ("&", "|", "^"):
                a, b = int(izq.valor), int(der.valor)
                r = {"&": a & b, "|": a | b, "^": a ^ b}[op]
                return ast.BoolLiteral(valor=bool(r))
            return None

        # --- Aritmetica / comparacion entre enteros.
        ii, id_ = self._int_info(izq), self._int_info(der)
        if ii is not None and id_ is not None:
            return self._plegar_enteros(op, ii, id_, expr)

        return None

    def _plegar_enteros(self, op, ii, id_, expr):
        (a, a_long), (b, b_long) = ii, id_
        es_long = a_long or b_long

        # Comparaciones -> booleano.
        comparaciones = {
            "<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b,
            "==": a == b, "!=": a != b,
        }
        if op in comparaciones:
            return ast.BoolLiteral(valor=comparaciones[op])

        # Aritmetica -> entero (con guardas de rango y division por cero).
        if op == "+":
            r = a + b
        elif op == "-":
            r = a - b
        elif op == "*":
            r = a * b
        elif op in ("/", "%"):
            if b == 0:
                return None   # division por cero: preservar comportamiento en runtime
            r = self._div_java(a, b) if op == "/" else self._mod_java(a, b)
        elif op in ("&", "|", "^"):
            r = {"&": a & b, "|": a | b, "^": a ^ b}[op]
        else:
            return None

        if not self._cabe(r, es_long):
            return None   # desbordamiento: no plegar para no cambiar la semantica

        return ast.IntLiteral(line=expr.line, column=expr.column,
                              valor=f"{r}L" if es_long else str(r))

    def _identidad(self, op, izq, der):
        """Identidades algebraicas que preservan efectos secundarios."""
        izq_cero, der_cero = self._es_cero(izq), self._es_cero(der)
        izq_uno, der_uno = self._es_uno(izq), self._es_uno(der)

        if op == "+":
            if der_cero:
                return izq            # x + 0 -> x
            if izq_cero:
                return der            # 0 + x -> x
        elif op == "-":
            if der_cero:
                return izq            # x - 0 -> x
        elif op == "*":
            if der_uno:
                return izq            # x * 1 -> x
            if izq_uno:
                return der            # 1 * x -> x
            if der_cero and self._puro(izq):
                return ast.IntLiteral(valor="0")   # x * 0 -> 0 (x puro)
            if izq_cero and self._puro(der):
                return ast.IntLiteral(valor="0")   # 0 * x -> 0 (x puro)
        elif op == "/":
            if der_uno:
                return izq            # x / 1 -> x

        # Booleanas (respetando cortocircuito).
        elif op == "&&":
            if self._es_bool(izq, True):
                return der            # true && x -> x
            if self._es_bool(izq, False):
                return izq            # false && x -> false (x no se evalua)
            if self._es_bool(der, True):
                return izq            # x && true -> x
            if self._es_bool(der, False) and self._puro(izq):
                return der            # x && false -> false (x puro)
        elif op == "||":
            if self._es_bool(izq, False):
                return der            # false || x -> x
            if self._es_bool(izq, True):
                return izq            # true || x -> true (x no se evalua)
            if self._es_bool(der, False):
                return izq            # x || false -> x
            if self._es_bool(der, True) and self._puro(izq):
                return der            # x || true -> true (x puro)

        return None

    def _simplificar_unaria(self, expr: ast.UnaryOp):
        op, operando = expr.op, expr.operando

        if op == "!":
            if isinstance(operando, ast.BoolLiteral):
                r = ast.BoolLiteral(valor=not operando.valor)
                self.cambios.append(f"Constante plegada: (!{self._txt(operando)}) "
                                    f"-> {self._txt(r)}.")
                return r
            # !!x -> x
            if isinstance(operando, ast.UnaryOp) and operando.op == "!":
                self.cambios.append("Doble negacion '!!' eliminada.")
                return operando.operando

        if op == "-" and expr.prefijo:
            info = self._int_info(operando)
            if info is not None:
                v, es_long = info
                r = -v
                if self._cabe(r, es_long):
                    lit = ast.IntLiteral(line=expr.line, column=expr.column,
                                         valor=f"{r}L" if es_long else str(r))
                    self.cambios.append(f"Constante plegada: (-{self._txt(operando)}) "
                                        f"-> {self._txt(lit)}.")
                    return lit

        if op == "+" and expr.prefijo and self._int_info(operando) is not None:
            # +literal -> literal (el '+' unario no aporta nada)
            self.cambios.append("Operador unario '+' redundante eliminado.")
            return operando

        if op == "~" and expr.prefijo:
            info = self._int_info(operando)
            if info is not None:
                v, es_long = info
                r = ~v
                if self._cabe(r, es_long):
                    lit = ast.IntLiteral(line=expr.line, column=expr.column,
                                         valor=f"{r}L" if es_long else str(r))
                    self.cambios.append(f"Constante plegada: (~{self._txt(operando)}) "
                                        f"-> {self._txt(lit)}.")
                    return lit

        return expr

    # -------------------------------------------------------- utilidades

    @staticmethod
    def _div_java(a: int, b: int) -> int:
        """Division entera con truncado hacia cero (semantica de Java/C#)."""
        q = abs(a) // abs(b)
        return -q if (a < 0) != (b < 0) else q

    @classmethod
    def _mod_java(cls, a: int, b: int) -> int:
        return a - cls._div_java(a, b) * b

    @staticmethod
    def _cabe(valor: int, es_long: bool) -> bool:
        if es_long:
            return _INT64_MIN <= valor <= _INT64_MAX
        return _INT32_MIN <= valor <= _INT32_MAX

    @staticmethod
    def _int_info(nodo) -> Optional[Tuple[int, bool]]:
        """(valor, es_long) si el nodo es un literal entero; None en otro caso."""
        if not isinstance(nodo, ast.IntLiteral):
            return None
        texto = nodo.valor
        es_long = texto[-1:] in ("l", "L")
        cuerpo = texto[:-1] if es_long else texto
        try:
            return int(cuerpo), es_long
        except ValueError:
            return None

    @staticmethod
    def _texto_literal(nodo) -> Optional[str]:
        """Representacion textual de un literal para concatenacion de cadenas."""
        if isinstance(nodo, ast.StringLiteral):
            return nodo.valor
        if isinstance(nodo, ast.IntLiteral):
            return nodo.valor[:-1] if nodo.valor[-1:] in ("l", "L") else nodo.valor
        if isinstance(nodo, ast.FloatLiteral):
            v = nodo.valor
            return v[:-1] if v[-1:] in ("f", "F", "d", "D") else v
        if isinstance(nodo, ast.CharLiteral):
            return nodo.valor
        if isinstance(nodo, ast.BoolLiteral):
            return "true" if nodo.valor else "false"
        return None

    def _es_cero(self, nodo) -> bool:
        info = self._int_info(nodo)
        return info is not None and info[0] == 0

    def _es_uno(self, nodo) -> bool:
        info = self._int_info(nodo)
        return info is not None and info[0] == 1

    @staticmethod
    def _es_bool(nodo, valor: bool) -> bool:
        return isinstance(nodo, ast.BoolLiteral) and nodo.valor == valor

    @staticmethod
    def _puro(nodo) -> bool:
        """True si evaluar `nodo` no produce efectos secundarios y puede
        descartarse con seguridad."""
        return isinstance(nodo, (ast.IntLiteral, ast.FloatLiteral, ast.CharLiteral,
                                 ast.StringLiteral, ast.BoolLiteral, ast.NullLiteral,
                                 ast.VarRef, ast.ThisExpr, ast.SuperExpr))

    @staticmethod
    def _txt(nodo) -> str:
        """Texto corto de un literal para los mensajes de cambios."""
        if isinstance(nodo, ast.StringLiteral):
            return f'"{nodo.valor}"'
        if isinstance(nodo, (ast.IntLiteral, ast.FloatLiteral)):
            return nodo.valor
        if isinstance(nodo, ast.CharLiteral):
            return f"'{nodo.valor}'"
        if isinstance(nodo, ast.BoolLiteral):
            return "true" if nodo.valor else "false"
        if isinstance(nodo, ast.VarRef):
            return nodo.nombre
        return type(nodo).__name__
