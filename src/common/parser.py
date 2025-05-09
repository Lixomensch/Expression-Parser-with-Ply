"""Modulo parser."""

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611

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
    """expression : INTEGER
    | FLOAT"""

    if isinstance(p[1], int):
        p[0] = ("int", p[1])
    else:
        p[0] = ("float", p[1])


def p_expression_id(p):
    "expression : ID"
    p[0] = ("var", p[1])


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


def print_ast(node):
    """
    Imprime a árvore sintática em forma de expressão prefixa.
    Exemplo: ('+', 3, 5) -> (+ 3 5)
    """
    if isinstance(node, tuple):
        return f"({node[0]} {' '.join(print_ast(child) for child in node[1:])})"

    return str(node)


parser = yacc.yacc()
