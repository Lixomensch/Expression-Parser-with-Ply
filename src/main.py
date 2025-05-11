"""Main module."""

import os

from .common import eval_ast, parser, print_ast


def process_file(file_path):
    """
    Reads a file and processes it as a whole block.

    :param file_path: The path to the file containing code.
    :return: None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            print("File is empty.")
            return

        try:
            asts = parser.parse(content)
            if isinstance(asts, list):
                for ast in asts:
                    if ast is not None:
                        print("AST:", print_ast(ast))
            else:
                if asts is not None:
                    print("AST:", print_ast(asts))
                    eval_ast(asts)
        except SyntaxError as e:
            print(f"Syntax error: {e}")
        except ValueError as e:
            print(f"Value error: {e}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")


def process_input(input_line):
    """
    Process a single input line directly (for interactive input).

    :param input_line: The input expression to be processed.
    :return: None
    """
    try:
        ast = parser.parse(input_line.strip())
        if ast is not None:
            print("AST:", print_ast(ast))
            result = eval_ast(ast)
            print("Result:", result)
    except SyntaxError as e:
        print(f"Syntax error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")


def main():
    """
    Entry point of the application.

    The program will either process user input interactively or from a file,
    depending on what the user provides.
    """
    print("Enter 'exit' to quit.")
    while True:
        input_line = input("cmd > ").strip()

        if input_line.lower() == "exit":
            print("Exiting the program.")
            break

        if os.path.isfile(input_line):
            print(f"Processing file: {input_line}")
            process_file(input_line)

        else:
            print(f"Processing expression: {input_line}")
            process_input(input_line)


if __name__ == "__main__":
    main()
