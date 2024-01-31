import unittest
from simplelang.compiler.tac import TAC
from simplelang.sl_parser import BinaryOpNode, VarDeclNode, ForNode, WhileNode, PrintNode, ElseNode, IfNode

class TestTAC(unittest.TestCase):
    def test_init(self):
        tac = TAC()
        self.assertEqual(tac.code, [])
        self.assertEqual(tac.temp_counter, 0)

    def test_emit(self):
        tac = TAC()
        tac.emit('+', 'a', 'b', 'c')
        self.assertEqual(len(tac.code), 1)
        self.assertEqual(tac.code[0], ('+', 'a', 'b', 'c'))

    def test_str(self):
        tac = TAC()
        tac.emit('+', 'a', 'b', 'c')
        self.assertEqual(str(tac), "c = a + b\n")

    def test_gen_temp(self):
        tac = TAC()
        self.assertEqual(tac.gen_temp(), 't0')
        self.assertEqual(tac.gen_temp(), 't1')

    def test_VarDeclNode(self):
        tac = TAC()
        node = VarDeclNode('a', 1)
        tac.generate_tac(node)
        print(tac.code)
        self.assertEqual(str(tac), "a = 1\n")

    def test_BinaryOpNode(self):
        tac = TAC()
        node = BinaryOpNode(1, '+', 2)
        tac.generate_tac(node)
        self.assertEqual(str(tac), "t0 = 1 + 2\n")

    def test_WhileNode(self):
        tac = TAC()
        node = WhileNode(BinaryOpNode('i', '<', 3), [VarDeclNode('i', BinaryOpNode('i', '+', 1))])
        tac.generate_tac(node)
        print(tac.code)
        print(str(tac))
        expected_ir_str ="""l0:
t0 = i < 3
if_not t0 goto l1
t1 = i + 1
i = t1
goto l0
l1:
"""
        self.assertEqual(tac.code[0], ('label', None, None, 'l0'))
        self.assertEqual(tac.code[1], ('<', 'i', 3, 't0'))
        self.assertEqual(tac.code[2], ('ifFalse', 't0', None, 'l1'))
        self.assertEqual(tac.code[3], ('+', 'i', 1, 't1'))
        self.assertEqual(tac.code[4], ('=', 't1', None, 'i'))
        self.assertEqual(tac.code[5], ('goto', None, None, 'l0'))
        self.assertEqual(tac.code[6], ('label', None, None, 'l1'))
        self.assertEqual(str(tac), expected_ir_str)

    def test_PrintNode(self):
        tac = TAC()
        node = PrintNode('a')
        tac.generate_tac(node)
        self.assertEqual(str(tac), "print a\n")

    def test_ForNode(self):
        tac = TAC()
        node = ForNode('i', 1, 10, [PrintNode('i')])
        tac.generate_tac(node)
        expected_ir_str = """i = 1
l0:
t0 = i < 10
if_not t0 goto l1
print i
t1 = i + 1
i = t1
goto l0
l1:
"""
        self.assertEqual(tac.code[0], ('=', 1, None, 'i'))
        self.assertEqual(tac.code[1], ('label', None, None, 'l0'))
        self.assertEqual(tac.code[2], ('<', 'i', 10, 't0'))
        self.assertEqual(tac.code[3], ('ifFalse', 't0', None, 'l1'))
        self.assertEqual(tac.code[4], ('print', 'i', None, None))
        self.assertEqual(tac.code[5], ('+', 'i', 1, 't1'))
        self.assertEqual(tac.code[6], ('=', 't1', None, 'i'))
        self.assertEqual(tac.code[7], ('goto', None, None, 'l0'))
        self.assertEqual(tac.code[8], ('label', None, None, 'l1'))
        self.assertEqual(str(tac), expected_ir_str)

    def test_ElseNode(self):
        tac = TAC()
        node = ElseNode([PrintNode('i')])
        tac.generate_tac(node)
        expected_ir_str = """l0:
print i
"""
        self.assertEqual(tac.code[0], ('label', None, None, 'l0'))
        self.assertEqual(tac.code[1], ('print', 'i', None, None))
        self.assertEqual(str(tac), expected_ir_str)

    def test_IfNode(self):
        tac = TAC()
        node = IfNode(BinaryOpNode('i', '<', 3), [PrintNode('i')])
        tac.generate_tac(node)
        print(str(tac))
        self.assertEqual(tac.code[0], ('label', None, None, 'l0'))
        self.assertEqual(tac.code[1], ('<', 'i', 3, 't0'))
        self.assertEqual(tac.code[2], ('ifFalse', 't0', None, 'l1'))
        self.assertEqual(tac.code[3], ('print', 'i', None, None))
        self.assertEqual(tac.code[4], ('goto', None, None, 'l2'))
        self.assertEqual(tac.code[5], ('label', None, None, 'l1'))
        self.assertEqual(tac.code[6], ('label', None, None, 'l2'))

    def test_IfWithElseNode(self):
        tac = TAC()
        node = IfNode(BinaryOpNode('i', '<', 3), [PrintNode('i')], ElseNode([PrintNode(2)]))
        tac.generate_tac(node)
        print(str(tac))
        self.assertEqual(tac.code[0], ('label', None, None, 'l0'))
        self.assertEqual(tac.code[1], ('<', 'i', 3, 't0'))
        self.assertEqual(tac.code[2], ('ifFalse', 't0', None, 'l1'))
        self.assertEqual(tac.code[3], ('print', 'i', None, None))
        self.assertEqual(tac.code[4], ('goto', None, None, 'l2'))
        self.assertEqual(tac.code[5], ('label', None, None, 'l1'))
        self.assertEqual(tac.code[6], ('print', 2, None, None))
        self.assertEqual(tac.code[7], ('label', None, None, 'l2'))


if __name__ == '__main__':
    unittest.main()