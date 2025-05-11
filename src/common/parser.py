"""Modulo parser."""

from ply import yacc

from .lexer import tokens  # pylint: disable=W0611

functions = {}
env = {}

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("left", "SIN", "COS", "TAN", "EXP", "SQRT", "LOG", "ABS"),
    ("right", "POWER"),
    ("right", "UMINUS"),
)


def p_program(p):
    "program : statements"
    p[0] = ("program", p[1])


def p_statement_expr(p):
    "statement : expression"
    p[0] = p[1]


def p_expression_call(p):
    "expression : function_call"
    p[0] = p[1]


def p_statement_assign(p):
    "statement : ID EQUALS expression"

    p[0] = ("assign", p[1], p[3])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_empty(p):
    "empty :"
    p[0] = None


def p_statements(p):
    "statements : statements statement"
    p[0] = p[1] + [p[2]]


def p_statements_single(p):
    "statements : statement"
    p[0] = [p[1]]


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


def p_statement_if(p):
    "statement : IF LPAREN expression RPAREN block"
    p[0] = ("if", p[3], p[5])


def p_statement_if_else(p):
    "statement : IF LPAREN expression RPAREN block ELSE block"
    p[0] = ("if", p[3], p[5], p[7])


def p_statement_while(p):
    "statement : WHILE LPAREN expression RPAREN block"
    p[0] = ("while", p[3], p[5])


def p_opt_params(p):
    """opt_params : ID
    | ID COMMA opt_params
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_statement_function(p):
    "statement : DEF ID LPAREN opt_params RPAREN block"
    functions[p[2]] = {"params": p[4], "body": p[6]}
    p[0] = ("def", p[2], p[4], p[6])


def p_opt_args(p):
    """opt_args : expression
    | expression COMMA opt_args
    | empty"""
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_statement_print(p):
    "statement : PRINT LPAREN expression RPAREN"
    p[0] = ("print", p[3])


def p_statement_print_call(p):
    "statement : PRINT function_call"
    p[0] = ("print", p[2])


def p_statement_sin(p):
    "expression : SIN LPAREN expression RPAREN"
    p[0] = ("sin", p[3])


def p_statement_cos(p):
    "expression : COS LPAREN expression RPAREN"
    p[0] = ("cos", p[3])


def p_statement_tan(p):
    "expression : TAN LPAREN expression RPAREN"
    p[0] = ("tan", p[3])


def p_statement_exp(p):
    "expression : EXP LPAREN expression RPAREN"
    p[0] = ("exp", p[3])


def p_statement_sqrt(p):
    "expression : SQRT LPAREN expression RPAREN"
    p[0] = ("sqrt", p[3])


def p_statement_log(p):
    "expression : LOG LPAREN expression RPAREN"
    p[0] = ("log", p[3])


def p_statement_abs(p):
    "expression : ABS LPAREN expression RPAREN"
    p[0] = ("abs", p[3])


def p_expression_comparison(p):
    """
    expression : expression LT expression
               | expression GT expression
               | expression LE expression
               | expression GE expression
               | expression EQ expression
               | expression NE expression
    """
    p[0] = (p[2], p[1], p[3])


def p_statement_return(p):
    "statement : RETURN expression"
    p[0] = ("return", p[2])


def p_block(p):
    "block : LBRACE statements RBRACE"
    p[0] = p[2]


def p_function_call(p):
    "function_call : ID LPAREN opt_args RPAREN"
    p[0] = ("call", p[1], p[3])


def p_error(p):
    """
    Handles errors in the parser.

    This function is called when a syntax error is found during parsing. It prints an
    error message indicating the error, the line number, and a suggestion to fix it.
    :param p: The token containing the error.
    """
    if p:
        line = p.lineno

        if p.type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "POWER"]:
            print(
                f"Error at line {line}: operator '{p.type}' without operand. "
                "Suggestion: Add an operand before or after the operator."
            )
        elif p.type == "LPAREN":
            print(
                f"Error at line {line}: opening parenthesis without a closing one. "
                "Suggestion: Add a ')' at the end."
            )
        elif p.type == "RPAREN":
            print(
                f"Error at line {line}: closing parenthesis without an opening one. "
                "Suggestion: Add a '(' before it."
            )
        elif p.type == "LBRACE":
            print(
                f"Error at line {line}: opening curly brace without a matching closing brace. "
                "Suggestion: Add a "
                f"{"}"}"
                " at the end."
            )
        elif p.type == "RBRACE":
            print(
                f"Error at line {line}: closing curly brace without a matching opening brace. "
                "Suggestion: Add a "
                f"{"{"}"
                " before it."
            )
        elif p.type == "ID":
            print(
                f"Error at line {line}: unexpected identifier '{p.value}'. "
                "Suggestion: Check if it is used correctly in a valid statement."
            )
        elif p.type == "EQUALS":
            print(
                f"Error at line {line}: equals sign '=' without a valid variable or expression. "
                "Suggestion: Check the assignment syntax."
            )
        elif p.type == "IF":
            print(
                f"Error at line {line}: incomplete if condition. "
                "Suggestion: Ensure you have a condition inside parentheses followed by a block."
            )
        elif p.type == "WHILE":
            print(
                f"Error at line {line}: incomplete while loop condition. "
                "Suggestion: Ensure you have a condition inside parentheses followed by a block."
            )
        else:
            print(f"Syntax error at line {line}: token '{p.value}' of type '{p.type}'.")


parser = yacc.yacc()
