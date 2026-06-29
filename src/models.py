import os
from dataclasses import dataclass


@dataclass
class Token:
    line: int
    column: int
    token_type: str
    lexeme: str

    def is_error(self) -> bool:
        return self.token_type == "ERROR_LEXICO"

    def to_csv_line(self) -> str:
        return f"{self.line},{self.column},{self.token_type},{self.lexeme}"

    @classmethod
    def from_csv_line(cls, csv_line: str) -> 'Token':
        parts = csv_line.strip().split(',', 3)
        if len(parts) != 4:
            raise ValueError(f"Formato CSV inválido: {csv_line}")
        return cls(
            line=int(parts[0]),
            column=int(parts[1]),
            token_type=parts[2],
            lexeme=parts[3]
        )


@dataclass
class AnalysisResult:
    tokens: list[Token]
    error_count: int
    success: bool
    message: str

    @property
    def token_count(self) -> int:
        return len([t for t in self.tokens if not t.is_error()])

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0

    def get_errors(self) -> list[Token]:
        return [t for t in self.tokens if t.is_error()]

    def get_summary(self) -> str:
        return (
            f"Tokens reconocidos: {self.token_count}\n"
            f"Errores léxicos: {self.error_count}"
        )


@dataclass
class LexerConfig:
    lexer_source: str = "src/lexer.l"
    build_dir: str = "build/"
    executable_name: str = "lexer"
    flex_command: str = "flex"
    gcc_command: str = "gcc"
    temp_file_prefix: str = "temp_"

    def get_executable_path(self) -> str:
        exe_name = f"{self.executable_name}.exe" if os.name == 'nt' else self.executable_name
        return os.path.join(self.build_dir, exe_name)
