from enum import Enum, auto

class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    EQUAL = auto()

    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()

    IDENTIFIER = auto()
    NUMBER = auto()

    LET = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    DEF = auto()
    RETURN = auto()

    EOF = auto()
    INVALID = auto()

    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    STRING = auto()
    SEMICOLON = auto()
