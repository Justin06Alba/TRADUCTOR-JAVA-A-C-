# Generated from traductor/grammar/JavaSubset.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .JavaSubsetParser import JavaSubsetParser
else:
    from JavaSubsetParser import JavaSubsetParser

# This class defines a complete generic visitor for a parse tree produced by JavaSubsetParser.

class JavaSubsetVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JavaSubsetParser#compilationUnit.
    def visitCompilationUnit(self, ctx:JavaSubsetParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#packageDeclaration.
    def visitPackageDeclaration(self, ctx:JavaSubsetParser.PackageDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#importDeclaration.
    def visitImportDeclaration(self, ctx:JavaSubsetParser.ImportDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx:JavaSubsetParser.TypeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#classDeclaration.
    def visitClassDeclaration(self, ctx:JavaSubsetParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#interfaceDeclaration.
    def visitInterfaceDeclaration(self, ctx:JavaSubsetParser.InterfaceDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#classBody.
    def visitClassBody(self, ctx:JavaSubsetParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#classBodyDeclaration.
    def visitClassBodyDeclaration(self, ctx:JavaSubsetParser.ClassBodyDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#memberDeclaration.
    def visitMemberDeclaration(self, ctx:JavaSubsetParser.MemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:JavaSubsetParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:JavaSubsetParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#constructorDeclaration.
    def visitConstructorDeclaration(self, ctx:JavaSubsetParser.ConstructorDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#variableDeclarators.
    def visitVariableDeclarators(self, ctx:JavaSubsetParser.VariableDeclaratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#variableDeclarator.
    def visitVariableDeclarator(self, ctx:JavaSubsetParser.VariableDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#variableInitializer.
    def visitVariableInitializer(self, ctx:JavaSubsetParser.VariableInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#arrayInitializer.
    def visitArrayInitializer(self, ctx:JavaSubsetParser.ArrayInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#formalParameters.
    def visitFormalParameters(self, ctx:JavaSubsetParser.FormalParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#formalParameterList.
    def visitFormalParameterList(self, ctx:JavaSubsetParser.FormalParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#formalParameter.
    def visitFormalParameter(self, ctx:JavaSubsetParser.FormalParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#modifier.
    def visitModifier(self, ctx:JavaSubsetParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#typeType.
    def visitTypeType(self, ctx:JavaSubsetParser.TypeTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#classOrInterfaceType.
    def visitClassOrInterfaceType(self, ctx:JavaSubsetParser.ClassOrInterfaceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#typeArguments.
    def visitTypeArguments(self, ctx:JavaSubsetParser.TypeArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#primitiveType.
    def visitPrimitiveType(self, ctx:JavaSubsetParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#typeList.
    def visitTypeList(self, ctx:JavaSubsetParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#block.
    def visitBlock(self, ctx:JavaSubsetParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#blockStatement.
    def visitBlockStatement(self, ctx:JavaSubsetParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#localVariableDeclaration.
    def visitLocalVariableDeclaration(self, ctx:JavaSubsetParser.LocalVariableDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#blockStmt.
    def visitBlockStmt(self, ctx:JavaSubsetParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#ifStmt.
    def visitIfStmt(self, ctx:JavaSubsetParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#forStmt.
    def visitForStmt(self, ctx:JavaSubsetParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#whileStmt.
    def visitWhileStmt(self, ctx:JavaSubsetParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#doWhileStmt.
    def visitDoWhileStmt(self, ctx:JavaSubsetParser.DoWhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#returnStmt.
    def visitReturnStmt(self, ctx:JavaSubsetParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#breakStmt.
    def visitBreakStmt(self, ctx:JavaSubsetParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#continueStmt.
    def visitContinueStmt(self, ctx:JavaSubsetParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#throwStmt.
    def visitThrowStmt(self, ctx:JavaSubsetParser.ThrowStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#localVarStmt.
    def visitLocalVarStmt(self, ctx:JavaSubsetParser.LocalVarStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#exprStmt.
    def visitExprStmt(self, ctx:JavaSubsetParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#emptyStmt.
    def visitEmptyStmt(self, ctx:JavaSubsetParser.EmptyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#forControl.
    def visitForControl(self, ctx:JavaSubsetParser.ForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#enhancedForControl.
    def visitEnhancedForControl(self, ctx:JavaSubsetParser.EnhancedForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#forInit.
    def visitForInit(self, ctx:JavaSubsetParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#expressionList.
    def visitExpressionList(self, ctx:JavaSubsetParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#newExpr.
    def visitNewExpr(self, ctx:JavaSubsetParser.NewExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#instanceofExpr.
    def visitInstanceofExpr(self, ctx:JavaSubsetParser.InstanceofExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#castExpr.
    def visitCastExpr(self, ctx:JavaSubsetParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#fieldAccessExpr.
    def visitFieldAccessExpr(self, ctx:JavaSubsetParser.FieldAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#orExpr.
    def visitOrExpr(self, ctx:JavaSubsetParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#bitXorExpr.
    def visitBitXorExpr(self, ctx:JavaSubsetParser.BitXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#shiftExpr.
    def visitShiftExpr(self, ctx:JavaSubsetParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#prefixExpr.
    def visitPrefixExpr(self, ctx:JavaSubsetParser.PrefixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#methodCallExpr.
    def visitMethodCallExpr(self, ctx:JavaSubsetParser.MethodCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#eqExpr.
    def visitEqExpr(self, ctx:JavaSubsetParser.EqExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#bitOrExpr.
    def visitBitOrExpr(self, ctx:JavaSubsetParser.BitOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#arrayAccessExpr.
    def visitArrayAccessExpr(self, ctx:JavaSubsetParser.ArrayAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:JavaSubsetParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#ternaryExpr.
    def visitTernaryExpr(self, ctx:JavaSubsetParser.TernaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#addExpr.
    def visitAddExpr(self, ctx:JavaSubsetParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#mulExpr.
    def visitMulExpr(self, ctx:JavaSubsetParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#postfixExpr.
    def visitPostfixExpr(self, ctx:JavaSubsetParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#callExpr.
    def visitCallExpr(self, ctx:JavaSubsetParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#relExpr.
    def visitRelExpr(self, ctx:JavaSubsetParser.RelExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#bitAndExpr.
    def visitBitAndExpr(self, ctx:JavaSubsetParser.BitAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#assignExpr.
    def visitAssignExpr(self, ctx:JavaSubsetParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#andExpr.
    def visitAndExpr(self, ctx:JavaSubsetParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#parenExpr.
    def visitParenExpr(self, ctx:JavaSubsetParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#thisExpr.
    def visitThisExpr(self, ctx:JavaSubsetParser.ThisExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#superExpr.
    def visitSuperExpr(self, ctx:JavaSubsetParser.SuperExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#literalExpr.
    def visitLiteralExpr(self, ctx:JavaSubsetParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#idExpr.
    def visitIdExpr(self, ctx:JavaSubsetParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#objectCreator.
    def visitObjectCreator(self, ctx:JavaSubsetParser.ObjectCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#arrayCreator.
    def visitArrayCreator(self, ctx:JavaSubsetParser.ArrayCreatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#arrayCreatorInit.
    def visitArrayCreatorInit(self, ctx:JavaSubsetParser.ArrayCreatorInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#arguments.
    def visitArguments(self, ctx:JavaSubsetParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#qualifiedName.
    def visitQualifiedName(self, ctx:JavaSubsetParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JavaSubsetParser#literal.
    def visitLiteral(self, ctx:JavaSubsetParser.LiteralContext):
        return self.visitChildren(ctx)



del JavaSubsetParser