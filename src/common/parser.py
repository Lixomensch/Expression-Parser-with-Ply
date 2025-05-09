"""Modulo parser."""

import math

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611

env = {}

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "POWER"),
    ("right", "UMINUS"),
)


def p_statement_expr(p):
    "statement : expression"
    p[0] = p[1]


def p_statement_assign(p):
    "statement : ID EQUALS expression"
    p[0] = ("assign", p[1], p[3])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_id(p):
    "expression : ID"
    p[0] = ("var", p[1])


def eval_ast(node):
    """
    Evaluates an abstract syntax tree (AST) and returns its result.

    This function is capable of evaluating a wide range of mathematical expressions
    including arithmetic, trigonometric and power expressions, as well as variable
    assignments.

    :param node: The root node of the AST to be evaluated.
    :return: The result of the evaluation of the AST.
    """
    if isinstance(node, (int, float)):
        return node

    if isinstance(node, tuple):
        op = node[0]

        operations = {
            "+": lambda: eval_ast(node[1]) + eval_ast(node[2]),
            "-": lambda: eval_ast(node[1]) - eval_ast(node[2]),
            "*": lambda: eval_ast(node[1]) * eval_ast(node[2]),
            "/": lambda: eval_ast(node[1]) / eval_ast(node[2]),
            "^": lambda: eval_ast(node[1]) ** eval_ast(node[2]),
            "neg": lambda: -eval_ast(node[1]),
            "assign": lambda: env.update({node[1]: eval_ast(node[2])}) or env[node[1]],
            "call": lambda: eval_function_call(node[1], node[2]),
            "var": lambda: eval_variable(node[1]),
        }

        if op in operations:
            return operations[op]()

        print(f"Erro: operador desconhecido '{op}'")
        return 0
    return 0


def eval_function_call(func_name, arg):
    """Evaluate function calls."""
    arg_val = eval_ast(arg)
    if func_name == "sin":
        return math.sin(arg_val)
    if func_name == "cos":
        return math.cos(arg_val)
    if func_name == "sqrt":
        return math.sqrt(arg_val)
    print(f"Erro: função desconhecida '{func_name}'")
    return 0


def eval_variable(name):
    """Evaluate variable lookups."""
    if name in env:
        return env[name]
    print(f"Erro: variável '{name}' não definida.")
    return 0


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression POWER expression"""
    p[0] = (p[2], p[1], p[3])


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = ("neg", p[2])


def p_expression_func(p):
    """expression : ID LPAREN expression RPAREN"""
    p[0] = ("call", p[1], p[3])


def p_error(p):
    """
    Handles errors in the parser.

    This function is called when a syntax error is found during parsing. It prints an
    error message indicating the error and a suggestion to fix it.
    :param p: The token containing the error.
    """
    if p:
        if p.type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "POWER"]:
            print(
                f"Erro: operador '{p.value}' extra. Sugestão: Remova o operador extra."
            )
        elif p.type == "LPAREN":
            print(
                "Erro: parêntese de abertura sem fechamento. Sugestão: Adicione um ')' no final."
            )
        elif p.type == "RPAREN":
            print(
                "Erro: parêntese de fechamento sem abertura. Sugestão: Adicione um '(' antes."
            )
        else:
            print(f"Erro sintático no token '{p.value}'.")
    else:
        print("Erro sintático: entrada incompleta. Sugestão: Adicione um ')' no final.")


def print_ast(node):
    """
    Imprime a árvore sintática em forma de expressão prefixa.
    Exemplo: ('+', 3, 5) -> (+ 3 5)
    """
    if isinstance(node, tuple):
        return f"({node[0]} {' '.join(print_ast(child) for child in node[1:])})"

    return str(node)


parser = yacc.yacc()
