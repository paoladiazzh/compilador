import sys

class LexerError(Exception):
    pass

KEYWORDS = {k.lower(): k for k in ["IF", "ELSE", "WHILE", "FOR", "INT", "FLOAT", "RETURN", "PRINT", "VOID"]}

class AFD:
    def __init__(self, estados, transiciones, estado_inicial, estados_aceptacion):
        self.estados = estados
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

    def mover(self, estado, simbolo):
        return self.transiciones.get(estado, {}).get(simbolo, None)

    def es_aceptacion(self, estado):
        return estado in self.estados_aceptacion

class Lexer:
    def __init__(self):
        trans_id_q0 = {c: "q1" for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"}
        trans_id_q1 = {c: "q1" for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"}
        self.afd_id = AFD(["q0", "q1"], {"q0": trans_id_q0, "q1": trans_id_q1}, "q0", ["q1"])

        trans_num_q0 = {c: "q1" for c in "0123456789"}
        trans_num_q1 = {c: "q1" for c in "0123456789"}
        trans_num_q1["."] = "q2"
        trans_num_q2 = {c: "q3" for c in "0123456789"}
        trans_num_q3 = {c: "q3" for c in "0123456789"}
        self.afd_num = AFD(["q0", "q1", "q2", "q3"], {"q0": trans_num_q0, "q1": trans_num_q1, "q2": trans_num_q2, "q3": trans_num_q3}, "q0", ["q1", "q3"])

    def limpiar_codigo(self, texto):
        result = ""
        i = 0
        n = len(texto)
        while i < n:
            c = texto[i]
            if c == "#":
                while i < n and texto[i] != "\n":
                    i += 1
            elif c == "/" and i + 1 < n and texto[i + 1] == "/":
                i += 2
                while i < n and texto[i] != "\n":
                    i += 1
            elif c == "/" and i + 1 < n and texto[i + 1] == "*":
                i += 2
                while i + 1 < n and not (texto[i] == "*" and texto[i+1] == "/"):
                    i += 1
                i += 2
            elif c in " \t\r\n":
                i += 1
            else:
                result += c
                i += 1
        return result

    def tokenize(self, texto):
        texto = self.limpiar_codigo(texto)
        tokens = []
        pos = 0
        n = len(texto)

        while pos < n:
            c = texto[pos]
            matched = False 

            estado = self.afd_num.estado_inicial
            start = pos
            temp_pos = pos
            while temp_pos < n:
                siguiente = self.afd_num.mover(estado, texto[temp_pos])
                if siguiente is None:
                    break
                estado = siguiente
                temp_pos += 1
            if self.afd_num.es_aceptacion(estado):
                lex = texto[start:temp_pos]
                if temp_pos < n and (texto[temp_pos].isalpha() or texto[temp_pos] == '_'):
                    raise LexerError(f"Lexema inválido '{texto[start:temp_pos+1]}'")
                tokens.append(("NUM", lex))
                pos = temp_pos
                matched = True
                continue

            dos_char_ops = {"==": "OP_EQ", "!=": "OP_NEQ", "<=": "OP_LE", ">=": "OP_GE", "&&": "OP_AND", "||": "OP_OR"}
            if pos + 1 < n and texto[pos:pos+2] in dos_char_ops:
                tokens.append((dos_char_ops[texto[pos:pos+2]], texto[pos:pos+2]))
                pos += 2
                matched = True
                continue

            uno_char_ops = {"+": "OP_SUMA", "-": "OP_RESTA", "*": "OP_MUL", "/": "OP_DIV", "%": "OP_MOD",
                            "=": "ASIGNACION", "!": "OP_NOT", "<": "OP_LT", ">": "OP_GT",
                            "(": "LPAREN", ")": "RPAREN", "{": "LBRACE", "}": "RBRACE", ";": "PUNTOYCOMA", ",": "COMA"}
            if c in uno_char_ops:
                tokens.append((uno_char_ops[c], c))
                pos += 1
                matched = True
                continue

            estado = self.afd_id.estado_inicial
            start = pos
            while pos < n:
                siguiente = self.afd_id.mover(estado, texto[pos])
                if siguiente is None:
                    break
                estado = siguiente
                pos += 1
            if self.afd_id.es_aceptacion(estado):
                lex = texto[start:pos]

                palabra_reservada = None
                for kw in KEYWORDS:
                    if lex.startswith(kw) and (len(lex) == len(kw) or not lex[len(kw)].isalnum() and lex[len(kw)] != "_"):
                        palabra_reservada = kw
                        break
                    elif lex.startswith(kw):
                        palabra_reservada = kw
                        break

                if palabra_reservada:
                    tokens.append((KEYWORDS[palabra_reservada], lex[:len(palabra_reservada)]))
                    pos = start + len(palabra_reservada)
                else:
                    tokens.append(("ID", lex))

                matched = True
                continue

            if not matched:
                raise LexerError(f"Carácter inesperado: {texto[pos]}")

        return tokens

def format_tokens(tokens):
    return "\n".join(f"<{t[0]}, \"{t[1]}\">" for t in tokens)

def main():
    if len(sys.argv) < 2:
        print("Uso: python lexer.py <archivo_fuente>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        tokens = Lexer().tokenize(src)
        print(format_tokens(tokens))
    except LexerError as e:
        print(f"LexerError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()