from src.models import Token


class TokenParser:
    """Convierte la salida CSV del lexer en una lista de objetos Token."""

    def parse(self, csv_output: str) -> list[Token]:
        tokens = []
        for line in csv_output.strip().split('\n'):
            if not line or not line.strip():
                continue
            try:
                token = Token.from_csv_line(line)
                tokens.append(token)
            except (ValueError, IndexError):
                continue
        return tokens
