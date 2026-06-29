# Generated from traductor/grammar/JavaSubset.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .JavaSubsetParser import JavaSubsetParser
else:
    from JavaSubsetParser import JavaSubsetParser

# This class defines a complete listener for a parse tree produced by JavaSubsetParser.
class JavaSubsetListener(ParseTreeListener):

    # Enter a parse tree produced by JavaSubsetParser#compilationUnit.
    def enterCompilationUnit(self, ctx:JavaSubsetParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#compilationUnit.
    def exitCompilationUnit(self, ctx:JavaSubsetParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:JavaSubsetParser.PackageDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#packageDeclaration.
    def exitPackageDeclaration(self, ctx:JavaSubsetParser.PackageDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaSubsetParser.ImportDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#importDeclaration.
    def exitImportDeclaration(self, ctx:JavaSubsetParser.ImportDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#typeDeclaration.
    def enterTypeDeclaration(self, ctx:JavaSubsetParser.TypeDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#typeDeclaration.
    def exitTypeDeclaration(self, ctx:JavaSubsetParser.TypeDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaSubsetParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#classDeclaration.
    def exitClassDeclaration(self, ctx:JavaSubsetParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#interfaceDeclaration.
    def enterInterfaceDeclaration(self, ctx:JavaSubsetParser.InterfaceDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#interfaceDeclaration.
    def exitInterfaceDeclaration(self, ctx:JavaSubsetParser.InterfaceDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#classBody.
    def enterClassBody(self, ctx:JavaSubsetParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#classBody.
    def exitClassBody(self, ctx:JavaSubsetParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#classBodyDeclaration.
    def enterClassBodyDeclaration(self, ctx:JavaSubsetParser.ClassBodyDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#classBodyDeclaration.
    def exitClassBodyDeclaration(self, ctx:JavaSubsetParser.ClassBodyDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#memberDeclaration.
    def enterMemberDeclaration(self, ctx:JavaSubsetParser.MemberDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#memberDeclaration.
    def exitMemberDeclaration(self, ctx:JavaSubsetParser.MemberDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:JavaSubsetParser.FieldDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#fieldDeclaration.
    def exitFieldDeclaration(self, ctx:JavaSubsetParser.FieldDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:JavaSubsetParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:JavaSubsetParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:JavaSubsetParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:JavaSubsetParser.ConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#variableDeclarators.
    def enterVariableDeclarators(self, ctx:JavaSubsetParser.VariableDeclaratorsContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#variableDeclarators.
    def exitVariableDeclarators(self, ctx:JavaSubsetParser.VariableDeclaratorsContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#variableDeclarator.
    def enterVariableDeclarator(self, ctx:JavaSubsetParser.VariableDeclaratorContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#variableDeclarator.
    def exitVariableDeclarator(self, ctx:JavaSubsetParser.VariableDeclaratorContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#variableInitializer.
    def enterVariableInitializer(self, ctx:JavaSubsetParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#variableInitializer.
    def exitVariableInitializer(self, ctx:JavaSubsetParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:JavaSubsetParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:JavaSubsetParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#formalParameters.
    def enterFormalParameters(self, ctx:JavaSubsetParser.FormalParametersContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#formalParameters.
    def exitFormalParameters(self, ctx:JavaSubsetParser.FormalParametersContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#formalParameterList.
    def enterFormalParameterList(self, ctx:JavaSubsetParser.FormalParameterListContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#formalParameterList.
    def exitFormalParameterList(self, ctx:JavaSubsetParser.FormalParameterListContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#formalParameter.
    def enterFormalParameter(self, ctx:JavaSubsetParser.FormalParameterContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#formalParameter.
    def exitFormalParameter(self, ctx:JavaSubsetParser.FormalParameterContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#modifier.
    def enterModifier(self, ctx:JavaSubsetParser.ModifierContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#modifier.
    def exitModifier(self, ctx:JavaSubsetParser.ModifierContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#typeType.
    def enterTypeType(self, ctx:JavaSubsetParser.TypeTypeContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#typeType.
    def exitTypeType(self, ctx:JavaSubsetParser.TypeTypeContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#classOrInterfaceType.
    def enterClassOrInterfaceType(self, ctx:JavaSubsetParser.ClassOrInterfaceTypeContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#classOrInterfaceType.
    def exitClassOrInterfaceType(self, ctx:JavaSubsetParser.ClassOrInterfaceTypeContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#typeArguments.
    def enterTypeArguments(self, ctx:JavaSubsetParser.TypeArgumentsContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#typeArguments.
    def exitTypeArguments(self, ctx:JavaSubsetParser.TypeArgumentsContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#primitiveType.
    def enterPrimitiveType(self, ctx:JavaSubsetParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#primitiveType.
    def exitPrimitiveType(self, ctx:JavaSubsetParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#typeList.
    def enterTypeList(self, ctx:JavaSubsetParser.TypeListContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#typeList.
    def exitTypeList(self, ctx:JavaSubsetParser.TypeListContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#block.
    def enterBlock(self, ctx:JavaSubsetParser.BlockContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#block.
    def exitBlock(self, ctx:JavaSubsetParser.BlockContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#blockStatement.
    def enterBlockStatement(self, ctx:JavaSubsetParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#blockStatement.
    def exitBlockStatement(self, ctx:JavaSubsetParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#localVariableDeclaration.
    def enterLocalVariableDeclaration(self, ctx:JavaSubsetParser.LocalVariableDeclarationContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#localVariableDeclaration.
    def exitLocalVariableDeclaration(self, ctx:JavaSubsetParser.LocalVariableDeclarationContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#blockStmt.
    def enterBlockStmt(self, ctx:JavaSubsetParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#blockStmt.
    def exitBlockStmt(self, ctx:JavaSubsetParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#ifStmt.
    def enterIfStmt(self, ctx:JavaSubsetParser.IfStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#ifStmt.
    def exitIfStmt(self, ctx:JavaSubsetParser.IfStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#forStmt.
    def enterForStmt(self, ctx:JavaSubsetParser.ForStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#forStmt.
    def exitForStmt(self, ctx:JavaSubsetParser.ForStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#whileStmt.
    def enterWhileStmt(self, ctx:JavaSubsetParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#whileStmt.
    def exitWhileStmt(self, ctx:JavaSubsetParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#doWhileStmt.
    def enterDoWhileStmt(self, ctx:JavaSubsetParser.DoWhileStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#doWhileStmt.
    def exitDoWhileStmt(self, ctx:JavaSubsetParser.DoWhileStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#returnStmt.
    def enterReturnStmt(self, ctx:JavaSubsetParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#returnStmt.
    def exitReturnStmt(self, ctx:JavaSubsetParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#breakStmt.
    def enterBreakStmt(self, ctx:JavaSubsetParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#breakStmt.
    def exitBreakStmt(self, ctx:JavaSubsetParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#continueStmt.
    def enterContinueStmt(self, ctx:JavaSubsetParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#continueStmt.
    def exitContinueStmt(self, ctx:JavaSubsetParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#throwStmt.
    def enterThrowStmt(self, ctx:JavaSubsetParser.ThrowStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#throwStmt.
    def exitThrowStmt(self, ctx:JavaSubsetParser.ThrowStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#localVarStmt.
    def enterLocalVarStmt(self, ctx:JavaSubsetParser.LocalVarStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#localVarStmt.
    def exitLocalVarStmt(self, ctx:JavaSubsetParser.LocalVarStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#exprStmt.
    def enterExprStmt(self, ctx:JavaSubsetParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#exprStmt.
    def exitExprStmt(self, ctx:JavaSubsetParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#emptyStmt.
    def enterEmptyStmt(self, ctx:JavaSubsetParser.EmptyStmtContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#emptyStmt.
    def exitEmptyStmt(self, ctx:JavaSubsetParser.EmptyStmtContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#forControl.
    def enterForControl(self, ctx:JavaSubsetParser.ForControlContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#forControl.
    def exitForControl(self, ctx:JavaSubsetParser.ForControlContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#enhancedForControl.
    def enterEnhancedForControl(self, ctx:JavaSubsetParser.EnhancedForControlContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#enhancedForControl.
    def exitEnhancedForControl(self, ctx:JavaSubsetParser.EnhancedForControlContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#forInit.
    def enterForInit(self, ctx:JavaSubsetParser.ForInitContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#forInit.
    def exitForInit(self, ctx:JavaSubsetParser.ForInitContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#expressionList.
    def enterExpressionList(self, ctx:JavaSubsetParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#expressionList.
    def exitExpressionList(self, ctx:JavaSubsetParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#newExpr.
    def enterNewExpr(self, ctx:JavaSubsetParser.NewExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#newExpr.
    def exitNewExpr(self, ctx:JavaSubsetParser.NewExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#instanceofExpr.
    def enterInstanceofExpr(self, ctx:JavaSubsetParser.InstanceofExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#instanceofExpr.
    def exitInstanceofExpr(self, ctx:JavaSubsetParser.InstanceofExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#castExpr.
    def enterCastExpr(self, ctx:JavaSubsetParser.CastExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#castExpr.
    def exitCastExpr(self, ctx:JavaSubsetParser.CastExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#fieldAccessExpr.
    def enterFieldAccessExpr(self, ctx:JavaSubsetParser.FieldAccessExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#fieldAccessExpr.
    def exitFieldAccessExpr(self, ctx:JavaSubsetParser.FieldAccessExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#orExpr.
    def enterOrExpr(self, ctx:JavaSubsetParser.OrExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#orExpr.
    def exitOrExpr(self, ctx:JavaSubsetParser.OrExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#bitXorExpr.
    def enterBitXorExpr(self, ctx:JavaSubsetParser.BitXorExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#bitXorExpr.
    def exitBitXorExpr(self, ctx:JavaSubsetParser.BitXorExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#shiftExpr.
    def enterShiftExpr(self, ctx:JavaSubsetParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#shiftExpr.
    def exitShiftExpr(self, ctx:JavaSubsetParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#prefixExpr.
    def enterPrefixExpr(self, ctx:JavaSubsetParser.PrefixExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#prefixExpr.
    def exitPrefixExpr(self, ctx:JavaSubsetParser.PrefixExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#methodCallExpr.
    def enterMethodCallExpr(self, ctx:JavaSubsetParser.MethodCallExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#methodCallExpr.
    def exitMethodCallExpr(self, ctx:JavaSubsetParser.MethodCallExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#eqExpr.
    def enterEqExpr(self, ctx:JavaSubsetParser.EqExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#eqExpr.
    def exitEqExpr(self, ctx:JavaSubsetParser.EqExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#bitOrExpr.
    def enterBitOrExpr(self, ctx:JavaSubsetParser.BitOrExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#bitOrExpr.
    def exitBitOrExpr(self, ctx:JavaSubsetParser.BitOrExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#arrayAccessExpr.
    def enterArrayAccessExpr(self, ctx:JavaSubsetParser.ArrayAccessExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#arrayAccessExpr.
    def exitArrayAccessExpr(self, ctx:JavaSubsetParser.ArrayAccessExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:JavaSubsetParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:JavaSubsetParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#ternaryExpr.
    def enterTernaryExpr(self, ctx:JavaSubsetParser.TernaryExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#ternaryExpr.
    def exitTernaryExpr(self, ctx:JavaSubsetParser.TernaryExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#addExpr.
    def enterAddExpr(self, ctx:JavaSubsetParser.AddExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#addExpr.
    def exitAddExpr(self, ctx:JavaSubsetParser.AddExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#mulExpr.
    def enterMulExpr(self, ctx:JavaSubsetParser.MulExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#mulExpr.
    def exitMulExpr(self, ctx:JavaSubsetParser.MulExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#postfixExpr.
    def enterPostfixExpr(self, ctx:JavaSubsetParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#postfixExpr.
    def exitPostfixExpr(self, ctx:JavaSubsetParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#callExpr.
    def enterCallExpr(self, ctx:JavaSubsetParser.CallExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#callExpr.
    def exitCallExpr(self, ctx:JavaSubsetParser.CallExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#relExpr.
    def enterRelExpr(self, ctx:JavaSubsetParser.RelExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#relExpr.
    def exitRelExpr(self, ctx:JavaSubsetParser.RelExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#bitAndExpr.
    def enterBitAndExpr(self, ctx:JavaSubsetParser.BitAndExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#bitAndExpr.
    def exitBitAndExpr(self, ctx:JavaSubsetParser.BitAndExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#assignExpr.
    def enterAssignExpr(self, ctx:JavaSubsetParser.AssignExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#assignExpr.
    def exitAssignExpr(self, ctx:JavaSubsetParser.AssignExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#andExpr.
    def enterAndExpr(self, ctx:JavaSubsetParser.AndExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#andExpr.
    def exitAndExpr(self, ctx:JavaSubsetParser.AndExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#parenExpr.
    def enterParenExpr(self, ctx:JavaSubsetParser.ParenExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#parenExpr.
    def exitParenExpr(self, ctx:JavaSubsetParser.ParenExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#thisExpr.
    def enterThisExpr(self, ctx:JavaSubsetParser.ThisExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#thisExpr.
    def exitThisExpr(self, ctx:JavaSubsetParser.ThisExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#superExpr.
    def enterSuperExpr(self, ctx:JavaSubsetParser.SuperExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#superExpr.
    def exitSuperExpr(self, ctx:JavaSubsetParser.SuperExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#literalExpr.
    def enterLiteralExpr(self, ctx:JavaSubsetParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#literalExpr.
    def exitLiteralExpr(self, ctx:JavaSubsetParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#idExpr.
    def enterIdExpr(self, ctx:JavaSubsetParser.IdExprContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#idExpr.
    def exitIdExpr(self, ctx:JavaSubsetParser.IdExprContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#objectCreator.
    def enterObjectCreator(self, ctx:JavaSubsetParser.ObjectCreatorContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#objectCreator.
    def exitObjectCreator(self, ctx:JavaSubsetParser.ObjectCreatorContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#arrayCreator.
    def enterArrayCreator(self, ctx:JavaSubsetParser.ArrayCreatorContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#arrayCreator.
    def exitArrayCreator(self, ctx:JavaSubsetParser.ArrayCreatorContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#arrayCreatorInit.
    def enterArrayCreatorInit(self, ctx:JavaSubsetParser.ArrayCreatorInitContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#arrayCreatorInit.
    def exitArrayCreatorInit(self, ctx:JavaSubsetParser.ArrayCreatorInitContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#arguments.
    def enterArguments(self, ctx:JavaSubsetParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#arguments.
    def exitArguments(self, ctx:JavaSubsetParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#qualifiedName.
    def enterQualifiedName(self, ctx:JavaSubsetParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#qualifiedName.
    def exitQualifiedName(self, ctx:JavaSubsetParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by JavaSubsetParser#literal.
    def enterLiteral(self, ctx:JavaSubsetParser.LiteralContext):
        pass

    # Exit a parse tree produced by JavaSubsetParser#literal.
    def exitLiteral(self, ctx:JavaSubsetParser.LiteralContext):
        pass



del JavaSubsetParser