"""Generador de codigo C#.

Visitor que recorre el AST de Java (java_ast) y emite codigo C# como texto.
Las sentencias devuelven List[str] (lineas) y las expresiones devuelven str.
"""

from __future__ import annotations

from typing import List, Optional

from traductor import java_ast as ast
from traductor.mapeos import MapeoTipos, MapeoMetodos, MODIFICADORES


class GeneradorCSharp:

    def __init__(self) -> None:
        self.tipos = MapeoTipos()
        self.metodos = MapeoMetodos()
        self._nivel = 0
        self._usings = {"System", "System.Collections.Generic"}

    # ------------------------------------------------------------------ API

    def generar(self, unidad: ast.CompilationUnit) -> str:
        cuerpo: List[str] = []

        # namespace
        tiene_ns = unidad.package is not None
        if tiene_ns:
            cuerpo.append(f"namespace {self._namespace(unidad.package.nombre)}")
            cuerpo.append("{")
            self._nivel += 1

        for i, tipo in enumerate(unidad.tipos):
            if i > 0:
                cuerpo.append("")
            if isinstance(tipo, ast.ClassDecl):
                cuerpo.extend(self._clase(tipo))
            elif isinstance(tipo, ast.InterfaceDecl):
                cuerpo.extend(self._interfaz(tipo))

        if tiene_ns:
            self._nivel -= 1
            cuerpo.append("}")

        # usings al final (ya recolectados durante la generacion)
        encabezado = [f"using {u};" for u in sorted(self._usings)]
        encabezado.append("")
        return "\n".join(encabezado + cuerpo) + "\n"

    # ----------------------------------------------------------- tipos (decl)

    def _clase(self, clase: ast.ClassDecl) -> List[str]:
        lineas: List[str] = []
        firma = self._mods_clase(clase.modificadores) + f"class {clase.nombre}"
        bases = []
        if clase.superclase is not None:
            bases.append(self.tipos.mapear(clase.superclase))
        bases.extend(self.tipos.mapear(i) for i in clase.interfaces)
        if bases:
            firma += " : " + ", ".join(bases)

        lineas.append(self._ind() + firma)
        lineas.append(self._ind() + "{")
        self._nivel += 1
        lineas.extend(self._miembros(clase.nombre, clase.miembros))
        self._nivel -= 1
        lineas.append(self._ind() + "}")
        return lineas

    def _interfaz(self, itf: ast.InterfaceDecl) -> List[str]:
        lineas: List[str] = []
        firma = self._mods_clase([m for m in itf.modificadores if m != "abstract"])
        firma += f"interface {itf.nombre}"
        if itf.interfaces:
            firma += " : " + ", ".join(self.tipos.mapear(i) for i in itf.interfaces)
        lineas.append(self._ind() + firma)
        lineas.append(self._ind() + "{")
        self._nivel += 1
        for m in itf.miembros:
            if isinstance(m, ast.MethodDecl):
                tipo_ret = self.tipos.mapear(m.tipo_retorno)
                params = self._parametros(m.parametros)
                lineas.append(f"{self._ind()}{tipo_ret} {m.nombre}({params});")
        self._nivel -= 1
        lineas.append(self._ind() + "}")
        return lineas

    def _miembros(self, nombre_clase: str, miembros: List[ast.NodoAST]) -> List[str]:
        lineas: List[str] = []
        primero = True
        for m in miembros:
            if not primero and not isinstance(m, ast.FieldDecl):
                lineas.append("")
            primero = False
            if isinstance(m, ast.FieldDecl):
                lineas.append(self._campo(m))
            elif isinstance(m, ast.ConstructorDecl):
                lineas.extend(self._constructor(nombre_clase, m))
            elif isinstance(m, ast.MethodDecl):
                lineas.extend(self._metodo(m))
        return lineas

    def _campo(self, campo: ast.FieldDecl) -> str:
        mods = self._mods_miembro(campo.modificadores)
        tipo = self.tipos.mapear(campo.tipo)
        linea = f"{self._ind()}{mods}{tipo} {campo.nombre}"
        if campo.valor is not None:
            linea += f" = {self._expr(campo.valor)}"
        return linea + ";"

    def _constructor(self, nombre_clase: str, ctor: ast.ConstructorDecl) -> List[str]:
        mods = self._mods_miembro([m for m in ctor.modificadores])
        params = self._parametros(ctor.parametros)
        cabecera = f"{self._ind()}{mods}{nombre_clase}({params})"
        return self._con_cuerpo(cabecera, ctor.cuerpo)

    def _metodo(self, metodo: ast.MethodDecl) -> List[str]:
        mods = self._mods_miembro(metodo.modificadores)
        tipo_ret = self.tipos.mapear(metodo.tipo_retorno)
        params = self._parametros(metodo.parametros)
        cabecera = f"{self._ind()}{mods}{tipo_ret} {metodo.nombre}({params})"
        if metodo.cuerpo is None:
            return [cabecera + ";"]
        return self._con_cuerpo(cabecera, metodo.cuerpo)

    def _con_cuerpo(self, cabecera: str, cuerpo: ast.Block) -> List[str]:
        lineas = [cabecera, self._ind() + "{"]
        self._nivel += 1
        lineas.extend(self._sentencias(cuerpo.sentencias))
        self._nivel -= 1
        lineas.append(self._ind() + "}")
        return lineas

    def _parametros(self, params: List[ast.Parameter]) -> str:
        return ", ".join(f"{self.tipos.mapear(p.tipo)} {p.nombre}" for p in params)

    # ----------------------------------------------------------- sentencias

    def _sentencias(self, stmts: List[ast.NodoAST]) -> List[str]:
        lineas: List[str] = []
        for s in stmts:
            lineas.extend(self._stmt(s))
        return lineas

    def _stmt(self, stmt) -> List[str]:
        if stmt is None:
            return []
        if isinstance(stmt, ast.LocalVarDecl):
            tipo = self.tipos.mapear(stmt.tipo)
            linea = f"{self._ind()}{tipo} {stmt.nombre}"
            if stmt.valor is not None:
                linea += f" = {self._expr(stmt.valor)}"
            return [linea + ";"]

        if isinstance(stmt, ast.ExprStmt):
            return [f"{self._ind()}{self._expr(stmt.expr)};"]

        if isinstance(stmt, ast.ReturnStmt):
            if stmt.valor is None:
                return [f"{self._ind()}return;"]
            return [f"{self._ind()}return {self._expr(stmt.valor)};"]

        if isinstance(stmt, ast.BreakStmt):
            return [f"{self._ind()}break;"]

        if isinstance(stmt, ast.ContinueStmt):
            return [f"{self._ind()}continue;"]

        if isinstance(stmt, ast.ThrowStmt):
            return [f"{self._ind()}throw {self._expr(stmt.valor)};"]

        if isinstance(stmt, ast.Block):
            lineas = [f"{self._ind()}{{"]
            self._nivel += 1
            lineas.extend(self._sentencias(stmt.sentencias))
            self._nivel -= 1
            lineas.append(f"{self._ind()}}}")
            return lineas

        if isinstance(stmt, ast.IfStmt):
            return self._if(stmt)

        if isinstance(stmt, ast.WhileStmt):
            lineas = [f"{self._ind()}while ({self._expr(stmt.condicion)})"]
            lineas.extend(self._cuerpo_bloque(stmt.cuerpo))
            return lineas

        if isinstance(stmt, ast.DoWhileStmt):
            lineas = [f"{self._ind()}do"]
            lineas.extend(self._cuerpo_bloque(stmt.cuerpo))
            lineas.append(f"{self._ind()}while ({self._expr(stmt.condicion)});")
            return lineas

        if isinstance(stmt, ast.ForEachStmt):
            tipo = self.tipos.mapear(stmt.tipo)
            cab = f"{self._ind()}foreach ({tipo} {stmt.nombre} in {self._expr(stmt.iterable)})"
            return [cab] + self._cuerpo_bloque(stmt.cuerpo)

        if isinstance(stmt, ast.ForStmt):
            return self._for(stmt)

        return []

    def _if(self, stmt: ast.IfStmt) -> List[str]:
        lineas = [f"{self._ind()}if ({self._expr(stmt.condicion)})"]
        lineas.extend(self._cuerpo_bloque(stmt.entonces))
        if stmt.sino is not None:
            # else if encadenado
            if isinstance(stmt.sino, ast.IfStmt):
                sub = self._if(stmt.sino)
                sub[0] = f"{self._ind()}else " + sub[0].lstrip()
                lineas.extend(sub)
            else:
                lineas.append(f"{self._ind()}else")
                lineas.extend(self._cuerpo_bloque(stmt.sino))
        return lineas

    def _for(self, stmt: ast.ForStmt) -> List[str]:
        init = self._for_init(stmt.init)
        cond = self._expr(stmt.condicion) if stmt.condicion else ""
        upd = ", ".join(self._expr(u) for u in stmt.update)
        cab = f"{self._ind()}for ({init}; {cond}; {upd})"
        return [cab] + self._cuerpo_bloque(stmt.cuerpo)

    def _for_init(self, init: List[ast.NodoAST]) -> str:
        if not init:
            return ""
        primero = init[0]
        if isinstance(primero, ast.LocalVarDecl):
            tipo = self.tipos.mapear(primero.tipo)
            partes = []
            for i, d in enumerate(init):
                if i == 0:
                    txt = f"{tipo} {d.nombre}"
                else:
                    txt = d.nombre
                if d.valor is not None:
                    txt += f" = {self._expr(d.valor)}"
                partes.append(txt)
            return ", ".join(partes)
        return ", ".join(self._expr(e) for e in init)

    def _cuerpo_bloque(self, cuerpo) -> List[str]:
        """Emite el cuerpo de un if/for/while siempre con llaves (estilo C#)."""
        if isinstance(cuerpo, ast.Block):
            lineas = [f"{self._ind()}{{"]
            self._nivel += 1
            lineas.extend(self._sentencias(cuerpo.sentencias))
            self._nivel -= 1
            lineas.append(f"{self._ind()}}}")
            return lineas
        # sentencia simple -> envolver en llaves
        lineas = [f"{self._ind()}{{"]
        self._nivel += 1
        lineas.extend(self._stmt(cuerpo))
        self._nivel -= 1
        lineas.append(f"{self._ind()}}}")
        return lineas

    # ----------------------------------------------------------- expresiones

    def _expr(self, expr) -> str:
        if expr is None:
            return ""
        if isinstance(expr, ast.IntLiteral):
            return expr.valor
        if isinstance(expr, ast.FloatLiteral):
            return expr.valor
        if isinstance(expr, ast.CharLiteral):
            return f"'{expr.valor}'"
        if isinstance(expr, ast.StringLiteral):
            return f'"{expr.valor}"'
        if isinstance(expr, ast.BoolLiteral):
            return "true" if expr.valor else "false"
        if isinstance(expr, ast.NullLiteral):
            return "null"
        if isinstance(expr, ast.VarRef):
            return expr.nombre
        if isinstance(expr, ast.ThisExpr):
            return "this"
        if isinstance(expr, ast.SuperExpr):
            return "base"
        if isinstance(expr, ast.Assign):
            return f"{self._expr(expr.destino)} {expr.op} {self._expr(expr.valor)}"
        if isinstance(expr, ast.BinaryOp):
            return f"{self._expr(expr.izq)} {expr.op} {self._expr(expr.der)}"
        if isinstance(expr, ast.UnaryOp):
            if expr.prefijo:
                return f"{expr.op}{self._expr(expr.operando)}"
            return f"{self._expr(expr.operando)}{expr.op}"
        if isinstance(expr, ast.Ternary):
            return (f"{self._expr(expr.condicion)} ? "
                    f"{self._expr(expr.si)} : {self._expr(expr.no)}")
        if isinstance(expr, ast.Cast):
            return f"({self.tipos.mapear(expr.tipo)}){self._expr(expr.expr)}"
        if isinstance(expr, ast.InstanceOf):
            return f"{self._expr(expr.expr)} is {self.tipos.mapear(expr.tipo)}"
        if isinstance(expr, ast.FieldAccess):
            return self._field_access(expr)
        if isinstance(expr, ast.ArrayAccess):
            return f"{self._expr(expr.objeto)}[{self._expr(expr.indice)}]"
        if isinstance(expr, ast.MethodCall):
            return self._method_call(expr)
        if isinstance(expr, ast.NewObject):
            args = ", ".join(self._expr(a) for a in expr.argumentos)
            return f"new {self.tipos.mapear(expr.tipo)}({args})"
        if isinstance(expr, ast.NewArray):
            return self._new_array(expr)
        if isinstance(expr, ast.ArrayInit):
            elems = ", ".join(self._expr(e) for e in expr.elementos)
            return f"{{ {elems} }}"
        return ""

    def _field_access(self, expr: ast.FieldAccess) -> str:
        obj = self._expr(expr.objeto)
        # length de array Java -> Length en C#
        if expr.nombre == "length":
            return f"{obj}.Length"
        return f"{obj}.{expr.nombre}"

    def _new_array(self, expr: ast.NewArray) -> str:
        base = self.tipos.mapear(expr.tipo)
        if expr.inicializador is not None:
            elems = ", ".join(self._expr(e) for e in expr.inicializador.elementos)
            return f"new {base}[] {{ {elems} }}"
        dims = "".join(f"[{self._expr(d)}]" for d in expr.dims_exprs)
        return f"new {base}{dims}"

    def _method_call(self, expr: ast.MethodCall) -> str:
        args = [self._expr(a) for a in expr.argumentos]
        args_str = ", ".join(args)

        # System.out.println / print -> Console.WriteLine / Write
        receptor = self._receptor_texto(expr.objeto)
        if receptor == "System.out":
            if expr.nombre == "println":
                return f"Console.WriteLine({args_str})"
            if expr.nombre == "print":
                return f"Console.Write({args_str})"
        if receptor == "System.err":
            if expr.nombre in ("println", "print"):
                metodo = "WriteLine" if expr.nombre == "println" else "Write"
                return f"Console.Error.{metodo}({args_str})"

        # Llamada sin receptor (metodo de la misma clase)
        if expr.objeto is None:
            return f"{expr.nombre}({args_str})"

        obj = self._expr(expr.objeto)
        nombre = expr.nombre

        # Propiedades: x.size() -> x.Count, x.length() -> x.Length
        if self.metodos.es_propiedad(nombre) and not args:
            prop = self.metodos.mapear_propiedad(nombre)
            if prop == "__is_empty__":
                # isEmpty() aplica tanto a String como a colecciones; sin
                # inferencia de tipos completa usamos LINQ, valido para ambos.
                self._usings.add("System.Linq")
                return f"!{obj}.Any()"
            return f"{obj}.{prop}"

        metodo = self.metodos.mapear_metodo(nombre)

        # Casos especiales con forma distinta
        if metodo == "__indexer__":        # get(i)/charAt(i) -> obj[i]
            return f"{obj}[{args[0]}]" if args else f"{obj}[]"
        if metodo == "__set_indexer__":    # list.set(i, v) -> obj[i] = v
            return f"{obj}[{args[0]}] = {args[1]}"
        if metodo == "__put__":            # map.put(k, v) -> obj[k] = v
            return f"{obj}[{args[0]}] = {args[1]}"

        return f"{obj}.{metodo}({args_str})"

    def _receptor_texto(self, objeto) -> Optional[str]:
        """Reconstruye 'System.out' a partir de FieldAccess/VarRef anidados."""
        if isinstance(objeto, ast.FieldAccess):
            base = self._receptor_texto(objeto.objeto)
            return f"{base}.{objeto.nombre}" if base else objeto.nombre
        if isinstance(objeto, ast.VarRef):
            return objeto.nombre
        return None

    # ----------------------------------------------------------- helpers

    def _namespace(self, paquete: str) -> str:
        return ".".join(p[:1].upper() + p[1:] for p in paquete.split("."))

    def _mods_clase(self, mods: List[str]) -> str:
        salida = []
        for m in mods:
            if m == "final":
                salida.append("sealed")
            elif m == "static":
                salida.append("static")
            elif m in MODIFICADORES and m != "final":
                salida.append(MODIFICADORES[m])
        return (" ".join(salida) + " ") if salida else ""

    def _mods_miembro(self, mods: List[str]) -> str:
        salida = []
        for m in mods:
            if m == "final":
                # 'final' en campo -> readonly; en metodo no tiene equivalente directo.
                salida.append("readonly")
            elif m in MODIFICADORES:
                salida.append(MODIFICADORES[m])
        return (" ".join(salida) + " ") if salida else ""

    def _ind(self) -> str:
        return "    " * self._nivel
