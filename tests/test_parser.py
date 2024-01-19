import unittest
from simplelang.lexer import Lexer, TokenType, Token
from simplelang.sl_parser import Parser, VarDeclNode, BinaryOpNode, IfNode, ElseNode, WhileNode, PrintNode, FunctionNode, ReturnNode, FunctionCallNode, ArrayNode, ArrayIndexNode

class TestParser(unittest.TestCase):
    def test_if_statement(self):
        text = 'if (x > 10) {let x = 9;}'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, IfNode)
        self.assertIsInstance(node.condition, BinaryOpNode)
        self.assertEqual(node.condition.left, 'x')
        self.assertEqual(node.condition.op.type, TokenType.GREATER)
        self.assertEqual(node.condition.right, 10)
        self.assertIsInstance(node.body[0], VarDeclNode)
        self.assertEqual(node.body[0].var_name, 'x')
        self.assertEqual(node.body[0].value, 9)

    def test_print_statement(self):
        text = 'print(10);'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, PrintNode)
        self.assertEqual(node.value, 10)

    def test_else_statement(self):
        text = 'else {let x = 11;}'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, ElseNode)
        self.assertIsInstance(node.body[0], VarDeclNode)
        self.assertEqual(node.body[0].var_name, 'x')
        self.assertEqual(node.body[0].value, 11)
    
    def test_parse_string(self):
        text = '"Hello"'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        self.assertEqual(node[0], 'Hello')

    def test_parse_function(self):
        text = 'def add(x, y) { return x + y; }'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, FunctionNode)
        self.assertEqual(node.name, 'add')
        self.assertEqual(node.parameters, ['x', 'y'])
        self.assertIsInstance(node.body[0], ReturnNode)
        self.assertIsInstance(node.body[0].value, BinaryOpNode)
        self.assertEqual(node.body[0].value.left, 'x')
        self.assertEqual(node.body[0].value.op.type, TokenType.PLUS)
        self.assertEqual(node.body[0].value.right, 'y')

    def test_function_call(self):
        text = 'add(1, 2);'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, FunctionCallNode)
        self.assertEqual(node.name, 'add')
        self.assertEqual(node.arguments, [1, 2])

    def test_function_call_with_variable(self):
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
        nodes = parser.parse()
        self.assertIsInstance(nodes[0], FunctionNode)
        self.assertEqual(nodes[0].name, 'add')
        self.assertEqual(nodes[0].parameters, ['x', 'y'])
        self.assertIsInstance(nodes[0].body[0], ReturnNode)
        self.assertIsInstance(nodes[0].body[0].value, BinaryOpNode)
        self.assertEqual(nodes[0].body[0].value.left, 'x')
        self.assertEqual(nodes[0].body[0].value.op.type, TokenType.PLUS)
        self.assertEqual(nodes[0].body[0].value.right, 'y')
        self.assertIsInstance(nodes[1], VarDeclNode)
        self.assertEqual(nodes[1].var_name, 'result')
        self.assertIsInstance(nodes[1].value, FunctionCallNode)
        self.assertEqual(nodes[1].value.name, 'add')
        self.assertEqual(nodes[1].value.arguments, [10, 20])
        self.assertIsInstance(nodes[2], PrintNode)
        self.assertEqual(nodes[2].value, 'result')

    def test_while_loop(self):
        text = 'while (x > 10) {let x = 9;}'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, WhileNode)
        self.assertIsInstance(node.condition, BinaryOpNode)
        self.assertEqual(node.condition.left, 'x')
        self.assertEqual(node.condition.op.type, TokenType.GREATER)
        self.assertEqual(node.condition.right, 10)
        self.assertIsInstance(node.body[0], VarDeclNode)
        self.assertEqual(node.body[0].var_name, 'x')
        self.assertEqual(node.body[0].value, 9)

    def test_array(self):
        text = 'let a = [1, 2, 3];'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, VarDeclNode)
        self.assertEqual(node.var_name, 'a')
        self.assertIsInstance(node.value, ArrayNode)
        self.assertEqual(node.value.elements, [1, 2, 3])

    def test_array_index(self):
        text = 'let a = [1, 2, 3]; print(a[0]);'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        nodes = parser.parse()
        node = nodes[0]
        self.assertIsInstance(node, VarDeclNode)
        self.assertEqual(node.var_name, 'a')
        self.assertIsInstance(node.value, ArrayNode)
        self.assertEqual(node.value.elements, [1, 2, 3])
        node = nodes[1]
        self.assertIsInstance(node, PrintNode)
        self.assertIsInstance(node.value, ArrayIndexNode)            

    def test_variable_declaration(self):
        text = 'let x = 10;'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        node = node[0]
        self.assertIsInstance(node, VarDeclNode)
        self.assertEqual(node.var_name, 'x')
        self.assertEqual(node.value, 10)
    
    def test_binary_operation(self):
        test_cases = [
            ("10 + 5;", TokenType.PLUS),
            ("10 - 5;", TokenType.MINUS),
            ("10 * 5;", TokenType.MUL),
            ("10 / 5;", TokenType.DIV),
            ("x == y;", TokenType.EQUAL_EQUAL),
            ("x != y;", TokenType.NOT_EQUAL),
            ("x && y;", TokenType.AND),
            ("x || y;", TokenType.OR)
        ]
        for text, op_type in test_cases:
            with self.subTest(text=text):
                lexer = Lexer(text)
                tokens = []
                while True:
                    token = lexer.get_next_token()
                    if token.type == TokenType.EOF:
                        break
                    tokens.append(token)
                parser = Parser(tokens)
                node = parser.parse()
                node = node[0]
                print(node)
                self.assertIsInstance(node, BinaryOpNode)
                self.assertEqual(node.op.type, op_type)
                if type(node.left) == int:
                    self.assertEqual(node.left, int(text.split()[0]))
                    self.assertEqual(node.right, int(text.split()[2][:-1]))
                else:
                    self.assertEqual(node.left, text.split()[0])
                    self.assertEqual(node.right, text.split()[2][:-1])

    def test_sequence_of_statements(self):
        text = 'let x = 10; let y = 20;'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        parser = Parser(tokens)
        node = parser.parse()
        self.assertIsInstance(node[0], VarDeclNode)
        self.assertEqual(node[0].var_name, 'x')
        self.assertEqual(node[0].value, 10)
        self.assertIsInstance(node[1], VarDeclNode)
        self.assertEqual(node[1].var_name, 'y')
        self.assertEqual(node[1].value, 20)

if __name__ == '__main__':
    unittest.main()
