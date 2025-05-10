"""Modulo lexer."""

from ply import lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'def': 'DEF',
    'return': 'RETURN',
}

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
    "POWER",
    'LBRACE',
    'RBRACE',
    'COMMA',
    'LT',
    'GT',
) + tuple(reserved.values())

# pylint: disable=C0103,W0107,W0613
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EQUALS = r"="
t_POWER = r"\^"
t_ignore = " \t"
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_LT = r'<'
t_GT = r'>'

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r"\d+(\.\d+)?"
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_COMMENT_LINE(t):
    r"//.*"
    pass


def t_COMMENT_BLOCK(t):
    r"/\*.*?\*/"
    pass


# pylint: enable=C0103,W0107,W0613


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
