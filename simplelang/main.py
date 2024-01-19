import argparse
from simplelang.lexer import Lexer, TokenType
from simplelang.sl_parser import Parser
from simplelang.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path-to-source-code", type=str, required=True)
    args = parser.parse_args()

    with open(args.path_to_source_code, 'r') as file:
        text = file.read()

    lexer = Lexer(text)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type == TokenType.EOF:
            break
        tokens.append(token)

    parser = Parser(tokens)
    interpreter = Interpreter(parser)
    interpreter.interpret()

if __name__ == "__main__":
    main()