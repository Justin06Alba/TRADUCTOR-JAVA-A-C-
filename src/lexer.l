%{
#include <stdio.h>
#include <string.h>

int yycolumn = 1;

void update_column() {
    yycolumn += yyleng;
}

void emit_token(const char* type, const char* lexeme) {
    printf("%d,%d,%s,%s\n", yylineno, yycolumn, type, lexeme);
}
%}

%option noyywrap

DIGIT           [0-9]
LETTER          [a-zA-Z]
IDENTIFIER_CHAR [a-zA-Z0-9_]
WHITESPACE      [ \t]
NEWLINE         \n

%%

"si"            { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"sino"          { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"mientras"      { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"para"          { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"retornar"      { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"entero"        { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"decimal"       { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"texto"         { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"verdad"        { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"falso"         { emit_token("PALABRA_RESERVADA", yytext); update_column(); }
"nulo"          { emit_token("PALABRA_RESERVADA", yytext); update_column(); }

"=="            { emit_token("OPERADOR_REL", yytext); update_column(); }
"!="            { emit_token("OPERADOR_REL", yytext); update_column(); }
"<="            { emit_token("OPERADOR_REL", yytext); update_column(); }
">="            { emit_token("OPERADOR_REL", yytext); update_column(); }
"<"             { emit_token("OPERADOR_REL", yytext); update_column(); }
">"             { emit_token("OPERADOR_REL", yytext); update_column(); }

"&&"            { emit_token("OPERADOR_LOG", yytext); update_column(); }
"||"            { emit_token("OPERADOR_LOG", yytext); update_column(); }
"!"             { emit_token("OPERADOR_LOG", yytext); update_column(); }

"//".*          { emit_token("COMENTARIO", yytext); update_column(); }

"+"             { emit_token("OPERADOR_ARIT", yytext); update_column(); }
"-"             { emit_token("OPERADOR_ARIT", yytext); update_column(); }
"*"             { emit_token("OPERADOR_ARIT", yytext); update_column(); }
"/"             { emit_token("OPERADOR_ARIT", yytext); update_column(); }
"%"             { emit_token("OPERADOR_ARIT", yytext); update_column(); }

"="             { emit_token("OPERADOR_ASIG", yytext); update_column(); }

"("             { emit_token("DELIMITADOR", yytext); update_column(); }
")"             { emit_token("DELIMITADOR", yytext); update_column(); }
"{"             { emit_token("DELIMITADOR", yytext); update_column(); }
"}"             { emit_token("DELIMITADOR", yytext); update_column(); }
"["             { emit_token("DELIMITADOR", yytext); update_column(); }
"]"             { emit_token("DELIMITADOR", yytext); update_column(); }
";"             { emit_token("DELIMITADOR", yytext); update_column(); }
","             { emit_token("DELIMITADOR", yytext); update_column(); }

\"([^\"\n]|\\.)*\"  { emit_token("CADENA", yytext); update_column(); }

{DIGIT}+"."{DIGIT}+     { emit_token("DECIMAL", yytext); update_column(); }
{DIGIT}+                { emit_token("ENTERO", yytext); update_column(); }

({LETTER}|_){IDENTIFIER_CHAR}*  { emit_token("IDENTIFICADOR", yytext); update_column(); }

{WHITESPACE}+   { update_column(); }

{NEWLINE}       { yylineno++; yycolumn = 1; }

.               { emit_token("ERROR_LEXICO", yytext); update_column(); }

%%

int main(int argc, char** argv) {
    if (argc > 1) {
        FILE* file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Error: No se puede abrir el archivo %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    }
    yylex();
    if (argc > 1) {
        fclose(yyin);
    }
    return 0;
}
