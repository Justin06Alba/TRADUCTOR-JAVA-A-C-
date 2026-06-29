"""Punto de entrada para el ejecutable empaquetado con PyInstaller."""
import sys
import os

# Cuando PyInstaller empaqueta la app, los recursos quedan en sys._MEIPASS.
# Agregamos esa ruta al sys.path para que los imports de 'src' funcionen.
if getattr(sys, "frozen", False):
    base_dir = sys._MEIPASS  # type: ignore[attr-defined]
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.main_gui import main

if __name__ == "__main__":
    main()
