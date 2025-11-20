import sys
import os

# Importar el lexer del directorio 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))
from lexer import Lexer, LexerError

class ParseError(Exception):
    pass

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = None
        self.advance()
    
    def advance(self):
        """Avanza al siguiente token"""
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = ("EOF", "")
    
    def current_type(self):
        """Retorna el tipo del token actual"""
        return self.current_token[0] if self.current_token else "EOF"
    
    def match(self, expected_type):
        """Verifica y consume si coincide"""
        if self.current_type() == expected_type:
            self.advance()
            return True
        return False
    
    def expect(self, expected_type):
        """Verifica que el token actual sea del tipo esperado"""
        if not self.match(expected_type):
            raise ParseError(f"Se esperaba {expected_type}, se encontró {self.current_type()}")
    
    # Reglas de la gramática
    
    def parse(self):
        """S → bof PROGRAMA eof"""
        try:
            self.programa()
            if self.current_type() != "EOF":
                raise ParseError(f"Se esperaba EOF, se encontró {self.current_type()}")
            return True
        except ParseError as e:
            print(f"Error de sintaxis: {e}")
            return False
    
    def programa(self):
        """PROGRAMA → LISTADECL"""
        self.listadecl()
    
    def listadecl(self):
        """LISTADECL → DECL LISTADECL | ε"""
        # FIRST(DECL) = {INT, FLOAT, VOID}
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            self.decl()
            self.listadecl()
        # ε en FOLLOW(LISTADECL) = {EOF}
    
    def decl(self):
        """DECL → TIPO DECL'"""
        self.tipo()
        self.decl_prima()
    
    def decl_prima(self):
        """DECL' → id DECL''"""
        self.expect("ID")
        self.decl_dobleprima()
    
    def decl_dobleprima(self):
        """DECL'' → LISTAID' puntoycoma | lparen DECL'''"""
        if self.current_type() == "LPAREN":
            self.advance()
            self.decl_tripleprima()
        else:
            self.listaid_prima()
            self.expect("PUNTOYCOMA")
    
    def decl_tripleprima(self):
        """DECL''' → PARAMETROS rparen BLOQUE"""
        self.parametros()
        self.expect("RPAREN")
        self.bloque()
    
    def listaid_prima(self):
        """LISTAID' → coma LISTAID | ε"""
        if self.current_type() == "COMA":
            self.advance()
            self.expect("ID")
            self.listaid_prima()
        # ε en FOLLOW(LISTAID') = {PUNTOYCOMA}
    
    def tipo(self):
        """TIPO → int | float | void"""
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            self.advance()
        else:
            raise ParseError(f"Se esperaba un tipo (INT, FLOAT, VOID), se encontró {self.current_type()}")
    
    def parametros(self):
        """PARAMETROS → PARAMLISTA | ε"""
        # FIRST(PARAMLISTA) = {INT, FLOAT, VOID}
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            self.paramlista()
        # ε en FOLLOW(PARAMETROS) = {RPAREN}
    
    def paramlista(self):
        """PARAMLISTA → PARAM PARAMLISTA'"""
        self.param()
        self.paramlista_prima()
    
    def paramlista_prima(self):
        """PARAMLISTA' → coma PARAM PARAMLISTA' | ε"""
        if self.current_type() == "COMA":
            self.advance()
            self.param()
            self.paramlista_prima()
        # ε en FOLLOW(PARAMLISTA') = {RPAREN}
    
    def param(self):
        """PARAM → TIPO id"""
        self.tipo()
        self.expect("ID")
    
    def bloque(self):
        """BLOQUE → lbrace LISTASENTENCIAS rbrace"""
        self.expect("LBRACE")
        self.listasentencias()
        self.expect("RBRACE")
    
    def listasentencias(self):
        """LISTASENTENCIAS → SENTENCIA LISTASENTENCIAS | ε"""
        # FIRST(SENTENCIA) = {INT, FLOAT, VOID, ID, LPAREN, NUM, OP_NOT, PUNTOYCOMA, 
        #                     IF, WHILE, FOR, RETURN, PRINT, LBRACE}
        first_sentencia = ["INT", "FLOAT", "VOID", "ID", "LPAREN", "NUM", "OP_NOT", 
                          "PUNTOYCOMA", "IF", "WHILE", "FOR", "RETURN", "PRINT", "LBRACE"]
        
        if self.current_type() in first_sentencia:
            self.sentencia()
            self.listasentencias()
        # ε en FOLLOW(LISTASENTENCIAS) = {RBRACE}
    
    def sentencia(self):
        """
        SENTENCIA → SENTENCIAEXPR | SENTENCIASEL | SENTENCIAITER | 
                    SENTENCIARET | SENTENCIAPRINT | BLOQUE | DECLLOCAL
        
        LL(1): Usamos el token actual para decidir qué producción aplicar
        """
        token = self.current_type()
        
        # FIRST(DECLLOCAL) = {INT, FLOAT, VOID}
        if token in ["INT", "FLOAT", "VOID"]:
            self.decllocal()
        # FIRST(SENTENCIASEL) = {IF}
        elif token == "IF":
            self.sentenciasel()
        # FIRST(SENTENCIAITER) = {WHILE, FOR}
        elif token in ["WHILE", "FOR"]:
            self.sentenciaiter()
        # FIRST(SENTENCIARET) = {RETURN}
        elif token == "RETURN":
            self.sentenciaret()
        # FIRST(SENTENCIAPRINT) = {PRINT}
        elif token == "PRINT":
            self.sentenciaprint()
        # FIRST(BLOQUE) = {LBRACE}
        elif token == "LBRACE":
            self.bloque()
        # FIRST(SENTENCIAEXPR) = {ID, LPAREN, NUM, OP_NOT, PUNTOYCOMA}
        else:
            self.sentenciaexpr()
    
    def decllocal(self):
        """
        DECLLOCAL → TIPO id DECLLOCAL' puntoycoma
        
        Maneja declaraciones locales como:
        - int x;
        - int x = 5;
        - int x = 5, y, z = 10;
        """
        self.tipo()
        self.expect("ID")
        self.decllocal_prima()
        self.expect("PUNTOYCOMA")
    
    def decllocal_prima(self):
        """DECLLOCAL' → asignacion EXPR DECLLOCAL'' | DECLLOCAL''"""
        if self.current_type() == "ASIGNACION":
            self.advance()
            self.expr()
        self.decllocal_dobleprima()
    
    def decllocal_dobleprima(self):
        """DECLLOCAL'' → coma id DECLLOCAL' | ε"""
        if self.current_type() == "COMA":
            self.advance()
            self.expect("ID")
            self.decllocal_prima()
        # ε en FOLLOW(DECLLOCAL'') = {PUNTOYCOMA}
    
    def sentenciaexpr(self):
        """SENTENCIAEXPR → EXPR puntoycoma | puntoycoma"""
        if self.current_type() == "PUNTOYCOMA":
            self.advance()
        else:
            self.expr()
            self.expect("PUNTOYCOMA")
    
    def sentenciasel(self):
        """SENTENCIASEL → if lparen EXPR rparen SENTENCIA SENTENCIASEL'"""
        self.expect("IF")
        self.expect("LPAREN")
        self.expr()
        self.expect("RPAREN")
        self.sentencia()
        self.sentenciasel_prima()
    
    def sentenciasel_prima(self):
        """SENTENCIASEL' → else SENTENCIA | ε"""
        if self.current_type() == "ELSE":
            self.advance()
            self.sentencia()
        # ε en FOLLOW(SENTENCIASEL')
    
    def sentenciaiter(self):
        """
        SENTENCIAITER → while lparen EXPR rparen SENTENCIA
                      | for lparen EXPR puntoycoma EXPR puntoycoma EXPR rparen SENTENCIA
        """
        if self.current_type() == "WHILE":
            self.advance()
            self.expect("LPAREN")
            self.expr()
            self.expect("RPAREN")
            self.sentencia()
        elif self.current_type() == "FOR":
            self.advance()
            self.expect("LPAREN")
            self.expr()
            self.expect("PUNTOYCOMA")
            self.expr()
            self.expect("PUNTOYCOMA")
            self.expr()
            self.expect("RPAREN")
            self.sentencia()
    
    def sentenciaret(self):
        """SENTENCIARET → return EXPR puntoycoma"""
        self.expect("RETURN")
        self.expr()
        self.expect("PUNTOYCOMA")
    
    def sentenciaprint(self):
        """SENTENCIAPRINT → print lparen EXPR rparen puntoycoma"""
        self.expect("PRINT")
        self.expect("LPAREN")
        self.expr()
        self.expect("RPAREN")
        self.expect("PUNTOYCOMA")
    
    def expr(self):
        """EXPR → EXPRAND EXPR'"""
        self.exprand()
        self.expr_prima()
    
    def expr_prima(self):
        """EXPR' → op_or EXPRAND EXPR' | ε"""
        if self.current_type() == "OP_OR":
            self.advance()
            self.exprand()
            self.expr_prima()
        # ε en FOLLOW(EXPR')
    
    def exprand(self):
        """EXPRAND → EXPREQ EXPRAND'"""
        self.expreq()
        self.exprand_prima()
    
    def exprand_prima(self):
        """EXPRAND' → op_and EXPREQ EXPRAND' | ε"""
        if self.current_type() == "OP_AND":
            self.advance()
            self.expreq()
            self.exprand_prima()
        # ε en FOLLOW(EXPRAND')
    
    def expreq(self):
        """EXPREQ → EXPRREL EXPREQ'"""
        self.exprrel()
        self.expreq_prima()
    
    def expreq_prima(self):
        """EXPREQ' → (op_eq | op_neq) EXPRREL EXPREQ' | ε"""
        if self.current_type() in ["OP_EQ", "OP_NEQ"]:
            self.advance()
            self.exprrel()
            self.expreq_prima()
        # ε en FOLLOW(EXPREQ')
    
    def exprrel(self):
        """EXPRREL → EXPRADIT EXPRREL'"""
        self.expradit()
        self.exprrel_prima()
    
    def exprrel_prima(self):
        """EXPRREL' → (op_lt | op_gt | op_le | op_ge) EXPRADIT EXPRREL' | ε"""
        if self.current_type() in ["OP_LT", "OP_GT", "OP_LE", "OP_GE"]:
            self.advance()
            self.expradit()
            self.exprrel_prima()
        # ε en FOLLOW(EXPRREL')
    
    def expradit(self):
        """EXPRADIT → TERM EXPRADIT'"""
        self.term()
        self.expradit_prima()
    
    def expradit_prima(self):
        """EXPRADIT' → (op_suma | op_resta) TERM EXPRADIT' | ε"""
        if self.current_type() in ["OP_SUMA", "OP_RESTA"]:
            self.advance()
            self.term()
            self.expradit_prima()
        # ε en FOLLOW(EXPRADIT')
    
    def term(self):
        """TERM → FACTOR TERM'"""
        self.factor()
        self.term_prima()
    
    def term_prima(self):
        """TERM' → (op_mul | op_div | op_mod) FACTOR TERM' | ε"""
        if self.current_type() in ["OP_MUL", "OP_DIV", "OP_MOD"]:
            self.advance()
            self.factor()
            self.term_prima()
        # ε en FOLLOW(TERM')
    
    def factor(self):
        """
        FACTOR → lparen EXPR rparen | num | op_not FACTOR | id FACTOR'
        """
        token = self.current_type()
        
        if token == "LPAREN":
            self.advance()
            self.expr()
            self.expect("RPAREN")
        elif token == "NUM":
            self.advance()
        elif token == "OP_NOT":
            self.advance()
            self.factor()
        elif token == "ID":
            self.advance()
            self.factor_prima()
        else:
            raise ParseError(f"Se esperaba LPAREN, NUM, OP_NOT o ID, se encontró {token}")
    
    def factor_prima(self):
        """
        FACTOR' → asignacion EXPR | lparen ARGLIST rparen | lparen rparen | ε
        
        LL(1): Decisión basada en el token actual:
        - ASIGNACION → primera producción
        - LPAREN → llamada a función
        - Otros (operadores, delimitadores) → ε
        """
        token = self.current_type()
        
        if token == "ASIGNACION":
            self.advance()
            self.expr()
        elif token == "LPAREN":
            self.advance()
            # Verificar si hay argumentos o es llamada vacía
            if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID"]:
                self.arglist()
            self.expect("RPAREN")
        # ε en FOLLOW(FACTOR') = {operadores, delimitadores}
    
    def arglist(self):
        """ARGLIST → EXPR ARGLIST'"""
        self.expr()
        self.arglist_prima()
    
    def arglist_prima(self):
        """ARGLIST' → coma ARGLIST | ε"""
        if self.current_type() == "COMA":
            self.advance()
            self.arglist()
        # ε en FOLLOW(ARGLIST')


def main():
    if len(sys.argv) < 2:
        print("Uso: python parser.py <archivo_fuente>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        
        lexer = Lexer()
        tokens = lexer.tokenize(src)
        
        print("Análisis Léxico terminado")
        print(f"Tokens generados: {len(tokens)}")
        print()
        
        print("Iniciando Análisis Sintáctico....")
        parser = Parser(tokens)
        
        if parser.parse():
            print("Analizador sintáctico completado con éxito :) !")
            sys.exit(0)
        else:
            print("Analizador sintáctico fallido :(")
            sys.exit(1)
    
    except LexerError as e:
        print(f"Error léxico: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()