grammar JavaSubset;

// ============================================================================
// Gramatica de un SUBCONJUNTO de Java orientado a objetos (nucleo).
// Cubre: paquetes/imports, clases con herencia/interfaces, campos, metodos,
// constructores, sentencias comunes (if/for/foreach/while/return) y una
// jerarquia completa de expresiones con precedencia.
//
// ANTLR resuelve la recursion por la izquierda de 'expression', por eso las
// alternativas se escriben en orden de mayor a menor precedencia.
// ============================================================================

// ---------------------------------------------------------------- PARSER

compilationUnit
    : packageDeclaration? importDeclaration* typeDeclaration* EOF
    ;

packageDeclaration
    : 'package' qualifiedName ';'
    ;

importDeclaration
    : 'import' 'static'? qualifiedName ('.' '*')? ';'
    ;

typeDeclaration
    : classDeclaration
    | interfaceDeclaration
    | ';'
    ;

// ----- Clases -----

classDeclaration
    : modifier* 'class' IDENTIFIER
        ('extends' typeType)?
        ('implements' typeList)?
        classBody
    ;

interfaceDeclaration
    : modifier* 'interface' IDENTIFIER
        ('extends' typeList)?
        classBody
    ;

classBody
    : '{' classBodyDeclaration* '}'
    ;

classBodyDeclaration
    : ';'
    | memberDeclaration
    ;

memberDeclaration
    : methodDeclaration
    | constructorDeclaration
    | fieldDeclaration
    ;

// ----- Miembros -----

fieldDeclaration
    : modifier* typeType variableDeclarators ';'
    ;

methodDeclaration
    : modifier* (typeType | 'void') IDENTIFIER formalParameters
        (block | ';')
    ;

constructorDeclaration
    : modifier* IDENTIFIER formalParameters block
    ;

variableDeclarators
    : variableDeclarator (',' variableDeclarator)*
    ;

variableDeclarator
    : IDENTIFIER ('=' variableInitializer)?
    ;

variableInitializer
    : arrayInitializer
    | expression
    ;

arrayInitializer
    : '{' (variableInitializer (',' variableInitializer)* ','?)? '}'
    ;

formalParameters
    : '(' (formalParameterList)? ')'
    ;

formalParameterList
    : formalParameter (',' formalParameter)*
    ;

formalParameter
    : modifier* typeType IDENTIFIER
    ;

modifier
    : 'public' | 'private' | 'protected'
    | 'static' | 'final' | 'abstract'
    ;

// ----- Tipos -----

typeType
    : (classOrInterfaceType | primitiveType) ('[' ']')*
    ;

classOrInterfaceType
    : IDENTIFIER typeArguments? ('.' IDENTIFIER typeArguments?)*
    ;

typeArguments
    : '<' typeType (',' typeType)* '>'
    ;

primitiveType
    : 'boolean' | 'char' | 'byte' | 'short'
    | 'int' | 'long' | 'float' | 'double'
    ;

typeList
    : typeType (',' typeType)*
    ;

// ----- Sentencias -----

block
    : '{' blockStatement* '}'
    ;

blockStatement
    : localVariableDeclaration ';'
    | statement
    ;

localVariableDeclaration
    : typeType variableDeclarators
    ;

statement
    : block                                                      # blockStmt
    | 'if' '(' expression ')' statement ('else' statement)?      # ifStmt
    | 'for' '(' forControl ')' statement                         # forStmt
    | 'while' '(' expression ')' statement                       # whileStmt
    | 'do' statement 'while' '(' expression ')' ';'              # doWhileStmt
    | 'return' expression? ';'                                   # returnStmt
    | 'break' ';'                                                # breakStmt
    | 'continue' ';'                                             # continueStmt
    | 'throw' expression ';'                                     # throwStmt
    | localVariableDeclaration ';'                               # localVarStmt
    | expression ';'                                             # exprStmt
    | ';'                                                        # emptyStmt
    ;

forControl
    : enhancedForControl
    | forInit? ';' expression? ';' forUpdate=expressionList?
    ;

enhancedForControl
    : typeType IDENTIFIER ':' expression
    ;

forInit
    : localVariableDeclaration
    | expressionList
    ;

expressionList
    : expression (',' expression)*
    ;

// ----- Expresiones (orden = precedencia, mayor primero) -----

expression
    : primary                                                   # primaryExpr
    | expression '.' IDENTIFIER                                 # fieldAccessExpr
    | expression '.' IDENTIFIER arguments                       # methodCallExpr
    | expression '[' expression ']'                            # arrayAccessExpr
    | IDENTIFIER arguments                                      # callExpr
    | 'new' creator                                            # newExpr
    | '(' typeType ')' expression                             # castExpr
    | expression op=('++' | '--')                             # postfixExpr
    | op=('+' | '-' | '++' | '--' | '!' | '~') expression     # prefixExpr
    | expression op=('*' | '/' | '%') expression             # mulExpr
    | expression op=('+' | '-') expression                   # addExpr
    | expression op=('<<' | '>>' | '>>>') expression         # shiftExpr
    | expression op=('<=' | '>=' | '<' | '>') expression     # relExpr
    | expression 'instanceof' typeType                       # instanceofExpr
    | expression op=('==' | '!=') expression                 # eqExpr
    | expression '&' expression                              # bitAndExpr
    | expression '^' expression                              # bitXorExpr
    | expression '|' expression                              # bitOrExpr
    | expression '&&' expression                             # andExpr
    | expression '||' expression                             # orExpr
    | expression '?' expression ':' expression               # ternaryExpr
    | <assoc=right> expression
        op=('=' | '+=' | '-=' | '*=' | '/=' | '%=') expression # assignExpr
    ;

primary
    : '(' expression ')'                                        # parenExpr
    | 'this'                                                     # thisExpr
    | 'super'                                                    # superExpr
    | literal                                                    # literalExpr
    | IDENTIFIER                                                 # idExpr
    ;

creator
    : classOrInterfaceType arguments                            # objectCreator
    | (classOrInterfaceType | primitiveType) ('[' expression ']')+ ('[' ']')*  # arrayCreator
    | (classOrInterfaceType | primitiveType) ('[' ']')+ arrayInitializer       # arrayCreatorInit
    ;

arguments
    : '(' expressionList? ')'
    ;

qualifiedName
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

literal
    : DECIMAL_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | 'true'
    | 'false'
    | 'null'
    ;

// ---------------------------------------------------------------- LEXER

// Palabras reservadas se reconocen por sus literales en el parser.

DECIMAL_LITERAL : ('0' | [1-9] [0-9]*) [lL]? ;
FLOAT_LITERAL   : [0-9]+ '.' [0-9]* [fFdD]? | '.' [0-9]+ [fFdD]? | [0-9]+ [fFdD] ;
CHAR_LITERAL    : '\'' (~['\\\r\n] | EscapeSequence) '\'' ;
STRING_LITERAL  : '"' (~["\\\r\n] | EscapeSequence)* '"' ;

fragment EscapeSequence
    : '\\' [btnfr"'\\]
    | '\\' ([0-3]? [0-7])? [0-7]
    | '\\' 'u'+ [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F]
    ;

IDENTIFIER : [a-zA-Z_$] [a-zA-Z0-9_$]* ;

WS           : [ \t\r\n]+ -> skip ;
COMMENT      : '/*' .*? '*/' -> channel(HIDDEN) ;
LINE_COMMENT : '//' ~[\r\n]* -> channel(HIDDEN) ;
