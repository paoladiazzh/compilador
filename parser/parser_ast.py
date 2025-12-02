import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))
from lexer import Lexer, LexerError
from ast_nodes import *

class ParseError(Exception):
    pass

class ParserAST:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = None
        self.advance()
    
    def advance(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = ("EOF", "")
    
    def current_type(self):
        return self.current_token[0] if self.current_token else "EOF"
    
    def current_value(self):
        return self.current_token[1] if self.current_token else ""
    
    def match(self, expected_type):
        if self.current_type() == expected_type:
            value = self.current_value()
            self.advance()
            return value
        return None
    
    def expect(self, expected_type):
        value = self.match(expected_type)
        if value is None:
            raise ParseError(f"Se esperaba {expected_type}, se encontró {self.current_type()}")
        return value
    
    def parse(self):
        try:
            ast = self.programa()
            if self.current_type() != "EOF":
                raise ParseError(f"Se esperaba EOF, se encontró {self.current_type()}")
            return ast
        except ParseError as e:
            print(f"Error de sintaxis: {e}")
            return None
    
    def programa(self):
        declarations = self.listadecl()
        return ProgramNode(declarations)
    
    def listadecl(self):
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
        var_type = self.tipo()
        var_name = self.expect("ID")
        
        if self.current_type() == "LPAREN":
            self.advance()
            params = self.parametros()
            self.expect("RPAREN")
            body = self.bloque()
            return FuncDeclNode(var_type, var_name, params, body)
        else:
            vars_list = [VarDeclNode(var_type, var_name, None)]
            
            if self.current_type() == "ASIGNACION":
                self.advance()
                init_expr = self.expr()
                vars_list[0].init_expr = init_expr
            
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
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            tipo_str = self.current_type().lower()
            self.advance()
            return tipo_str
        else:
            raise ParseError(f"Se esperaba un tipo, se encontró {self.current_type()}")
    
    def parametros(self):
        if self.current_type() in ["INT", "FLOAT", "VOID"]:
            return self.paramlista()
        return []
    
    def paramlista(self):
        params = [self.param()]
        while self.current_type() == "COMA":
            self.advance()
            params.append(self.param())
        return params
    
    def param(self):
        param_type = self.tipo()
        param_name = self.expect("ID")
        return ParamNode(param_type, param_name)
    
    def bloque(self):
        self.expect("LBRACE")
        statements = self.listasentencias()
        self.expect("RBRACE")
        return BlockNode(statements)
    
    def listasentencias(self):
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
        if self.current_type() == "PUNTOYCOMA":
            self.advance()
            return None
        else:
            if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID", "OP_RESTA"]:
                expr = self.expr()
                self.expect("PUNTOYCOMA")
                return ExprStmtNode(expr)
            else:
                self.expect("PUNTOYCOMA")
                return None
    
    def sentenciasel(self):
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
            
            if self.current_type() == "PUNTOYCOMA":
                init_expr = EmptyExprNode()
            else:
                init_expr = self.expr()
            self.expect("PUNTOYCOMA")
            
            if self.current_type() == "PUNTOYCOMA":
                condition = EmptyExprNode()
            else:
                condition = self.expr()
            self.expect("PUNTOYCOMA")
            
            if self.current_type() == "RPAREN":
                update_expr = EmptyExprNode()
            else:
                update_expr = self.expr()
            self.expect("RPAREN")
            
            body = self.sentencia()
            return ForNode(init_expr, condition, update_expr, body)
    
    def sentenciaret(self):
        self.expect("RETURN")
        if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID", "OP_RESTA"]:
            expr = self.expr()
        else:
            expr = EmptyExprNode()
        self.expect("PUNTOYCOMA")
        return ReturnNode(expr)
    
    def sentenciaprint(self):
        self.expect("PRINT")
        self.expect("LPAREN")
        expr = self.expr()
        self.expect("RPAREN")
        self.expect("PUNTOYCOMA")
        return PrintNode(expr)
    
    def expr(self):
        left = self.exprand()
        while self.current_type() == "OP_OR":
            op = self.current_value()
            self.advance()
            right = self.exprand()
            left = BinaryOpNode(op, left, right)
        return left
    
    def exprand(self):
        left = self.expreq()
        while self.current_type() == "OP_AND":
            op = self.current_value()
            self.advance()
            right = self.expreq()
            left = BinaryOpNode(op, left, right)
        return left
    
    def expreq(self):
        left = self.exprrel()
        while self.current_type() in ["OP_EQ", "OP_NEQ"]:
            op = self.current_value()
            self.advance()
            right = self.exprrel()
            left = BinaryOpNode(op, left, right)
        return left
    
    def exprrel(self):
        left = self.expradit()
        if self.current_type() in ["OP_LT", "OP_GT", "OP_LE", "OP_GE"]:
            op = self.current_value()
            self.advance()
            right = self.expradit()
            left = BinaryOpNode(op, left, right)
        return left
    
    def expradit(self):
        left = self.term()
        while self.current_type() in ["OP_SUMA", "OP_RESTA"]:
            op = self.current_value()
            self.advance()
            right = self.term()
            left = BinaryOpNode(op, left, right)
        return left
    
    def term(self):
        left = self.factor()
        while self.current_type() in ["OP_MUL", "OP_DIV", "OP_MOD"]:
            op = self.current_value()
            self.advance()
            right = self.factor()
            left = BinaryOpNode(op, left, right)
        return left
    
    def factor(self):
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
        elif token == "OP_RESTA":
            self.advance()
            expr = self.factor()
            return UnaryOpNode("-", expr)
        elif token == "ID":
            var_name = self.current_value()
            self.advance()
            
            if self.current_type() == "ASIGNACION":
                self.advance()
                expr = self.expr()
                return AssignNode(var_name, expr)
            elif self.current_type() == "LPAREN":
                self.advance()
                args = []
                if self.current_type() in ["LPAREN", "NUM", "OP_NOT", "ID", "OP_RESTA"]:
                    args = self.arglist()
                self.expect("RPAREN")
                return FuncCallNode(var_name, args)
            else:
                return VarNode(var_name)
        else:
            raise ParseError(f"Se esperaba LPAREN, NUM, OP_NOT, OP_RESTA o ID, se encontró {token}")
    
    def arglist(self):
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
        
        print("Análisis léxico exitoso")
        print(f"Tokens generados: {len(tokens)}\n")
        
        print("Iniciando construcción del AST")
        parser = ParserAST(tokens)
        ast = parser.parse()
        
        if ast:
            print("AST construido exitosamente")
            print(f"\n{ast}")
            sys.exit(0)
        else:
            print("Error al construir el AST")
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