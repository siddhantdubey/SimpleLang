from simplelang.compiler.tac import TAC
from simplelang.sl_parser import VarDeclNode, BinaryOpNode
from simplelang.lexer import TokenType

class ARMGenerator:
    def __init__(self):
        self.tac = TAC()
        self.assembly_code = []
        self.reg_counter = 1
        self.var_to_reg = {}

    def generate_arm(self, nodes):
        for node in nodes:
            self._generate_node(node)
        return self.assembly_code

    def _generate_node(self, node):
        if isinstance(node, VarDeclNode):
            self._generate_node(node.value)
            self.var_to_reg[node.var_name] = self.reg_counter - 1
        elif isinstance(node, BinaryOpNode):
            self._generate_node(node.left)
            left_reg = self.reg_counter - 1
            self._generate_node(node.right)
            right_reg = self.reg_counter - 1
            if node.op.type == TokenType.PLUS:
                self.assembly_code.append(f'ADD R{self.reg_counter}, R{left_reg}, R{right_reg}')
            elif node.op.type == TokenType.MINUS:
                self.assembly_code.append(f'SUB R{self.reg_counter}, R{left_reg}, R{right_reg}')
            elif node.op.type == TokenType.MUL:
                self.assembly_code.append(f'MUL R{self.reg_counter}, R{left_reg}, R{right_reg}')
            elif node.op.type == TokenType.DIV:
                self.assembly_code.append(f'DIV R{self.reg_counter}, R{left_reg}, R{right_reg}')
            self.reg_counter += 1
        elif isinstance(node, str):
            if node in self.var_to_reg:
                self.assembly_code.append(f'MOV R{self.reg_counter}, R{self.var_to_reg[node]}')
                self.reg_counter += 1
        elif isinstance(node, int):
            self.assembly_code.append(f'MOV R{self.reg_counter}, #{node}')
            self.reg_counter += 1

