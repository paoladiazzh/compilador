import sys
import os

# Importar el lexer y los nodos del AST
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))
from lexer import Lexer, LexerError
from ast_nodes import *

class ParseError(Exception):
    pass

class ParserAST:
    """Parser que construye un Abstract Syntax Tree (AST)"""
    
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
    
    def current_value(self):
        """Retorna el valor del token actual"""
        return self.current_token[1] if self.current_token else ""
    
    def match(self, expected_type):
        """Verifica y consume si coincide"""
        if self.current_type() == expected_type:
            value = self.current_value()
            self.advance()
            return value
        return None
    
    def expect(self, expected_type):
        """Verifica que el token actual sea del tipo esperado"""
        value = self.match(expected_type)
        if value is None:
            raise ParseError(f"Se esperaba {expected_type}, se encontró {self.current_type()}")
        return value
    
    # ==================== PARSING CON CONSTRUCCIÓN DE AST ====================
    
    def parse(self):
        """S → bof PROGRAMA eof"""
        try:
            ast = self.programa()
            if self.current_type() != "EOF":
                raise ParseError(f"Se esperaba EOF, se encontró {self.current_type()}")
            return ast
        except ParseError as e:
            print(f"Error de sintaxis: {e}")
            return None
    
    def programa(self):
        """PROGRAMA → LISTADECL"""
        declarations = self.listadecl()
        return ProgramNode(declarations)
    
    def listadecl(self):
        """LISTADECL → DECL LISTADECL | ε"""
        declarations = []
        while self.current_type() in ["INT", "FLOAT", "VOID"]:
            decl = self.decl()
            if decl:
                if isinstance(decl, list):
                    declarations.extend(decl)
                else:
                    declarations.append(decl)
        return declarations
    
    def decl(self):
        """DECL → TIPO id (declaración de variable o función)"""
        var_type = self.tipo()
        var_name = self.expect("ID")
        
        # Decidir si es variable o función
        if self.current_type() == "LPAREN":
            # Es una función
            self.advance()
            params = self.parametros()
            self.expect("RPAREN")
            body = self.bloque()
            return FuncDeclNode(var_type, var_name, params, body)
        else:
            # Es una o más variables
            vars_list = [VarDeclNode(var_type, var_name, None)]
            
            # Verificar si hay inicialización
            if self.current_type() == "ASIGNACION":
                self.advance()
                init_expr = self.expr()
                vars_list[0].init_expr = init_expr
            
            # Verificar si hay más variables
            while self.current_type() == "COMA":
                self.advance()
                next_name = self.expect("ID")
                next_init = None
                if self.current_type() == "ASIGNACION":
                    self.advance()
                    next_init = self.expr()
                vars_list.append(VarDeclNode(var_type, next_name, next_init))
            
            self.expect("PUNTOYCOMA")
            return vars_list
    
    def tipo(self):
        """TIPO → int | float | void"""
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            tipo_str = self.current_type().lower()
            self.advance()
            return tipo_str
        else:
            raise ParseError(f"Se esperaba un tipo, se encontró {self.current_type()}")
    
    def parametros(self):
        """PARAMETROS → PARAMLISTA | ε"""
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            return self.paramlista()
        return []
    
    def paramlista(self):
        """PARAMLISTA → PARAM (, PARAM)*"""
        params = [self.param()]
        while self.current_type() == "COMA":
            self.advance()
            params.append(self.param())
        return params
    
    def param(self):
        """PARAM → TIPO id"""
        param_type = self.tipo()
        param_name = self.expect("ID")
        return ParamNode(param_type, param_name)
    
    def bloque(self):
        """BLOQUE → { LISTASENTENCIAS }"""
        self.expect("LBRACE")
        statements = self.listasentencias()
        self.expect("RBRACE")
        return BlockNode(statements)
    
    def listasentencias(self):
        """LISTASENTENCIAS → SENTENCIA*"""
        statements = []
        first_sentencia = ["INT", "FLOAT", "VOID", "ID", "LPAREN", "NUM", "OP_NOT", 
                          "PUNTOYCOMA", "IF", "WHILE", "FOR", "RETURN", "PRINT", "LBRACE"]
        
        while self.current_type() in first_sentencia:
            stmt = self.sentencia()
            if stmt:
                if isinstance(stmt, list):
                    statements.extend(stmt)
                else:
                    statements.append(stmt)
        return statements
    
    def sentencia(self):
        """SENTENCIA → declaración local o sentencias de control"""
        token = self.current_type()
        
        if token in ["INT", "FLOAT", "VOID"]:
            return self.decllocal()
        elif token == "IF":
            return self.sentenciasel()
        elif token in ["WHILE", "FOR"]:
            return self.sentenciaiter()
        elif token == "RETURN":
            return self.sentenciaret()
        elif token == "PRINT":
            return self.sentenciaprint()
        elif token == "LBRACE":
            return self.bloque()
        else:
            return self.sentenciaexpr()
    
    def decllocal(self):
        """DECLLOCAL → TIPO id (= EXPR)? (, id (= EXPR)?)* ;"""
        var_type = self.tipo()
        var_name = self.expect("ID")
        
        vars_list = [VarDeclNode(var_type, var_name, None)]
        
        if self.current_type() == "ASIGNACION":
            self.advance()
            vars_list[0].init_expr = self.expr()
        
        while self.current_type() == "COMA":
            self.advance()
            next_name = self.expect("ID")
            next_init = None
            if self.current_type() == "ASIGNACION":
                self.advance()
                next_init = self.expr()
            vars_list.append(VarDeclNode(var_type, next_name, next_init))
        
        self.expect("PUNTOYCOMA")
        return vars_list
    
    def sentenciaexpr(self):
        """SENTENCIAEXPR → EXPR; | ;"""
        if self.current_type() == "PUNTOYCOMA":
            self.advance()
            return None
        else:
            # Verificar que no sea solo un punto y coma vacío
            if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID"]:
                expr = self.expr()
                self.expect("PUNTOYCOMA")
                return ExprStmtNode(expr)
            else:
                self.expect("PUNTOYCOMA")
                return None
    
    def sentenciasel(self):
        """SENTENCIASEL → if (EXPR) SENTENCIA (else SENTENCIA)?"""
        self.expect("IF")
        self.expect("LPAREN")
        condition = self.expr()
        self.expect("RPAREN")
        then_stmt = self.sentencia()
        else_stmt = None
        if self.current_type() == "ELSE":
            self.advance()
            else_stmt = self.sentencia()
        return IfNode(condition, then_stmt, else_stmt)
    
    def sentenciaiter(self):
        """SENTENCIAITER → while (EXPR) SENTENCIA | for (EXPR; EXPR; EXPR) SENTENCIA"""
        if self.current_type() == "WHILE":
            self.advance()
            self.expect("LPAREN")
            condition = self.expr()
            self.expect("RPAREN")
            body = self.sentencia()
            return WhileNode(condition, body)
        elif self.current_type() == "FOR":
            self.advance()
            self.expect("LPAREN")
            
            # Inicialización (puede estar vacía)
            if self.current_type() == "PUNTOYCOMA":
                init_expr = EmptyExprNode()
            else:
                init_expr = self.expr()
            self.expect("PUNTOYCOMA")
            
            # Condición (puede estar vacía)
            if self.current_type() == "PUNTOYCOMA":
                condition = EmptyExprNode()
            else:
                condition = self.expr()
            self.expect("PUNTOYCOMA")
            
            # Actualización (puede estar vacía)
            if self.current_type() == "RPAREN":
                update_expr = EmptyExprNode()
            else:
                update_expr = self.expr()
            self.expect("RPAREN")
            
            body = self.sentencia()
            return ForNode(init_expr, condition, update_expr, body)
    
    def sentenciaret(self):
        """SENTENCIARET → return EXPR;"""
        self.expect("RETURN")
        # Manejar expresiones en el return
        if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID"]:
            expr = self.expr()
        else:
            # Return sin expresión (para funciones void)
            expr = EmptyExprNode()
        self.expect("PUNTOYCOMA")
        return ReturnNode(expr)
    
    def sentenciaprint(self):
        """SENTENCIAPRINT → print(EXPR);"""
        self.expect("PRINT")
        self.expect("LPAREN")
        expr = self.expr()
        self.expect("RPAREN")
        self.expect("PUNTOYCOMA")
        return PrintNode(expr)
    
    # ==================== EXPRESIONES ====================
    
    def expr(self):
        """EXPR → EXPRAND (|| EXPRAND)*"""
        left = self.exprand()
        while self.current_type() == "OP_OR":
            op = self.current_value()
            self.advance()
            right = self.exprand()
            left = BinaryOpNode(op, left, right)
        return left
    
    def exprand(self):
        """EXPRAND → EXPREQ (&& EXPREQ)*"""
        left = self.expreq()
        while self.current_type() == "OP_AND":
            op = self.current_value()
            self.advance()
            right = self.expreq()
            left = BinaryOpNode(op, left, right)
        return left
    
    def expreq(self):
        """EXPREQ → EXPRREL ((== | !=) EXPRREL)*"""
        left = self.exprrel()
        while self.current_type() in ["OP_EQ", "OP_NEQ"]:
            op = self.current_value()
            self.advance()
            right = self.exprrel()
            left = BinaryOpNode(op, left, right)
        return left
    
    def exprrel(self):
        """EXPRREL → EXPRADIT ((< | > | <= | >=) EXPRADIT)*"""
        left = self.expradit()
        while self.current_type() in ["OP_LT", "OP_GT", "OP_LE", "OP_GE"]:
            op = self.current_value()
            self.advance()
            right = self.expradit()
            left = BinaryOpNode(op, left, right)
        return left
    
    def expradit(self):
        """EXPRADIT → TERM ((+ | -) TERM)*"""
        left = self.term()
        while self.current_type() in ["OP_SUMA", "OP_RESTA"]:
            op = self.current_value()
            self.advance()
            right = self.term()
            left = BinaryOpNode(op, left, right)
        return left
    
    def term(self):
        """TERM → FACTOR ((* | / | %) FACTOR)*"""
        left = self.factor()
        while self.current_type() in ["OP_MUL", "OP_DIV", "OP_MOD"]:
            op = self.current_value()
            self.advance()
            right = self.factor()
            left = BinaryOpNode(op, left, right)
        return left
    
    def factor(self):
        """FACTOR → (EXPR) | num | !FACTOR | id (= EXPR | (ARGS) | ε)"""
        token = self.current_type()
        
        if token == "LPAREN":
            self.advance()
            expr = self.expr()
            self.expect("RPAREN")
            return expr
        elif token == "NUM":
            value = self.current_value()
            self.advance()
            return NumNode(value)
        elif token == "OP_NOT":
            self.advance()
            expr = self.factor()
            return UnaryOpNode("!", expr)
        elif token == "ID":
            var_name = self.current_value()
            self.advance()
            
            # Verificar asignación, llamada a función o solo variable
            if self.current_type() == "ASIGNACION":
                self.advance()
                expr = self.expr()
                return AssignNode(var_name, expr)
            elif self.current_type() == "LPAREN":
                self.advance()
                args = []
                if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID"]:
                    args = self.arglist()
                self.expect("RPAREN")
                return FuncCallNode(var_name, args)
            else:
                return VarNode(var_name)
        else:
            raise ParseError(f"Se esperaba LPAREN, NUM, OP_NOT o ID, se encontró {token}")
    
    def arglist(self):
        """ARGLIST → EXPR (, EXPR)*"""
        args = [self.expr()]
        while self.current_type() == "COMA":
            self.advance()
            args.append(self.expr())
        return args


def main():
    if len(sys.argv) < 2:
        print("Uso: python parser_ast.py <archivo_fuente>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        
        lexer = Lexer()
        tokens = lexer.tokenize(src)
        
        print("=== Análisis Léxico Exitoso ===")
        print(f"Tokens generados: {len(tokens)}\n")
        
        print("=== Iniciando Construcción del AST ===")
        parser = ParserAST(tokens)
        ast = parser.parse()
        
        if ast:
            print("✓ AST construido exitosamente!")
            print(f"\n{ast}")
            sys.exit(0)
        else:
            print("✗ Error al construir el AST")
            sys.exit(1)
    
    except LexerError as e:
        print(f"Error léxico: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()