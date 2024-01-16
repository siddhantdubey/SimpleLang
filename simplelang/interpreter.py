from simplelang.lexer import TokenType, Lexer
from simplelang.sl_parser import Parser

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.variables = {}

    def visit_VarDeclNode(self, node):
        self.variables[node.var_name] = self.visit(node.value)

    def visit_BinaryOpNode(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        # Add other operations here...

    def visit_PrintNode(self, node):
        print(self.visit(node.value))

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def visit_int(self, node):
        return node
    
    def visit_str(self, node):
        return node

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def interpret(self):
        tree = self.parser.parse()
        for node in tree:
            self.visit(node)

text = 'let x = 10; let y = 20; print(x + y);'
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