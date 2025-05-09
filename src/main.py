"""Main module."""

from .common import eval_ast, parser, print_ast


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
            line = input("calc > ")
            if line.strip() == "exit":
                break
            ast = parser.parse(line)
            if ast is not None:
                print("AST:", print_ast(ast))
                result = eval_ast(ast)
                print("Resultado:", result)
        except EOFError:
            break
        except SyntaxError as e:
            print(f"Erro de sintaxe: {e}")
        except ValueError as e:
            print(f"Erro de valor: {e}")


if __name__ == "__main__":
    main()
