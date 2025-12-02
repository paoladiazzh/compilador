import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))
from lexer import Lexer, LexerError
from parser_ast import ParserAST
from ast_nodes import *

class SemanticError(Exception):
    pass

class SymbolTable:
    """Tabla de símbolos con soporte para ámbitos"""
    
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def add_symbol(self, name, symbol_type, is_function=False):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SemanticError(f"Variable '{name}' ya está declarada en este ámbito")
        current_scope[name] = symbol_type
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def add_function(self, name, return_type, param_types):
        if name in self.functions:
            raise SemanticError(f"Función '{name}' ya está declarada")
        self.functions[name] = (return_type, param_types)
    
    def lookup_function(self, name):
        return self.functions.get(name, None)
    
    def get_table_representation(self):
        lines = []
        
        # --- Variables Globales ---
        lines.append("--- Variables Globales ---")
        global_scope = self.scopes[0]
        if global_scope:
            for name, var_type in global_scope.items():
                lines.append(f"{name} ({var_type})")
        else:
            lines.append("(ninguna)")
        
        lines.append("")  # línea en blanco
        
        # --- Funciones ---
        lines.append("--- Funciones ---")
        if self.functions:
            # Calcular anchos de columnas
            nombres = list(self.functions.keys())
            max_name = max(len("Nombre"), max(len(n) for n in nombres))
            max_ret = max(len("Tipo Retorno"),
                          max(len(info[0]) for info in self.functions.values()))
            
            header = f"{'Nombre'.ljust(max_name)}   {'Tipo Retorno'.ljust(max_ret)}   Parámetros"
            lines.append(header)
            lines.append("-" * len(header))
            
            for name, (ret_type, params) in self.functions.items():
                params_str = ", ".join(params) if params else "(sin parámetros)"
                line = f"{name.ljust(max_name)}   {ret_type.ljust(max_ret)}   {params_str}"
                lines.append(line)
        else:
            lines.append("(ninguna)")
        
        lines.append("")  # línea en blanco
        lines.append("=" * 80)
        
        return "\n".join(lines)


