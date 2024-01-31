import unittest
from simplelang.lexer import Lexer, TokenType
from simplelang.sl_parser import Parser
from simplelang.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def test_if_statement(self):
        text = 'let x = 11; if (x > 10) {let x = 9;}'
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
        self.assertEqual(interpreter.variables['x'], 9)

    def test_if_else_statement(self):
        text = 'let x = 8; if (x > 10) {let x = 9;} else {let x = 10;}'
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
        self.assertEqual(interpreter.variables['x'], 10)

    def test_function_call(self):
        text = '''
        def add(x, y) {
            let a = x + y;
            return a;
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
        self.assertEqual(interpreter.variables['result'], 30)

    def test_function_calling_other_function(self):
        text = '''
        def add(x, y) {
            return x + y;
        }
        def add_2(x) {
            return add(x, 2);
        }
        let result = add_2(10);
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
        self.assertEqual(interpreter.variables['result'], 12)

    def test_recursive_function(self):
        text = '''
        def factorial(x) {
            if (x == 0) {
                return 1;
            }
            return x * factorial(x - 1);
        }

        let result = factorial(5);
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
        self.assertEqual(interpreter.variables['result'], 120)