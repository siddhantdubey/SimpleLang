import re
from simplelang.tokens import TokenType

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON)

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())

            if self.current_char == '"':
                return Token(TokenType.STRING, self.string())

            if self.current_char.isalpha() or self.current_char == '_':
                ident = self.identifier()
                keyword_token = self.check_keyword(ident)
                if keyword_token:
                    return keyword_token
                return Token(TokenType.IDENTIFIER, ident)

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA)

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQUAL_EQUAL)
                self.advance()
                return Token(TokenType.EQUAL)

            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.NOT_EQUAL)
                self.advance()
                return Token(TokenType.NOT)

            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LESS_EQUAL)
                self.advance()
                return Token(TokenType.LESS)

            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL)
                self.advance()
                return Token(TokenType.GREATER)

            if self.current_char == '&':
                if self.peek() == '&':
                    self.advance()
                    self.advance()
                    return Token(TokenType.AND)

            if self.current_char == '|':
                if self.peek() == '|':
                    self.advance()
                    self.advance()
                    return Token(TokenType.OR)

            self.advance()
            return Token(TokenType.INVALID)
        return Token(TokenType.EOF)

    def check_keyword(self, ident):
        keywords = {
            'let': TokenType.LET,
            'print': TokenType.PRINT,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'def': TokenType.DEF,
            'return': TokenType.RETURN
        }
        return Token(keywords.get(ident)) if ident in keywords else None
