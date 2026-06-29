import os
import subprocess
import shutil
import glob


# Rutas adicionales donde buscar flex/gcc en Windows
_WINDOWS_EXTRA_PATHS = [
    # MSYS2 ucrt64 (instalado con winget o manualmente)
    r"C:\msys64\ucrt64\bin",
    r"C:\msys64\mingw64\bin",
    r"C:\msys64\usr\bin",
    # MinGW-w64 instalaciones comunes
    r"C:\mingw64\bin",
    r"C:\mingw32\bin",
    r"C:\TDM-GCC-64\bin",
]

# Nombres alternativos de flex en Windows (win_flex_bison instala win_flex.exe)
_FLEX_ALIASES = ["flex", "win_flex", "win_flex.exe", "flex.exe"]
_GCC_ALIASES  = ["gcc", "gcc.exe"]


def _find_tool(aliases: list[str], extra_paths: list[str] | None = None) -> str | None:
    """Busca una herramienta por nombre en PATH y rutas adicionales.
    
    Retorna la ruta completa al ejecutable o None si no se encuentra.
    """
    # 1. Buscar en PATH estándar con todos los alias
    for alias in aliases:
        found = shutil.which(alias)
        if found:
            return found

    # 2. Buscar en rutas adicionales explícitas
    if extra_paths:
        for directory in extra_paths:
            for alias in aliases:
                candidate = os.path.join(directory, alias)
                if os.path.isfile(candidate):
                    return candidate

    # 3. En Windows, buscar win_flex en la carpeta de WinGet
    if os.name == "nt":
        winget_base = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Microsoft", "WinGet", "Packages"
        )
        if os.path.isdir(winget_base):
            for alias in aliases:
                pattern = os.path.join(winget_base, "WinFlexBison*", alias)
                matches = glob.glob(pattern)
                if matches:
                    return matches[0]

    return None


class LexerCompiler:
    """Compila lexer.l a un ejecutable usando flex (o win_flex) y gcc."""

    def __init__(self, lexer_file: str = "src/lexer.l", build_dir: str = "build"):
        self.lexer_file = lexer_file
        self.build_dir = build_dir
        self.executable_name = "lexer"
        self.is_windows = os.name == "nt"
        self.c_output_file = os.path.join(self.build_dir, "lex.yy.c")
        self.executable_path = os.path.join(
            self.build_dir,
            f"{self.executable_name}.exe" if self.is_windows else self.executable_name,
        )

    def _find_flex(self) -> str | None:
        return _find_tool(_FLEX_ALIASES, _WINDOWS_EXTRA_PATHS if self.is_windows else None)

    def _find_gcc(self) -> str | None:
        return _find_tool(_GCC_ALIASES, _WINDOWS_EXTRA_PATHS if self.is_windows else None)

    def check_dependencies(self) -> tuple[bool, list[str]]:
        missing = []
        if not self._find_flex():
            missing.append("flex / win_flex")
        if not self._find_gcc():
            missing.append("gcc")
        return (len(missing) == 0, missing)

    def compile(self) -> tuple[bool, str]:
        flex_exe = self._find_flex()
        gcc_exe  = self._find_gcc()

        missing = []
        if not flex_exe:
            missing.append("flex / win_flex")
        if not gcc_exe:
            missing.append("gcc")
        if missing:
            return (False, f"Dependencias faltantes: {', '.join(missing)}")

        if not os.path.exists(self.lexer_file):
            return (False, f"Archivo no encontrado: {self.lexer_file}")

        try:
            os.makedirs(self.build_dir, exist_ok=True)
        except OSError as e:
            return (False, f"Error al crear directorio build: {e}")

        # Generar lex.yy.c con flex / win_flex
        try:
            flex_result = subprocess.run(
                [flex_exe, "-o", self.c_output_file, self.lexer_file],
                capture_output=True, text=True, check=False,
            )
            if flex_result.returncode != 0:
                error_msg = flex_result.stderr or "Error desconocido de flex"
                return (False, f"Error en flex: {error_msg}")
            if not os.path.exists(self.c_output_file):
                return (False, f"flex no generó el archivo {self.c_output_file}")
        except FileNotFoundError:
            return (False, f"No se pudo ejecutar flex: {flex_exe}")
        except Exception as e:
            return (False, f"Error inesperado al ejecutar flex: {e}")

        # Compilar lex.yy.c con gcc
        # MSYS2/MinGW gcc necesita su propia carpeta en PATH para encontrar DLLs internas
        env_compilacion = os.environ.copy()
        directorio_gcc = os.path.dirname(gcc_exe)
        rutas_actuales = env_compilacion.get("PATH", "")
        if directorio_gcc not in rutas_actuales:
            env_compilacion["PATH"] = directorio_gcc + os.pathsep + rutas_actuales

        try:
            gcc_result = subprocess.run(
                [gcc_exe, self.c_output_file, "-o", self.executable_path],
                capture_output=True, text=True, check=False,
                env=env_compilacion,
            )
            if gcc_result.returncode != 0:
                error_msg = gcc_result.stderr or "Error desconocido de gcc"
                return (False, f"Error en gcc: {error_msg}")
            if not os.path.exists(self.executable_path):
                return (False, f"gcc no generó el ejecutable {self.executable_path}")
        except FileNotFoundError:
            return (False, f"No se pudo ejecutar gcc: {gcc_exe}")
        except Exception as e:
            return (False, f"Error inesperado al ejecutar gcc: {e}")

        return (True, f"Compilación exitosa: {self.executable_path}")
