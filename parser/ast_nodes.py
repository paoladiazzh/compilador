class ASTNode:
    def __init__(self):
        self.line = 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class ProgramNode(ASTNode):
    def __init__(self, declarations):
        super().__init__()
        self.declarations = declarations
    
    def __repr__(self):
        return f"Program({len(self.declarations)} declarations)"

class VarDeclNode(ASTNode):
    def __init__(self, var_type, var_name, init_expr=None):
        super().__init__()
        self.var_type = var_type
        self.var_name = var_name
        self.init_expr = init_expr
    
    def __repr__(self):
        init = f", init={self.init_expr}" if self.init_expr else ""
        return f"VarDecl({self.var_type} {self.var_name}{init})"

class FuncDeclNode(ASTNode):
    def __init__(self, return_type, func_name, params, body):
        super().__init__()
        self.return_type = return_type
        self.func_name = func_name
        self.params = params
        self.body = body
    
    def __repr__(self):
        return f"FuncDecl({self.return_type} {self.func_name}, {len(self.params)} params)"

class ParamNode(ASTNode):
    def __init__(self, param_type, param_name):
        super().__init__()
        self.param_type = param_type
        self.param_name = param_name
    
    def __repr__(self):
        return f"Param({self.param_type} {self.param_name})"

class BlockNode(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"

class IfNode(ASTNode):
    def __init__(self, condition, then_stmt, else_stmt=None):
        super().__init__()
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
    
    def __repr__(self):
        return f"If(cond={self.condition})"

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"While(cond={self.condition})"

class ForNode(ASTNode):
    def __init__(self, init_expr, condition, update_expr, body):
        super().__init__()
        self.init_expr = init_expr
        self.condition = condition
        self.update_expr = update_expr
        self.body = body
    
    def __repr__(self):
        return f"For(init={self.init_expr}, cond={self.condition})"

class ReturnNode(ASTNode):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    
    def __repr__(self):
        return f"Return({self.expr})"

class PrintNode(ASTNode):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    
    def __repr__(self):
        return f"Print({self.expr})"

class ExprStmtNode(ASTNode):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    
    def __repr__(self):
        return f"ExprStmt({self.expr})"

class BinaryOpNode(ASTNode):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.expr_type = None
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class UnaryOpNode(ASTNode):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op
        self.expr = expr
        self.expr_type = None
    
    def __repr__(self):
        return f"UnaryOp({self.op}{self.expr})"

class AssignNode(ASTNode):
    def __init__(self, var_name, expr):
        super().__init__()
        self.var_name = var_name
        self.expr = expr
    
    def __repr__(self):
        return f"Assign({self.var_name} = {self.expr})"

class VarNode(ASTNode):
    def __init__(self, var_name):
        super().__init__()
        self.var_name = var_name
        self.expr_type = None
    
    def __repr__(self):
        return f"Var({self.var_name})"

class NumNode(ASTNode):
    def __init__(self, value):
        super().__init__()
        value_str = str(value)
        
        if '.' in value_str:
            self.value = float(value_str)
            self.expr_type = 'float'
        else:
            self.value = int(value_str)
            self.expr_type = 'int'
        
        self.is_dummy = False 
    
    def __repr__(self):
        return f"Num({self.value})"
    
    def get_numeric_value(self):
        return self.value

class EmptyExprNode(ASTNode):
    def __init__(self):
        super().__init__()
        self.expr_type = 'void'
    
    def __repr__(self):
        return "EmptyExpr()"

class FuncCallNode(ASTNode):
    def __init__(self, func_name, args):
        super().__init__()
        self.func_name = func_name
        self.args = args
        self.expr_type = None
    
    def __repr__(self):
        return f"FuncCall({self.func_name}, {len(self.args)} args)"