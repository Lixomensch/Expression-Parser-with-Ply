"""Modulo parser."""

from ply import yacc

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "UMINUS"),
)


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_binop(p):
    """expression : expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression"""
    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = -p[2]


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
