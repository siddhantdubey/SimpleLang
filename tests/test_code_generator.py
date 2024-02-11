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
    arm_generator = ARMGenerator()
    arm_code = arm_generator.generate_arm(nodes)
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
    arm_generator = ARMGenerator()
    arm_code = arm_generator.generate_arm(nodes)
    expected_code = [
        'MOV R1, #10',  # Load 5 into R1
        'MOV R2, #5',  # Load 2 into R2
        'MOV R3, #2',  # Load 10 into R4
        'MUL R4, R2, R3',  # Multiply R1 and R2, result in R3
        'ADD R5, R1, R4',  # Add R4 and R3, result in R0 for variable result
    ]
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
    arm_generator = ARMGenerator()
    arm_code = arm_generator.generate_arm(nodes)
    expected_code = [
        'MOV R1, #10',  # Load 5 into R1
        'MOV R2, #5',  # Load 10 into R2
        'MOV R3, R1',  # Load 10 into R3 (inefficient)
        'MOV R4, R2',  # Load 5 into R4 (inefficient)
        'ADD R5, R3, R4',  # Add R1 and R2, result in R0 for variable a
    ]
    assert arm_code == expected_code, f"Expected {expected_code}, got {arm_code}"