class SemanticAnalyzer:
    """Analizador semántico que recorre el AST y valida restricciones"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function_return_type = None
    
    def add_error(self, message):
        self.errors.append(message)
    
    def analyze(self, ast):
        try:
            self.visit_program(ast)
            return len(self.errors) == 0
        except SemanticError as e:
            self.add_error(str(e))
            return False
    
    def visit_program(self, node):
        for decl in node.declarations:
            if isinstance(decl, FuncDeclNode):
                self.visit_func_decl(decl)
            elif isinstance(decl, VarDeclNode):
                self.visit_var_decl(decl, is_global=True)
    
    def visit_func_decl(self, node):
        param_types = [p.param_type for p in node.params]
        try:
            self.symbol_table.add_function(node.func_name, node.return_type, param_types)
        except SemanticError as e:
            self.add_error(str(e))
            return
        
        self.symbol_table.enter_scope()
        self.current_function_return_type = node.return_type
        
        for param in node.params:
            try:
                self.symbol_table.add_symbol(param.param_name, param.param_type)
            except SemanticError as e:
                self.add_error(str(e))
        
        self.visit_block(node.body)
        
        self.symbol_table.exit_scope()
        self.current_function_return_type = None
    
    def visit_var_decl(self, node, is_global=False):
        try:
            self.symbol_table.add_symbol(node.var_name, node.var_type)
        except SemanticError as e:
            self.add_error(str(e))
            return
        
        if node.init_expr:
            expr_type = self.visit_expr(node.init_expr)
            if not self.types_compatible(node.var_type, expr_type):
                self.add_error(f"Tipo incompatible en inicialización de '{node.var_name}': "
                             f"se esperaba '{node.var_type}', se encontró '{expr_type}'")
    
    def visit_block(self, node):
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            if isinstance(stmt, list):
                for s in stmt:
                    self.visit_statement(s)
            else:
                self.visit_statement(stmt)
        self.symbol_table.exit_scope()
    
    def visit_statement(self, node):
        if node is None:
            return
        elif isinstance(node, VarDeclNode):
            self.visit_var_decl(node)
        elif isinstance(node, IfNode):
            self.visit_if(node)
        elif isinstance(node, WhileNode):
            self.visit_while(node)
        elif isinstance(node, ForNode):
            self.visit_for(node)
        elif isinstance(node, ReturnNode):
            self.visit_return(node)
        elif isinstance(node, PrintNode):
            self.visit_print(node)
        elif isinstance(node, ExprStmtNode):
            if node.expr:
                self.visit_expr(node.expr)
        elif isinstance(node, BlockNode):
            self.visit_block(node)
    
    def visit_if(self, node):
        cond_type = self.visit_expr(node.condition)
        if cond_type not in ['int', 'float', 'bool', 'unknown']:
            self.add_error(f"La condición del 'if' debe ser una expresión booleana o numérica, se encontró '{cond_type}'")
        
        self.visit_statement(node.then_stmt)
        if node.else_stmt:
            self.visit_statement(node.else_stmt)
    
    def visit_while(self, node):
        cond_type = self.visit_expr(node.condition)
        if cond_type not in ['int', 'float', 'bool', 'unknown']:
            self.add_error(f"La condición del 'while' debe ser una expresión booleana o numérica, se encontró '{cond_type}'")
        
        self.visit_statement(node.body)
    
    def visit_for(self, node):
        if not isinstance(node.init_expr, EmptyExprNode):
            self.visit_expr(node.init_expr)
        
        if not isinstance(node.condition, EmptyExprNode):
            cond_type = self.visit_expr(node.condition)
            if cond_type not in ['int', 'float', 'bool', 'unknown']:
                self.add_error(f"La condición del 'for' debe ser una expresión booleana o numérica, se encontró '{cond_type}'")
        
        if not isinstance(node.update_expr, EmptyExprNode):
            self.visit_expr(node.update_expr)
            
        self.visit_statement(node.body)
    
    def visit_return(self, node):
        if isinstance(node.expr, EmptyExprNode):
            expr_type = 'void'
        else:
            expr_type = self.visit_expr(node.expr)
        
        if self.current_function_return_type:
            if not self.types_compatible(self.current_function_return_type, expr_type):
                self.add_error(f"Tipo de retorno incompatible: se esperaba '{self.current_function_return_type}', "
                             f"se encontró '{expr_type}'")
    
    def visit_print(self, node):
        self.visit_expr(node.expr)
    
    def visit_expr(self, node):
        if node is None:
            return 'void'
        elif isinstance(node, EmptyExprNode):
            return 'void'
        elif isinstance(node, NumNode):
            return node.expr_type
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.visit_unary_op(node)
        elif isinstance(node, AssignNode):
            return self.visit_assign(node)
        elif isinstance(node, VarNode):
            return self.visit_var(node)
        elif isinstance(node, FuncCallNode):
            return self.visit_func_call(node)
        else:
            self.add_error(f"Tipo de expresión desconocido: {type(node)}")
            return 'unknown'
    
    def visit_binary_op(self, node):
        left_type = self.visit_expr(node.left)
        right_type = self.visit_expr(node.right)
        
        if node.op in ['+', '-', '*', '/', '%']:
            if left_type not in ['int', 'float', 'unknown'] or right_type not in ['int', 'float', 'unknown']:
                self.add_error(f"Operador '{node.op}' requiere operandos numéricos, "
                             f"se encontró '{left_type}' y '{right_type}'")
                return 'unknown'
            result_type = 'float' if 'float' in [left_type, right_type] else 'int'
            node.expr_type = result_type
            return result_type
        
        elif node.op in ['<', '>', '<=', '>=', '==', '!=']:
            if left_type not in ['int', 'float', 'unknown'] or right_type not in ['int', 'float', 'unknown']:
                self.add_error(f"Operador '{node.op}' requiere operandos numéricos, "
                             f"se encontró '{left_type}' y '{right_type}'")
                return 'unknown'
            node.expr_type = 'bool'
            return 'bool'
        
        elif node.op in ['&&', '||']:
            node.expr_type = 'bool'
            return 'bool'
        
        else:
            self.add_error(f"Operador binario desconocido: {node.op}")
            return 'unknown'
    
    def visit_unary_op(self, node):
        expr_type = self.visit_expr(node.expr)
        
        if node.op == '!':
            node.expr_type = 'bool'
            return 'bool'
        elif node.op == '-':
            if expr_type not in ['int', 'float', 'unknown']:
                self.add_error(f"Operador '-' unario requiere operando numérico, se encontró '{expr_type}'")
                return 'unknown'
            node.expr_type = expr_type
            return expr_type
        else:
            self.add_error(f"Operador unario desconocido: {node.op}")
            return 'unknown'
    
    def visit_assign(self, node):
        var_type = self.symbol_table.lookup(node.var_name)
        if var_type is None:
            self.add_error(f"Variable '{node.var_name}' no está declarada")
            return 'unknown'
        
        expr_type = self.visit_expr(node.expr)
        if not self.types_compatible(var_type, expr_type):
            self.add_error(f"Asignación de tipo incompatible a '{node.var_name}': "
                         f"se esperaba '{var_type}', se encontró '{expr_type}'")
        
        return var_type
    
    def visit_var(self, node):
        var_type = self.symbol_table.lookup(node.var_name)
        if var_type is None:
            self.add_error(f"Variable '{node.var_name}' no está declarada")
            return 'unknown'
        
        node.expr_type = var_type
        return var_type
    
    def visit_func_call(self, node):
        func_info = self.symbol_table.lookup_function(node.func_name)
        if func_info is None:
            self.add_error(f"Función '{node.func_name}' no está declarada")
            return 'unknown'
        
        return_type, param_types = func_info
        
        if len(node.args) != len(param_types):
            self.add_error(f"Llamada a función '{node.func_name}' con número incorrecto de argumentos: "
                         f"se esperaban {len(param_types)}, se encontraron {len(node.args)}")
            return return_type
        
        for i, (arg, expected_type) in enumerate(zip(node.args, param_types)):
            arg_type = self.visit_expr(arg)
            if not self.types_compatible(expected_type, arg_type):
                self.add_error(f"Argumento {i+1} de función '{node.func_name}' tiene tipo incompatible: "
                             f"se esperaba '{expected_type}', se encontró '{arg_type}'")
        
        node.expr_type = return_type
        return return_type
    
    def types_compatible(self, expected, actual):
        if expected == actual:
            return True
        if expected == 'float' and actual == 'int':
            return True
        if actual == 'unknown':
            return True
        return False
    
    def get_errors_report(self):
        if not self.errors:
            return "Sin errores semánticos"
        
        lines = ["Errores semánticos:"]
        for i, error in enumerate(self.errors, 1):
            lines.append(f"  {i}. {error}")
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Uso: python semantic_analyzer.py <archivo_fuente>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        
        lexer = Lexer()
        tokens = lexer.tokenize(src)
        print("Análisis léxico exitoso")
        print(f"Tokens generados: {len(tokens)}\n")
        
        parser = ParserAST(tokens)
        ast = parser.parse()
        
        if not ast:
            print("Error en construcción del AST")
            sys.exit(1)
        
        print("AST construido exitosamente\n")
        
        print("Iniciando análisis semántico\n")
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        print(analyzer.symbol_table.get_table_representation())
        print()
        
        print(analyzer.get_errors_report())
        
        if success:
            print("\nAnálisis semántico completado exitosamente")
            sys.exit(0)
        else:
            print("\nAnálisis semántico falló")
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