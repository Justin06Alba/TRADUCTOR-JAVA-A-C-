"""Pruebas del traductor Java -> C#.

Ejercen el pipeline completo (lexico -> sintactico -> AST -> semantico ->
generacion) a traves de traducir_texto().
"""

from __future__ import annotations

import pytest

from traductor.main import traducir_texto


def _traducir_ok(fuente: str) -> str:
    resultado = traducir_texto(fuente)
    assert resultado.exitoso, f"errores: {[str(e) for e in resultado.errores]}"
    return resultado.codigo


# --------------------------------------------------------------- tipos

def test_clase_basica_y_constructor():
    cs = _traducir_ok("""
        public class Hola {
            private String nombre;
            public Hola(String nombre) { this.nombre = nombre; }
        }
    """)
    assert "public class Hola" in cs
    assert "private string nombre;" in cs
    assert "public Hola(string nombre)" in cs
    assert "this.nombre = nombre;" in cs


def test_mapeo_de_tipos_primitivos():
    cs = _traducir_ok("""
        public class N {
            private boolean b;
            private int x;
            private double y;
            public void f(boolean activo) {}
        }
    """)
    assert "private bool b;" in cs
    assert "private int x;" in cs
    assert "private double y;" in cs
    assert "public void f(bool activo)" in cs


def test_system_out_println():
    cs = _traducir_ok("""
        public class P { public void f() { System.out.println("hola"); } }
    """)
    assert 'Console.WriteLine("hola")' in cs


def test_concatenacion_de_cadenas():
    cs = _traducir_ok("""
        public class P { public void f(String n) { System.out.println("Hola, " + n); } }
    """)
    assert 'Console.WriteLine("Hola, " + n)' in cs


# --------------------------------------------------------------- colecciones

def test_lista_generica_y_add():
    cs = _traducir_ok("""
        import java.util.*;
        public class C {
            private List<String> items;
            public void agregar(String x) { items.add(x); }
        }
    """)
    assert "List<string> items;" in cs
    assert "items.Add(x);" in cs


def test_foreach():
    cs = _traducir_ok("""
        import java.util.*;
        public class C {
            private List<String> items;
            public void f() { for (String s : items) { System.out.println(s); } }
        }
    """)
    assert "foreach (string s in items)" in cs


def test_map_se_traduce_a_dictionary_y_put_a_indexador():
    cs = _traducir_ok("""
        import java.util.*;
        public class C {
            private Map<String, Integer> m;
            public void f(String k) { m.put(k, 1); }
        }
    """)
    assert "Dictionary<string, int> m;" in cs
    assert "m[k] = 1;" in cs


def test_get_y_size():
    cs = _traducir_ok("""
        import java.util.*;
        public class C {
            public void f(List<String> xs) {
                for (int i = 0; i < xs.size(); i++) { String s = xs.get(i); }
            }
        }
    """)
    assert "xs.Count" in cs
    assert "xs[i]" in cs


# --------------------------------------------------------------- sentencias

def test_for_clasico():
    cs = _traducir_ok("""
        public class C { public void f() { for (int i = 0; i < 10; i++) { } } }
    """)
    assert "for (int i = 0; i < 10; i++)" in cs


def test_if_else_if():
    cs = _traducir_ok("""
        public class C {
            public String f(String s) {
                if (s.length() > 5) { return s.toUpperCase(); }
                else if (s.length() > 2) { return s; }
                return s;
            }
        }
    """)
    assert "if (s.Length > 5)" in cs
    assert "else if (s.Length > 2)" in cs
    assert "s.ToUpper()" in cs


def test_ternario():
    cs = _traducir_ok("""
        public class C { public int f(int x) { return x > 0 ? x : -1; } }
    """)
    assert "return x > 0 ? x : -1;" in cs


def test_paquete_se_traduce_a_namespace():
    cs = _traducir_ok("""
        package com.ejemplo.demo;
        public class C {}
    """)
    assert "namespace Com.Ejemplo.Demo" in cs


def test_herencia_e_interfaces():
    cs = _traducir_ok("""
        public class C extends Base implements Comparable {}
    """)
    assert "class C : Base, Comparable" in cs


# --------------------------------------------------------------- errores

def test_error_sintactico_no_genera_codigo():
    resultado = traducir_texto("public class C { public void f( { } }")
    assert not resultado.exitoso
    assert resultado.codigo is None
    assert any(e.fase in ("SINTACTICO", "LEXICO") for e in resultado.errores)


def test_variable_no_declarada():
    resultado = traducir_texto("""
        public class C { public void f() { y = 3; } }
    """)
    assert not resultado.exitoso
    assert any("no ha sido declarado" in e.mensaje for e in resultado.errores)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
