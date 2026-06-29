"""Punto de entrada para el ejecutable del traductor Java -> C#."""
import os
import sys

if getattr(sys, "frozen", False):
    base_dir = sys._MEIPASS  # type: ignore[attr-defined]
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# La carpeta del parser generado debe estar en sys.path para que los modulos
# JavaSubset* (que se importan por su nombre simple) se resuelvan.
generated = os.path.join(base_dir, "traductor", "generated")
for ruta in (generated, base_dir):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from traductor.gui_traductor import main

if __name__ == "__main__":
    main()
