"""Constructor de AST: convierte el arbol de ANTLR en nodos de java_ast.

Se implementa como subclase del visitor generado (JavaSubsetVisitor). Cada
metodo visitXxx devuelve el nodo de java_ast correspondiente.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

from JavaSubsetParser import JavaSubsetParser as P  # noqa: E402
from JavaSubsetVisitor import JavaSubsetVisitor      # noqa: E402

from traductor import java_ast as ast                # noqa: E402


def _pos(ctx):
    return ctx.start.line, ctx.start.column


class ASTBuilder(JavaSubsetVisitor):

    # ----------------------------------------------------- unidad de compilacion

    def visitCompilationUnit(self, ctx: P.CompilationUnitContext):
        line, col = _pos(ctx)
        paquete = None
        if ctx.packageDeclaration():
            paquete = self.visit(ctx.packageDeclaration())
        imports = [self.visit(i) for i in ctx.importDeclaration()]
        tipos = []
        for td in ctx.typeDeclaration():
            nodo = self.visit(td)
            if nodo is not None:
                tipos.append(nodo)
        return ast.CompilationUnit(line=line, column=col,
                                   package=paquete, imports=imports, tipos=tipos)

    def visitPackageDeclaration(self, ctx: P.PackageDeclarationContext):
        line, col = _pos(ctx)
        return ast.PackageDecl(line=line, column=col,
                               nombre=ctx.qualifiedName().getText())

    def visitImportDeclaration(self, ctx: P.ImportDeclarationContext):
        line, col = _pos(ctx)
        texto = ctx.getText()
        return ast.ImportDecl(
            line=line, column=col,
            nombre=ctx.qualifiedName().getText(),
            estatico="static" in texto[:13],
            wildcard=".*" in texto,
        )

    def visitTypeDeclaration(self, ctx: P.TypeDeclarationContext):
        if ctx.classDeclaration():
            return self.visit(ctx.classDeclaration())
        if ctx.interfaceDeclaration():
            return self.visit(ctx.interfaceDeclaration())
        return None   # ';' suelto

    # ----------------------------------------------------- clases / interfaces

    def visitClassDeclaration(self, ctx: P.ClassDeclarationContext):
        line, col = _pos(ctx)
        mods = [m.getText() for m in ctx.modifier()]
        superclase = self._tipo(ctx.typeType()) if ctx.typeType() else None
        interfaces = self._type_list(ctx.typeList())
        miembros = self._class_body(ctx.classBody())
        return ast.ClassDecl(line=line, column=col,
                             nombre=ctx.IDENTIFIER().getText(),
                             modificadores=mods, superclase=superclase,
                             interfaces=interfaces, miembros=miembros)

    def visitInterfaceDeclaration(self, ctx: P.InterfaceDeclarationContext):
        line, col = _pos(ctx)
        mods = [m.getText() for m in ctx.modifier()]
        interfaces = self._type_list(ctx.typeList())
        miembros = self._class_body(ctx.classBody())
        return ast.InterfaceDecl(line=line, column=col,
                                 nombre=ctx.IDENTIFIER().getText(),
                                 modificadores=mods, interfaces=interfaces,
                                 miembros=miembros)

    def _class_body(self, ctx: P.ClassBodyContext) -> List[ast.NodoAST]:
        miembros: List[ast.NodoAST] = []
        for decl in ctx.classBodyDeclaration():
            md = decl.memberDeclaration()
            if md is None:
                continue
            nodo = self.visit(md)
            if isinstance(nodo, list):
                miembros.extend(nodo)
            elif nodo is not None:
                miembros.append(nodo)
        return miembros

    def visitMemberDeclaration(self, ctx: P.MemberDeclarationContext):
        if ctx.methodDeclaration():
            return self.visit(ctx.methodDeclaration())
        if ctx.constructorDeclaration():
            return self.visit(ctx.constructorDeclaration())
        return self.visit(ctx.fieldDeclaration())

    # ----------------------------------------------------- miembros

    def visitFieldDeclaration(self, ctx: P.FieldDeclarationContext):
        mods = [m.getText() for m in ctx.modifier()]
        tipo = self._tipo(ctx.typeType())
        campos = []
        for vd in ctx.variableDeclarators().variableDeclarator():
            line, col = _pos(vd)
            nombre, valor = self._var_declarator(vd)
            campos.append(ast.FieldDecl(line=line, column=col, nombre=nombre,
                                        tipo=tipo, valor=valor, modificadores=mods))
        return campos

    def visitMethodDeclaration(self, ctx: P.MethodDeclarationContext):
        line, col = _pos(ctx)
        mods = [m.getText() for m in ctx.modifier()]
        tipo_ret = self._tipo(ctx.typeType()) if ctx.typeType() else None
        params = self._formal_params(ctx.formalParameters())
        cuerpo = self.visit(ctx.block()) if ctx.block() else None
        return ast.MethodDecl(line=line, column=col,
                              nombre=ctx.IDENTIFIER().getText(),
                              tipo_retorno=tipo_ret, parametros=params,
                              cuerpo=cuerpo, modificadores=mods)

    def visitConstructorDeclaration(self, ctx: P.ConstructorDeclarationContext):
        line, col = _pos(ctx)
        mods = [m.getText() for m in ctx.modifier()]
        params = self._formal_params(ctx.formalParameters())
        cuerpo = self.visit(ctx.block())
        return ast.ConstructorDecl(line=line, column=col,
                                   nombre=ctx.IDENTIFIER().getText(),
                                   parametros=params, cuerpo=cuerpo,
                                   modificadores=mods)

    def _formal_params(self, ctx: P.FormalParametersContext) -> List[ast.Parameter]:
        params: List[ast.Parameter] = []
        lista = ctx.formalParameterList()
        if lista is None:
            return params
        for fp in lista.formalParameter():
            line, col = _pos(fp)
            params.append(ast.Parameter(
                line=line, column=col,
                nombre=fp.IDENTIFIER().getText(),
                tipo=self._tipo(fp.typeType()),
                modificadores=[m.getText() for m in fp.modifier()],
            ))
        return params

    def _var_declarator(self, ctx: P.VariableDeclaratorContext):
        nombre = ctx.IDENTIFIER().getText()
        valor = None
        if ctx.variableInitializer():
            valor = self._var_initializer(ctx.variableInitializer())
        return nombre, valor

    def _var_initializer(self, ctx: P.VariableInitializerContext):
        if ctx.arrayInitializer():
            return self._array_initializer(ctx.arrayInitializer())
        return self.visit(ctx.expression())

    def _array_initializer(self, ctx: P.ArrayInitializerContext):
        line, col = _pos(ctx)
        elems = [self._var_initializer(vi) for vi in ctx.variableInitializer()]
        return ast.ArrayInit(line=line, column=col, elementos=elems)

    # ----------------------------------------------------- tipos

    def _tipo(self, ctx: P.TypeTypeContext) -> Optional[ast.Tipo]:
        if ctx is None:
            return None
        dims = sum(1 for ch in ctx.getChildren()
                   if getattr(ch, "getText", lambda: "")() == "[")
        if ctx.primitiveType():
            return ast.Tipo(nombre=ctx.primitiveType().getText(), dims=dims)
        coi = ctx.classOrInterfaceType()
        nombre = ".".join(t.getText() for t in coi.IDENTIFIER())
        genericos: List[ast.Tipo] = []
        targs = coi.typeArguments()
        if targs:
            ultimo = targs[-1] if isinstance(targs, list) else targs
            genericos = [self._tipo(t) for t in ultimo.typeType()]
        return ast.Tipo(nombre=nombre, genericos=genericos, dims=dims)

    def _type_list(self, ctx) -> List[ast.Tipo]:
        if ctx is None:
            return []
        return [self._tipo(t) for t in ctx.typeType()]

    # ----------------------------------------------------- sentencias

    def visitBlock(self, ctx: P.BlockContext):
        line, col = _pos(ctx)
        sentencias: List[ast.NodoAST] = []
        for bs in ctx.blockStatement():
            nodo = self.visit(bs)
            if isinstance(nodo, list):
                sentencias.extend(nodo)
            elif nodo is not None:
                sentencias.append(nodo)
        return ast.Block(line=line, column=col, sentencias=sentencias)

    def visitBlockStatement(self, ctx: P.BlockStatementContext):
        if ctx.localVariableDeclaration():
            return self._local_var_decls(ctx.localVariableDeclaration())
        return self.visit(ctx.statement())

    def _local_var_decls(self, ctx: P.LocalVariableDeclarationContext):
        tipo = self._tipo(ctx.typeType())
        decls = []
        for vd in ctx.variableDeclarators().variableDeclarator():
            line, col = _pos(vd)
            nombre, valor = self._var_declarator(vd)
            decls.append(ast.LocalVarDecl(line=line, column=col, nombre=nombre,
                                          tipo=tipo, valor=valor))
        return decls

    def visitBlockStmt(self, ctx: P.BlockStmtContext):
        return self.visit(ctx.block())

    def visitLocalVarStmt(self, ctx: P.LocalVarStmtContext):
        decls = self._local_var_decls(ctx.localVariableDeclaration())
        # En contexto de sentencia simple devolvemos una lista; el llamador la
        # aplana. Solo ocurre cuando un 'for'/'if' sin llaves declara variables.
        return decls

    def visitIfStmt(self, ctx: P.IfStmtContext):
        line, col = _pos(ctx)
        cond = self.visit(ctx.expression())
        stmts = ctx.statement()
        entonces = self.visit(stmts[0])
        sino = self.visit(stmts[1]) if len(stmts) > 1 else None
        return ast.IfStmt(line=line, column=col, condicion=cond,
                          entonces=self._como_stmt(entonces),
                          sino=self._como_stmt(sino))

    def visitWhileStmt(self, ctx: P.WhileStmtContext):
        line, col = _pos(ctx)
        return ast.WhileStmt(line=line, column=col,
                             condicion=self.visit(ctx.expression()),
                             cuerpo=self._como_stmt(self.visit(ctx.statement())))

    def visitDoWhileStmt(self, ctx: P.DoWhileStmtContext):
        line, col = _pos(ctx)
        return ast.DoWhileStmt(line=line, column=col,
                               cuerpo=self._como_stmt(self.visit(ctx.statement())),
                               condicion=self.visit(ctx.expression()))

    def visitForStmt(self, ctx: P.ForStmtContext):
        line, col = _pos(ctx)
        fc = ctx.forControl()
        cuerpo = self._como_stmt(self.visit(ctx.statement()))
        if fc.enhancedForControl():
            efc = fc.enhancedForControl()
            return ast.ForEachStmt(
                line=line, column=col,
                tipo=self._tipo(efc.typeType()),
                nombre=efc.IDENTIFIER().getText(),
                iterable=self.visit(efc.expression()),
                cuerpo=cuerpo,
            )
        # for clasico
        init: List[ast.NodoAST] = []
        if fc.forInit():
            fi = fc.forInit()
            if fi.localVariableDeclaration():
                init = self._local_var_decls(fi.localVariableDeclaration())
            else:
                init = [self.visit(e) for e in fi.expressionList().expression()]
        cond = self.visit(fc.expression()) if fc.expression() else None
        update = []
        if fc.expressionList():
            update = [self.visit(e) for e in fc.expressionList().expression()]
        return ast.ForStmt(line=line, column=col, init=init, condicion=cond,
                           update=update, cuerpo=cuerpo)

    def visitReturnStmt(self, ctx: P.ReturnStmtContext):
        line, col = _pos(ctx)
        valor = self.visit(ctx.expression()) if ctx.expression() else None
        return ast.ReturnStmt(line=line, column=col, valor=valor)

    def visitBreakStmt(self, ctx: P.BreakStmtContext):
        line, col = _pos(ctx)
        return ast.BreakStmt(line=line, column=col)

    def visitContinueStmt(self, ctx: P.ContinueStmtContext):
        line, col = _pos(ctx)
        return ast.ContinueStmt(line=line, column=col)

    def visitThrowStmt(self, ctx: P.ThrowStmtContext):
        line, col = _pos(ctx)
        return ast.ThrowStmt(line=line, column=col,
                             valor=self.visit(ctx.expression()))

    def visitExprStmt(self, ctx: P.ExprStmtContext):
        line, col = _pos(ctx)
        return ast.ExprStmt(line=line, column=col,
                            expr=self.visit(ctx.expression()))

    def visitEmptyStmt(self, ctx: P.EmptyStmtContext):
        return None

    def _como_stmt(self, nodo):
        """Una sentencia sin llaves puede expandirse a una lista (decl multiple).
        La envolvemos en un Block para que el generador la trate uniforme."""
        if isinstance(nodo, list):
            return ast.Block(line=0, column=0, sentencias=nodo)
        return nodo

    # ----------------------------------------------------- expresiones

    def visitPrimaryExpr(self, ctx: P.PrimaryExprContext):
        return self.visit(ctx.primary())

    def visitParenExpr(self, ctx: P.ParenExprContext):
        return self.visit(ctx.expression())

    def visitThisExpr(self, ctx: P.ThisExprContext):
        line, col = _pos(ctx)
        return ast.ThisExpr(line=line, column=col)

    def visitSuperExpr(self, ctx: P.SuperExprContext):
        line, col = _pos(ctx)
        return ast.SuperExpr(line=line, column=col)

    def visitIdExpr(self, ctx: P.IdExprContext):
        line, col = _pos(ctx)
        return ast.VarRef(line=line, column=col, nombre=ctx.IDENTIFIER().getText())

    def visitLiteralExpr(self, ctx: P.LiteralExprContext):
        return self._literal(ctx.literal())

    def _literal(self, ctx: P.LiteralContext):
        line, col = _pos(ctx)
        texto = ctx.getText()
        if ctx.DECIMAL_LITERAL():
            return ast.IntLiteral(line=line, column=col, valor=texto)
        if ctx.FLOAT_LITERAL():
            return ast.FloatLiteral(line=line, column=col, valor=texto)
        if ctx.CHAR_LITERAL():
            return ast.CharLiteral(line=line, column=col, valor=texto[1:-1])
        if ctx.STRING_LITERAL():
            return ast.StringLiteral(line=line, column=col, valor=texto[1:-1])
        if texto in ("true", "false"):
            return ast.BoolLiteral(line=line, column=col, valor=texto == "true")
        return ast.NullLiteral(line=line, column=col)

    def visitFieldAccessExpr(self, ctx: P.FieldAccessExprContext):
        line, col = _pos(ctx)
        return ast.FieldAccess(line=line, column=col,
                               objeto=self.visit(ctx.expression()),
                               nombre=ctx.IDENTIFIER().getText())

    def visitMethodCallExpr(self, ctx: P.MethodCallExprContext):
        line, col = _pos(ctx)
        return ast.MethodCall(line=line, column=col,
                              objeto=self.visit(ctx.expression()),
                              nombre=ctx.IDENTIFIER().getText(),
                              argumentos=self._args(ctx.arguments()))

    def visitCallExpr(self, ctx: P.CallExprContext):
        line, col = _pos(ctx)
        return ast.MethodCall(line=line, column=col, objeto=None,
                              nombre=ctx.IDENTIFIER().getText(),
                              argumentos=self._args(ctx.arguments()))

    def visitArrayAccessExpr(self, ctx: P.ArrayAccessExprContext):
        line, col = _pos(ctx)
        exprs = ctx.expression()
        return ast.ArrayAccess(line=line, column=col,
                               objeto=self.visit(exprs[0]),
                               indice=self.visit(exprs[1]))

    def visitNewExpr(self, ctx: P.NewExprContext):
        return self.visit(ctx.creator())

    def visitObjectCreator(self, ctx: P.ObjectCreatorContext):
        line, col = _pos(ctx)
        tipo = self._coi_tipo(ctx.classOrInterfaceType())
        return ast.NewObject(line=line, column=col, tipo=tipo,
                             argumentos=self._args(ctx.arguments()))

    def visitArrayCreator(self, ctx: P.ArrayCreatorContext):
        line, col = _pos(ctx)
        tipo = self._creator_base_tipo(ctx)
        dims_exprs = [self.visit(e) for e in ctx.expression()]
        return ast.NewArray(line=line, column=col, tipo=tipo, dims_exprs=dims_exprs)

    def visitArrayCreatorInit(self, ctx: P.ArrayCreatorInitContext):
        line, col = _pos(ctx)
        tipo = self._creator_base_tipo(ctx)
        init = self._array_initializer(ctx.arrayInitializer())
        return ast.NewArray(line=line, column=col, tipo=tipo, inicializador=init)

    def _creator_base_tipo(self, ctx) -> ast.Tipo:
        if ctx.primitiveType():
            return ast.Tipo(nombre=ctx.primitiveType().getText())
        return self._coi_tipo(ctx.classOrInterfaceType())

    def _coi_tipo(self, coi: P.ClassOrInterfaceTypeContext) -> ast.Tipo:
        nombre = ".".join(t.getText() for t in coi.IDENTIFIER())
        genericos: List[ast.Tipo] = []
        targs = coi.typeArguments()
        if targs:
            ultimo = targs[-1] if isinstance(targs, list) else targs
            genericos = [self._tipo(t) for t in ultimo.typeType()]
        return ast.Tipo(nombre=nombre, genericos=genericos)

    def visitCastExpr(self, ctx: P.CastExprContext):
        line, col = _pos(ctx)
        return ast.Cast(line=line, column=col, tipo=self._tipo(ctx.typeType()),
                        expr=self.visit(ctx.expression()))

    def visitPrefixExpr(self, ctx: P.PrefixExprContext):
        line, col = _pos(ctx)
        return ast.UnaryOp(line=line, column=col, op=ctx.op.text,
                           operando=self.visit(ctx.expression()), prefijo=True)

    def visitPostfixExpr(self, ctx: P.PostfixExprContext):
        line, col = _pos(ctx)
        return ast.UnaryOp(line=line, column=col, op=ctx.op.text,
                           operando=self.visit(ctx.expression()), prefijo=False)

    def visitInstanceofExpr(self, ctx: P.InstanceofExprContext):
        line, col = _pos(ctx)
        return ast.InstanceOf(line=line, column=col,
                              expr=self.visit(ctx.expression()),
                              tipo=self._tipo(ctx.typeType()))

    def visitTernaryExpr(self, ctx: P.TernaryExprContext):
        line, col = _pos(ctx)
        e = ctx.expression()
        return ast.Ternary(line=line, column=col, condicion=self.visit(e[0]),
                           si=self.visit(e[1]), no=self.visit(e[2]))

    def visitAssignExpr(self, ctx: P.AssignExprContext):
        line, col = _pos(ctx)
        e = ctx.expression()
        return ast.Assign(line=line, column=col, op=ctx.op.text,
                          destino=self.visit(e[0]), valor=self.visit(e[1]))

    # operadores binarios: todos comparten la misma forma (op + 2 expresiones)
    def _binop(self, ctx):
        line, col = _pos(ctx)
        e = ctx.expression()
        return ast.BinaryOp(line=line, column=col, op=ctx.op.text,
                            izq=self.visit(e[0]), der=self.visit(e[1]))

    def visitMulExpr(self, ctx):   return self._binop(ctx)
    def visitAddExpr(self, ctx):   return self._binop(ctx)
    def visitShiftExpr(self, ctx): return self._binop(ctx)
    def visitRelExpr(self, ctx):   return self._binop(ctx)
    def visitEqExpr(self, ctx):    return self._binop(ctx)

    def _binop_fixed(self, ctx, op):
        line, col = _pos(ctx)
        e = ctx.expression()
        return ast.BinaryOp(line=line, column=col, op=op,
                            izq=self.visit(e[0]), der=self.visit(e[1]))

    def visitBitAndExpr(self, ctx): return self._binop_fixed(ctx, "&")
    def visitBitXorExpr(self, ctx): return self._binop_fixed(ctx, "^")
    def visitBitOrExpr(self, ctx):  return self._binop_fixed(ctx, "|")
    def visitAndExpr(self, ctx):    return self._binop_fixed(ctx, "&&")
    def visitOrExpr(self, ctx):     return self._binop_fixed(ctx, "||")

    # ----------------------------------------------------- helpers

    def _args(self, ctx: P.ArgumentsContext) -> List[ast.NodoAST]:
        if ctx is None or ctx.expressionList() is None:
            return []
        return [self.visit(e) for e in ctx.expressionList().expression()]
