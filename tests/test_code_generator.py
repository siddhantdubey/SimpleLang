from simplelang.compiler.code_generator import ARMGenerator
from simplelang.lexer import Lexer, TokenType
from simplelang.sl_parser import Parser

def test_generate_arm_basic_assignment():
    program_text = '''
    let x = 15;
    '''
    lexer = Lexer(program_text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        tokens.append(token)
    parser = Parser(tokens)
    nodes = parser.parse()
    arm_generator = ARMGenerator(nodes)
    arm_code = arm_generator.generate_arm()
    expected_code = [
        'MOV R1, #15', 
    ]
    assert arm_code == expected_code, f"Expected {expected_code}, got {arm_code}"

def test_generate_arm_complex_expression():
    program_text = '''
    let result = 10 + (5 * 2);
    '''
    lexer = Lexer(program_text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        tokens.append(token)
    parser = Parser(tokens)
    nodes = parser.parse()
    arm_generator = ARMGenerator(nodes)
    arm_code = arm_generator.generate_arm()
    expected_code = ['MOV R1, #5', 'MOV R2, #2', 'MUL R3, R1, R2', 'MOV R4, #10', 'ADD R5, R4, R3', 'MOV R6, #t0']
    assert arm_code == expected_code, f"Expected {expected_code}, got {arm_code}"

def test_variable_bin_op():
    program_text = '''
let x = 10;
let y = 5;
let a = x + y;
'''
    lexer = Lexer(program_text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        tokens.append(token)
    parser = Parser(tokens)
    nodes = parser.parse()
    arm_generator = ARMGenerator(nodes)
    arm_code = arm_generator.generate_arm()
    expected_code = ['MOV R1, #10', 'MOV R2, #5', 'ADD R3, R1, R2', 'MOV R4, #t0']
    assert arm_code == expected_code, f"Expected {expected_code}, got {arm_code}"