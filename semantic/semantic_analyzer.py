"""
Analizador Semántico para miniC
Realiza validaciones semánticas sobre el AST:
1. Declaración antes de uso de variables
2. Tipos compatibles en operaciones
3. Número y tipo de parámetros en funciones
4. Ciclos y condicionales con expresiones válidas
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lexer'))
from lexer import Lexer, LexerError
from parser_ast import ParserAST
from ast_nodes import *

class SemanticError(Exception):
    pass

class SymbolTable:
    """Tabla de símbolos con soporte para ámbitos (scopes)"""
    
    def __init__(self):
        self.scopes = [{}]  # Stack de ámbitos, el primer elemento es el ámbito global
        self.functions = {}  # Tabla de funciones: {nombre: (tipo_retorno, [tipos_params])}
    
    def enter_scope(self):
        """Entra a un nuevo ámbito (bloque)"""
        self.scopes.append({})
    
    def exit_scope(self):
        """Sale del ámbito actual"""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def add_symbol(self, name, symbol_type, is_function=False):
        """Añade un símbolo al ámbito actual"""
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SemanticError(f"Variable '{name}' ya está declarada en este ámbito")
        current_scope[name] = symbol_type
    
    def lookup(self, name):
        """Busca un símbolo en todos los ámbitos (del más interno al más externo)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def add_function(self, name, return_type, param_types):
        """Registra una función"""
        if name in self.functions:
            raise SemanticError(f"Función '{name}' ya está declarada")
        self.functions[name] = (return_type, param_types)
    
    def lookup_function(self, name):
        """Busca una función"""
        return self.functions.get(name, None)
    
    def get_table_representation(self):
        """Genera una representación en forma de tabla de los símbolos"""
        lines = []
        lines.append("=" * 80)
        lines.append("TABLA DE SÍMBOLOS")
        lines.append("=" * 80)
        
        # Variables globales
        lines.append("\n--- Variables Globales ---")
        if self.scopes[0]:
            lines.append(f"{'Nombre':<20} {'Tipo':<15}")
            lines.append("-" * 35)
            for name, var_type in self.scopes[0].items():
                lines.append(f"{name:<20} {var_type:<15}")
        else:
            lines.append("(ninguna)")
        
        # Funciones
        lines.append("\n--- Funciones ---")
        if self.functions:
            lines.append(f"{'Nombre':<20} {'Tipo Retorno':<15} {'Parámetros':<30}")
            lines.append("-" * 65)
            for name, (ret_type, params) in self.functions.items():
                params_str = ", ".join(params) if params else "(sin parámetros)"
                lines.append(f"{name:<20} {ret_type:<15} {params_str:<30}")
        else:
            lines.append("(ninguna)")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


