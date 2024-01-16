import unittest
from simplelang.lexer import Lexer, TokenType, Token
from simplelang.sl_parser import Parser, VarDeclNode, BinaryOpNode, IfNode, ElseNode, WhileNode, PrintNode

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
