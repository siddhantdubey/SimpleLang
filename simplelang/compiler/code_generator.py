from simplelang.compiler.ir_generator import IRGenerator
from simplelang.sl_parser import VarDeclNode, BinaryOpNode, ForNode
from simplelang.lexer import TokenType, Token

class ARMGenerator:
    def __init__(self, ast):
        self.ir_generator = IRGenerator()
        self.ir = self.ir_generator.generate_ir(ast)
        self.assembly_code = []
        self.reg_counter = 1
        self.var_to_reg = {}
        self.op_to_arm = {
            TokenType.PLUS: 'ADD',
            TokenType.MINUS: 'SUB',
            TokenType.MUL: 'MUL',
            TokenType.DIV: 'DIV',
        }
        self.label_counter = 0

    def generate_arm(self):
        def handle_expression(expression):
            op = expression[0]
            if isinstance(op, Token) and op.type in [TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV]:
                arg1, arg2 = expression[1], expression[2]
                result = expression[3]
                if isinstance(arg1, BinaryOpNode):
                    handle_expression(arg1)
                    arg1 = self.var_to_reg[arg1[3]]
                elif arg1 in self.var_to_reg:
                    arg1 = self.var_to_reg[arg1]
                else:
                    self.assembly_code.append(f'MOV R{self.reg_counter}, #{arg1}')
                    self.var_to_reg[arg1] = f'R{self.reg_counter}'
                    self.reg_counter += 1
                    arg1 = self.var_to_reg[arg1]
                if isinstance(arg2, BinaryOpNode):
                    handle_expression(arg2)
                    arg2 = self.var_to_reg[arg2[3]]
                elif arg2 in self.var_to_reg:
                    arg2 = self.var_to_reg[arg2]
                else:
                    self.assembly_code.append(f'MOV R{self.reg_counter}, #{arg2}')
                    self.var_to_reg[arg2] = f'R{self.reg_counter}'
                    self.reg_counter += 1
                    arg2 = self.var_to_reg[arg2]
                if result not in self.var_to_reg:
                    self.var_to_reg[result] = f'R{self.reg_counter}'
                self.assembly_code.append(f'{self.op_to_arm[op.type]} {self.var_to_reg[result]}, {arg1}, {arg2}')
                self.reg_counter += 1

        for instruction in self.ir:
            if instruction[0] == '=':
                result = instruction[3]
                if result not in self.var_to_reg:
                    self.var_to_reg[result] = f'R{self.reg_counter}'
                    self.reg_counter += 1
                self.assembly_code.append(f'MOV {self.var_to_reg[result]}, #{instruction[1]}')
            else:
                handle_expression(instruction)
        return self.assembly_code
