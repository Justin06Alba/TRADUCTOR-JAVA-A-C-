"""Mapeos Java -> C#: tipos, metodos de la biblioteca estandar y modificadores.

Tablas de conversion declarativas usadas por el generador de C#.
"""

from __future__ import annotations

from typing import Optional

from traductor.java_ast import Tipo


class MapeoTipos:
    """Traduce tipos Java a su equivalente en C#."""

    TIPOS = {
        # primitivos
        "boolean": "bool",
        "char": "char",
        "byte": "byte",
        "short": "short",
        "int": "int",
        "long": "long",
        "float": "float",
        "double": "double",
        # referencia comunes
        "String": "string",
        "Object": "object",
        "Integer": "int",
        "Long": "long",
        "Double": "double",
        "Float": "float",
        "Boolean": "bool",
        "Character": "char",
        # colecciones
        "List": "List",
        "ArrayList": "List",
        "LinkedList": "List",
        "Map": "Dictionary",
        "HashMap": "Dictionary",
        "TreeMap": "SortedDictionary",
        "Set": "HashSet",
        "HashSet": "HashSet",
        "TreeSet": "SortedSet",
        "Collection": "ICollection",
        "Iterable": "IEnumerable",
        # excepciones
        "Exception": "Exception",
        "RuntimeException": "Exception",
        "IllegalArgumentException": "ArgumentException",
        "IllegalStateException": "InvalidOperationException",
        "NullPointerException": "NullReferenceException",
        "IndexOutOfBoundsException": "IndexOutOfRangeException",
        "UnsupportedOperationException": "NotSupportedException",
    }

    def mapear(self, tipo: Optional[Tipo]) -> str:
        if tipo is None:
            return "void"
        nombre = self.TIPOS.get(tipo.nombre, tipo.nombre)
        if tipo.genericos:
            gens = ", ".join(self.mapear(g) for g in tipo.genericos)
            nombre = f"{nombre}<{gens}>"
        nombre += "[]" * tipo.dims
        return nombre


class MapeoMetodos:
    """Traduce metodos/propiedades de la biblioteca estandar de Java a C#."""

    # Metodo Java -> Metodo C# (misma forma: llamada con parentesis)
    METODOS = {
        "equals": "Equals",
        "toString": "ToString",
        "hashCode": "GetHashCode",
        "compareTo": "CompareTo",
        # String
        "substring": "Substring",
        "indexOf": "IndexOf",
        "lastIndexOf": "LastIndexOf",
        "toLowerCase": "ToLower",
        "toUpperCase": "ToUpper",
        "contains": "Contains",
        "startsWith": "StartsWith",
        "endsWith": "EndsWith",
        "replace": "Replace",
        "split": "Split",
        "trim": "Trim",
        "charAt": "__indexer__",     # s.charAt(i) -> s[i]
        "valueOf": "ToString",
        # colecciones
        "add": "Add",
        "remove": "Remove",
        "get": "__indexer__",        # list.get(i) -> list[i]
        "set": "__set_indexer__",    # list.set(i, v) -> list[i] = v
        "put": "__put__",            # map.put(k, v) -> map[k] = v
        "containsKey": "ContainsKey",
        "containsValue": "ContainsValue",
        "keySet": "Keys",            # propiedad
        "values": "Values",          # propiedad
        "clear": "Clear",
        "addAll": "AddRange",
    }

    # Metodos Java que en C# son propiedades (sin parentesis)
    PROPIEDADES = {"length", "size", "isEmpty"}

    # Mapeo concreto de propiedades
    PROP_MAP = {
        "length": "Length",
        "size": "Count",
        "isEmpty": "__is_empty__",   # x.isEmpty() -> x.Count == 0 / x.Length == 0
    }

    def es_propiedad(self, nombre: str) -> bool:
        return nombre in self.PROPIEDADES

    def mapear_metodo(self, nombre: str) -> str:
        return self.METODOS.get(nombre, nombre)

    def mapear_propiedad(self, nombre: str) -> str:
        return self.PROP_MAP.get(nombre, nombre)


# Modificadores Java -> C#
MODIFICADORES = {
    "public": "public",
    "private": "private",
    "protected": "protected",
    "static": "static",
    "final": "readonly",     # en campos; en clases se traduce a 'sealed'
    "abstract": "abstract",
}
