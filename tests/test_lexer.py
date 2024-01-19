import unittest
from simplelang.lexer import Lexer
from simplelang.tokens import TokenType

class TestLexer(unittest.TestCase):
    def test_peek_empty(self):
        text = ''
        lexer = Lexer(text)
        self.assertEqual(lexer.peek(), None)

    def test_comma_lex(self):
        text = ','
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.COMMA)

    def test_not_lex(self):
        text = '!'
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.NOT)

    def test_less_lex(self):
        text = '<'
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.LESS)
    
    def test_less_equal_lex(self):
        text = '<='
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.LESS_EQUAL)

    def test_greater_equal_lex(self):
        text = '>='
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.GREATER_EQUAL)

    def test_empty_program(self):
        text = ''
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.EOF)

    def test_whitespace(self):
        text = '    \n\t   '
        lexer = Lexer(text)
        token = lexer.get_next_token()
        self.assertEqual(token.type, TokenType.EOF)

    def test_single_token(self):
        text = 'let'
        lexer = Lexer(text)
        tokens = [lexer.get_next_token() for _ in range(2)]
        self.assertEqual(tokens[0].type, TokenType.LET)
        self.assertEqual(tokens[1].type, TokenType.EOF)

    def test_multiple_same_tokens(self):
        text = 'let let let'
        lexer = Lexer(text)
        tokens = [lexer.get_next_token() for _ in range(4)]
        self.assertEqual([t.type for t in tokens], [TokenType.LET, TokenType.LET, TokenType.LET, TokenType.EOF])

    def test_different_tokens(self):
        text = 'let x = 10'
        lexer = Lexer(text)
        tokens = [lexer.get_next_token() for _ in range(5)]
        self.assertEqual([t.type for t in tokens], [TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER, TokenType.EOF])

    def test_unexpected_token(self):
        text = '@'
        lexer = Lexer(text)
        self.assertEqual(lexer.get_next_token().type, TokenType.INVALID)

    def test_lex_array(self):
        text = '[1, 2, 3]'
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        self.assertEqual([t.type for t in tokens], [TokenType.LBRACKET, TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER, TokenType.COMMA, TokenType.NUMBER, TokenType.RBRACKET, TokenType.EOF])

    def test_simple_program(self):
        text = '''
        let x = 10;
        let y = "Hello";
        if (x > 5 && y == "Hello") {
            print(x);
        }
        '''
        lexer = Lexer(text)
        tokens = []
        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens = [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER, TokenType.SEMICOLON,
            TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.STRING, TokenType.SEMICOLON,
            TokenType.IF, TokenType.LPAREN, TokenType.IDENTIFIER, TokenType.GREATER, 
            TokenType.NUMBER, TokenType.AND, TokenType.IDENTIFIER, TokenType.EQUAL_EQUAL, 
            TokenType.STRING, TokenType.RPAREN, TokenType.LBRACE, TokenType.PRINT, 
            TokenType.LPAREN, TokenType.IDENTIFIER, TokenType.RPAREN, TokenType.SEMICOLON, TokenType.RBRACE, 
            TokenType.EOF
        ]

        self.assertEqual([t.type for t in tokens], expected_tokens)

if __name__ == '__main__':
    unittest.main()