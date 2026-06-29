#!/usr/bin/env bash
# Regenera el lexer/parser/visitor de Python desde la gramatica ANTLR.
# Requiere Java y tools/antlr-4.13.1-complete.jar (ver README).
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
java -jar "$DIR/tools/antlr-4.13.1-complete.jar" \
    -Dlanguage=Python3 -visitor \
    -o "$DIR/traductor/generated" \
    "$DIR/traductor/grammar/JavaSubset.g4"
echo "Parser regenerado en traductor/generated/"
