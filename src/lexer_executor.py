import os
import subprocess
import tempfile


class LexerExecutor:
    """Ejecuta el lexer compilado con código MiniLex de entrada."""

    def __init__(self, lexer_executable: str):
        self.lexer_executable = lexer_executable

    def execute(self, code: str) -> tuple[bool, str, str]:
        if not code or not str(code).strip():
            return (False, "", "Error: El código de entrada está vacío")

        if not os.path.exists(self.lexer_executable):
            return (False, "", f"Error: No se encuentra el ejecutable: {self.lexer_executable}")

        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.ml', prefix='temp_minilex_',
                delete=False, encoding='utf-8'
            ) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            result = subprocess.run(
                [self.lexer_executable, temp_file_path],
                capture_output=True, text=True, check=False, timeout=30
            )

            stdout = result.stdout
            stderr = result.stderr

            if result.returncode != 0 and not stdout:
                return (False, stdout, stderr or "Error desconocido al ejecutar lexer")

            return (True, stdout, stderr)

        except FileNotFoundError:
            return (False, "", f"Error: Ejecutable no encontrado: {self.lexer_executable}")
        except subprocess.CalledProcessError as e:
            return (False, e.stdout or "", f"Error al ejecutar lexer: {e.stderr or str(e)}")
        except subprocess.TimeoutExpired:
            return (False, "", "Error: El lexer excedió el tiempo de ejecución (30s)")
        except Exception as e:
            return (False, "", f"Error inesperado: {str(e)}")
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except OSError:
                    pass
