from simplelang.lexer import Lexer, Token
from simplelang.tokens import TokenType

# Node Classes
class VarDeclNode:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"VarDeclNode({self.var_name}, {self.value})"

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.op}, {self.right})"

class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"IfNode({self.condition}, {self.body})"
    
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"

class ElseNode:
    def __init__(self, body):
        self.body = body
    
    def __repr__(self):
        return f"ElseNode({self.body})"

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        if self.current_token.type == TokenType.LET:
            return self.parse_var_decl()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.ELSE:
            return self.parse_else()
        elif self.current_token == TokenType.WHILE:
            return self.parse_while()
        else:
            return self.parse_logical_op()
        return None

    def parse_var_decl(self):
        self.advance()
        var_name = self.current_token.value
        self.advance()
        self.advance()
        value = self.parse_expression()
        return VarDeclNode(var_name, value)

    def parse_expression(self):
        return self.parse_binary_op(self.parse_factor, [TokenType.PLUS, TokenType.MINUS])

    def parse_factor(self):
        return self.parse_binary_op(self.parse_atom, [TokenType.MUL, TokenType.DIV])

    def parse_comparison(self):
        return self.parse_binary_op(self.parse_expression, [TokenType.GREATER, TokenType.LESS, TokenType.GREATER_EQUAL, TokenType.LESS_EQUAL, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL])

    def parse_logical_op(self):
        return self.parse_binary_op(self.parse_comparison, [TokenType.AND, TokenType.OR])
    
    def parse_if(self):
        self.advance()
        condition = self.parse_logical_op()
        body = self.parse_block()
        return IfNode(condition, body)

    def parse_else(self):
        self.advance()
        body = self.parse_block()
        return ElseNode(body)

    def parse_while(self):
        self.advance()
        condition = self.parse_logical_op()
        body = self.parse_block()
        return WhileNode(condition, body)
        
    def parse_block(self):
        if self.current_token.type == TokenType.LBRACE:
            self.advance()
            body = []
            while self.current_token.type != TokenType.RBRACE:
                statement = self.parse()
                body.append(statement)
                if self.current_token.type == TokenType.SEMICOLON:
                    self.advance() 
            self.advance() 
            return body
        else:
            statement = self.parse()
            if self.current_token.type == TokenType.SEMICOLON:
                self.advance() 
            return [statement]


    def parse_atom(self):
        token = self.current_token
        if token.type in (TokenType.NUMBER, TokenType.IDENTIFIER):
            self.advance()
            return token.value
        elif token.type == TokenType.LPAREN:
            self.advance()
            result = self.parse_logical_op()
            if self.current_token.type != TokenType.RPAREN:
                raise Exception("Missing closing parenthesis")
            self.advance()
            return result
        raise Exception(f"Invalid syntax at {token}")

    def parse_binary_op(self, func, ops):
        left = func()
        while self.current_token is not None and self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right = func()
            left = BinaryOpNode(left, op, right)
        return left