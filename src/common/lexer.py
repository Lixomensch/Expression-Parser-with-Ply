"""Modulo lexer."""

from ply import lex

tokens = (
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "ID",
    "EQUALS",
)

# pylint: disable=C0103
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EQUALS = r"="

t_ignore = " \t"


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    return t


# pylint: enable=C0103


def t_error(t):
    """
    Handles errors in the lexer.

    This function is called when an illegal character is encountered
    during lexical analysis. It prints an error message indicating
    the illegal character and skips it to continue processing.

    :param t: The token containing the illegal character.
    """
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
