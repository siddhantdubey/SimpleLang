from simplelang.lexer import TokenType, Lexer
from simplelang.sl_parser import Parser, ReturnNode

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}
        self.functions = {}
        self.return_value = None

    def visit_FunctionNode(self, node):
        self.functions[node.name] = node
    
    def visit_ReturnNode(self, node):
        self.return_value = self.visit(node.value)

    def visit_FunctionCallNode(self, node):
        function = self.functions.get(node.name)
        if function is None:
            raise Exception(f"Undefined function: {node.name}")
        if len(node.arguments) != len(function.parameters):
            raise Exception(f"Argument mismatch for function: {node.name}")
        for param, arg in zip(function.parameters, node.arguments):
            self.variables[param] = self.visit(arg)
        for statement in function.body:
            self.visit(statement)
            if isinstance(statement, ReturnNode):
                break
        return_value = self.return_value
        self.return_value = None
        return return_value

    def visit_VarDeclNode(self, node):
        self.variables[node.var_name] = self.visit(node.value)

    def visit_BinaryOpNode(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            right = self.visit(node.right)
            if right == 0:
                raise Exception("Division by zero")
            return self.visit(node.left) / right
        elif node.op.type == TokenType.GREATER:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left > right
        elif node.op.type == TokenType.LESS:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left < right
        elif node.op.type == TokenType.EQUAL_EQUAL:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left == right
        elif node.op.type == TokenType.NOT_EQUAL:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left != right
        elif node.op.type == TokenType.GREATER_EQUAL:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left >= right
        elif node.op.type == TokenType.LESS_EQUAL:
            right = self.visit(node.right)
            left = self.visit(node.left)
            return left <= right
 
    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)
    
    def visit_WhileNode(self, node):
        while self.visit(node.condition):
            for statement in node.body:
                self.visit(statement)

    def visit_ForNode(self, node):
        start = self.visit(node.start)
        end = self.visit(node.end)
        self.variables[node.variable] = start
        while self.variables[node.variable] < end:
            for statement in node.body:
                self.visit(statement)
            self.variables[node.variable] += 1
    
    def visit_IfNode(self, node):
        if self.visit(node.condition):
            for statement in node.body:
                self.visit(statement)
    
    def visit_ElseNode(self, node):
        for statement in node.body:
            self.visit(statement)
    
    def visit_LogicalOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.type == TokenType.AND:
            return left and right
        elif node.op.type == TokenType.OR:
            return left or right

    def visit(self, node):
        if isinstance(node, int):
            return node
        elif isinstance(node, str):
            if node in self.variables:
                return self.variables[node]
            return node
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def visit_int(self, node):
        return node
        
    def visit_str(self, node):
        if node in self.variables:
            return self.variables[node]
        raise Exception(f"Undefined variable: {node}")

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def interpret(self):
        tree = self.parser.parse()
        for node in tree:
            self.visit(node)

text = 'let x = 15; print(x); while (x > 10) {print(x); let x = x - 1;}'
text1 = 'print(1 != 2);'
text_for = 'for x = 1 to 10 {print(x);}'

lexer = Lexer(text_for)
tokens = []
while True:
    token = lexer.get_next_token()
    if token.type == TokenType.EOF:
        break
    tokens.append(token)
parser = Parser(tokens)
interpreter = Interpreter(parser)
interpreter.interpret()
text = '''
def add(x, y) {
    return x + y;
}

let result = add(10, 20);
print(result);
'''
lexer = Lexer(text)
tokens = []
while True:
    token = lexer.get_next_token()
    if token.type == TokenType.EOF:
        break
    tokens.append(token)
parser = Parser(tokens)
interpreter = Interpreter(parser)
interpreter.interpret()