class SemanticAnalyzer:
    """Analizador semántico que recorre el AST y valida restricciones semánticas"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function_return_type = None  # Para validar returns
    
    def add_error(self, message):
        """Registra un error semántico"""
        self.errors.append(message)
    
    def analyze(self, ast):
        """Punto de entrada del análisis semántico"""
        try:
            self.visit_program(ast)
            return len(self.errors) == 0
        except SemanticError as e:
            self.add_error(str(e))
            return False
    
    # ==================== VISITADORES DE NODOS ====================
    
    def visit_program(self, node):
        """Visita el nodo Program"""
        for decl in node.declarations:
            if isinstance(decl, FuncDeclNode):
                self.visit_func_decl(decl)
            elif isinstance(decl, VarDeclNode):
                self.visit_var_decl(decl, is_global=True)
    
    def visit_func_decl(self, node):
        """Visita una declaración de función"""
        # Registrar función en la tabla
        param_types = [p.param_type for p in node.params]
        try:
            self.symbol_table.add_function(node.func_name, node.return_type, param_types)
        except SemanticError as e:
            self.add_error(str(e))
            return
        
        # Entrar a un nuevo ámbito para la función
        self.symbol_table.enter_scope()
        self.current_function_return_type = node.return_type
        
        # Añadir parámetros al ámbito local
        for param in node.params:
            try:
                self.symbol_table.add_symbol(param.param_name, param.param_type)
            except SemanticError as e:
                self.add_error(str(e))
        
        # Visitar el cuerpo de la función
        self.visit_block(node.body)
        
        # Salir del ámbito de la función
        self.symbol_table.exit_scope()
        self.current_function_return_type = None
    
    def visit_var_decl(self, node, is_global=False):
        """Visita una declaración de variable"""
        try:
            self.symbol_table.add_symbol(node.var_name, node.var_type)
        except SemanticError as e:
            self.add_error(str(e))
            return
        
        # Si tiene inicialización, validar tipo
        if node.init_expr:
            expr_type = self.visit_expr(node.init_expr)
            if not self.types_compatible(node.var_type, expr_type):
                self.add_error(f"Tipo incompatible en inicialización de '{node.var_name}': "
                             f"se esperaba '{node.var_type}', se encontró '{expr_type}'")
    
    def visit_block(self, node):
        """Visita un bloque de código"""
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            if isinstance(stmt, list):
                for s in stmt:
                    self.visit_statement(s)
            else:
                self.visit_statement(stmt)
        self.symbol_table.exit_scope()
    
    def visit_statement(self, node):
        """Visita una sentencia"""
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
        """Visita un if"""
        # Validar que la condición sea una expresión válida
        cond_type = self.visit_expr(node.condition)
        if cond_type not in ['int', 'float', 'bool', 'unknown']:
            self.add_error(f"La condición del 'if' debe ser una expresión booleana o numérica, se encontró '{cond_type}'")
        
        self.visit_statement(node.then_stmt)
        if node.else_stmt:
            self.visit_statement(node.else_stmt)
    
    def visit_while(self, node):
        """Visita un while"""
        # Validar que la condición sea una expresión válida
        cond_type = self.visit_expr(node.condition)
        if cond_type not in ['int', 'float', 'bool', 'unknown']:
            self.add_error(f"La condición del 'while' debe ser una expresión booleana o numérica, se encontró '{cond_type}'")
        
        self.visit_statement(node.body)
    
    def visit_for(self, node):
        """Visita un for"""
        # Validar expresiones del for (pueden ser vacías)
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
        """Visita un return"""
        # CORRECCIÓN: Manejar correctamente EmptyExprNode
        if isinstance(node.expr, EmptyExprNode):
            expr_type = 'void'
        else:
            expr_type = self.visit_expr(node.expr)
        
        # Validar que el tipo de retorno coincida con la función
        if self.current_function_return_type:
            if not self.types_compatible(self.current_function_return_type, expr_type):
                self.add_error(f"Tipo de retorno incompatible: se esperaba '{self.current_function_return_type}', "
                             f"se encontró '{expr_type}'")
    
    def visit_print(self, node):
        """Visita un print"""
        self.visit_expr(node.expr)
    
    def visit_expr(self, node):
        """Visita una expresión y retorna su tipo"""
        if node is None:
            return 'void'
        elif isinstance(node, EmptyExprNode):
            return 'void'
        elif isinstance(node, NumNode):
            # CORRECCIÓN CRÍTICA: Los números literales no necesitan declaración
            # Solo retornar su tipo directamente
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
        """Visita una operación binaria y valida tipos"""
        left_type = self.visit_expr(node.left)
        right_type = self.visit_expr(node.right)
        
        # Operadores aritméticos: +, -, *, /, %
        if node.op in ['+', '-', '*', '/', '%']:
            if left_type not in ['int', 'float', 'unknown'] or right_type not in ['int', 'float', 'unknown']:
                self.add_error(f"Operador '{node.op}' requiere operandos numéricos, "
                             f"se encontró '{left_type}' y '{right_type}'")
                return 'unknown'
            # Promoción de tipo: int + float = float
            result_type = 'float' if 'float' in [left_type, right_type] else 'int'
            node.expr_type = result_type
            return result_type
        
        # Operadores relacionales: <, >, <=, >=, ==, !=
        elif node.op in ['<', '>', '<=', '>=', '==', '!=']:
            if left_type not in ['int', 'float', 'unknown'] or right_type not in ['int', 'float', 'unknown']:
                self.add_error(f"Operador '{node.op}' requiere operandos numéricos, "
                             f"se encontró '{left_type}' y '{right_type}'")
                return 'unknown'
            node.expr_type = 'bool'
            return 'bool'
        
        # Operadores lógicos: &&, ||
        elif node.op in ['&&', '||']:
            # En miniC, las expresiones lógicas pueden trabajar con números
            node.expr_type = 'bool'
            return 'bool'
        
        else:
            self.add_error(f"Operador binario desconocido: {node.op}")
            return 'unknown'
    
    def visit_unary_op(self, node):
        """Visita una operación unaria"""
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
        """Visita una asignación"""
        # Validación 1: La variable debe estar declarada
        var_type = self.symbol_table.lookup(node.var_name)
        if var_type is None:
            self.add_error(f"Variable '{node.var_name}' no está declarada")
            return 'unknown'
        
        # Validación 2: El tipo de la expresión debe ser compatible
        expr_type = self.visit_expr(node.expr)
        if not self.types_compatible(var_type, expr_type):
            self.add_error(f"Asignación de tipo incompatible a '{node.var_name}': "
                         f"se esperaba '{var_type}', se encontró '{expr_type}'")
        
        return var_type
    
    def visit_var(self, node):
        """Visita una variable"""
        # Validación 1: La variable debe estar declarada antes de usarse
        var_type = self.symbol_table.lookup(node.var_name)
        if var_type is None:
            self.add_error(f"Variable '{node.var_name}' no está declarada")
            return 'unknown'
        
        node.expr_type = var_type
        return var_type
    
    def visit_func_call(self, node):
        """Visita una llamada a función"""
        # Validación 1: La función debe estar declarada
        func_info = self.symbol_table.lookup_function(node.func_name)
        if func_info is None:
            self.add_error(f"Función '{node.func_name}' no está declarada")
            return 'unknown'
        
        return_type, param_types = func_info
        
        # Validación 2: Número de argumentos debe coincidir
        if len(node.args) != len(param_types):
            self.add_error(f"Llamada a función '{node.func_name}' con número incorrecto de argumentos: "
                         f"se esperaban {len(param_types)}, se encontraron {len(node.args)}")
            return return_type
        
        # Validación 3: Tipos de argumentos deben ser compatibles
        for i, (arg, expected_type) in enumerate(zip(node.args, param_types)):
            arg_type = self.visit_expr(arg)
            if not self.types_compatible(expected_type, arg_type):
                self.add_error(f"Argumento {i+1} de función '{node.func_name}' tiene tipo incompatible: "
                             f"se esperaba '{expected_type}', se encontró '{arg_type}'")
        
        node.expr_type = return_type
        return return_type
    
    def types_compatible(self, expected, actual):
        """Verifica si dos tipos son compatibles"""
        if expected == actual:
            return True
        # Permitir promoción implícita: int -> float
        if expected == 'float' and actual == 'int':
            return True
        # Tipo desconocido siempre es compatible (para evitar errores en cascada)
        if actual == 'unknown':
            return True
        return False
    
    def get_errors_report(self):
        """Genera un reporte de errores semánticos"""
        if not self.errors:
            return "✓ No se encontraron errores semánticos"
        
        lines = ["=" * 80, "ERRORES SEMÁNTICOS ENCONTRADOS", "=" * 80]
        for i, error in enumerate(self.errors, 1):
            lines.append(f"{i}. {error}")
        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Uso: python semantic_analyzer.py <archivo_fuente>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        
        # Análisis léxico
        lexer = Lexer()
        tokens = lexer.tokenize(src)
        print("=== Análisis Léxico Exitoso ===")
        print(f"Tokens generados: {len(tokens)}\n")
        
        # Construcción del AST
        parser = ParserAST(tokens)
        ast = parser.parse()
        
        if not ast:
            print("✗ Error en la construcción del AST")
            sys.exit(1)
        
        print("=== AST Construido Exitosamente ===\n")
        
        # Análisis semántico
        print("=== Iniciando Análisis Semántico ===\n")
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        # Mostrar tabla de símbolos
        print(analyzer.symbol_table.get_table_representation())
        print()
        
        # Mostrar errores (si los hay)
        print(analyzer.get_errors_report())
        
        if success:
            print("\n✓ Análisis semántico completado exitosamente!")
            sys.exit(0)
        else:
            print("\n✗ Análisis semántico falló")
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