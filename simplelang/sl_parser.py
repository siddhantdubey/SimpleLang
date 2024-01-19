from simplelang.tokens import TokenType

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

class ArrayNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"ArrayNode({self.elements})"

class ArrayIndexNode:
    def __init__(self, array_identifier, index):
        self.array_identifier = array_identifier
        self.index = index
    
    def __repr__(self):
        return f"ArrayIndexNode({self.array_identifier}, {self.index})"

class PrintNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PrintNode({self.value})"

class ForNode:
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body
    
    def __repr__(self):
        return f"ForNode({self.variable}, {self.start}, {self.end}, {self.body})"

class FunctionNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionNode({self.name}, {self.parameters}, {self.body})"

class ReturnNode:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"ReturnNode({self.value})"
    
class FunctionCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCallNode({self.name}, {self.arguments})"

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

    def peek(self):
        peek_pos = self.pos + 1
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else None
    
    def parse(self):
        """ Parse the entire program and return a list of nodes. """
        nodes = []
        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            else:
                nodes.append(self.parse_statement())
        return nodes
    
    def parse_function_call(self):
        name = self.current_token.value
        self.advance()
        arguments = self.parse_arguments()
        return FunctionCallNode(name, arguments)

    def parse_arguments(self):
        arguments = []
        if self.current_token.type != TokenType.LPAREN:
            raise Exception("Expected '(' after function name")
        self.advance()

        while self.current_token is not None and self.current_token.type != TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current_token.type == TokenType.COMMA:
                self.advance()

        if self.current_token is None or self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected ')' after arguments")
        self.advance()

        return arguments

    def parse_statement(self):
        if self.current_token.type == TokenType.IDENTIFIER and self.peek().type == TokenType.LPAREN:
            return self.parse_function_call()
        elif self.current_token.type == TokenType.LBRACKET:
            return self.parse_array()
        elif self.current_token.type == TokenType.IDENTIFIER and self.peek().type == TokenType.LBRACKET:
            return self.parse_array_index()
        elif self.current_token.type == TokenType.LET:
            return self.parse_var_decl()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if()
        elif self.current_token.type == TokenType.ELSE:
            return self.parse_else()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for()
        elif self.current_token.type == TokenType.DEF:
            return self.parse_def()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        else:
            return self.parse_logical_op()

    def parse_array(self):
        self.advance()
        elements = self.parse_array_elements()
        if self.current_token.type != TokenType.RBRACKET:
            raise Exception("Expected ']' after array elements")
        self.advance()
        return ArrayNode(elements)
    
    def parse_array_elements(self):
        elements = []
        while self.current_token is not None and self.current_token.type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            if self.current_token.type == TokenType.COMMA:
                self.advance()
        return elements

    def parse_var_decl(self):
        self.advance()
        var_name = self.current_token.value
        self.advance()
        self.advance()
        value = self.parse_expression()
        return VarDeclNode(var_name, value)
    
    def parse_print(self):
        self.advance()
        if self.current_token.type == TokenType.IDENTIFIER and self.peek().type == TokenType.LBRACKET:
            value = self.parse_array_index()
        else:
            value = self.parse_expression()
        return PrintNode(value)

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
    
    def parse_for(self):
        self.advance()
        variable = self.current_token.value
        self.advance()
        self.advance()
        start = self.parse_expression()
        self.advance()
        end = self.parse_expression()
        body = self.parse_block()
        return ForNode(variable, start, end, body)

    def parse_def(self):
        self.advance()
        name = self.current_token.value
        self.advance()
        parameters = self.parse_parameters()
        body = self.parse_block()
        return FunctionNode(name, parameters, body)
    
    def parse_array_index(self):
        array_identifier = self.current_token.value
        self.advance()
        self.advance()
        index = self.parse_expression()
        if self.current_token.type != TokenType.RBRACKET:
            raise Exception("Expected ']' after array index")
        self.advance()
        return ArrayIndexNode(array_identifier, index)

    def parse_parameters(self):
        parameters = []
        if self.current_token.type != TokenType.LPAREN:
            raise Exception("Expected '(' after function name")
        self.advance()

        while self.current_token is not None and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.IDENTIFIER:
                parameters.append(self.current_token.value)
                self.advance()
            if self.current_token.type == TokenType.COMMA:
                self.advance()

        if self.current_token is None or self.current_token.type != TokenType.RPAREN:
            raise Exception("Expected ')' after parameters")
        self.advance()

        return parameters
    def parse_return(self):
        self.advance()
        value = self.parse_expression()
        return ReturnNode(value)


    def parse_block(self):
        if self.current_token.type != TokenType.LBRACE:
            raise Exception("Expected '{' at the start of a block")
        self.advance()
        body = []
        while self.current_token is not None and self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.SEMICOLON:
                self.advance() 
            else:
                body.append(self.parse_statement())
        if self.current_token is None or self.current_token.type != TokenType.RBRACE:
            raise Exception("Expected '}' at the end of a block")
        self.advance()
        return body

    def parse_atom(self):
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.advance()
            return int(token.value)
        elif token.type == TokenType.STRING:
            self.advance()
            return str(token.value)
        elif token.type == TokenType.IDENTIFIER:
            if self.peek().type == TokenType.LPAREN:
                return self.parse_function_call()
            elif self.peek().type == TokenType.LBRACKET:  # Added condition to handle array indexing
                return self.parse_array_index()
            self.advance()
            return token.value
        elif token.type == TokenType.LPAREN:
            self.advance()
            result = self.parse_logical_op()
            if self.current_token.type != TokenType.RPAREN:
                raise Exception("Missing closing parenthesis")
            self.advance()
            return result
        elif self.current_token.type == TokenType.LBRACKET:
            self.advance()
            elements = self.parse_array_elements()
            if self.current_token.type != TokenType.RBRACKET:
                raise Exception("Expected ']' after array elements")
            self.advance()
            return ArrayNode(elements)


    def parse_binary_op(self, func, ops):
        left = func()
        while self.current_token is not None and self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right = func()
            left = BinaryOpNode(left, op, right)
        return left