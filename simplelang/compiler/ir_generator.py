from simplelang.compiler.tac import TAC

class IRGenerator:
    def __init__(self):
        self.tac = TAC()
    
    def generate_ir(self, ast):
        for node in ast:
            self.tac.generate_tac(node)
        return self.tac.code