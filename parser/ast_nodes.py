"""
Definición de nodos del Abstract Syntax Tree (AST)
Cada nodo representa una construcción del lenguaje miniC
"""

class ASTNode:
    """Clase base para todos los nodos del AST"""
    def __init__(self):
        self.line = 0  # Para reportar errores
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"

# ==================== PROGRAMA ====================

class ProgramNode(ASTNode):
    def __init__(self, declarations):
        super().__init__()
        self.declarations = declarations  # Lista de DeclarationNode
    
    def __repr__(self):
        return f"Program({len(self.declarations)} declarations)"

# ==================== DECLARACIONES ====================

class VarDeclNode(ASTNode):
    """Declaración de variable: int x = 5;"""
    def __init__(self, var_type, var_name, init_expr=None):
        super().__init__()
        self.var_type = var_type  # 'int', 'float', 'void'
        self.var_name = var_name
        self.init_expr = init_expr  # ExprNode o None
    
    def __repr__(self):
        init = f", init={self.init_expr}" if self.init_expr else ""
        return f"VarDecl({self.var_type} {self.var_name}{init})"

class FuncDeclNode(ASTNode):
    """Declaración de función: int suma(int a, int b) { ... }"""
    def __init__(self, return_type, func_name, params, body):
        super().__init__()
        self.return_type = return_type  # 'int', 'float', 'void'
        self.func_name = func_name
        self.params = params  # Lista de ParamNode
        self.body = body  # BlockNode
    
    def __repr__(self):
        return f"FuncDecl({self.return_type} {self.func_name}, {len(self.params)} params)"

class ParamNode(ASTNode):
    """Parámetro de función: int x"""
    def __init__(self, param_type, param_name):
        super().__init__()
        self.param_type = param_type
        self.param_name = param_name
    
    def __repr__(self):
        return f"Param({self.param_type} {self.param_name})"

# ==================== SENTENCIAS ====================

class BlockNode(ASTNode):
    """Bloque de código: { ... }"""
    def __init__(self, statements):
        super().__init__()
        self.statements = statements  # Lista de StatementNode
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"

class IfNode(ASTNode):
    """Sentencia if: if (cond) { ... } else { ... }"""
    def __init__(self, condition, then_stmt, else_stmt=None):
        super().__init__()
        self.condition = condition  # ExprNode
        self.then_stmt = then_stmt  # StatementNode
        self.else_stmt = else_stmt  # StatementNode o None
    
    def __repr__(self):
        return f"If(cond={self.condition})"

class WhileNode(ASTNode):
    """Bucle while: while (cond) { ... }"""
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition  # ExprNode
        self.body = body  # StatementNode
    
    def __repr__(self):
        return f"While(cond={self.condition})"

class ForNode(ASTNode):
    """Bucle for: for (init; cond; update) { ... }"""
    def __init__(self, init_expr, condition, update_expr, body):
        super().__init__()
        self.init_expr = init_expr  # ExprNode
        self.condition = condition  # ExprNode
        self.update_expr = update_expr  # ExprNode
        self.body = body  # StatementNode
    
    def __repr__(self):
        return f"For(init={self.init_expr}, cond={self.condition})"

class ReturnNode(ASTNode):
    """Sentencia return: return expr;"""
    def __init__(self, expr):
        super().__init__()
        self.expr = expr  # ExprNode
    
    def __repr__(self):
        return f"Return({self.expr})"

class PrintNode(ASTNode):
    """Sentencia print: print(expr);"""
    def __init__(self, expr):
        super().__init__()
        self.expr = expr  # ExprNode
    
    def __repr__(self):
        return f"Print({self.expr})"

class ExprStmtNode(ASTNode):
    """Sentencia de expresión: expr;"""
    def __init__(self, expr):
        super().__init__()
        self.expr = expr  # ExprNode
    
    def __repr__(self):
        return f"ExprStmt({self.expr})"

# ==================== EXPRESIONES ====================

class BinaryOpNode(ASTNode):
    """Operación binaria: left op right"""
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op  # '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||'
        self.left = left  # ExprNode
        self.right = right  # ExprNode
        self.expr_type = None  # Se determina en análisis semántico
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class UnaryOpNode(ASTNode):
    """Operación unaria: op expr"""
    def __init__(self, op, expr):
        super().__init__()
        self.op = op  # '!', '-'
        self.expr = expr  # ExprNode
        self.expr_type = None
    
    def __repr__(self):
        return f"UnaryOp({self.op}{self.expr})"

class AssignNode(ASTNode):
    """Asignación: var = expr"""
    def __init__(self, var_name, expr):
        super().__init__()
        self.var_name = var_name
        self.expr = expr  # ExprNode
    
    def __repr__(self):
        return f"Assign({self.var_name} = {self.expr})"

class VarNode(ASTNode):
    """Variable: x"""
    def __init__(self, var_name):
        super().__init__()
        self.var_name = var_name
        self.expr_type = None
    
    def __repr__(self):
        return f"Var({self.var_name})"

class NumNode(ASTNode):
    """Número literal: 42, 3.14"""
    def __init__(self, value):
        super().__init__()
        self.value = value
        # Determinar tipo
        if '.' in str(value):
            self.expr_type = 'float'
        else:
            self.expr_type = 'int'
        self.is_dummy = False  # Flag para expresiones dummy
    
    def __repr__(self):
        return f"Num({self.value})"

class EmptyExprNode(ASTNode):
    """Expresión vacía (para for loops vacíos, etc.)"""
    def __init__(self):
        super().__init__()
        self.expr_type = 'void'
    
    def __repr__(self):
        return "EmptyExpr()"

class FuncCallNode(ASTNode):
    """Llamada a función: func(arg1, arg2)"""
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.args = args  # Lista de ExprNode
        self.expr_type = None
    
    def __repr__(self):
        return f"FuncCall({self.func_name}, {len(self.args)} args)"