"""Main module."""

from .common import parser, print_ast


def main():
    """
    Entry point of the application.

    It enters an infinite loop where it reads user input and tries to parse and evaluate it as a
    mathematical expression. If the input is valid, it prints the result.
    If the input is invalid, it prints an error message.

    The loop is exited when the user inputs 'exit' or 'quit' (case insensitive).

    :return: None
    """
    print("Digite expressões matemáticas. Use 'exit' para sair.")
    while True:
        try:
            expr = input("calc > ")
            if expr.lower() in ["exit", "quit"]:
                break

            result = parser.parse(expr)

            if result is not None:
                print("AST:", print_ast(result))
        except SyntaxError as e:
            print("Erro de sintaxe:", e)


if __name__ == "__main__":
    main()
