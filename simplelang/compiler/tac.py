from simplelang.sl_parser import BinaryOpNode, VarDeclNode, ForNode, WhileNode, PrintNode, ElseNode, IfNode

class TAC:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def emit(self, op, arg1=None, arg2=None, result=None):
        self.code.append((op, arg1, arg2, result))
        
    def gen_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def gen_label(self):
        label = f"l{self.label_counter}"
        self.label_counter += 1
        return label
    
    def generate_tac(self, node):
        if isinstance(node, VarDeclNode):
            value = self.generate_tac(node.value)
            self.emit('=', value, None, node.var_name)

        elif isinstance(node, BinaryOpNode):
            temp = self.gen_temp()
            self.generate_tac(node.left)
            self.generate_tac(node.right)
            self.emit(node.op, node.left, node.right, temp)
            return temp

        elif isinstance(node, WhileNode):
            l1 = self.gen_label()
            l2 = self.gen_label()
            self.emit('label', None, None, l1)
            result = self.generate_tac(node.condition)
            self.emit('ifFalse', result, None, l2)
            for n in node.body:
                print(n)
                self.generate_tac(n)
            self.emit('goto', None, None, l1)
            self.emit('label', None, None, l2)

        elif isinstance(node, PrintNode):
            value = self.generate_tac(node.value)
            self.emit('print', value, None, None)

        elif isinstance(node, ForNode):
            l1 = self.gen_label()
            l2 = self.gen_label()
            start = self.generate_tac(node.start)
            self.emit('=', start, None, node.variable)
            self.emit('label', None, None, l1)
            result = self.generate_tac(BinaryOpNode(node.variable, '<', node.end))
            self.emit('ifFalse', result, None, l2)
            for n in node.body:
                self.generate_tac(n)
            temp = self.gen_temp()
            self.emit('+', node.variable, 1, temp)
            self.emit('=', temp, None, node.variable)
            self.emit('goto', None, None, l1)
            self.emit('label', None, None, l2)

        elif isinstance(node, int):
            return node
        
        elif isinstance(node, str):
            return node
        
        elif isinstance(node, ElseNode):
            l1 = self.gen_label()
            self.emit('label', None, None, l1)
            for n in node.body:
                self.generate_tac(n)

        elif isinstance(node, IfNode):
            """
            if (i < 3) {
                print(i);
            } else {
                print(2);
            }
            becomes
            IfNode(BinaryOpNode('i', '<', 3), [PrintNode('i')], ElseNode([PrintNode(2)]))
            becomes
            l0:
            t0 = i < 3
            if_not t0 goto l1
            print i
            goto l2
            l1:
            print 2
            l2:
            """
            l1 = self.gen_label()
            l2 = self.gen_label()
            l3 = self.gen_label()
            self.emit('label', None, None, l1)
            result = self.generate_tac(node.condition)
            self.emit('ifFalse', result, None, l2)
            for n in node.body:
                self.generate_tac(n)
            self.emit('goto', None, None, l3)
            self.emit('label', None, None, l2)
            else_node = node.else_node
            if else_node:
                for n in else_node.body:
                    self.generate_tac(n)
            self.emit('label', None, None, l3)
        
    def __str__(self):
        tac_str = ""
        for (op, arg1, arg2, result) in self.code:
            if op in ['+', '-', '/', '*', '<', '>', '<=', '>=', '==', '!=']:
                tac_str += f"{result} = {arg1} {op} {arg2}\n"
            elif op == '=':
                tac_str += f"{result} = {arg1}\n"
            elif op == 'label':
                tac_str += f"{result}:\n"
            elif op == 'ifFalse':
                tac_str += f"if_not {arg1} goto {result}\n"
            elif op == 'goto':
                tac_str += f"goto {result}\n"
            elif op == 'print':
                tac_str += f"print {arg1}\n"
        return tac_str
