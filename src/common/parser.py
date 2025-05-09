"""Modulo parser."""

import math

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611

names = {}

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
    names[p[1]] = p[3]
    p[0] = p[3]


def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = int(p[1])


def p_expression_float(p):
    "expression : FLOAT"
    p[0] = float(p[1])


def p_expression_var(p):
    "expression : ID"
    try:
        p[0] = names[p[1]]
    except KeyError:
        print(f"Undefined variable '{p[1]}'")
        p[0] = 0


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression POWER expression"""
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]
    elif p[2] == "^":
        p[0] = p[1] ** p[3]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_func(p):
    """expression : ID LPAREN expression RPAREN"""
    func_name = p[1]
    arg = p[3]
    if func_name == "sin":
        p[0] = math.sin(arg)
    elif func_name == "sqrt":
        p[0] = math.sqrt(arg)
    else:
        print(f"Unknown function '{func_name}'")
        p[0] = 0


def p_error(p):
    """
    Error handling function for the parser.

    This function is called when the parser encounters a syntax error.
    If the error is due to an invalid token, it prints an error message
    with the token value. If the error is due to an incomplete input,
    it prints an error message indicating that the input is incomplete.

    :param p: The token that caused the error.
    :type p: :class:`ply.lex.LexToken`
    """
    if p:
        print(f"Erro sintático no token '{p.value}'")
    else:
        print("Erro sintático: entrada incompleta")


parser = yacc.yacc()
